"""Check the real stdio server with the optional official MCP Python SDK (v1)."""
from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
from pathlib import Path
import site
import sys
import tempfile
import time

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))


async def check(installed=False):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from jsonschema import Draft202012Validator
    from sklib.service import Library

    with tempfile.TemporaryDirectory(prefix="sklib-sdk-") as temporary:
        base = Path(temporary)
        folder = base / "中文 source" / "large"
        folder.mkdir(parents=True)
        original = "---\nname: pdf-audit\ndescription: Extract PDF tables\n---\n" + "中文 instructions 😀\n" * 2000
        (folder / "SKILL.md").write_bytes(original.encode("utf-8"))
        (folder / "guide.txt").write_bytes(b"first\nsecond\nthird\n")
        lib = Library(base / "isolated state")
        lib.index(folder.parent)
        launcher = PROJECT / "scripts" / "sklib_launcher.py"
        params = StdioServerParameters(command=sys.executable,
            args=(["-m", "sklib"] if installed else [str(launcher)]) + ["--home", str(lib.store.home), "mcp"], cwd=str(base))
        started = time.perf_counter()
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                initialization = await session.initialize()
                initialize_ms = round((time.perf_counter() - started) * 1000, 2)
                listing = await session.list_tools()
                assert len(listing.tools) == 5
                for tool in listing.tools:
                    Draft202012Validator.check_schema(tool.inputSchema)
                    Draft202012Validator.check_schema(tool.outputSchema)
                inventory = await session.call_tool("list_library", {"queue": "unclassified"})
                assert not inventory.isError and inventory.structuredContent["total"] == 1
                source = await session.call_tool("check_source", {"root": str(folder.parent), "verify": True})
                assert not source.isError and source.structuredContent["state"] == "clean"
                search = await session.call_tool("search_skills", {"query": "PDF tables"})
                assert not search.isError
                identifier = search.structuredContent["results"][0]["id"]
                constrained = await session.call_tool("search_skills", {"query": "PDF tables", "required_terms": ["PDF"]})
                assert not constrained.isError and constrained.structuredContent["results"][0]["id"] == identifier
                absent = await session.call_tool("search_skills", {"query": "PDF tables", "required_terms": ["Flutter"]})
                assert not absent.isError and absent.structuredContent["returned"] == 0
                invalid = await session.call_tool("search_skills", {"query": "PDF", "required_terms": [" "]})
                assert invalid.isError
                arguments = {"id": identifier}
                chunks, pages = [], 0
                while True:
                    response = await session.call_tool("get_skill", arguments)
                    assert not response.isError
                    result = response.structuredContent
                    assert json.loads(response.content[0].text) == result
                    chunks.append(result["content"])
                    pages += 1
                    if not result["next"]:
                        break
                    arguments = dict(result["next"])
                    arguments.pop("tool")
                assert pages > 1 and "".join(chunks) == original
                first = await session.call_tool("read_skill_file", {"id": identifier,
                    "relative_path": "guide.txt", "max_lines": 1})
                second = await session.call_tool("read_skill_file", {"id": identifier,
                    "relative_path": "guide.txt", "start_line": first.structuredContent["next_start_line"],
                    "expected_revision": first.structuredContent["revision"]})
                assert first.structuredContent["content"] + second.structuredContent["content"] == "first\nsecond\nthird\n"
                failure = await session.call_tool("get_skill", {"id": "missing"})
                assert failure.isError and failure.structuredContent["code"] == "entry_not_found"
                await session.send_ping()
                report = {"sdk": "mcp", "sdk_version": importlib.metadata.version("mcp"),
                    "protocol": initialization.protocolVersion, "tools": [tool.name for tool in listing.tools],
                    "initialize_ms": initialize_ms, "paged_skill_pages": pages,
                    "server_launch": "installed module" if installed else "source launcher",
                    "checks": ["initialize", "tool schemas", "list_library", "check_source", "search_skills", "required terms",
                        "constraint error recovery", "get_skill pagination",
                        "read_skill_file continuation", "structured/text agreement", "tool error", "ping after error", "arbitrary cwd"],
                    "passed": True, "model_inference": False}
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk-path", type=Path, help="Optional isolated pip --target directory")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--installed", action="store_true", help="Launch the installed module from outside the source checkout")
    args = parser.parse_args()
    if args.sdk_path:
        directory = str(args.sdk_path.resolve())
        site.addsitedir(directory)
        sys.path.remove(directory)
        sys.path.insert(0, directory)
    report = asyncio.run(check(args.installed))
    value = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
    print(value)


if __name__ == "__main__":
    main()
