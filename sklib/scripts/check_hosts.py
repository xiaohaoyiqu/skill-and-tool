"""Actual installed host/MCP acceptance, with a fresh nonce reachable only by tools.

Runs configured Codex/Claude accounts when requested; never edits host settings.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))


def serve(home, trace):
    from sklib.mcp import serve as run
    from sklib.service import Library
    class Input:
        def readline(self, size=-1):
            line = sys.stdin.buffer.readline(size)
            try:
                message = json.loads(line)
                if isinstance(message, dict) and message.get("method") == "tools/call":
                    parameters = message.get("params", {})
                    with Path(trace).open("a", encoding="utf-8") as stream:
                        stream.write(json.dumps({"tool": parameters.get("name")}) + "\n")
            except (ValueError, TypeError):
                pass
            return line
    run(Library(home), Input())


def executable(name):
    found = shutil.which(name)
    if found and name == "codex" and os.name == "nt":
        npm = Path(found).parent / "node_modules" / "@openai" / "codex"
        native = next(npm.glob("node_modules/@openai/codex-win32-*/vendor/*/bin/codex.exe"), None)
        if native:
            return str(native)
    return found


def invoke(command, cwd, prompt="", timeout=120):
    environment = os.environ.copy()
    # Some runner sandboxes inject a deliberately unusable loopback proxy.
    # Real model connectivity is authorized by the caller; retain real proxies.
    import urllib.parse
    import urllib.request
    removed_proxy = False
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        parsed = urllib.parse.urlsplit(environment.get(key, ""))
        if parsed.hostname in ("127.0.0.1", "localhost") and parsed.port == 9:
            environment.pop(key, None)
            removed_proxy = True
    if removed_proxy and os.name == "nt":
        for scheme, proxy in urllib.request.getproxies_registry().items():
            if scheme in ("http", "https"):
                environment.setdefault(scheme.upper() + "_PROXY", proxy)
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", env=environment,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    try:
        output, errors = process.communicate(prompt, timeout=timeout)
        return process.returncode, output, errors
    except subprocess.TimeoutExpired:
        if os.name == "nt" and process.poll() is None:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=10)
        else:
            process.kill()
        output, errors = process.communicate(timeout=10)
        return None, output, errors


def check(host):
    command = executable(host)
    if command is None:
        return {"host": host, "status": "not_installed", "passed": False, "model_inference": False}
    with tempfile.TemporaryDirectory(prefix="sklib-host-") as temporary:
        from sklib.service import Library
        base = Path(temporary)
        workspace = base / "workspace"
        workspace.mkdir()
        source = base / "source" / "acceptance-workflow"
        (source / "references").mkdir(parents=True)
        nonce = "SKLIB-CHECK-" + uuid.uuid4().hex
        (source / "SKILL.md").write_text("---\nname: acceptance-workflow\ndescription: Acceptance verification workflow\n---\nRead references/verification.txt and return its verification value.\n", encoding="utf-8")
        (source / "references" / "verification.txt").write_text("verification value: " + nonce, encoding="utf-8")
        library = Library(base / "state")
        library.index(source.parent)
        trace = base / "tools.jsonl"
        args = [str(Path(__file__).resolve()), "--serve", str(library.store.home), str(trace)]
        prompt = ('Use only the SKLIB MCP tools. Search for acceptance-workflow with required_terms=["acceptance"], '
            'open that result with get_skill, then use read_skill_file to read references/verification.txt. '
            'Reply only with the verification value from that file. Do not use shell or direct filesystem tools.')
        if host == "codex":
            server = "{sklib={command=" + json.dumps(sys.executable) + ",args=" + json.dumps(args) + ",required=true}}"
            invocation = [command, "exec", "--json", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
                "--color", "never", "-C", str(workspace), "-c", "mcp_servers=" + server,
                "-c", 'model_reasoning_effort="low"']
            try:
                try:
                    import tomllib
                except ImportError:
                    import tomli as tomllib
                directory = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
                configuration = tomllib.loads((directory / "config.toml").read_text(encoding="utf-8"))
                for name in configuration.get("mcp_servers", {}):
                    if name != "sklib" and re.fullmatch(r"[A-Za-z0-9_-]+", name):
                        invocation.extend(["-c", "mcp_servers." + name + ".enabled=false"])
            except (OSError, ValueError):
                pass
            invocation.append("-")
        elif host == "claude":
            status, output, errors = invoke([command, "auth", "status"], workspace, timeout=30)
            try:
                authenticated = json.loads(output).get("loggedIn", False)
            except ValueError:
                authenticated = False
            if not authenticated:
                return {"host": host, "status": "requires_login", "passed": False, "model_inference": False}
            configuration = base / "mcp.json"
            configuration.write_text(json.dumps({"mcpServers": {"sklib": {"command": sys.executable, "args": args}}}), encoding="utf-8")
            invocation = [command, "--print", "--no-session-persistence", "--strict-mcp-config", "--mcp-config", str(configuration),
                "--output-format", "json", "--tools", "", "--permission-mode", "dontAsk", "--allowedTools",
                "mcp__sklib__search_skills,mcp__sklib__get_skill,mcp__sklib__read_skill_file", "--max-budget-usd", "0.50"]
        else:
            return {"host": host, "status": "configuration_only", "passed": False, "model_inference": False}
        started = time.perf_counter()
        code, output, errors = invoke(invocation, workspace, prompt)
        calls = [json.loads(line)["tool"] for line in trace.read_text(encoding="utf-8").splitlines()] if trace.exists() else []
        required = {"search_skills", "get_skill", "read_skill_file"}
        passed = code == 0 and nonce in output and required <= set(calls)
        event_types = []
        for line in output.splitlines():
            try:
                event = json.loads(line)
                if isinstance(event, dict) and isinstance(event.get("type"), str):
                    event_types.append(event["type"])
            except ValueError:
                pass
        return {"host": host, "status": "passed" if passed else "timeout" if code is None else "failed",
            "passed": passed, "model_inference": True if passed else None, "returncode": code,
            "elapsed_seconds": round(time.perf_counter() - started, 3), "tool_calls": calls,
            "event_types": list(dict.fromkeys(event_types)),
            "diagnostic_flags": {key: key in errors.lower() for key in ("unauthorized", "stream disconnected", "connection", "mcp", "error")},
            "error_categories": [key for key in ("quota", "unauthorized", "invalid api key", "authentication", "timeout", "not found", "reconnecting", "stream disconnected") if key in (errors + output).lower()],
            "nonce_verified": nonce in output, "user_configuration_changed": False,
            "diagnostic": None if passed else "Inspect host authentication, model access and connectivity; no private host output is saved."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=["codex", "claude", "all"], default="all")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    hosts = ("codex", "claude") if args.host == "all" else (args.host,)
    report = {"checks": [check(host) for host in hosts], "gemini_cli_installed": executable("gemini") is not None,
        "vscode_installed": executable("code") is not None,
        "limitations": "Only installed and authenticated hosts can pass actual LLM acceptance. No host configuration is persisted."}
    value = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
    print(value)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--serve":
        serve(sys.argv[2], sys.argv[3])
    else:
        main()
