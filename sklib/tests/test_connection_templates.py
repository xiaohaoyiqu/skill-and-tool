"""Launch the actual stdio commands shipped in each host configuration example."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


class ConnectionTemplateTests(unittest.TestCase):
    def test_four_host_templates_launch_from_unrelated_directory(self):
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        project = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="sklib-template-") as temporary:
            base = Path(temporary)
            working = base / "中文工作目录"
            working.mkdir()
            for client in ("codex", "claude", "gemini", "vscode"):
                with self.subTest(client=client):
                    if client == "codex":
                        config = tomllib.loads((project / "examples/mcp/codex.toml").read_text(encoding="utf-8"))["mcp_servers"]["sklib"]
                    else:
                        config = json.loads((project / f"examples/mcp/{client}.json").read_text(encoding="utf-8"))[
                            "servers" if client == "vscode" else "mcpServers"]["sklib"]
                    if not Path(config["command"]).is_file():
                        self.skipTest("Example interpreter path needs adjustment on this machine")
                    arguments = list(config["args"])
                    arguments[arguments.index("--home") + 1] = str(base / client)
                    frames = [
                        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                            "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": client, "version": "acceptance"}}},
                        {"jsonrpc": "2.0", "method": "notifications/initialized"},
                        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_skill", "arguments": {"id": "missing"}}},
                        {"jsonrpc": "2.0", "id": 4, "method": "ping"},
                    ]
                    result = subprocess.run([config["command"], *arguments], cwd=working,
                        input="".join(json.dumps(frame) + "\n" for frame in frames),
                        capture_output=True, text=True, encoding="utf-8", timeout=20)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    replies = [json.loads(line) for line in result.stdout.splitlines()]
                    self.assertEqual(len(replies[1]["result"]["tools"]), 5)
                    self.assertTrue(replies[2]["result"]["isError"])
                    self.assertEqual(replies[3]["id"], 4)
