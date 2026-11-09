"""Behavioral regressions found in the second implementation review."""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import time
import threading
import urllib.request
import urllib.error
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from test_library import Fixture, skill
from sklib import indexer
from sklib.mcp import serve
from sklib.records import Records
from sklib.semantic import OllamaEmbeddings, embed_library
from sklib.web import create_server


class ReviewRegressions(Fixture):
    def test_yaml_date_key_does_not_abort_whole_index(self):
        self.write("bad/SKILL.md", "---\nname: bad\ndescription: malformed metadata\n2026-11-07: value\n---\n# Bad\n")
        self.write("good/SKILL.md", skill("good", "Good skill"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.status()["documents"], 2)
        self.assertTrue(self.lib.search("bad")["results"][0]["warnings"])

    def test_yaml_surrogate_value_cannot_break_mcp_output(self):
        self.write("bad/SKILL.md", '---\nname: bad\ndescription: valid description\nextra: "\\uD800"\n---\n# Bad\n')
        self.lib.index(self.root)
        identifier = self.lib.search("bad")["results"][0]["id"]
        json.dumps(self.lib.get(identifier), ensure_ascii=False).encode("utf-8")

    def test_manifest_exact_limit_and_true_overflow(self):
        self.sample()
        # SKILL.md and guide.md already exist; add exactly 254 regular files.
        for index in range(254):
            self.write(f"pdf/skills/pdf-tables/assets/{index}.txt", "text")
        identifier = self.pdf_id()
        value = self.lib.get(identifier)
        self.assertEqual(len(value["files"]), 256)
        self.assertFalse(value["file_list_truncated"])
        self.write("pdf/skills/pdf-tables/assets/more.txt", "text")
        self.assertTrue(self.lib.get(identifier)["file_list_truncated"])

    def test_http_malformed_inputs_and_explicit_scan_budget(self):
        self.sample()
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        token = re.search(r'name="sklib-token" content="([^"]+)"', opener.open(base).read().decode())[1]
        for path, payload, actual_token, status in [
            ("/api/annotate", b"{}", "é", 403),
            ("/api/annotate", b"[" * 2000 + b"]" * 2000, token, 400),
            ("/api/annotate", b'{"id":NaN}', token, 400),
            ("/api/index", json.dumps({"root": str(self.root), "max_files": 1}).encode(), token, 400),
            ("/api/index", json.dumps({"root": str(self.root), "max_files": "invalid"}).encode(), token, 400),
            ("/api/records/commit", b'{"message":"without preview"}', token, 400),
        ]:
            with self.subTest(path=path, status=status):
                request = urllib.request.Request(base + path, data=payload, headers={"Content-Type": "application/json", "X-Sklib-Token": actual_token})
                with self.assertRaises(urllib.error.HTTPError) as failed:
                    opener.open(request)
                self.assertEqual(failed.exception.code, status)
                self.assertIn("error", json.loads(failed.exception.read()))
        self.assertEqual(self.lib.status()["documents"], 4)

    def test_unchanged_file_is_reclassified_when_repository_appears(self):
        readme = self.write("team/nested/README.md", "# Nested project\n")
        self.lib.index(self.root, include_docs=True)
        (readme.parent / ".git").mkdir()
        self.lib.index(self.root, include_docs=True)
        self.assertEqual(self.lib.search("Nested", kind="project")["returned"], 1)
        self.assertEqual(self.lib.search("Nested", kind="document")["returned"], 0)

    def test_old_scan_cannot_prune_new_scan_or_resurrect_removed_root(self):
        self.sample()
        real_walk = indexer.os.walk
        for operation in ("new_scan", "remove_root"):
            with self.subTest(operation=operation):
                if not self.lib.status()["roots"]:
                    self.lib.index(self.root)
                scanned, release = threading.Event(), threading.Event()
                def delayed_walk(*args, **kwargs):
                    yield from real_walk(*args, **kwargs)
                    if threading.current_thread().name.startswith("older"):
                        scanned.set()
                        if not release.wait(10):
                            raise RuntimeError("test scan was not released")
                with patch("sklib.indexer.os.walk", delayed_walk), ThreadPoolExecutor(max_workers=1, thread_name_prefix="older") as pool:
                    future = pool.submit(self.lib.index, self.root)
                    try:
                        self.assertTrue(scanned.wait(10))
                        if operation == "new_scan":
                            self.write("new/SKILL.md", skill("new", "Newly indexed skill"))
                            self.lib.index(self.root)
                        else:
                            self.lib.remove_root(self.root)
                    finally:
                        release.set()
                    with self.assertRaisesRegex(ValueError, "changed|scan"):
                        future.result(timeout=10)
                if operation == "new_scan":
                    self.assertEqual(self.lib.search("new")["returned"], 1)
                else:
                    self.assertEqual(self.lib.status()["documents"], 0)

    def test_removed_source_notes_remain_in_export(self):
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, note="retain my review", tags=["important"])
        self.lib.remove_root(self.root)
        exported = self.lib.snapshot()
        orphan = next(item for item in exported.get("orphaned_annotations", []) if item["id"] == identifier)
        self.assertEqual(orphan["note"], "retain my review")
        self.assertEqual(orphan["tags"], ["important"])

    def test_pure_semantic_order_is_not_changed_by_exact_name(self):
        self.write("exact/SKILL.md", skill("exact", "Unrelated text"))
        self.write("meaning/SKILL.md", skill("meaning", "Relevant idea"))
        self.lib.index(self.root)
        class Provider:
            model = "test:review"
            pack = staticmethod(OllamaEmbeddings.pack)
            similarity = staticmethod(OllamaEmbeddings.similarity)
            def encode(self, texts):
                return [[0., 1.] if "Unrelated" in text else [1., 0.] for text in texts]
        provider = Provider()
        embed_library(self.lib, provider)
        result = self.lib.search("exact", mode="semantic", semantic=provider)
        self.assertEqual(result["results"][0]["name"], "meaning")

    def test_compact_cli_result_is_readable_without_path_field(self):
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, tags=[str(i) + "x" * 70 for i in range(30)], note="n" * 1000)
        result = subprocess.run([sys.executable, "-m", "sklib", "--home", str(self.lib.store.home),
                                 "search", "pdf-tables", "--max-chars", "1500"],
                                capture_output=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(identifier, result.stdout)

    def test_non_unicode_mcp_frame_does_not_kill_following_requests(self):
        messages = [
            {"jsonrpc": "2.0", "id": "\ud800", "method": "ping"},
            {"jsonrpc": "2.0", "id": 2, "method": "ping"},
        ]
        source = io.BytesIO(("\n".join(json.dumps(value) for value in messages) + "\n").encode())
        output = io.BytesIO()
        serve(self.lib, source, output)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(responses[-1]["id"], 2)
        self.assertIn("error", responses[0])

    def test_nonfinite_mcp_frame_is_rejected_then_ping_succeeds(self):
        output = io.BytesIO()
        serve(self.lib, io.BytesIO(b'{"jsonrpc":"2.0","id":NaN,"method":"ping"}\n{"jsonrpc":"2.0","id":2,"method":"ping"}\n'), output)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[-1]["id"], 2)

    def records(self):
        self.sample()
        records = Records(self.lib)
        records.init()
        for name, value in (("user.name", "Review fixture"), ("user.email", "review@example.invalid")):
            subprocess.run(["git", "-C", str(records.directory), "config", name, value], check=True, capture_output=True)
        return records

    def test_commit_rejects_stale_preview_and_keeps_reviewed_file(self):
        records = self.records()
        preview = records.preview()
        reviewed = records.catalog.read_bytes()
        self.assertIn('"entries"', preview["diff"])
        self.lib.annotate(self.pdf_id(), note="changed after preview")
        with self.assertRaisesRegex(ValueError, "changed since preview"):
            records.commit("Old preview", expected_preview=preview["preview_token"])
        self.assertEqual(records.catalog.read_bytes(), reviewed)
        self.assertEqual(records.log()["commits"], [])
        fresh = records.preview()
        self.assertTrue(records.commit("Fresh preview", expected_preview=fresh["preview_token"])["committed"])
        self.lib.remove_root(self.root)
        preview = records.preview()
        records.commit("Retain orphaned notes", expected_preview=preview["preview_token"])
        saved = json.loads(subprocess.run(["git", "-C", str(records.directory), "show", "HEAD:catalog.json"], capture_output=True, encoding="utf-8", check=True).stdout)
        self.assertEqual(saved["orphaned_annotations"][0]["note"], "changed after preview")

    def test_commit_rejects_changed_head_and_preserves_unicode_subject(self):
        records = self.records()
        records.commit("Review\u2028subject")
        log = records.log()["commits"]
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["message"], "Review\u2028subject")
        self.lib.annotate(self.pdf_id(), note="uncommitted review")
        preview = records.preview()
        external = records.directory / "external.txt"
        external.write_text("external content", encoding="utf-8")
        subprocess.run(["git", "-C", str(records.directory), "add", "external.txt"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(records.directory), "commit", "--only", "-m", "External commit", "--", "external.txt"], check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "changed since preview"):
            records.commit("Stale base", expected_preview=preview["preview_token"])

    def test_record_export_waits_for_another_process(self):
        records = self.records()
        code = "from pathlib import Path; import sys; from sklib.locking import exclusive\nwith exclusive(Path(sys.argv[1])):\n print('locked',flush=True)\n sys.stdin.readline()\n"
        child = subprocess.Popen([sys.executable, "-c", code, str(records.lock)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        try:
            self.assertEqual(child.stdout.readline().strip(), "locked")
            entered = threading.Event()
            original = records._snapshot_bytes
            def snapshot():
                entered.set()
                return original()
            with patch.object(records, "_snapshot_bytes", side_effect=snapshot), ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(records.export)
                try:
                    self.assertFalse(entered.wait(.15), "export bypassed the process lock")
                finally:
                    child.stdin.write("release\n")
                    child.stdin.flush()
                result = future.result(timeout=15)
                self.assertTrue(entered.is_set())
                self.assertTrue(result["changed"])
            child.wait(timeout=5)
            self.assertEqual(child.returncode, 0, child.stderr.read())
        finally:
            if child.poll() is None:
                child.kill()
                child.wait(timeout=5)
            child.stdin.close()
            child.stdout.close()
            child.stderr.close()


if __name__ == "__main__":
    unittest.main()
