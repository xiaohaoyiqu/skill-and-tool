"""Collect this batch of source repositories; no dependencies or model assets."""
import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
LIMIT = 100_000_000
REPORT = ROOT / 'scripts/repository-review-20261115.json'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({
    'http': 'http://127.0.0.1:6987', 'https': 'http://127.0.0.1:6987'}))
ENV = os.environ.copy()
for key in list(ENV):
    if 'proxy' in key.lower():
        ENV.pop(key)
ENV['GIT_LFS_SKIP_SMUDGE'] = '1'

def api(suffix):
    request = urllib.request.Request('https://api.github.com/repos/' + suffix,
                                    headers={'User-Agent': 'repository-catalog'})
    with OPENER.open(request, timeout=60) as response:
        return json.load(response)

def git(path, *args):
    command = ['git', '-c', 'safe.directory=' + path.as_posix(),
               '-c', 'http.proxy=http://127.0.0.1:6987',
               '-c', 'https.proxy=http://127.0.0.1:6987', '-C', str(path), *args]
    result = subprocess.run(command, env=ENV, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=1800)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.strip()

def size(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())

def collect(repo):
    path = ROOT / repo.split('/')[-1]
    record = {'repository': repo, 'url': 'https://github.com/' + repo,
              'local_path': str(path), 'size_exception': repo == 'f/prompts.chat'}
    try:
        metadata = api(repo)
        record.update(description=metadata['description'], branch=metadata['default_branch'],
                      github_size_kib=metadata['size'], license_api=metadata['license'])
        tree = api(repo + '/git/trees/' + metadata['default_branch'] + '?recursive=1')
        if tree['truncated']:
            raise RuntimeError('Truncated source tree; size cannot be verified')
        record.update(remote_head=tree['sha'], tracked_source_bytes=sum(
            x.get('size', 0) for x in tree['tree'] if x['type'] == 'blob'),
            skill_paths=[x['path'] for x in tree['tree'] if x['path'].endswith('SKILL.md')],
            submodules=[x for x in tree['tree'] if x['type'] == 'commit'])
        record['previously_present'] = path.exists()
        if record['tracked_source_bytes'] >= LIMIT and not record['size_exception']:
            record['action'] = 'skipped-source-over-limit'
            return record
        if not path.exists():
            print('Cloning ' + repo, flush=True)
            git(ROOT, 'clone', '--depth', '1', '--no-checkout', record['url'] + '.git', str(path))
            record['git_bytes_before_checkout'] = size(path / '.git')
            source_bytes = sum(int(line.split()[3]) for line in git(path, 'ls-tree', '-rl', 'HEAD').splitlines()
                               if line.split()[1] == 'blob')
            record['projected_bytes_including_git'] = source_bytes + record['git_bytes_before_checkout']
            if record['projected_bytes_including_git'] >= LIMIT and not record['size_exception']:
                record['action'] = 'skipped-checkout-over-limit'
                return record
            git(path, 'checkout', metadata['default_branch'])
            record['action'] = 'cloned-shallow'
        else:
            record['action'] = 'verified-existing'
        record.update(head=git(path, 'rev-parse', 'HEAD'),
                      origin=git(path, 'remote', 'get-url', 'origin'),
                      worktree_clean=not git(path, 'status', '--porcelain'),
                      shallow=git(path, 'rev-parse', '--is-shallow-repository') == 'true',
                      fsck_output=git(path, 'fsck', '--no-reflogs'),
                      local_file_bytes_including_git=size(path))
        record['matches_remote_head'] = record['head'] == tree['sha']
        record['size_below_limit'] = record['local_file_bytes_including_git'] < LIMIT
        print(json.dumps(record, ensure_ascii=True), flush=True)
    except Exception as exc:
        record.update(action='failed', error=str(exc))
        print(repo + ': ' + str(exc), flush=True)
    return record

if __name__ == '__main__':
    repos = ['f/prompts.chat', 'ZiChuanLan/freebie-radar', 'Thysrael/Horizon',
             'GoogleChrome/modern-web-guidance-src', 'OpenBMB/VoxCPM',
             'GoogleChrome/modern-web-guidance']
    report = {'recorded_date': '2026-11-15', 'limit_bytes': LIMIT,
              'size_policy': 'Source plus Git file lengths; decimal MB; shallow clones. prompts.chat explicitly exempted.',
              'twitter': 'Cancelled by user; replaced with GoogleChrome/modern-web-guidance-src',
              'repositories': []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(collect, repos):
            report['repositories'].append(result)
            REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report['completed_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
