"""Source drift and portable annotation restore, including concurrent failures."""
from __future__ import annotations

import copy
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
import threading
import urllib.request
import urllib.error
import re
from pathlib import Path
import io
import contextlib
from unittest.mock import patch

from test_library import Fixture, skill
from sklib.failures import OperationFailure
from sklib.jobs import IndexJobs
from sklib.monitor import SourceMonitor
from sklib.service import Library
from sklib.restoring import read_snapshot
from sklib.web import create_server


class SourceCheckTests(Fixture):
    def test_broken_alias_cannot_remove_a_different_registered_source(self):
        self.sample()
        original = self.root.resolve()
        alias = self.base / "alias"
        alias.mkdir()
        exists = Path.exists
        with patch.object(Path, "exists", autospec=True, side_effect=lambda path: False if path == alias else exists(path)), patch.object(Path, "resolve", return_value=original), patch("sklib.sources.is_link", side_effect=lambda path: path == alias):
            result = self.lib.remove_root(alias)
        self.assertEqual(result["removed_from_index"], 0)
        self.assertEqual(self.lib.status()["documents"], 4)

    def test_removing_registered_root_does_not_follow_its_new_link_target(self):
        self.sample()
        registered = self.lib.status()["roots"][0]["path"]
        other = self.base / "other"
        other.mkdir()
        (other / "SKILL.md").write_text(skill("other", "Retain this source"), encoding="utf-8")
        self.lib.index(other)
        with patch.object(Path, "resolve", return_value=other):
            removed = self.lib.remove_root(registered)
        self.assertEqual(removed["removed_from_index"], 4)
        self.assertEqual(self.lib.status()["documents"], 1)
        self.assertTrue((other / "SKILL.md").exists())

    def test_cli_watch_does_not_replay_failed_change_and_reports_prior_updates(self):
        from sklib.cli import main
        self.sample()
        path = self.root / "broken/SKILL.md"
        path.parent.mkdir()
        path.write_bytes(b"\xff invalid utf8")
        output, errors = io.StringIO(), io.StringIO()
        with patch("sklib.cli.Library", return_value=self.lib), patch("time.sleep", side_effect=[None, KeyboardInterrupt]), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = main(["sources", "watch", "--refresh", "--interval", "30"])
        self.assertEqual(code, 130)
        self.assertEqual(json.loads(errors.getvalue())["outcome"], "partial")
        self.assertIn('"refresh_suppressed": true', output.getvalue())
        self.assertEqual(len([event for event in self.lib.history() if event["action"] == "index"]), 2)

    def test_embedding_timeout_and_model_types_are_bounded(self):
        from sklib.semantic import OllamaEmbeddings
        for timeout in (0, 601, True, 1.5):
            with self.assertRaises(ValueError):
                OllamaEmbeddings("fixture", timeout=timeout)
        for model in (None, 12, True, " "):
            with self.assertRaises(ValueError):
                OllamaEmbeddings(model)
        self.assertEqual(OllamaEmbeddings("fixture", timeout=120).timeout, 120)

    def test_monitor_does_not_replay_same_failed_change(self):
        self.sample()
        jobs = IndexJobs(self.lib)
        self.addCleanup(jobs.close)
        monitor = SourceMonitor(self.lib, jobs)
        self.addCleanup(monitor.close)
        path = self.root / "broken/SKILL.md"
        path.parent.mkdir()
        path.write_bytes(b"\xff invalid utf8")
        monitor.configure(enabled=True, auto_refresh=True)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            journal = jobs.list()["jobs"]
            if journal and journal[0]["state"] == "partial":
                break
            time.sleep(.02)
        self.assertEqual(jobs.list()["jobs"][0]["state"], "partial")
        monitor.configure(check_now=True)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            reports = monitor.status()["reports"]
            if reports and reports[0].get("refresh_suppressed"):
                break
            time.sleep(.02)
        self.assertEqual(len(jobs.list()["jobs"]), 1)
        self.assertTrue(monitor.status()["reports"][0]["refresh_suppressed"])
        self.assertEqual(monitor.status()["reports"][0]["refresh_job"], jobs.list()["jobs"][0]["id"])

    def test_check_detects_source_removed_during_walk(self):
        self.sample()
        from sklib.indexer import candidate_kind
        removed = False
        def removing(*args, **options):
            nonlocal removed
            if not removed:
                removed = True
                self.lib.remove_root(self.root)
            return candidate_kind(*args, **options)
        with patch("sklib.sources.candidate_kind", side_effect=removing):
            report = self.lib.check_source(str(self.root))
        self.assertFalse(report["complete"])
        self.assertTrue(report["stale"])
        self.assertEqual(self.lib.status()["roots"], [])

    def test_change_detection_does_not_mutate_index_and_reuses_discovery(self):
        self.sample()
        before = self.lib.snapshot()
        self.assertEqual(self.lib.check_source(str(self.root))["state"], "clean")
        self.write("new/SKILL.md", skill("new", "new workflow"))
        self.write("ignored/tests/SKILL.md", skill("ignored", "excluded"))
        self.write("deep/a/README.md", "Not indexed without docs or project markers")
        path = self.root / "writer/humanize/SKILL.md"
        path.unlink()
        self.write("pdf/skills/pdf-tables/SKILL.md", skill("pdf-tables", "Modified PDF workflow"))
        result = self.lib.check_source(str(self.root))
        self.assertTrue(result["complete"])
        self.assertEqual((result["added"], result["modified"], result["removed"]), (1, 1, 1))
        self.assertEqual(self.lib.snapshot(), before)

    def test_verify_catches_modification_with_same_stat(self):
        self.sample()
        path = self.root / "pdf/skills/pdf-tables/SKILL.md"
        info = path.stat()
        path.write_bytes(path.read_bytes().replace(b"Extract", b"Replace"))
        os.utime(path, ns=(info.st_atime_ns, info.st_mtime_ns))
        self.assertEqual(self.lib.check_source(str(self.root))["state"], "clean")
        self.assertEqual(self.lib.check_source(str(self.root), verify=True)["modified"], 1)

    def test_partial_walk_does_not_infer_deletions(self):
        self.sample()
        def denied(root, *, followlinks, onerror):
            onerror(PermissionError("fixture denied"))
            return iter([])
        with patch("sklib.sources.os.walk", side_effect=denied):
            result = self.lib.check_source(str(self.root))
        self.assertFalse(result["complete"])
        self.assertEqual(result["state"], "attention")
        self.assertEqual(result["removed"], 0)
        self.assertEqual(result["failures"][0]["code"], "permission_denied")

    def test_missing_root_and_changed_registration_do_not_claim_clean(self):
        self.sample()
        canonical = self.lib.status()["roots"][0]["path"]
        with patch("sklib.sources.is_link", return_value=True), patch.object(Path, "resolve", side_effect=RuntimeError("must not resolve a link")):
            self.assertEqual(self.lib.check_source(canonical)["state"], "attention")
        shutil.rmtree(self.root)
        result = self.lib.check_source(str(self.root))
        self.assertFalse(result["complete"])
        self.assertEqual(result["removed"], 0)
        self.assertEqual(self.lib.status()["documents"], 4)

    def test_saved_encoding_docs_options_and_change_sample_limit(self):
        self.write("docs/a.txt", "old text")
        self.lib.index(self.root, include_docs=True, encoding="gb18030")
        for number in range(4):
            self.write(f"docs/{number}.txt", "new text")
        result = self.lib.check_source(str(self.root), max_changes=2)
        self.assertEqual(result["added"], 4)
        self.assertEqual(len(result["changes"]), 2)
        self.assertTrue(result["changes_truncated"])

    def test_source_epoch_protects_automatic_queued_refresh(self):
        self.sample()
        result = self.lib.check_source(str(self.root))
        jobs = IndexJobs(self.lib)
        self.addCleanup(jobs.close)
        self.lib.remove_root(self.root)
        with self.assertRaises(OperationFailure) as failure:
            jobs.submit(str(self.root), expected_source_epoch=result["source_epoch"])
        self.assertEqual(failure.exception.code, "source_conflict")
        self.assertEqual(self.lib.status()["roots"], [])

    def test_monitor_manual_check_and_opt_in_incremental_refresh(self):
        self.sample()
        jobs = IndexJobs(self.lib)
        self.addCleanup(jobs.close)
        monitor = SourceMonitor(self.lib, jobs)
        self.addCleanup(monitor.close)
        self.assertFalse(monitor.status()["enabled"])
        monitor.configure(check_now=True)
        deadline = time.monotonic() + 10
        while not monitor.status()["reports"] and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertEqual(monitor.status()["reports"][0]["state"], "clean")
        self.write("new/SKILL.md", skill("new", "new workflow"))
        monitor.configure(enabled=True, auto_refresh=True)
        deadline = time.monotonic() + 10
        while self.lib.status()["documents"] != 5 and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertEqual(self.lib.status()["documents"], 5)
        self.assertTrue(monitor.status()["enabled"])
        monitor.configure(enabled=False)
        self.assertFalse(monitor.status()["auto_refresh"])

    def test_cli_check_and_mcp_read_only_tool(self):
        from sklib.mcp import Session
        self.sample()
        result = subprocess.run([sys.executable, "-m", "sklib", "--home", str(self.lib.store.home), "sources", "check"],
            capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["reports"][0]["state"], "clean")
        session = Session(self.lib)
        session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {}}})
        session.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
        result = session.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": "check_source", "arguments": {"root": str(self.root)}}})
        self.assertEqual(result["result"]["structuredContent"]["state"], "clean")


