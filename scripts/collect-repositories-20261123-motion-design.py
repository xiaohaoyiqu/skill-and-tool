"""Record the requested batch; download source only under the catalog size rules."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
LIMIT = 120_000_000
REPOS = ['showheyohtaki/motion-prompt', 'heygen-com/hyperframes',
         'remotion-dev/skills', 'EL4CTEO/blender-skills',
         'motiondivision/motion', 'motion-canvas/motion-canvas', 'emilkowalski/skills']
LOCAL_NAMES = {'remotion-dev/skills': 'remotion-skills', 'emilkowalski/skills': 'emilkowalski-skills'}
API_REPORT = ROOT / 'scripts/repository-api-20261123-motion-design.json'
REPORT = ROOT / 'scripts/repository-review-20261123-motion-design.json'
ENV = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1', GIT_TERMINAL_PROMPT='0')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def request(url, as_json=True):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({
        'https': 'http://127.0.0.1:6987', 'http': 'http://127.0.0.1:6987'}))
    req = urllib.request.Request(url, headers={'User-Agent': 'local-repository-catalog'})
    with opener.open(req, timeout=45) as response:
        data = response.read()
    return json.loads(data) if as_json else data.decode('utf-8', errors='replace')


def api(suffix):
    return request('https://api.github.com/repos/' + suffix)


def git(path, *args, timeout=240):
    command = ['git', '-c', 'safe.directory=' + path.as_posix(),
               '-c', 'http.version=HTTP/1.1', '-c', 'http.lowSpeedLimit=1',
               '-c', 'http.lowSpeedTime=45', '-c', 'submodule.recurse=false',
               '-C', str(path), *args]
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        process = subprocess.Popen(command, stdout=out, stderr=err, env=ENV)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait(timeout=15)
            raise TimeoutError('Git timeout: ' + args[0])
        out.seek(0)
        err.seek(0)
        stdout, stderr = out.read().decode('utf-8'), err.read().decode('utf-8', errors='replace')
    if code:
        raise RuntimeError(stderr or stdout)
    return stdout.rstrip('\n')


def size(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def preflight(repo):
    record = dict(repository=repo, url='https://github.com/' + repo)
    try:
        meta = api(repo)
        branch = meta['default_branch']
        commit = api(repo + '/commits/' + urllib.parse.quote(branch, safe=''))
        tree = api(repo + '/git/trees/' + commit['commit']['tree']['sha'] + '?recursive=1')
        if tree.get('truncated'):
            raise RuntimeError('Truncated API tree; stop before cloning')
        name = LOCAL_NAMES.get(repo, repo.split('/')[-1])
        save(ROOT / ('scripts/repository-tree-20261123-motion-design-' + name + '.json'), tree)
        blobs = [x for x in tree['tree'] if x['type'] == 'blob']
        record.update(branch=branch, remote_head=commit['sha'], tree_sha=tree['sha'],
                      commit_date=commit['commit']['committer']['date'],
                      description=meta['description'], license_api=meta['license'],
                      github_size_kib=meta['size'], truncated=False,
                      tracked_source_bytes=sum(x['size'] for x in blobs),
                      tracked_entries=len(blobs),
                      skill_paths=[x['path'] for x in blobs if x['path'].split('/')[-1] == 'SKILL.md'],
                      submodules=[x['path'] for x in tree['tree'] if x['type'] == 'commit'],
                      license_paths=[x['path'] for x in blobs if '/' not in x['path'] and
                                     x['path'].lower().startswith(('license', 'copying', 'notice'))],
                      previously_present=(ROOT / name).exists())
        print(repo + ': source=' + str(record['tracked_source_bytes']) + ' HEAD=' + commit['sha'][:8], flush=True)
    except Exception as exc:
        record.update(error=str(exc))
        print(repo + ': ' + str(exc), flush=True)
    return record


def remove_temporary(path):
    resolved = path.resolve()
    if resolved.parent != ROOT.resolve() or not resolved.name.startswith('repository-20261123-motion-design-'):
        raise RuntimeError('Refuse unexpected cleanup path: ' + str(resolved))
    def writable_then_retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(resolved, onerror=writable_then_retry)


def collect(metadata):
    record = dict(metadata)
    path = ROOT / LOCAL_NAMES.get(record['repository'], record['repository'].split('/')[-1])
    record.update(local_path=str(path), size_exception=False,
                  dependencies_installed=False, global_skills_installed=False,
                  submodules_initialized=False, lfs_entities_downloaded=False)
    temporary = None
    try:
        if 'error' in record:
            raise RuntimeError('Preflight failed: ' + record['error'])
        if not path.exists() and record['tracked_source_bytes'] >= LIMIT:
            record['action'] = 'skipped-source-over-limit'
            return record
        if path.exists():
            record['head_before'] = git(path, 'rev-parse', 'HEAD')
            record['origin'] = git(path, 'remote', 'get-url', 'origin')
            if record['origin'].removesuffix('.git').lower() != record['url'].lower():
                raise RuntimeError('Existing origin does not match requested repository')
            if git(path, 'status', '--porcelain'):
                record.update(action='skipped-dirty', head=record['head_before'])
                return record
            if git(path, 'branch', '--show-current') != record['branch']:
                raise RuntimeError('Preserve existing non-default branch')
            git(path, 'fetch', '--no-tags', '--no-recurse-submodules', 'origin', record['branch'])
            target = git(path, 'rev-parse', 'FETCH_HEAD')
            if target != record['remote_head']:
                raise RuntimeError('Upstream moved since preflight; refresh preflight')
            ahead, behind = map(int, git(path, 'rev-list', '--left-right', '--count', 'HEAD...' + target).split())
            record.update(ahead=ahead, behind=behind)
            if ahead:
                record.update(action='skipped-diverged', head=record['head_before'])
                return record
            if behind:
                git(path, 'merge', '--ff-only', target)
            record['action'] = 'updated-fast-forward' if behind else 'current'
            stage = path
        else:
            temporary = Path(tempfile.mkdtemp(prefix='repository-20261123-motion-design-', dir=ROOT))
            stage = temporary / path.name
            print('Cloning ' + record['repository'], flush=True)
            git(ROOT, 'clone', '--depth', '1', '--single-branch', '--no-tags',
                '--branch', record['branch'], '--no-checkout', '--no-recurse-submodules',
                '--config', 'core.autocrlf=false', '--config', 'core.longpaths=true',
                record['url'] + '.git', str(stage))
            if git(stage, 'rev-parse', 'HEAD') != record['remote_head']:
                raise RuntimeError('Upstream moved since preflight; refresh preflight')
            if git(stage, 'rev-parse', 'HEAD^{tree}') != record['tree_sha']:
                raise RuntimeError('Downloaded tree differs from preflight')
            record['matches_preflight_tree'] = True
            record['git_bytes_before_checkout'] = size(stage / '.git')
            record['projected_bytes_including_git'] = record['tracked_source_bytes'] + record['git_bytes_before_checkout']
            if record['projected_bytes_including_git'] >= LIMIT:
                record.update(action='skipped-checkout-over-limit', temporary_clone_removed=True)
                return record
            git(stage, 'checkout', record['branch'])
            record['action'] = 'cloned-shallow'
        record['worktree_status'] = git(stage, 'status', '--porcelain')
        if record['worktree_status']:
            record['worktree_diff_stat'] = git(stage, 'diff', '--stat')
            record['worktree_diff'] = git(stage, 'diff', '--no-ext-diff', '--numstat')
        record.update(head=git(stage, 'rev-parse', 'HEAD'),
                      origin=git(stage, 'remote', 'get-url', 'origin'),
                      worktree_clean=not git(stage, 'status', '--porcelain'),
                      shallow=git(stage, 'rev-parse', '--is-shallow-repository') == 'true',
                      fsck_output=git(stage, 'fsck', '--no-reflogs'), fsck_exit_code=0,
                      git_bytes=size(stage / '.git'), local_file_bytes_including_git=size(stage),
                      verified_skill_file_count=sum((stage / p).is_file() for p in record['skill_paths']))
        record['matches_remote_head'] = record['head'] == record['remote_head']
        record['size_below_limit'] = record['local_file_bytes_including_git'] < LIMIT
        if not record['matches_remote_head'] or not record['worktree_clean']:
            raise RuntimeError('Revision or worktree verification failed')
        if temporary:
            if not record['size_below_limit']:
                record.update(action='skipped-actual-size-over-limit', temporary_clone_removed=True)
                return record
            if path.exists():
                raise RuntimeError('Destination appeared; preserve it')
            stage.rename(path)
        print(record['repository'] + ': ' + record['action'], flush=True)
    except Exception as exc:
        record.update(action='failed', error=str(exc))
        print(record['repository'] + ': FAILED ' + str(exc), flush=True)
    finally:
        if temporary:
            remove_temporary(temporary)
        record['local_directory_exists'] = path.exists()
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['preflight', 'collect'])
    parser.add_argument('--only', nargs='+')
    args = parser.parse_args()
    if args.phase == 'preflight':
        existing = json.loads(API_REPORT.read_text(encoding='utf-8')) if API_REPORT.exists() else []
        requested = [r for r in REPOS if not args.only or LOCAL_NAMES.get(r, r.split('/')[-1]) in args.only]
        results = {r['repository']: r for r in existing}
        operation, inputs, destination = preflight, requested, API_REPORT
    else:
        metadata = json.loads(API_REPORT.read_text(encoding='utf-8'))
        old = json.loads(REPORT.read_text(encoding='utf-8')) if REPORT.exists() else {'repositories': []}
        results = {r['repository']: r for r in old['repositories']}
        inputs = [r for r in metadata if not args.only or LOCAL_NAMES.get(r['repository'], r['repository'].split('/')[-1]) in args.only]
        operation, destination = collect, REPORT
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(operation, x) for x in inputs]):
            result = future.result()
            results[result['repository']] = result
            records = [results[r] for r in REPOS if r in results]
            value = records if args.phase == 'preflight' else dict(
                recorded_date='2026-11-23', updated_at_utc=datetime.now(timezone.utc).isoformat(),
                limit_bytes=LIMIT, size_policy='New repositories strictly below 120 MB including Git; existing clean repositories may exceed the limit.',
                repositories=records)
            save(destination, value)
    raise SystemExit(any('error' in results[r] for r in results))
