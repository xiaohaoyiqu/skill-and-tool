"""Verify that synchronization preserves local work and enforces checkout limits."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'sync-repositories.py'
SPEC = importlib.util.spec_from_file_location('repository_sync', SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RepositorySyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='repository-sync-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.origin = self.root / 'origin'
        self.origin.mkdir()
        self.git(self.origin, 'init', '-b', 'main')
        self.commit(self.origin, 'initial')
        self.clone = self.root / 'clone'
        self.git(self.root, 'clone', str(self.origin), str(self.clone))

    def git(self, path, *args):
        return subprocess.check_output(['git', '-c', 'user.name=Sync Test',
                                        '-c', 'user.email=sync-test@example.invalid',
                                        '-c', 'core.autocrlf=false',
                                        '-C', str(path), *args], text=True,
                                       encoding='utf-8', stderr=subprocess.STDOUT).strip()

    def commit(self, path, content):
        (path / 'source.txt').write_text(content, encoding='utf-8')
        self.git(path, 'add', 'source.txt')
        self.git(path, 'commit', '-m', content)

    def test_fast_forward_and_current(self):
        self.commit(self.origin, 'upstream update')
        result = MODULE.sync(self.clone, True, 120_000_000)
        self.assertEqual(result['action'], 'updated')
        self.assertEqual(result['head_after'], self.git(self.origin, 'rev-parse', 'HEAD'))
        self.assertTrue(result['worktree_clean'])
        self.assertEqual(MODULE.sync(self.clone, True, 120_000_000)['action'], 'current')

    def test_dirty_work_is_preserved(self):
        self.commit(self.origin, 'upstream update')
        (self.clone / 'source.txt').write_text('local work', encoding='utf-8')
        before = self.git(self.clone, 'rev-parse', 'HEAD')
        result = MODULE.sync(self.clone, True, 120_000_000)
        self.assertEqual(result['action'], 'skipped-dirty')
        self.assertEqual(self.git(self.clone, 'rev-parse', 'HEAD'), before)
        self.assertEqual((self.clone / 'source.txt').read_text(encoding='utf-8'), 'local work')

    def test_divergence_preserves_local_commit(self):
        self.commit(self.origin, 'upstream update')
        self.commit(self.clone, 'local commit')
        before = self.git(self.clone, 'rev-parse', 'HEAD')
        result = MODULE.sync(self.clone, True, 120_000_000)
        self.assertEqual(result['action'], 'skipped-diverged')
        self.assertEqual(self.git(self.clone, 'rev-parse', 'HEAD'), before)

    def test_over_limit_fetch_does_not_checkout(self):
        before = self.git(self.clone, 'rev-parse', 'HEAD')
        self.commit(self.origin, 'upstream update')
        result = MODULE.sync(self.clone, True, 1)
        self.assertEqual(result['action'], 'skipped-over-limit')
        self.assertGreater(result.get('projected_bytes_including_git', result.get('git_bytes_before_fetch')), 1)
        self.assertEqual(self.git(self.clone, 'rev-parse', 'HEAD'), before)

    def test_detached_head_is_preserved(self):
        self.git(self.clone, 'checkout', '--detach')
        self.assertEqual(MODULE.sync(self.clone, True, 120_000_000)['action'], 'skipped-no-upstream')

    def test_read_only_does_not_fetch(self):
        self.commit(self.origin, 'upstream update')
        before = self.git(self.clone, 'rev-parse', 'origin/main')
        self.assertEqual(MODULE.sync(self.clone, False, 120_000_000)['action'], 'inspected')
        self.assertEqual(self.git(self.clone, 'rev-parse', 'origin/main'), before)

    def test_partial_archive_does_not_hydrate(self):
        self.git(self.clone, 'config', 'remote.origin.promisor', 'true')
        self.commit(self.origin, 'upstream update')
        before = self.git(self.clone, 'rev-parse', 'origin/main')
        result = MODULE.sync(self.clone, True, 120_000_000)
        self.assertEqual(result['action'], 'skipped-partial-clone')
        self.assertEqual(self.git(self.clone, 'rev-parse', 'origin/main'), before)

    def test_source_expansion_is_checked_after_fetch(self):
        before = self.git(self.clone, 'rev-parse', 'HEAD')
        (self.origin / 'source.txt').write_text('x' * 1_000_000, encoding='utf-8')
        self.git(self.origin, 'add', 'source.txt')
        self.git(self.origin, 'commit', '-m', 'large source')
        result = MODULE.sync(self.clone, True, 100_000)
        self.assertEqual(result['action'], 'skipped-over-limit')
        self.assertGreater(result['tracked_source_bytes'], 100_000)
        self.assertEqual(self.git(self.clone, 'rev-parse', 'HEAD'), before)

    def test_explicit_size_exception_allows_update(self):
        self.commit(self.origin, 'authorized update')
        result = MODULE.sync(self.clone, True, 1, allow_over_limit=True)
        self.assertEqual(result['action'], 'updated')
        self.assertTrue(result['size_exception'])
        self.assertEqual(self.git(self.clone, 'rev-parse', 'HEAD'), self.git(self.origin, 'rev-parse', 'HEAD'))


if __name__ == '__main__':
    unittest.main()