class RestoreTests(Fixture):
    def test_unique_content_rename_and_ambiguous_copies(self):
        self.backup()
        snapshot = self.lib.snapshot()
        source = next(entry for entry in snapshot["entries"] if entry["note"])
        snapshot["entries"] = [source]
        renamed = self.base / "renamed-source"
        renamed.mkdir()
        target_file = renamed / "different-name" / "SKILL.md"
        target_file.parent.mkdir()
        target_file.write_bytes((self.root / "pdf/skills/pdf-tables/SKILL.md").read_bytes())
        target = self.target(renamed)
        mapping = {source["root"]: str(renamed)}
        preview = target.restore_annotations(snapshot, root_map=mapping, match_content=True)
        self.assertEqual(preview["entries"][0]["match"], "unique_content")
        duplicate = renamed / "duplicate" / "SKILL.md"
        duplicate.parent.mkdir()
        duplicate.write_bytes(target_file.read_bytes())
        target.index(renamed)
        ambiguous = target.restore_annotations(snapshot, root_map=mapping, match_content=True)
        self.assertEqual(ambiguous["counts"]["ambiguous"], 1)
        self.assertTrue(ambiguous["entries"][0]["orphan"])
        with self.assertRaises(OperationFailure):
            target.restore_annotations(snapshot, root_map=mapping, match_content=True, apply=True, expected_preview=preview["preview_token"])

    def test_snapshot_export_atomic_failure_and_utf16_import(self):
        self.backup()
        path = self.base / "backup.json"
        self.lib.export_snapshot(str(path))
        original = path.read_bytes()
        self.lib.annotate(self.pdf_id(), note="new change")
        with patch("sklib.restoring.os.replace", side_effect=OSError("fixture full")):
            with self.assertRaises(OSError):
                self.lib.export_snapshot(str(path))
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(list(self.base.glob(".sklib-snapshot-*")))
        path.write_text(json.dumps(self.lib.snapshot()), encoding="utf-16")
        self.assertEqual(read_snapshot(path)["schema_version"], 1)
        with self.assertRaises(ValueError):
            self.lib.export_snapshot(str(self.root / "backup.json"))

    def test_filtered_snapshot_batches_keep_schema_and_paging(self):
        self.backup()
        snapshot = self.lib.portable_snapshot(annotated_only=True, limit=1)
        self.assertEqual(len(snapshot["entries"]), 1)
        self.assertEqual(snapshot["entries"][0]["note"], "portable note")
        first = self.lib.portable_snapshot(limit=2)
        second = self.lib.portable_snapshot(offset=first["selection"]["next_offset"], limit=2)
        self.assertEqual(first["selection"]["total"], 4)
        self.assertIsNone(second["selection"]["next_offset"])
        self.assertEqual(len(first["entries"]) + len(second["entries"]), 4)
        with self.assertRaises(ValueError):
            self.lib.portable_snapshot(root=str(self.base / "unknown"))

    def test_large_http_restore_has_session_gate_and_atomic_apply(self):
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        with opener.open(base, timeout=10) as response:
            token = re.search(r'name="sklib-token" content="([^"]+)"', response.read().decode("utf-8"))[1]
        snapshot = {"schema_version": 1, "entries": [], "orphaned_annotations": [
            {"id": f"orphan-{number}", "tags": [], "note": "x" * 10000, "favorite": False, "state": "useful"} for number in range(8)]}
        def post(path, value, session=token):
            request = urllib.request.Request(base + path, data=json.dumps(value).encode("utf-8"),
                headers={"Content-Type": "application/json", "X-Sklib-Token": session})
            with opener.open(request, timeout=10) as response:
                return json.load(response)
        with self.assertRaises(urllib.error.HTTPError) as denied:
            post("/api/records/import-preview", {"snapshot": snapshot}, session="wrong")
        self.assertEqual(denied.exception.code, 403)
        preview = post("/api/records/import-preview", {"snapshot": snapshot})
        self.assertEqual(preview["counts"]["insert"], 8)
        self.assertEqual(post("/api/records/import-apply", {"snapshot": snapshot, "preview_token": preview["preview_token"]})["updated"], 8)

    def backup(self):
        self.sample()
        self.lib.annotate(self.pdf_id(), tags=["PDF", "资料"], note="portable note", state="useful", favorite=True)
        return self.lib.snapshot()

    def target(self, root=None):
        target = Library(self.base / "target-state")
        target.index(root or self.root)
        return target

    def apply(self, target, snapshot, **options):
        preview = target.restore_annotations(snapshot, **options)
        return target.restore_annotations(snapshot, apply=True, expected_preview=preview["preview_token"], **options)

    def test_restore_preserves_notes_and_does_not_register_or_write_sources(self):
        snapshot = self.backup()
        target = self.target()
        before = {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        result = self.apply(target, snapshot)
        self.assertEqual(result["updated"], 1)
        annotation = target.get(self.pdf_id())["annotation"]
        self.assertEqual(annotation["note"], "portable note")
        self.assertEqual(json.loads(annotation["tags"]), ["PDF", "资料"])
        self.assertTrue(annotation["favorite"])
        self.assertEqual(before, {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()})

    def test_existing_record_default_keep_and_explicit_resolution(self):
        snapshot = self.backup()
        target = self.target()
        identifier = self.pdf_id()
        target.annotate(identifier, note="new local note")
        result = self.apply(target, snapshot)
        self.assertEqual(result["counts"]["conflict"], 1)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(target.get(identifier)["annotation"]["note"], "new local note")
        self.apply(target, snapshot, resolutions={identifier: "replace"})
        self.assertEqual(target.get(identifier)["annotation"]["note"], "portable note")

    def test_stale_preview_rejects_changed_records_and_changed_input(self):
        snapshot = self.backup()
        target = self.target()
        preview = target.restore_annotations(snapshot, policy="replace")
        target.annotate(self.pdf_id(), note="concurrent edit")
        with self.assertRaises(OperationFailure) as failure:
            target.restore_annotations(snapshot, policy="replace", apply=True, expected_preview=preview["preview_token"])
        self.assertEqual(failure.exception.code, "restore_preview_stale")
        self.assertEqual(target.get(self.pdf_id())["annotation"]["note"], "concurrent edit")

    def test_root_mapping_and_current_library_migration_retain_original(self):
        snapshot = self.backup()
        new_root = self.base / "renamed"
        shutil.copytree(self.root, new_root)
        self.lib.index(new_root)
        preview = self.lib.migrate_annotations(str(self.root), str(new_root))
        result = self.lib.migrate_annotations(str(self.root), str(new_root), apply=True, expected_preview=preview["preview_token"])
        self.assertEqual(result["updated"], 1)
        migrated = self.lib.search("pdf", root=str(new_root))["results"][0]
        self.assertEqual(migrated["note"], "portable note")
        self.assertEqual(self.lib.get(self.pdf_id())["annotation"]["note"], "portable note")

    def test_unmatched_annotations_survive_as_orphans(self):
        snapshot = self.backup()
        target = Library(self.base / "empty-target")
        result = self.apply(target, snapshot)
        self.assertEqual(result["updated"], 1)
        self.assertEqual(target.snapshot()["orphaned_annotations"][0]["note"], "portable note")
        self.assertEqual(target.status()["roots"], [])
        target.index(self.root)
        self.assertEqual(target.get(self.pdf_id())["annotation"]["note"], "portable note")

    def test_all_annotations_fts_and_event_roll_back_on_failure(self):
        snapshot = self.backup()
        second_id = self.lib.search("vue")["results"][0]["id"]
        self.lib.annotate(second_id, note="second note")
        snapshot = self.lib.snapshot()
        target = self.target()
        preview = target.restore_annotations(snapshot)
        original = target._write_annotation
        calls = 0
        def fail_second(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise sqlite3.OperationalError("fixture locked")
            return original(*args)
        with patch.object(target, "_write_annotation", side_effect=fail_second):
            with self.assertRaises(sqlite3.Error):
                target.restore_annotations(snapshot, apply=True, expected_preview=preview["preview_token"])
        self.assertIsNone(target.get(self.pdf_id())["annotation"])
        self.assertIsNone(target.get(second_id)["annotation"])
        self.assertFalse(any(event["action"] == "annotations.restore" for event in target.history()))
        self.assertEqual(target.search("portable note")["returned"], 0)

    def test_invalid_snapshot_fails_before_any_annotation_write(self):
        snapshot = self.backup()
        target = self.target()
        invalid = []
        for key, value in [("tags", None), ("note", None), ("favorite", 1), ("state", None), ("relative_path", "../escape")]:
            item = copy.deepcopy(snapshot)
            item["entries"][0][key] = value
            invalid.append(item)
        duplicate = copy.deepcopy(snapshot)
        duplicate["entries"].append(duplicate["entries"][0])
        invalid.append(duplicate)
        for item in invalid:
            with self.subTest(item=item), self.assertRaises(ValueError):
                target.restore_annotations(item)
        self.assertIsNone(target.get(self.pdf_id())["annotation"])

    def test_preview_paging_and_explicit_target_collision(self):
        snapshot = self.backup()
        target = self.target()
        first = target.restore_annotations(snapshot, limit=1)
        second = target.restore_annotations(snapshot, offset=1, limit=1)
        self.assertEqual(first["preview_token"], second["preview_token"])
        self.assertEqual(first["next_offset"], 1)
        ids = [entry["id"] for entry in snapshot["entries"]]
        with self.assertRaises(ValueError):
            target.restore_annotations(snapshot, entry_map={ids[0]: ids[1]})

    def test_cli_preview_and_apply(self):
        snapshot = self.backup()
        target = self.target()
        path = self.base / "backup.json"
        path.write_text(json.dumps(snapshot), encoding="utf-8")
        command = [sys.executable, "-m", "sklib", "--home", str(target.store.home), "records", "import", str(path)]
        preview = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        token = json.loads(preview.stdout)["preview_token"]
        applied = subprocess.run(command + ["--apply", "--preview-token", token], capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(json.loads(applied.stdout)["updated"], 1)
