"""Collect the three requested repositories against the saved full-tree preflight."""
import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
LIMIT = 120_000_000
REPORT = ROOT / 'scripts/repository-review-20261117.json'
ENV = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1', GIT_TERMINAL_PROMPT='0')


def git(path, *args):
    result = subprocess.run(
        ['git', '-c', 'safe.directory=' + path.as_posix(),
         '-c', 'http.proxy=http://127.0.0.1:6987', '-C', str(path), *args],
        env=ENV, capture_output=True, text=True, encoding='utf-8',
        errors='replace', timeout=600)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.strip()


def size(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def collect(metadata):
    record = dict(metadata)
    name = record['repository'].split('/')[-1]
    path = ROOT / name
    record.update(url='https://github.com/' + record['repository'],
                  local_path=str(path), previously_present=path.exists(),
                  size_exception=False, local_directory_exists=path.exists())
    try:
        if metadata['truncated']:
            raise RuntimeError('Incomplete preflight tree; stop before download')
        if path.exists():
            raise RuntimeError('Destination exists; preserve it for a separate update review')
        if record['tracked_source_bytes'] >= LIMIT:
            record['action'] = 'skipped-source-over-limit'
            return record
        print('Cloning without checkout: ' + record['repository'], flush=True)
        # Only the task-owned temporary directory is automatically removed.
        with tempfile.TemporaryDirectory(prefix='repository-20261117-', dir=ROOT) as temporary:
            stage = Path(temporary) / name
            git(ROOT, 'clone', '--depth', '1', '--single-branch', '--no-tags',
                '--branch', record['branch'], '--no-checkout', '--no-recurse-submodules',
                record['url'] + '.git', str(stage))
            git(stage, 'config', '--local', 'core.autocrlf', 'false')
            head = git(stage, 'rev-parse', 'HEAD')
            if head != record['remote_head']:
                raise RuntimeError('Remote moved since preflight; refresh metadata before retrying')
            entries = git(stage, 'ls-tree', '-r', '-l', '-z', head).split('\0')
            local_tree = {}
            for entry in filter(None, entries):
                info, filename = entry.split('\t', 1)
                mode, kind, sha, length = info.split()
                local_tree[filename] = (mode, kind, sha, int(length) if kind == 'blob' else None)
            preflight = json.loads((ROOT / ('scripts/repository-tree-20261117-' + name + '.json')).read_text(encoding='utf-8'))
            expected = {x['path']: (x['mode'], x['type'], x['sha'], x.get('size'))
                        for x in preflight['tree'] if x['type'] != 'tree'}
            if local_tree != expected:
                raise RuntimeError('Downloaded tree differs from complete fixed-commit preflight')
            record['matches_preflight_tree'] = True
            record['git_bytes_before_checkout'] = size(stage / '.git')
            record['projected_bytes_including_git'] = (record['tracked_source_bytes'] +
                                                       record['git_bytes_before_checkout'])
            if record['projected_bytes_including_git'] >= LIMIT:
                record.update(action='skipped-checkout-over-limit',
                              temporary_clone_removed=True)
                print('Over limit before checkout: ' + record['repository'], flush=True)
                return record
            git(stage, 'checkout', record['branch'])
            actual = size(stage)
            if actual >= LIMIT:
                record.update(action='skipped-actual-size-over-limit',
                              measured_bytes_including_git=actual,
                              temporary_clone_removed=True)
                return record
            record.update(head=git(stage, 'rev-parse', 'HEAD'),
                          origin=git(stage, 'remote', 'get-url', 'origin'),
                          worktree_clean=not git(stage, 'status', '--porcelain'),
                          shallow=git(stage, 'rev-parse', '--is-shallow-repository') == 'true',
                          fsck_output=git(stage, 'fsck', '--no-reflogs'),
                          fsck_exit_code=0,
                          local_file_bytes_including_git=size(stage),
                          verified_skill_file_count=sum((stage / p).is_file() for p in record['skill_paths']),
                          submodules_initialized=False,
                          lfs_entities_downloaded=False)
            record['matches_remote_head'] = record['head'] == record['remote_head']
            record['size_below_limit'] = record['local_file_bytes_including_git'] < LIMIT
            if not record['worktree_clean'] or not record['matches_remote_head']:
                raise RuntimeError('Final worktree or revision verification failed')
            if path.exists() or stage.resolve().parent != Path(temporary).resolve():
                raise RuntimeError('Unexpected publication path; preserve existing destination')
            stage.rename(path)
            record.update(action='cloned-shallow', local_directory_exists=True)
        print('Completed: ' + record['repository'], flush=True)
    except Exception as exc:
        record.update(action='failed', error=str(exc), local_directory_exists=path.exists())
        print('Failed: ' + record['repository'] + ': ' + str(exc), flush=True)
    return record


if __name__ == '__main__':
    report = dict(recorded_date='2026-11-17', limit_bytes=LIMIT,
                  size_policy='Complete current source plus Git file lengths; decimal MB; strictly below 120 MB. No new-project exceptions.',
                  preflight='scripts/repository-api-20261117.json', repositories=[])
    metadata = json.loads((ROOT / report['preflight']).read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        pending = [pool.submit(collect, item) for item in metadata]
        for future in concurrent.futures.as_completed(pending):
            report['repositories'].append(future.result())
            report['updated_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report['completed_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(any(r['action'] == 'failed' for r in report['repositories']))
