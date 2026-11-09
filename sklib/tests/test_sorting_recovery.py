"""Sorting queues and failure outcomes; fixtures never modify source repositories."""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
import threading
import urllib.request
import urllib.error
from contextlib import contextmanager
from unittest.mock import patch

import test_library as fixtures
from test_library import Fixture, skill
from sklib.evaluation import evaluate
from sklib.mcp import Session
from sklib.records import Records
from sklib.semantic import embed_library
from sklib.web import create_server


class SortingRecoveryTests(Fixture):
    def test_browse_queues_tags_and_duplicates_preserve_each_location(self):
        value = skill("same", "Repeated skill")
        self.write("a/same/SKILL.md", value)
        self.write("b/same/SKILL.md", value)
        self.write("broken/SKILL.md", "# No metadata\n")
        self.write("web/package.json", '{"name":"sample-web"}')
        self.lib.index(self.root)
        all_items = self.lib.browse(kind="all")
        self.assertEqual(all_items["total"], 4)
        self.assertEqual(all_items["counts"]["duplicates"], 2)
        duplicate = self.lib.browse(queue="duplicates")
        self.assertEqual(duplicate["returned"], 2)
        identifier = duplicate["results"][0]["id"]
        self.lib.annotate(identifier, tags=["tools"], state="useful")
        self.assertEqual(self.lib.browse(queue="unclassified")["total"], 3)
        self.assertEqual(self.lib.browse(queue="needs_review")["total"], 3)
        self.assertEqual(self.lib.browse(queue="warnings")["total"], 1)
        self.assertEqual(self.lib.browse(tags=["tools"])["results"][0]["id"], identifier)
        self.assertEqual(self.lib.search("same", queue="unclassified")["returned"], 1)
        self.assertEqual(self.lib.browse(project_type="javascript")["total"], 1)

    def test_browse_pagination_and_validation(self):
        for index in range(6):
            self.write(f"s{index}/SKILL.md", skill(f"s{index}", "Queue entry"))
        self.lib.index(self.root)
        first = self.lib.browse(limit=2)
        second = self.lib.browse(limit=2, offset=first["next_offset"])
        self.assertFalse({r["id"] for r in first["results"]} & {r["id"] for r in second["results"]})
        for options in [{"queue": "invalid"}, {"limit": True}, {"offset": -1}, {"sort": "SQL"}]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.lib.browse(**options)
        self.write("quoted/SKILL.md", "---\nname: " + json.dumps('"' * 200) + "\ndescription: " + json.dumps('"' * 1000) + "\n---\nspecial-budget\n")
        self.lib.index(self.root)
        for result in [self.lib.browse(max_chars=1500), self.lib.search("special-budget", max_chars=1500)]:
            self.assertLessEqual(sum(len(json.dumps(item, ensure_ascii=False, sort_keys=True)) for item in result["results"]), 1500)

    def test_index_item_failure_rolls_back_document_and_fts_together(self):
        self.sample()
        identifier = self.pdf_id()
        self.write("pdf/skills/pdf-tables/SKILL.md", skill("replacement", "New body"))
        with patch("sklib.indexer.refresh_fts", side_effect=ValueError("injected FTS update failure")):
            report = self.lib.index(self.root)
        self.assertFalse(report["complete"])
        with self.lib.store.connect() as db:
            name = db.execute("SELECT name FROM documents WHERE id=?", (identifier,)).fetchone()[0]
        self.assertEqual(name, "pdf-tables")
        self.assertEqual(self.pdf_id(), identifier)
        self.assertIn("recovery", report["failures"][0])

    def test_cli_partial_scan_has_distinct_exit_status(self):
        self.write("invalid/SKILL.md", "").write_bytes(b"\xff invalid encoding")
        result = subprocess.run([sys.executable, "-m", "sklib", "--home", str(self.lib.store.home), "index", str(self.root)], capture_output=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertFalse(json.loads(result.stdout)["complete"])

    def test_progress_failure_after_commit_keeps_successful_result(self):
        self.write("new/SKILL.md", skill("new", "Progress notification"))
        def progress(value):
            if value["phase"] == "complete":
                raise OSError("progress pipe closed")
        result = self.lib.index(self.root, progress=progress)
        self.assertTrue(result["complete"])
        self.assertEqual(result["progress_warning"]["outcome"], "completed")
        self.assertEqual(self.lib.status()["documents"], 1)

    def test_annotation_failure_rolls_back_and_preserves_old_note(self):
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, note="saved note")
        with patch("sklib.service.refresh_fts", side_effect=sqlite3.OperationalError("database is locked")):
            with self.assertRaises(sqlite3.Error):
                self.lib.annotate(identifier, note="failed note")
        self.assertEqual(self.lib.get(identifier)["annotation"]["note"], "saved note")

    def test_blank_tags_rejected_and_whitespace_normalized(self):
        self.sample()
        identifier = self.pdf_id()
        result = self.lib.annotate(identifier, tags=[" tools ", "tools", " 办公 "])
        self.assertEqual(result["tags"], ["tools", "办公"])
        with self.assertRaises(ValueError):
            self.lib.annotate(identifier, tags=["   "])
        self.assertEqual(self.lib.browse(tags=[" 办公 "])["total"], 1)

    def test_database_write_failure_rolls_back_whole_scan(self):
        self.sample()
        self.write("new/SKILL.md", skill("new", "New source"))
        before = self.lib.snapshot()
        with patch("sklib.indexer.refresh_fts", side_effect=sqlite3.OperationalError("injected disk I/O failure")):
            with self.assertRaises(sqlite3.Error):
                self.lib.index(self.root)
        self.assertEqual(self.lib.snapshot(), before)

    def test_large_failure_report_is_bounded_and_counted(self):
        for index in range(205):
            self.write(f"f{index}/SKILL.md", "").write_bytes(b"\xff")
        result = self.lib.index(self.root)
        self.assertFalse(result["complete"])
        self.assertEqual(result["failure_count"], 205)
        self.assertEqual(len(result["failures"]), 200)
        self.assertTrue(result["errors_truncated"])
        self.assertEqual(result["failures"][0]["code"], "encoding_error")

    def test_export_failure_preserves_prior_catalog(self):
        self.sample()
        records = Records(self.lib)
        records.export()
        previous = records.catalog.read_bytes()
        self.lib.annotate(self.pdf_id(), note="new note")
        with patch("sklib.records.os.replace", side_effect=OSError("injected disk failure")):
            with self.assertRaises(OSError):
                records.export()
        self.assertEqual(records.catalog.read_bytes(), previous)
        self.assertEqual(list(records.directory.glob(".catalog-*")), [])

    def test_git_success_is_not_reported_as_failure_when_audit_write_fails(self):
        self.sample()
        records = Records(self.lib)
        records.init()
        for key, value in [("user.name", "Fixture"), ("user.email", "fixture@example.invalid")]:
            subprocess.run(["git", "-C", str(records.directory), "config", key, value], check=True, capture_output=True)
        real_connect = self.lib.store.connect
        calls = 0
        @contextmanager
        def fail_audit():
            nonlocal calls
            calls += 1
            if calls == 2:
                raise sqlite3.OperationalError("database is locked")
            with real_connect() as db:
                yield db
        with patch.object(self.lib.store, "connect", fail_audit):
            result = records.commit("Completed despite audit failure")
        self.assertTrue(result["committed"])
        self.assertEqual(result["warnings"][0]["code"], "activity_log_failed")
        self.assertEqual(records.log()["commits"][0]["commit"], result["commit"])
        with patch.object(self.lib.store, "connect", side_effect=sqlite3.DatabaseError("unavailable")):
            self.assertEqual(records.status()["head"], result["commit"])

    def test_git_failed_commit_keeps_staged_file_and_can_recover(self):
        self.sample()
        records = Records(self.lib)
        records.init()
        for key, value in [("user.name", ""), ("user.email", ""), ("user.useConfigOnly", "true")]:
            subprocess.run(["git", "-C", str(records.directory), "config", key, value], check=True, capture_output=True)
        with self.assertRaises(ValueError) as error:
            records.commit("Rejected identity")
        self.assertEqual(error.exception.code, "git_commit_failed")
        status = records.status()
        self.assertIsNone(status["head"])
        self.assertIn("catalog.json", status["status"])
        for key, value in [("user.name", "Fixture"), ("user.email", "fixture@example.invalid")]:
            subprocess.run(["git", "-C", str(records.directory), "config", key, value], check=True, capture_output=True)
        preview = records.preview()
        self.assertTrue(records.commit("Recovered identity", expected_preview=preview["preview_token"])["committed"])

    def test_embedding_failure_reports_committed_progress_and_resumes(self):
        self.sample()
        provider = fixtures.SemanticTests.Provider()
        original = provider.encode
        calls = 0
        def encode(texts):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("model connection failed")
            return original(texts)
        with patch.object(provider, "encode", encode):
            with self.assertRaises(ValueError) as caught:
                embed_library(self.lib, provider, batch_size=1)
        self.assertEqual(caught.exception.progress["embedded"], 1)
        self.assertEqual(self.lib.status()["vectors"], 1)
        self.assertEqual(embed_library(self.lib, provider, batch_size=1)["embedded"], 3)

    def test_embedding_failed_batch_rolls_back_and_force_repairs_cache(self):
        self.sample()
        provider = fixtures.SemanticTests.Provider()
        with patch.object(provider, "pack", side_effect=[b"one", ValueError("invalid vector")]):
            with self.assertRaises(ValueError) as error:
                embed_library(self.lib, provider, batch_size=2)
        self.assertEqual(error.exception.progress["embedded"], 0)
        self.assertEqual(self.lib.status()["vectors"], 0)
        embed_library(self.lib, provider)
        with self.lib.store.connect() as db:
            db.execute("UPDATE vectors SET embedding=?", (b"invalid",))
        with self.assertRaises(ValueError):
            self.lib.search("PDF", mode="semantic", semantic=provider)
        self.assertEqual(embed_library(self.lib, provider, force=True)["embedded"], 4)
        self.assertGreater(self.lib.search("PDF", mode="semantic", semantic=provider)["returned"], 0)

    def test_eval_rejects_unhashable_relevance_before_queries(self):
        path = self.base / "evaluation.json"
        path.write_text('[{"query":"PDF","relevant":[{}]}]', encoding="utf-8")
        with patch.object(self.lib, "search") as search:
            with self.assertRaisesRegex(ValueError, "relevant"):
                evaluate(self.lib, path)
            search.assert_not_called()

    def test_mcp_database_failure_is_a_tool_error_and_next_request_survives(self):
        self.sample()
        session = Session(self.lib)
        session.initialized = session.ready = True
        with patch.object(self.lib, "search", side_effect=sqlite3.OperationalError("database is locked")):
            result = session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_skills", "arguments": {"query": "PDF"}}})
        self.assertTrue(result["result"]["isError"])
        failure = result["result"]["structuredContent"]
        self.assertEqual(failure["code"], "database_busy")
        self.assertTrue(failure["retryable"])
        self.assertEqual(session.dispatch({"jsonrpc": "2.0", "id": 2, "method": "ping"})["result"], {})

    def test_mcp_inventory_without_keyword(self):
        self.sample()
        session = Session(self.lib)
        session.initialized = session.ready = True
        response = session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "list_library", "arguments": {"queue": "unclassified", "kind": "skill"}}})
        self.assertEqual(response["result"]["structuredContent"]["total"], 3)

    def test_http_catalog_and_failure_contract_with_actual_rollback(self):
        self.sample()
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        token = re.search(r'name="sklib-token" content="([^"]+)"', opener.open(base).read().decode())[1]
        catalog = json.loads(opener.open(base + "/api/browse?queue=unclassified&kind=skill").read())
        self.assertEqual(catalog["total"], 3)
        with patch.object(self.lib, "browse", side_effect=sqlite3.OperationalError("database is locked")):
            with self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(base + "/api/browse")
            self.assertEqual(error.exception.code, 503)
            self.assertEqual(json.loads(error.exception.read())["code"], "database_busy")
        identifier = self.pdf_id()
        request = urllib.request.Request(base + "/api/annotate", data=json.dumps({"id":identifier,"note":"failed save"}).encode(),
            headers={"Content-Type":"application/json","X-Sklib-Token":token})
        with patch("sklib.service.refresh_fts", side_effect=sqlite3.OperationalError("database is locked")):
            with self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(request)
            payload = json.loads(error.exception.read())
            self.assertEqual(payload["outcome"], "unchanged")
            self.assertTrue(payload["retryable"])
            self.assertIn("recovery", payload)
        self.assertIsNone(self.lib.get(identifier)["annotation"])


if __name__ == "__main__":
    import unittest
    unittest.main()
