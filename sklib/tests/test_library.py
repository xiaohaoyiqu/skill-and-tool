from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

from sklib.evaluation import evaluate
from sklib.mcp import MAX_MESSAGE, Session, serve
from sklib.records import Records
from sklib.semantic import OllamaEmbeddings, embed_library
from sklib.service import Library
from sklib.web import create_server


def skill(name: str, description: str, body: str = "Follow the complete workflow.") -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n# {name}\n\n{body}\n"


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sklib-test-")
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "sources"
        self.root.mkdir()
        self.lib = Library(self.base / "state")

    def write(self, path: str, text: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        return target

    def sample(self):
        self.write("pdf/skills/pdf-tables/SKILL.md", skill("pdf-tables", "Extract PDF tables into spreadsheets", "Extract tables from PDF. Read references/guide.md first."))
        self.write("pdf/skills/pdf-tables/references/guide.md", "first\nsecond\nthird\n")
        self.write("vue/.agents/skills/vue-performance/SKILL.md", skill("vue-performance", "Profile and optimize Vue frontend performance"))
        self.write("writer/humanize/SKILL.md", skill("humanize", "Rewrite prose and remove formulaic AI writing"))
        self.write("pdf/README.md", "# PDF Toolkit\nProcess PDF documents.\n")
        self.lib.index(self.root)

    def pdf_id(self):
        return self.lib.search("pdf-tables")["results"][0]["id"]


class IndexSearchTests(Fixture):
    def test_concurrent_overlapping_roots_cannot_both_register(self):
        self.write("child/a/SKILL.md", skill("a", "concurrent source"))
        def run(root):
            try:
                return self.lib.index(root)
            except ValueError:
                return None
        with ThreadPoolExecutor(max_workers=2) as workers:
            results = list(workers.map(run, [self.root, self.root / "child"]))
        self.assertEqual(sum(result is not None for result in results), 1)
        self.assertEqual(len(self.lib.status()["roots"]), 1)

    def test_incremental_and_projects(self):
        self.sample()
        self.assertEqual(self.lib.status()["counts"], {"skill": 3, "project": 1})
        report = self.lib.index(self.root)
        self.assertEqual(report["unchanged"], 4)
        self.assertEqual(report["added"], 0)
        self.assertEqual(self.lib.search("PDF", kind="project")["results"][0]["kind"], "project")

    def test_progress_callback_finishes_after_committed_index(self):
        self.sample()
        progress = []
        self.lib.index(self.root, progress=progress.append)
        self.assertEqual([value["phase"] for value in progress], ["scan", "index", "complete"])
        self.assertEqual(progress[-1]["unchanged"], 4)
        self.assertEqual(self.lib.status()["documents"], 4)

    def test_chinese_task_queries(self):
        self.sample()
        for query, expected in [("PDF 表格提取", "pdf-tables"), ("Vue 页面性能优化", "vue-performance"), ("文章改写去AI腔", "humanize")]:
            with self.subTest(query=query):
                self.assertEqual(self.lib.search(query)["results"][0]["name"], expected)

    def test_chinese_two_character_and_one_character(self):
        self.write("中文/SKILL.md", skill("中文", "提取专利技术说明书", "专利文本整理"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.search("专利")["returned"], 1)
        self.assertEqual(self.lib.search("专")["returned"], 1)

    def test_named_framework_absent_does_not_match_generic_expansions(self):
        self.write("gpu/SKILL.md", skill("gpu", "Performance optimization for GPU computation"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.search("Vue 页面性能优化")["returned"], 0)

    def test_product_named_skill_beats_incidental_product_mention(self):
        self.write("patent/SKILL.md", skill("patent-reader", "Obsidian 笔记 专利阅读", "Create Obsidian 笔记"))
        self.write("obsidian/SKILL.md", skill("obsidian-markdown", "Work with Obsidian Markdown notes"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.search("Obsidian 笔记")["results"][0]["name"], "obsidian-markdown")

    def test_query_syntax_is_literal(self):
        self.sample()
        self.assertIsInstance(self.lib.search('" OR * NEAR() - foo : pdf')["results"], list)
        for query in ["!!!", "*", "'\"()"]:
            self.assertEqual(self.lib.search(query)["returned"], 0)

    def test_duplicates_preserve_locations(self):
        value = skill("same", "Compare exact duplicate skills")
        self.write("a/same/SKILL.md", value)
        self.write("b/same/SKILL.md", value.replace("\n", "\r\n"))
        self.lib.index(self.root)
        results = self.lib.search("same")["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["duplicate_count"], 1)
        self.assertEqual(len(results[0]["other_locations"]), 1)

    def test_same_name_different_content_not_merged(self):
        self.write("a/same/SKILL.md", skill("same", "PDF extraction"))
        self.write("b/same/SKILL.md", skill("same", "Vue frontend"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.search("same")["returned"], 2)

    def test_annotations_search_and_filters(self):
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, tags=["收藏", "办公"], note="报销清单整理", favorite=True, state="useful")
        result = self.lib.search("报销", tags=["办公"], favorite=True, state="useful")
        self.assertEqual(result["results"][0]["id"], identifier)
        self.assertEqual(result["results"][0]["evidence"]["field"], "annotation")
        self.assertEqual(self.lib.search("PDF", tags=["不存在"])["returned"], 0)
        self.lib.index(self.root, verify=True)
        self.assertTrue(self.lib.search("PDF")["results"][0]["favorite"])

    def test_deletion_prunes_and_annotation_survives_reappearance(self):
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, note="preserve this")
        source = Path(self.lib.get(identifier)["path"])
        body = source.read_text(encoding="utf-8")
        source.unlink()
        self.assertEqual(self.lib.index(self.root)["removed"], 1)
        source.write_text(body, encoding="utf-8")
        self.lib.index(self.root)
        self.assertEqual(self.lib.get(identifier)["annotation"]["note"], "preserve this")

    def test_malformed_yaml_retained_with_warning(self):
        self.write("bad/SKILL.md", "---\nname: [broken\n---\n# Useful content\n")
        self.write("alias/SKILL.md", "---\nname: alias\na: &a [*a]\n---\nreference\n")
        self.lib.index(self.root)
        results = self.lib.search("bad")["results"]
        self.assertTrue(results[0]["warnings"])

    def test_nonfinite_yaml_metadata_cannot_corrupt_json_wire(self):
        self.write("number/SKILL.md", "---\nname: number\ndescription: numeric metadata\nvalue: .nan\n---\n# Number\n")
        self.lib.index(self.root)
        identifier = self.lib.search("number")["results"][0]["id"]
        value = self.lib.get(identifier)
        json.dumps(value, allow_nan=False)
        self.assertTrue(value["warnings"])

    def test_defaults_skip_tests_and_can_include_docs(self):
        self.write("tests/fake/SKILL.md", skill("fake", "Should not index test fixtures"))
        self.write("docs/guide.md", "# Architecture\nRetrieval structure\n")
        self.lib.index(self.root)
        self.assertEqual(self.lib.status()["documents"], 0)
        self.lib.index(self.root, include_docs=True)
        self.assertEqual(self.lib.search("Architecture", kind="document")["returned"], 1)

    def test_limits_leave_old_index_intact(self):
        self.sample()
        before = self.lib.snapshot()
        with self.assertRaises(ValueError):
            self.lib.index(self.root, max_files=1)
        self.assertEqual(self.lib.snapshot(), before)

    def test_partial_scan_never_prunes(self):
        self.sample()
        with patch("sklib.indexer.os.walk") as walk:
            def partial(*args, **kwargs):
                kwargs["onerror"](PermissionError("unreadable subtree"))
                return iter([])
            walk.side_effect = partial
            report = self.lib.index(self.root)
        self.assertFalse(report["complete"])
        self.assertEqual(report["removed"], 0)
        self.assertEqual(self.lib.status()["documents"], 4)

    def test_overlap_and_state_directory_rejected(self):
        self.sample()
        with self.assertRaises(ValueError):
            self.lib.index(self.root / "pdf")
        with self.assertRaises(ValueError):
            self.lib.index(self.lib.store.home)

    def test_remove_source_preserves_files_and_annotations(self):
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, note="preserve")
        result = self.lib.remove_root(self.root)
        self.assertEqual(result["removed_from_index"], 4)
        self.assertEqual(self.lib.status()["documents"], 0)
        self.assertTrue((self.root / "pdf/skills/pdf-tables/SKILL.md").exists())
        self.lib.index(self.root)
        self.assertEqual(self.lib.get(identifier)["annotation"]["note"], "preserve")

    def test_result_budget_bounds_large_metadata(self):
        self.write("big/SKILL.md", skill("big", "x" * 10000 + " keyword"))
        self.lib.index(self.root)
        identifier = self.lib.search("keyword")["results"][0]["id"]
        self.lib.annotate(identifier, tags=[str(i) + "z" * 70 for i in range(30)])
        result = self.lib.search("keyword", max_chars=1500)
        self.assertTrue(result["results"][0]["result_truncated"])
        self.assertLessEqual(sum(len(json.dumps(item, ensure_ascii=False, sort_keys=True)) for item in result["results"]), 1500)

    def test_verify_detects_same_stat_modification(self):
        path = self.write("thing/SKILL.md", skill("thing", "old content"))
        self.lib.index(self.root)
        stat = path.stat()
        path.write_bytes(skill("thing", "new content").encode("utf-8"))
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        self.assertEqual(self.lib.index(self.root, verify=True)["updated"], 1)

    def test_eval_reports_misses(self):
        self.sample()
        dataset = self.base / "eval.json"
        dataset.write_text(json.dumps([{"query": "PDF 表格提取", "relevant": ["pdf-tables"]}, {"query": "nonexistentidentifier", "relevant": ["missing"]}]), encoding="utf-8")
        result = evaluate(self.lib, dataset)
        self.assertEqual(result["hit_at_k"], .5)
        self.assertEqual(result["mrr_at_k"], .5)


class ResourceTests(Fixture):
    def test_invalid_api_types_return_validation_errors(self):
        self.sample()
        with self.assertRaises(ValueError):
            self.lib.get([])
        with self.assertRaises(ValueError):
            self.lib.annotate(self.pdf_id(), state=[])
        with self.assertRaises(ValueError):
            self.lib.read_file(self.pdf_id(), None)

    def test_full_read_paging_and_stale_revision(self):
        self.sample()
        identifier = self.pdf_id()
        doc = self.lib.get(identifier)
        self.assertIn("references/guide.md", doc["files"])
        self.assertIn("Follow", self.lib.get(self.lib.search("vue-performance")["results"][0]["id"])["content"])
        first = self.lib.read_file(identifier, "references/guide.md", max_lines=2)
        self.assertEqual(first["next_start_line"], 3)
        last = self.lib.read_file(identifier, "references/guide.md", start_line=3, expected_revision=first["revision"])
        self.assertEqual(last["content"], "third\n")
        self.assertIsNone(last["next_start_line"])
        Path(doc["path"]).write_text(doc["content"] + "changed", encoding="utf-8")
        self.assertTrue(self.lib.get(identifier)["stale"])
        with self.assertRaises(ValueError):
            self.lib.get(identifier, expected_revision=doc["revision"])

    def test_path_escape_and_cross_document_reads_rejected(self):
        self.sample()
        for path in ["../SKILL.md", "..\\outside.txt", "C:/Windows/win.ini", "/etc/passwd", "references/../../outside", ".env"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.lib.read_file(self.pdf_id(), path)
        project = self.lib.search("PDF", kind="project")["results"][0]["id"]
        with self.assertRaises(ValueError):
            self.lib.read_file(project, "skills/pdf-tables/SKILL.md")

    def test_long_lines_never_disappear_silently(self):
        self.sample()
        self.write("pdf/skills/pdf-tables/references/long.md", "x" * 300)
        with self.assertRaisesRegex(ValueError, "One line"):
            self.lib.read_file(self.pdf_id(), "references/long.md", max_chars=100)


class ProtocolTests(Fixture):
    def session(self):
        session = Session(self.lib)
        result = session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}})
        self.assertEqual(result["result"]["protocolVersion"], "2025-11-25")
        session.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return session

    def test_lifecycle_tools_call_and_input_validation(self):
        self.sample()
        session = self.session()
        tools = session.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]
        self.assertEqual({tool["name"] for tool in tools}, {"search_skills", "list_library", "get_skill", "read_skill_file", "check_source"})
        for arguments in [{"query": "PDF"}, {"query": "PDF", "limit": True}, {"query": "PDF", "unknown": 1}]:
            result = session.dispatch({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_skills", "arguments": arguments}})
            if len(arguments) == 1:
                self.assertTrue(result["result"]["structuredContent"]["results"])
            else:
                self.assertEqual(result["error"]["code"], -32602)
        self.assertIsNone(session.dispatch({"jsonrpc": "2.0", "method": "notifications/cancelled", "params": {"requestId": 3}}))

    def test_stdio_bad_frames_and_oversized_request_recover(self):
        request = {"jsonrpc": "2.0", "id": 9, "method": "ping"}
        data = b"invalid\n" + b"x" * (MAX_MESSAGE + 3) + b"\n" + json.dumps(request).encode() + b"\n"
        target = io.BytesIO()
        serve(self.lib, io.BytesIO(data), target)
        results = [json.loads(line) for line in target.getvalue().splitlines()]
        self.assertEqual(len(results), 3)
        self.assertEqual(results[-1]["id"], 9)

    def test_cli_subprocess_and_real_mcp_wire(self):
        self.sample()
        command = [sys.executable, "-m", "sklib", "--home", str(self.lib.store.home)]
        result = subprocess.run([*command, "search", "PDF 表格提取", "--json"], capture_output=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["results"][0]["name"], "pdf-tables")
        messages = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}}, {"jsonrpc": "2.0", "method": "notifications/initialized"}, {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_skill", "arguments": {"id": self.pdf_id()}}}]
        wire = subprocess.run([*command, "mcp"], input="\n".join(json.dumps(m) for m in messages) + "\n", capture_output=True, encoding="utf-8", timeout=15)
        self.assertEqual(wire.returncode, 0, wire.stderr)
        replies = [json.loads(line) for line in wire.stdout.splitlines()]
        self.assertEqual(len(replies), 2)
        self.assertIn("Read references/guide.md", replies[1]["result"]["structuredContent"]["content"])


class GitTests(Fixture):
    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.records.directory), *args], capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()

    def setup_records(self):
        self.sample()
        self.records = Records(self.lib)
        self.records.init()
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")

    def test_git_commit_noop_history_and_unrelated_staged_preserved(self):
        self.setup_records()
        unrelated = self.records.directory / "unrelated.txt"
        unrelated.write_text("preserve staged file", encoding="utf-8")
        self.git("add", "unrelated.txt")
        result = self.records.commit("Initial review records")
        self.assertTrue(result["committed"])
        self.assertEqual(self.git("show", "--pretty=", "--name-only", "HEAD"), "catalog.json")
        self.assertIn("unrelated.txt", self.git("diff", "--cached", "--name-only"))
        self.assertFalse(self.records.commit("No changes")["committed"])
        self.lib.annotate(self.pdf_id(), note="personal improvement")
        self.assertTrue(self.records.preview()["pending_changes"])
        self.records.commit("Add review note")
        self.assertEqual(len(self.records.log()["commits"]), 2)
        snapshot = json.loads(self.git("show", "HEAD:catalog.json"))
        self.assertTrue(any(item["note"] == "personal improvement" for item in snapshot["entries"]))

    def test_requires_explicit_init_and_does_not_use_parent_repo(self):
        records = Records(self.lib)
        with self.assertRaises(ValueError):
            records.commit("not initialized")


