from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import test_library as fixtures
from sklib.mcp import MAX_MESSAGE, PROTOCOLS, Session


def ready(library, version=PROTOCOLS[0]):
    session = Session(library)
    answer = session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": version, "capabilities": {}, "clientInfo": {"name": "audit", "version": "1"}}})
    assert answer["result"]["protocolVersion"] == version
    session.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})
    return session


class SystemAuditTests(fixtures.Fixture):
    def test_character_pages_reassemble_unicode_and_very_long_line(self):
        original = fixtures.skill("large", "paged workflow", "中文😀\\\"" * 25000)
        path = self.write("large/SKILL.md", original)
        self.lib.index(self.root)
        identifier = self.lib.browse()["results"][0]["id"]
        page = self.lib.get(identifier, max_chars=1500)
        self.assertTrue(page["content_truncated"])
        pieces = []
        while True:
            self.assertLessEqual(len(page["content"]), 1500)
            pieces.append(page["content"])
            if page["next"] is None:
                break
            arguments = dict(page["next"])
            arguments.pop("tool")
            arguments["document_id"] = arguments.pop("id")
            page = self.lib.get(**arguments)
        self.assertEqual("".join(pieces), original)
        self.assertEqual(self.lib.get(identifier)["content"], original)
        first = self.lib.get(identifier, max_chars=1500)
        path.write_text(original + "changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Source changed"):
            self.lib.get(identifier, start_char=first["next_start_char"],
                         expected_revision=first["revision"], expected_content_revision=first["content_revision"], max_chars=1500)
        with self.assertRaisesRegex(ValueError, "Continuation requires"):
            self.lib.get(identifier, start_char=1500, max_chars=1500)

    def test_character_continuation_detects_newline_only_change(self):
        original = fixtures.skill("newlines", "workflow", "instruction\n" * 3000)
        path = self.write("newlines/SKILL.md", original)
        self.lib.index(self.root)
        identifier = self.lib.browse()["results"][0]["id"]
        first = self.lib.get(identifier, max_chars=1500)
        path.write_bytes(original.replace("\n", "\r\n").encode("utf-8"))
        current = self.lib.get(identifier)
        self.assertEqual(first["revision"], current["revision"])
        self.assertNotEqual(first["content_revision"], current["content_revision"])
        continuation = dict(first["next"])
        continuation.pop("tool")
        continuation["document_id"] = continuation.pop("id")
        with self.assertRaisesRegex(ValueError, "Source changed since previous page"):
            self.lib.get(**continuation)

    def test_mcp_default_body_budget_and_version_negotiation(self):
        original = fixtures.skill("large", "workflow", "step\n" * 10000)
        self.write("large/SKILL.md", original)
        self.lib.index(self.root)
        identifier = self.lib.browse()["results"][0]["id"]
        for version in PROTOCOLS:
            with self.subTest(version=version):
                session = ready(self.lib, version)
                answer = session.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                    "name": "get_skill", "arguments": {"id": identifier}}})["result"]
                page = json.loads(answer["content"][0]["text"])
                self.assertFalse(answer["isError"])
                self.assertEqual(len(page["content"]), 24000)
                self.assertEqual("structuredContent" in answer, version >= "2025-06-18")
                tools = session.dispatch({"jsonrpc": "2.0", "id": 4, "method": "tools/list"})["result"]["tools"]
                self.assertEqual("outputSchema" in tools[0], version >= "2025-06-18")
                self.assertEqual("annotations" in tools[0], version >= "2025-03-26")
                following = dict(page["next"])
                following.pop("tool")
                answer2 = session.dispatch({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                    "name": "get_skill", "arguments": following}})["result"]
                self.assertEqual(json.loads(answer2["content"][0]["text"])["start_char"], 24000)

    def test_batch_supported_only_for_march_2025_with_notification_suppressed(self):
        for version in PROTOCOLS:
            session = ready(self.lib, version)
            batch = [{"jsonrpc": "2.0", "id": 2, "method": "ping"},
                     {"jsonrpc": "2.0", "method": "notifications/cancelled", "params": {"requestId": 1}},
                     {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}]
            response = session.dispatch(batch)
            if version == "2025-03-26":
                self.assertEqual([item["id"] for item in response], [2, 3])
                self.assertIsNone(session.dispatch([batch[1]]))
                self.assertIn("error", session.dispatch([]))
                self.assertIn("error", session.dispatch([batch[0]] * 101))
            else:
                self.assertIn("error", response)

    def test_oversized_output_is_tool_error_and_session_recovers(self):
        library = Mock()
        library.get.return_value = {"metadata": "中" * MAX_MESSAGE}
        session = ready(library)
        response = session.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": "get_skill", "arguments": {"id": "large"}}})
        self.assertLess(len(json.dumps(response).encode("utf-8")), MAX_MESSAGE)
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(response["result"]["structuredContent"]["code"], "tool_result_too_large")
        self.assertEqual(session.dispatch({"jsonrpc": "2.0", "id": 3, "method": "ping"})["result"], {})

    def test_launcher_works_from_unrelated_unicode_working_directory(self):
        folder = self.base / "different cwd 中文"
        folder.mkdir()
        launcher = Path(__file__).resolve().parents[1] / "scripts" / "sklib_launcher.py"
        frames = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": PROTOCOLS[0], "capabilities": {}, "clientInfo": {"name": "probe"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        ]
        process = subprocess.run([sys.executable, str(launcher), "--home", str(self.base / "isolated state"), "mcp"],
            input="".join(json.dumps(frame) + "\n" for frame in frames).encode("utf-8"),
            cwd=folder, capture_output=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr.decode("utf-8"))
        responses = [json.loads(line) for line in process.stdout.splitlines()]
        self.assertEqual(len(responses), 2)
        self.assertEqual(len(responses[1]["result"]["tools"]), 5)
        self.assertFalse((folder / ".sklib").exists())
