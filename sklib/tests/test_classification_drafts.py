from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import urllib.request
import urllib.error
from unittest.mock import patch

import test_library as fixtures
from sklib.failures import OperationFailure
from sklib.indexer import refresh_fts
from sklib.web import create_server


class ClassificationTests(fixtures.Fixture):
    def test_browser_draft_store_copy_isolation_and_failure_recovery(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node is not installed")
        from pathlib import Path
        script = Path(__file__).with_name("check_drafts.js")
        result = subprocess.run([node, str(script)], capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)

    def ids(self):
        return [item["id"] for item in self.lib.browse(kind="all")["results"]]

    def versions(self, identifiers):
        return {item["id"]: item["annotation_revision"] for item in self.lib.annotation_states(identifiers)["entries"]}

    def test_batch_tag_modes_state_favorite_preserve_notes_and_sources(self):
        self.sample()
        identifiers = self.ids()
        for identifier in identifiers:
            self.lib.annotate(identifier, tags=["existing"], note="Keep this note", favorite=True)
        result = self.lib.annotate_batch(identifiers, tags=[" tools ", "tools"], state="useful", expected_revisions=self.versions(identifiers))
        self.assertEqual(result["updated"], 4)
        for identifier in identifiers:
            annotation = self.lib.get(identifier)["annotation"]
            self.assertEqual(json.loads(annotation["tags"]), ["existing", "tools"])
            self.assertEqual(annotation["note"], "Keep this note")
            self.assertEqual(annotation["state"], "useful")
            self.assertTrue(annotation["favorite"])
        self.lib.annotate_batch(identifiers, tags=["existing"], tag_mode="remove", favorite=False)
        self.assertEqual(self.lib.browse(tags=["tools"])["total"], 4)
        self.lib.annotate_batch(identifiers, tags=["replacement"], tag_mode="replace")
        self.assertEqual(self.lib.browse(tags=["tools"])["total"], 0)
        self.lib.annotate_batch(identifiers, tag_mode="clear")
        self.assertEqual(self.lib.browse(queue="unclassified")["total"], 4)
        self.assertTrue((self.root / "pdf/skills/pdf-tables/SKILL.md").exists())

    def test_invalid_batch_inputs_do_not_change_annotations(self):
        self.sample()
        identifiers = self.ids()
        cases = [([], {}), (identifiers * 2, {}), (identifiers * 26, {}), (identifiers, {"tag_mode": "unknown"}),
                 (identifiers, {"tags": [" "]}), (identifiers, {"favorite": 1}), (identifiers, {}),
                 (identifiers, {"state": "invalid"}), (identifiers, {"tag_mode": "clear", "tags": ["x"]}),
                 (identifiers, {"tags": ["x"], "expected_revisions": {identifier: None for identifier in identifiers}})]
        for selection, options in cases:
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.lib.annotate_batch(selection, **options)
        with self.lib.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM annotations").fetchone()[0], 0)

    def test_missing_entry_and_one_stale_version_reject_entire_batch(self):
        self.sample()
        identifiers = self.ids()
        with self.assertRaises(OperationFailure):
            self.lib.annotate_batch([identifiers[0], "missing"], tags=["new"])
        self.assertIsNone(self.lib.get(identifiers[0])["annotation"])
        versions = self.versions(identifiers)
        self.lib.annotate(identifiers[-1], note="Changed by another editor")
        with self.assertRaises(OperationFailure) as error:
            self.lib.annotate_batch(identifiers, tags=["new"], expected_revisions=versions)
        self.assertEqual(error.exception.code, "annotation_conflict")
        for identifier in identifiers[:-1]:
            self.assertIsNone(self.lib.get(identifier)["annotation"])
        self.assertEqual(self.lib.get(identifiers[-1])["annotation"]["note"], "Changed by another editor")

    def test_second_fts_write_failure_rolls_back_annotations_fts_and_event(self):
        self.sample()
        identifiers = self.ids()
        before = self.lib.history()
        calls = []
        def fail_second(db, identifier, **options):
            calls.append(identifier)
            if len(calls) == 2:
                raise sqlite3.OperationalError("injected write failure")
            return refresh_fts(db, identifier, **options)
        with patch("sklib.service.refresh_fts", side_effect=fail_second), self.assertRaises(sqlite3.Error):
            self.lib.annotate_batch(identifiers, tags=["atomicrollbackmarker"])
        self.assertEqual(self.lib.history(), before)
        self.assertFalse(self.lib.search("atomicrollbackmarker", kind="all")["results"])
        for identifier in identifiers:
            self.assertIsNone(self.lib.get(identifier)["annotation"])
        with self.lib.store.connect() as db:
            db.execute("INSERT INTO documents_fts(documents_fts) VALUES('integrity-check')")

    def test_tag_union_limit_validated_before_any_writes(self):
        self.sample()
        identifiers = self.ids()
        self.lib.annotate(identifiers[-1], tags=[f"tag-{number}" for number in range(30)])
        with self.assertRaises(ValueError):
            self.lib.annotate_batch(identifiers, tags=["one-too-many"])
        self.assertIsNone(self.lib.get(identifiers[0])["annotation"])

    def test_unchanged_batch_preserves_versions_and_activity(self):
        self.sample()
        identifiers = self.ids()
        self.lib.annotate_batch(identifiers, tags=["stable"])
        before, history = self.versions(identifiers), self.lib.history()
        result = self.lib.annotate_batch(identifiers, tags=["stable"], expected_revisions=before)
        self.assertEqual(result["updated"], 0)
        self.assertEqual(result["unchanged"], 4)
        self.assertEqual(self.versions(identifiers), before)
        self.assertEqual(self.lib.history(), history)

    def test_single_edit_rejects_stale_and_concurrent_writers(self):
        self.sample()
        identifier = self.pdf_id()
        old = self.lib.get(identifier)["annotation_revision"]
        first = self.lib.annotate(identifier, note="First", expected_annotation_revision=old)
        with self.assertRaises(OperationFailure):
            self.lib.annotate(identifier, note="Stale", expected_annotation_revision=old)
        barrier = threading.Barrier(2)
        def write(note):
            barrier.wait(timeout=3)
            try:
                self.lib.annotate(identifier, note=note, expected_annotation_revision=first["annotation_revision"])
                return "saved"
            except OperationFailure as exc:
                return exc.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(write, ["Second", "Third"]))
        self.assertCountEqual(results, ["saved", "annotation_conflict"])
        self.assertIn(self.lib.get(identifier)["annotation"]["note"], ["Second", "Third"])

    def test_retrieval_versions_agree_and_source_reindex_does_not_change_notes_version(self):
        self.sample()
        identifier = self.pdf_id()
        version = self.lib.get(identifier)["annotation_revision"]
        self.assertEqual(self.lib.search("pdf-tables")["results"][0]["annotation_revision"], version)
        self.assertEqual(next(item for item in self.lib.browse()["results"] if item["id"] == identifier)["annotation_revision"], version)
        self.write("pdf/skills/pdf-tables/SKILL.md", fixtures.skill("pdf-tables", "Updated description"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.get(identifier)["annotation_revision"], version)

    def test_annotation_only_fts_update_preserves_body_and_repairs_missing_row(self):
        self.sample()
        identifier = self.pdf_id()
        with self.lib.store.connect() as db:
            rowid = db.execute("SELECT rowid FROM documents WHERE id=?", (identifier,)).fetchone()[0]
            before = tuple(db.execute("SELECT name,description,body FROM documents_fts WHERE rowid=?", (rowid,)).fetchone())
        self.lib.annotate(identifier, note="oldannotationmarker")
        self.lib.annotate(identifier, tags=["newannotationmarker"], note="")
        self.assertFalse(self.lib.search("oldannotationmarker")["results"])
        self.assertEqual(self.lib.search("newannotationmarker")["results"][0]["id"], identifier)
        with self.lib.store.connect() as db:
            self.assertEqual(tuple(db.execute("SELECT name,description,body FROM documents_fts WHERE rowid=?", (rowid,)).fetchone()), before)
            db.execute("DELETE FROM documents_fts WHERE rowid=?", (rowid,))
        self.lib.annotate(identifier, note="repairedannotationmarker")
        self.assertEqual(self.lib.search("pdf-tables")["results"][0]["id"], identifier)
        with self.lib.store.connect() as db:
            db.execute("INSERT INTO documents_fts(documents_fts) VALUES('integrity-check')")

    def test_http_batch_validation_conflict_and_summary(self):
        self.sample()
        identifiers = self.ids()
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        token = re.search(r'name="sklib-token" content="([^"]+)"', opener.open(base).read().decode())[1]
        def post(payload, session=token):
            request = urllib.request.Request(base + "/api/annotate-batch", data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json", "X-Sklib-Token": session})
            return json.loads(opener.open(request, timeout=5).read())
        for payload, session in [({"tags": ["x"]}, token), ({"ids": identifiers, "tags": ["x"]}, "wrong")]:
            with self.assertRaises(urllib.error.HTTPError):
                post(payload, session)
        summary = json.loads(opener.open(base + "/api/annotations?ids=" + ",".join(identifiers)).read())
        versions = {item["id"]: item["annotation_revision"] for item in summary["entries"]}
        result = post({"ids": identifiers, "tags": ["batchhttpmarker"], "expected_revisions": versions})
        self.assertEqual(result["updated"], 4)
        with self.assertRaises(urllib.error.HTTPError) as error:
            post({"ids": identifiers, "state": "useful", "expected_revisions": versions})
        self.assertEqual(json.loads(error.exception.read())["code"], "annotation_conflict")

    def test_cli_batch_preview_and_atomic_apply(self):
        self.sample()
        identifiers = self.ids()
        command = [sys.executable, "-m", "sklib", "--home", str(self.lib.store.home), "batch-annotate", *identifiers]
        preview = subprocess.run([*command, "--preview"], capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        versions = {item["id"]: item["annotation_revision"] for item in json.loads(preview.stdout)["entries"]}
        path = self.base / "versions.json"
        path.write_text(json.dumps(versions), encoding="utf-8")
        result = subprocess.run([*command, "--tag", "clibatchmarker", "--expected-versions", str(path)],
            capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["updated"], 4)