class WebTests(Fixture):
    def test_http_origin_session_mutations_and_static_assets(self):
        self.sample()
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        page = opener.open(base).read().decode()
        import re
        token = re.search(r'name="sklib-token" content="([^"]+)"', page)[1]
        for path in ["/app.js", "/styles.css", "/api/status", "/api/search?q=PDF"]:
            self.assertEqual(opener.open(base + path).status, 200)
        for headers in [{"Origin": "https://evil.invalid"}, {"Host": "evil.invalid"}]:
            with self.assertRaises(urllib.error.HTTPError) as error:
                opener.open(urllib.request.Request(base + "/api/status", headers=headers))
            self.assertEqual(error.exception.code, 403)
        data = json.dumps({"id": self.pdf_id(), "note": "from manual UI"}).encode()
        with self.assertRaises(urllib.error.HTTPError):
            opener.open(urllib.request.Request(base + "/api/annotate", data=data, headers={"Content-Type": "application/json"}))
        response = opener.open(urllib.request.Request(base + "/api/annotate", data=data, headers={"Content-Type": "application/json", "X-Sklib-Token": token}))
        self.assertEqual(json.loads(response.read())["note"], "from manual UI")


class SemanticTests(Fixture):
    class Provider:
        model = "test:deterministic"
        pack = staticmethod(OllamaEmbeddings.pack)
        similarity = staticmethod(OllamaEmbeddings.similarity)

        def encode(self, texts):
            return [[1., 0.] if "pdf" in value.lower() else [0., 1.] for value in texts]

    def test_optional_embeddings_incremental_and_revision_filtering(self):
        self.sample()
        provider = self.Provider()
        self.assertEqual(embed_library(self.lib, provider)["embedded"], 4)
        self.assertEqual(embed_library(self.lib, provider)["embedded"], 0)
        result = self.lib.search("pdf extraction", mode="semantic", semantic=provider)
        self.assertEqual(result["results"][0]["name"], "pdf-tables")
        self.assertEqual(result["semantic_coverage"], 3)
        self.write("pdf/skills/pdf-tables/SKILL.md", skill("pdf-tables", "Modified PDF"))
        self.lib.index(self.root)
        result = self.lib.search("pdf", mode="semantic", semantic=provider)
        self.assertEqual(result["semantic_coverage"], 2)
        with self.assertRaises(ValueError):
            self.lib.search("pdf", mode="hybrid")

    def test_embeddings_endpoint_is_explicitly_local(self):
        for url in ["http://example.com", "https://127.0.0.1", "http://user:pass@localhost", "http://127.0.0.1?token=secret"]:
            with self.assertRaises(ValueError):
                OllamaEmbeddings("test", url)

    def test_ollama_http_contract_and_validation(self):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                value = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                self.server.last_input = value
                data = json.dumps({"embeddings": [[3., 4.] for text in value["input"]]}).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        provider = OllamaEmbeddings("local-fixture", f"http://127.0.0.1:{server.server_address[1]}")
        result = provider.encode(["hello", "你好"])
        self.assertEqual(result, [[.6, .8], [.6, .8]])
        self.assertEqual(server.last_input["model"], "local-fixture")
        self.assertAlmostEqual(provider.similarity(result[0], provider.pack(result[1]), 2), 1, places=6)


if __name__ == "__main__":
    unittest.main()
