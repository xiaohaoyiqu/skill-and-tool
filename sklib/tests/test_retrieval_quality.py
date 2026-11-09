"""Retrieval quality metrics and bounded semantic ranking regressions."""
from __future__ import annotations

from contextlib import contextmanager
import json
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
from unittest.mock import Mock, patch
from types import SimpleNamespace

import test_library as fixtures
from test_library import Fixture, skill
from sklib.evaluation import evaluate
from sklib.failures import OperationFailure
from sklib.semantic import embed_library
from sklib.mcp import Session
from sklib.web import create_server


class EvaluationTests(Fixture):
    def dataset(self, cases):
        path = self.base / "evaluation.json"
        path.write_text(json.dumps(cases), encoding="utf-8")
        return path

    def test_positive_and_negative_metrics_have_separate_denominators(self):
        self.sample()
        result = evaluate(self.lib, self.dataset([
            {"query": "pdf", "relevant": ["pdf-tables"]},
            {"query": "nonexistentidentifier", "relevant": []},
            # Deliberately mark a present query negative to verify error counting.
            {"query": "vue-performance", "relevant": []},
        ]))
        self.assertEqual(result["positive_queries"], 1)
        self.assertEqual(result["negative_queries"], 2)
        self.assertEqual(result["hit_at_k"], 1)
        self.assertEqual(result["mrr_at_k"], 1)
        self.assertEqual(result["recall_at_k"], 1)
        self.assertEqual(result["precision_at_k"], .2)
        self.assertEqual(result["returned_precision"], 1)
        self.assertEqual(result["false_positive_rate"], .5)
        self.assertEqual(result["correct_empty_rate"], .5)
        self.assertFalse(result["details"][1]["false_positive"])
        self.assertIsNone(result["details"][1]["recall"])
        self.assertEqual(result["details"][2]["returned"], ["vue-performance"])
        self.assertTrue(result["details"][2]["returned_ids"])

    def test_all_negative_or_all_positive_reports_missing_metrics_as_null(self):
        result = evaluate(self.lib, self.dataset([{"query": "missing", "relevant": []}]))
        self.assertIsNone(result["hit_at_k"])
        self.assertIsNone(result["precision_at_k"])
        self.assertEqual(result["correct_empty_rate"], 1)
        result = evaluate(self.lib, self.dataset([{"query": "missing", "relevant": ["absent"]}]))
        self.assertEqual(result["hit_at_k"], 0)
        self.assertIsNone(result["false_positive_rate"])
        self.assertIsNone(result["correct_empty_rate"])

    def test_full_dataset_and_mode_validated_before_queries(self):
        valid = {"query": "PDF", "relevant": []}
        for bad in [None, {"query": "PDF"}, {"query": "PDF", "relevant": [{}]},
                    {"query": "PDF", "relevant": [" "]}, {**valid, "kind": "wrong"},
                    {"query": " " * 2048 + "PDF", "relevant": []},
                    {**valid, "required_terms": "PDF"}, {**valid, "required_terms": [" "]}]:
            with self.subTest(bad=bad), patch.object(self.lib, "search") as search:
                with self.assertRaises(ValueError):
                    evaluate(self.lib, self.dataset([valid, bad]))
                search.assert_not_called()
        with patch.object(self.lib, "search") as search:
            for options in [{"mode": "invalid"}, {"mode": "semantic"}, {"mode": []}, {"k": True}]:
                with self.assertRaises(ValueError):
                    evaluate(self.lib, self.dataset([valid]), **options)
            search.assert_not_called()

    def test_precision_uses_k_and_latency_uses_nearest_rank(self):
        responses = [{"results": [{"id": "other", "name": "other"}, {"id": "hit", "name": "target"}],
                      "elapsed_ms": number, "next_offset": None} for number in range(1, 21)]
        with patch.object(self.lib, "search", side_effect=responses):
            result = evaluate(self.lib, self.dataset([{"query": "task", "relevant": ["hit", "missing"]}] * 20))
        self.assertEqual(result["mrr_at_k"], .5)
        self.assertEqual(result["recall_at_k"], .5)
        self.assertAlmostEqual(result["precision_at_k"], .2)
        self.assertEqual(result["returned_precision"], .5)
        self.assertEqual(result["p95_ms"], 19)

    def test_result_budget_cutoff_is_visible(self):
        with patch.object(self.lib, "search", return_value={"results": [{"id": "a", "name": "a"}],
                "elapsed_ms": 1, "next_offset": 1}) as search:
            result = evaluate(self.lib, self.dataset([{"query": "a", "relevant": ["a"]}]))
        self.assertEqual(result["budget_limited_queries"], 1)
        self.assertTrue(result["details"][0]["budget_limited"])
        self.assertEqual(search.call_args.kwargs["max_chars"], 100000)

    def test_evaluation_can_compare_semantic_and_hybrid_modes(self):
        self.sample()
        provider = fixtures.SemanticTests.Provider()
        embed_library(self.lib, provider)
        dataset = self.dataset([{"query": "pdf", "relevant": ["pdf-tables"]}])
        for mode in ("semantic", "hybrid"):
            result = evaluate(self.lib, dataset, 1, mode=mode, semantic=provider)
            self.assertEqual(result["mode"], mode)
            self.assertEqual(result["hit_at_k"], 1)

    def test_cli_keeps_old_dataset_and_requires_explicit_embedding_model(self):
        dataset = self.dataset([{"query": "missing", "relevant": []}])
        command = [sys.executable, "-m", "sklib", "--home", str(self.lib.store.home), "eval", str(dataset)]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["correct_empty_rate"], 1)
        failed = subprocess.run(command + ["--mode", "semantic"], capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(failed.returncode, 2)
        self.assertIn("--model", json.loads(failed.stderr)["error"])


class SemanticRankingTests(Fixture):
    def vectors(self, count=305):
        self.write("seed/SKILL.md", skill("seed", "fixture"))
        self.lib.index(self.root)
        provider = fixtures.SemanticTests.Provider()
        scored = []
        with self.lib.store.connect() as db:
            template = dict(db.execute("SELECT * FROM documents").fetchone())
            columns = list(template)
            insert = f"INSERT INTO documents ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})"
            for number in range(count):
                identifier = f"vector-{number:04}"
                score = (number % 21) / 32  # Exact float32 values, including ties.
                row = {**template, "id": identifier, "path": str(self.root / identifier / "SKILL.md"),
                       "relative_path": identifier + "/SKILL.md", "name": identifier, "title": identifier,
                       "revision": identifier}
                db.execute(insert, [row[key] for key in columns])
                db.execute("INSERT INTO vectors VALUES(?,?,?,?,?)", (identifier, identifier, provider.model, 2,
                           provider.pack([score, 1.])))
                scored.append((score, identifier))
        return provider, [identifier for score, identifier in sorted(scored, key=lambda item: (-item[0], item[1]))]

    def test_bounded_pool_matches_full_sort_including_ties_and_pagination(self):
        provider, expected = self.vectors()
        result = self.lib.search("pdf", mode="semantic", semantic=provider, offset=150)
        self.assertEqual([item["id"] for item in result["results"]], expected[150:155])
        self.assertEqual(result["semantic_coverage"], 305)
        self.assertEqual(result["candidate_groups"], 200)
        self.assertEqual(result["next_offset"], 155)

    def test_pure_semantic_skips_fts_and_preserves_filters_and_metadata(self):
        self.sample()
        provider = fixtures.SemanticTests.Provider()
        embed_library(self.lib, provider)
        identifier = self.pdf_id()
        self.lib.annotate(identifier, tags=["chosen"], note="retain note", state="useful", favorite=True)
        statements = []
        original = self.lib.store.connect
        @contextmanager
        def traced():
            with original() as db:
                db.set_trace_callback(statements.append)
                yield db
        with patch.object(self.lib.store, "connect", traced):
            result = self.lib.search("pdf", mode="semantic", semantic=provider, tags=["chosen"], favorite=True, state="useful")
        self.assertEqual(result["semantic_coverage"], 1)
        self.assertEqual(result["results"][0]["id"], identifier)
        self.assertEqual(result["results"][0]["note"], "retain note")
        self.assertEqual(result["results"][0]["tags"], ["chosen"])
        self.assertFalse(any(" MATCH " in statement for statement in statements))

    def test_corrupt_vector_outside_winning_pool_still_reports_failure(self):
        provider, expected = self.vectors()
        with self.lib.store.connect() as db:
            db.execute("UPDATE vectors SET embedding=? WHERE document_id=?", (b"broken", expected[-1]))
        with self.assertRaises(OperationFailure) as failure:
            self.lib.search("pdf", mode="semantic", semantic=provider)
        self.assertEqual(failure.exception.code, "embedding_corrupt")


class RequiredTermTests(Fixture):
    def test_all_explicit_terms_match_including_annotations_and_unicode(self):
        self.sample()
        result = self.lib.search("PDF 表格提取", required_terms=["ＰＤＦ", "tables"])
        self.assertEqual([item["name"] for item in result["results"]], ["pdf-tables"])
        self.assertEqual(self.lib.search("PDF Vue", required_terms=["PDF", "Vue"])["returned"], 0)
        self.assertEqual(self.lib.search("performance optimization", required_terms=["Flutter"])["returned"], 0)
        self.lib.annotate(self.pdf_id(), tags=["中文分类"])
        self.assertEqual(self.lib.search("PDF", required_terms=["分类"])["returned"], 1)

    def test_invalid_required_terms_rejected_before_opening_index(self):
        for terms in ["PDF", True, [False], [" "], ["..."], ["a"] * 9, ["a" * 81], [" " * 80 + "a"], ["the"]]:
            with self.subTest(terms=terms), patch.object(self.lib.store, "connect") as connect:
                with self.assertRaises(ValueError):
                    self.lib.search("PDF", required_terms=terms)
                connect.assert_not_called()

    def test_constraints_apply_to_semantic_and_hybrid_candidates(self):
        self.sample()
        provider = fixtures.SemanticTests.Provider()
        embed_library(self.lib, provider)
        for mode in ("semantic", "hybrid"):
            result = self.lib.search("pdf", mode=mode, semantic=provider, required_terms=["Vue"])
            self.assertEqual([item["name"] for item in result["results"]], ["vue-performance"])
            self.assertEqual(result["semantic_coverage"], 1)
            self.assertEqual(result["required_terms"], ["Vue"])

    def test_user_boolean_syntax_is_quoted_as_literal_tokens(self):
        self.sample()
        self.assertEqual(self.lib.search("pdf", required_terms=['missing" OR pdf'])["returned"], 0)
        self.assertEqual(self.lib.search("pdf", required_terms=["pdf-tables"])["returned"], 1)

    def test_mcp_versions_accept_constraint_and_recover_after_invalid_value(self):
        self.sample()
        for version in ("2025-11-25", "2024-11-05"):
            session = Session(self.lib)
            session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": version, "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}})
            session.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
            def call(terms):
                return session.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                    "name": "search_skills", "arguments": {"query": "performance", "required_terms": terms}}})
            failed = call([" "])
            self.assertTrue(failed["result"]["isError"])
            result = call(["Flutter"])["result"]
            self.assertFalse(result["isError"])
            self.assertEqual(json.loads(result["content"][0]["text"])["returned"], 0)

    def test_cli_and_http_share_constraint(self):
        self.sample()
        command = [sys.executable, "-m", "sklib", "--home", str(self.lib.store.home), "search", "performance",
                   "--require-term", "Flutter", "--json"]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["returned"], 0)
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        parameters = urllib.parse.urlencode({"q": "performance", "required_terms": "Flutter"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
                f"http://127.0.0.1:{server.server_address[1]}/api/search?{parameters}", timeout=10) as response:
            self.assertEqual(json.load(response)["returned"], 0)

    def test_evaluation_preserves_explicit_constraints(self):
        self.sample()
        path = self.base / "constrained.json"
        path.write_text(json.dumps([{"query": "performance", "required_terms": ["Flutter"], "relevant": []}]), encoding="utf-8")
        result = evaluate(self.lib, path)
        self.assertEqual(result["correct_empty_rate"], 1)
        self.assertEqual(result["details"][0]["required_terms"], ["Flutter"])


class HttpResponseTests(Fixture):
    def test_disconnect_during_headers_or_body_stops_sending(self):
        server = create_server(self.lib, 0)
        self.addCleanup(server.server_close)
        for exception in (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
            for phase in ("headers", "body"):
                with self.subTest(exception=exception, phase=phase):
                    handler = object.__new__(server.RequestHandlerClass)
                    handler.send_response = Mock()
                    handler.send_header = Mock()
                    handler.end_headers = Mock(side_effect=exception() if phase == "headers" else None)
                    handler.wfile = SimpleNamespace(write=Mock(side_effect=exception() if phase == "body" else None))
                    handler.close_connection = False
                    handler._json(200, {"returned": 0})
                    self.assertTrue(handler.close_connection)
                    handler.send_response.assert_called_once_with(200)
                    if phase == "headers":
                        handler.wfile.write.assert_not_called()
