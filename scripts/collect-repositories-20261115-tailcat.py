"""Collect the requested Tailcat and open-code-review source snapshots."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / 'scripts/repository-review-20261115-tailcat.json'
LIMIT = 120_000_000
ENV = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1')


def git(path, *args):
    result = subprocess.run(['git', '-c', 'safe.directory=' + path.as_posix(), '-C', str(path), *args], env=ENV,
                            capture_output=True, text=True, encoding='utf-8',
                            errors='replace', timeout=300)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.strip()


def size(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def collect(repo, license_id):
    path = ROOT / repo.split('/')[-1]
    exists = path.exists()
    record = dict(repository=repo, url='https://github.com/' + repo,
                  local_path=str(path), previously_present=exists,
                  license=license_id, branch='main')
    record['size_exception'] = repo == 'GoogleChrome/modern-web-guidance-src'
    if exists:
        if git(path, 'status', '--porcelain'):
            raise RuntimeError('Local changes: ' + str(path))
        if git(path, 'remote', 'get-url', 'origin').removesuffix('.git') != record['url']:
            raise RuntimeError('Unexpected origin: ' + str(path))
        record['previous_head'] = git(path, 'rev-parse', 'HEAD')
        git(path, 'fetch', '--no-tags', 'origin', 'main')
        target = git(path, 'rev-parse', 'FETCH_HEAD')
        git(path, 'merge-base', '--is-ancestor', 'HEAD', target)
    else:
        git(ROOT, 'clone', '--depth', '1', '--single-branch', '--no-tags',
            '--no-checkout', '--no-recurse-submodules', record['url'] + '.git', str(path))
        git(path, 'config', '--local', 'core.autocrlf', 'false')
        target = git(path, 'rev-parse', 'HEAD')
    tree = git(path, 'ls-tree', '-rl', target).splitlines()
    record['remote_head'] = target
    record['tracked_source_bytes'] = sum(int(line.split()[3]) for line in tree
                                        if line.split()[1] == 'blob')
    record['skill_paths'] = [line.split('\t', 1)[1] for line in tree
                             if line.split('\t', 1)[1].split('/')[-1] == 'SKILL.md']
    record['submodules'] = [line for line in tree if line.split()[1] == 'commit']
    record['git_bytes_before_checkout'] = size(path / '.git')
    record['projected_bytes_including_git'] = (record['tracked_source_bytes'] +
                                               record['git_bytes_before_checkout'])
    if record['projected_bytes_including_git'] >= LIMIT and not record['size_exception']:
        record['action'] = 'skipped-checkout-over-limit'
        return record
    if exists:
        git(path, 'merge', '--ff-only', target)
        record['action'] = 'fast-forward' if target != record['previous_head'] else 'already-current'
    else:
        git(path, 'checkout', 'main')
        record['action'] = 'cloned-shallow'
    record.update(head=git(path, 'rev-parse', 'HEAD'),
                  origin=git(path, 'remote', 'get-url', 'origin'),
                  worktree_clean=not git(path, 'status', '--porcelain'),
                  shallow=git(path, 'rev-parse', '--is-shallow-repository') == 'true',
                  fsck_output=git(path, 'fsck', '--no-reflogs'),
                  local_file_bytes_including_git=size(path))
    record['matches_remote_head'] = record['head'] == target
    record['size_below_limit'] = record['local_file_bytes_including_git'] < LIMIT
    return record


if __name__ == '__main__':
    report = dict(recorded_date='2026-11-15', limit_bytes=LIMIT,
                  size_policy='Source plus Git file lengths; decimal MB.',
                  repositories=[])
    repos = [('tailscale/tailcat', 'BSD-3-Clause'),
             ('alibaba/open-code-review', 'Apache-2.0')]
    if '--additions' in sys.argv:
        report = json.loads(REPORT.read_text(encoding='utf-8'))
        repos = [('openai/codex-security', 'Apache-2.0'),
                 ('ChromeDevTools/chrome-devtools-mcp', 'Apache-2.0')]
    if '--modern' in sys.argv:
        report = json.loads(REPORT.read_text(encoding='utf-8'))
        report['initial_limit_bytes'] = 100_000_000
        report['limit_bytes'] = LIMIT
        report['size_policy'] = 'Source plus Git file lengths; decimal MB. User raised future default to 120 MB and explicitly authorized modern-web-guidance-src download.'
        report['repositories'] = [r for r in report['repositories']
                                  if r['repository'] != 'GoogleChrome/modern-web-guidance-src']
        repos = [('GoogleChrome/modern-web-guidance-src', 'Apache-2.0')]
    for repo, license_id in repos:
        record = collect(repo, license_id)
        report['repositories'].append(record)
        report['completed_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(record, ensure_ascii=True), flush=True)
    if '--additions' in sys.argv:
        metadata = json.loads((ROOT / 'scripts/repository-api-20261115-additions.json').read_text(encoding='utf-8-sig'))
        skipped = next(x for x in metadata if x['repository'] == 'GoogleChrome/modern-web-guidance-src')
        if skipped['truncated'] or skipped['source_bytes'] < LIMIT:
            raise RuntimeError('Unexpected upstream size; review required')
        skipped.update(action='skipped-source-over-limit', previously_recorded=True,
                       local_directory_exists=(ROOT / 'modern-web-guidance-src').exists())
        report['repositories'].append(skipped)
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
