"""Call SKLIB through the installed Codex app-server, without model inference."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time
import uuid

from check_hosts import executable
from sklib.service import Library


class Client:
    def __init__(self, command, cwd):
        self.process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        self.messages = queue.Queue()
        self.identifier = 0
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()

    def read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                pass
        self.messages.put(None)

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def call(self, method, parameters, timeout=30):
        self.identifier += 1
        identifier = self.identifier
        self.send({"id": identifier, "method": method, "params": parameters})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            message = self.messages.get(timeout=max(.01, deadline - time.monotonic()))
            if message is None:
                raise RuntimeError("Codex app-server exited before replying")
            if message.get("id") == identifier and "method" not in message:
                if "error" in message:
                    raise RuntimeError(str(message["error"]))
                return message["result"]
            if "id" in message and "method" in message:
                self.send({"id": message["id"], "error": {"code": -32601, "message": "Unsupported in read-only acceptance"}})
        raise TimeoutError("Codex app-server did not reply")

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.close()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(self.process.pid), "/T", "/F"], capture_output=True, timeout=10)
                else:
                    self.process.kill()
                self.process.wait(timeout=5)
        self.process.stdout.close()
        self.reader.join(timeout=2)


def check():
    command = executable("codex")
    if not command:
        return {"passed": False, "status": "not_installed", "model_inference": False}
    with tempfile.TemporaryDirectory(prefix="sklib-codex-mcp-") as temporary:
        base = Path(temporary)
        source = base / "source" / "acceptance-workflow"
        (source / "references").mkdir(parents=True)
        nonce = "SKLIB-CHECK-" + uuid.uuid4().hex
        (source / "SKILL.md").write_text("---\nname: acceptance-workflow\ndescription: Acceptance workflow\n---\nRead references/check.txt.\n", encoding="utf-8")
        (source / "references/check.txt").write_text(nonce, encoding="utf-8")
        library = Library(base / "state")
        library.index(source.parent)
        arguments = [str(Path(__file__).with_name("check_hosts.py")), "--serve", str(library.store.home), str(base / "trace.jsonl")]
        server = "{sklib={command=" + json.dumps(sys.executable) + ",args=" + json.dumps(arguments) + ",required=true}}"
        invocation = [command, "app-server", "-c", "mcp_servers=" + server]
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib
            import re
            settings = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"
            for name in tomllib.loads(settings.read_text(encoding="utf-8")).get("mcp_servers", {}):
                if name != "sklib" and re.fullmatch(r"[A-Za-z0-9_-]+", name):
                    invocation.extend(["-c", "mcp_servers." + name + ".enabled=false"])
        except (OSError, ValueError):
            pass
        client = Client(invocation, base)
        started = time.perf_counter()
        calls = []
        try:
            client.call("initialize", {"clientInfo": {"name": "sklib-acceptance", "version": "1"}, "capabilities": {"experimentalApi": True}})
            client.send({"method": "initialized", "params": {}})
            thread = client.call("thread/start", {"cwd": str(base), "ephemeral": True, "sandbox": "read-only", "approvalPolicy": "never"})
            thread_id = thread["thread"]["id"]
            inventory = client.call("mcpServerStatus/list", {"threadId": thread_id, "serverName": "sklib", "detail": "toolsAndAuthOnly"})
            tools = inventory["data"][0]["tools"]
            def tool(name, params):
                calls.append(name)
                value = client.call("mcpServer/tool/call", {"threadId": thread_id, "server": "sklib", "tool": name, "arguments": params})
                while "result" in value and "content" not in value:
                    value = value["result"]
                return value
            def body(value):
                return value.get("structuredContent") or json.loads(value["content"][0]["text"])
            assert body(tool("list_library", {}))["total"] == 1
            found = body(tool("search_skills", {"query": "acceptance", "required_terms": ["acceptance"]}))
            identifier = found["results"][0]["id"]
            assert body(tool("get_skill", {"id": identifier}))["id"] == identifier
            assert body(tool("read_skill_file", {"id": identifier, "relative_path": "references/check.txt"}))["content"] == nonce
            assert body(tool("check_source", {"root": str(source.parent), "verify": True}))["state"] == "clean"
            assert tool("get_skill", {"id": "missing"})["isError"]
            assert body(tool("list_library", {}))["total"] == 1
            return {"passed": True, "host": "Codex app-server", "tools": list(tools), "tool_calls": calls,
                "nonce_verified": True, "error_recovery": True, "elapsed_seconds": round(time.perf_counter() - started, 3),
                "model_inference": False, "user_configuration_changed": False, "ephemeral_thread": True}
        finally:
            client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check()
    value = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
    print(value)


if __name__ == "__main__":
    main()
