"""Inspect repositories; --pull fetches and fast-forwards clean trees within the size limit."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
GIT_TIMEOUT = 90


def redact(text):
    return re.sub(r'(https?://)[^/\s@]+@', r'\1***@', text)


def git(path, *args, check=True):
    command = ['git', '-c', 'safe.directory=' + path.as_posix(),
               '-c', 'submodule.recurse=false', '-c', 'http.lowSpeedLimit=1',
               '-c', 'http.lowSpeedTime=45', '-C', str(path), *args]
    # Files avoid inherited pipe handles blocking timeout recovery on Windows.
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(command,
                                   env=dict(os.environ, GIT_LFS_SKIP_SMUDGE='1', GIT_TERMINAL_PROMPT='0'),
                                   stdout=stdout, stderr=stderr)
        try:
            code = process.wait(timeout=GIT_TIMEOUT)
        except subprocess.TimeoutExpired:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
            else:
                process.kill()
            process.wait(timeout=15)
            raise TimeoutError(f'Git operation exceeded {GIT_TIMEOUT} seconds: ' + args[0])
        stdout.seek(0)
        stderr.seek(0)
        result = subprocess.CompletedProcess(command, code,
                                              stdout.read().decode('utf-8', errors='replace'),
                                              stderr.read().decode('utf-8', errors='replace'))
    if check and result.returncode:
        raise RuntimeError(redact(result.stderr or result.stdout[-4000:]))
    return result


def size(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def sync(path, pull, limit, allow_over_limit=False):
    record = dict(repository=path.name, path=str(path), action='inspected')
    record['size_exception'] = allow_over_limit
    try:
        record['head_before'] = git(path, 'rev-parse', 'HEAD').stdout.strip()
        record['head_after'] = record['head_before']
        record['branch'] = git(path, 'branch', '--show-current').stdout.strip()
        record['origin'] = redact(git(path, 'remote', 'get-url', 'origin', check=False).stdout.strip())
        status = git(path, 'status', '--porcelain').stdout.strip()
        record['dirty_files'] = status.splitlines() if status else []
        upstream = git(path, 'rev-parse', '--abbrev-ref', '@{upstream}', check=False)
        record['upstream'] = upstream.stdout.strip() if not upstream.returncode else ''
        if not pull:
            return record
        if status:
            record['action'] = 'skipped-dirty'
            return record
        if not record['upstream']:
            record['action'] = 'skipped-no-upstream'
            return record
        if git(path, 'config', '--get', 'remote.origin.promisor', check=False).stdout.strip() == 'true':
            record['action'] = 'skipped-partial-clone'
            record['reason'] = 'Preserve existing partial/sparse archive without hydrating missing source blobs.'
            return record
        remote = git(path, 'config', '--get', 'branch.' + record['branch'] + '.remote').stdout.strip()
        git_bytes = size(path / '.git')
        if git_bytes >= limit and not allow_over_limit:
            remote_ref = git(path, 'config', '--get', 'branch.' + record['branch'] + '.merge').stdout.strip()
            tip = git(path, 'ls-remote', '--refs', remote, remote_ref).stdout.split()
            if not tip:
                raise RuntimeError('Configured upstream branch is absent from remote.')
            record['remote_head'] = tip[0]
            record['git_bytes_before_fetch'] = git_bytes
            record['action'] = 'current' if tip[0] == record['head_before'] else 'skipped-over-limit'
            record['size_check_phase'] = 'before-fetch'
            return record
        git(path, 'fetch', '--prune', '--no-tags', '--no-recurse-submodules', remote)
        target = git(path, 'rev-parse', record['upstream']).stdout.strip()
        record['remote_head'] = target
        counts = git(path, 'rev-list', '--left-right', '--count', 'HEAD...' + target).stdout.split()
        record['ahead'], record['behind'] = map(int, counts)
        if record['ahead']:
            record['action'] = 'skipped-diverged' if record['behind'] else 'local-ahead'
            return record
        if not record['behind']:
            record['action'] = 'current'
            return record
        tree = git(path, 'ls-tree', '-rl', target).stdout.splitlines()
        record['tracked_source_bytes'] = sum(int(line.split()[3]) for line in tree if line.split()[1] == 'blob')
        record['projected_bytes_including_git'] = record['tracked_source_bytes'] + size(path / '.git')
        if record['projected_bytes_including_git'] >= limit and not allow_over_limit:
            record['action'] = 'skipped-over-limit'
            return record
        git(path, 'merge', '--ff-only', target)
        record['head_after'] = git(path, 'rev-parse', 'HEAD').stdout.strip()
        record['worktree_clean'] = not git(path, 'status', '--porcelain').stdout.strip()
        record['fsck_output'] = git(path, 'fsck', '--no-reflogs').stdout.strip()
        record['local_file_bytes_including_git'] = size(path)
        record['action'] = 'updated'
    except Exception as exc:
        record.update(action='failed', error=redact(str(exc)))
    finally:
        record['checked_at_utc'] = datetime.now(timezone.utc).isoformat()
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pull', action='store_true')
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--limit-bytes', type=int, default=120_000_000)
    parser.add_argument('--report', default='scripts/repository-sync-20261115.json')
    parser.add_argument('--only', nargs='*')
    parser.add_argument('--resume', action='store_true', help='Continue unfinished entries from the report.')
    parser.add_argument('--allow-over-limit', action='store_true', help='Use only with explicit authorization for oversized updates.')
    parser.add_argument('--git-timeout', type=int, default=90)
    args = parser.parse_args()
    GIT_TIMEOUT = args.git_timeout
    paths = sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith('.') and (p / '.git').exists())
    if args.only:
        paths = [p for p in paths if p.name in args.only]
    report = dict(started_at_utc=datetime.now(timezone.utc).isoformat(), limit_bytes=args.limit_bytes,
                  pull=args.pull, repositories=[])
    output = ROOT / args.report
    if args.resume and output.exists():
        report = json.loads(output.read_text(encoding='utf-8'))
        completed = {r['repository'] for r in report['repositories']}
        paths = [p for p in paths if p.name not in completed]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(sync, path, args.pull, args.limit_bytes, args.allow_over_limit) for path in paths]
        for future in as_completed(futures):
            r = future.result()
            report['repositories'].append(r)
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
            print(r['repository'] + ': ' + r['action'], flush=True)
    report['repositories'].sort(key=lambda r: r['repository'].lower())
    report['completed_at_utc'] = datetime.now(timezone.utc).isoformat()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    counts = {}
    for r in report['repositories']:
        counts[r['action']] = counts.get(r['action'], 0) + 1
    print(json.dumps(counts), flush=True)
