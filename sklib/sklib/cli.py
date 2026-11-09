from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

from . import __version__
from .records import Records
from .service import Library
from .files import ENCODINGS
from .projects import PROJECT_TYPES
from .catalog import QUEUES, SORTS, STATES
from .failures import failure_details


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sklib", description="Local skill retrieval for people and agents")
    root.add_argument("--home", default=os.environ.get("SKLIB_HOME", str(Path.cwd() / ".sklib")))
    root.add_argument("--version", action="version", version=__version__)
    commands = root.add_subparsers(dest="command", required=True)
    index = commands.add_parser("index", help="Incrementally index a local directory without changing source files")
    index.add_argument("root")
    index.add_argument("--verify", action="store_true", help="Rehash even when size and mtime are unchanged")
    index.add_argument("--include-docs", action=argparse.BooleanOptionalAction, default=None, help="Index MD/MDX/RST/TXT/AsciiDoc documentation; reuse saved setting when omitted")
    exclusions = index.add_mutually_exclusive_group()
    exclusions.add_argument("--exclude", action="append", default=None, help="Replace saved extra exclusions with these directory names")
    exclusions.add_argument("--clear-excludes", action="store_true", help="Clear saved extra exclusions; keep built-in exclusions")
    index.add_argument("--max-files", type=int, default=None)
    index.add_argument("--max-depth", type=int, default=None)
    index.add_argument("--encoding", choices=ENCODINGS, help="Fallback for non-UTF text; reuse saved source setting when omitted")
    index.add_argument("--progress", action="store_true", help="Write scan progress to stderr, keeping stdout JSON clean")
    remove = commands.add_parser("remove-root", help="Remove a source from the index; preserve source files and personal annotations")
    remove.add_argument("root")
    search = commands.add_parser("search", help="Find skills by task or exact name")
    search.add_argument("query")
    search.add_argument("--kind", choices=["skill", "project", "document", "all"], default="skill")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--offset", type=int, default=0)
    search.add_argument("--root")
    search.add_argument("--project-type", choices=PROJECT_TYPES)
    search.add_argument("--queue", choices=QUEUES, default="all")
    search.add_argument("--require-term", action="append", default=None, help="Require every specified literal term; repeat up to 8 times")
    search.add_argument("--tag", action="append", default=[])
    search.add_argument("--favorite", action="store_true")
    search.add_argument("--state", choices=["unreviewed", "to_try", "useful", "not_recommended"])
    search.add_argument("--json", action="store_true")
    search.add_argument("--max-chars", type=int, default=16000)
    search.add_argument("--mode", choices=["lexical", "semantic", "hybrid"], default="lexical")
    search.add_argument("--model", help="Explicitly selected local Ollama embedding model")
    search.add_argument("--endpoint", default="http://127.0.0.1:11434")
    search.add_argument("--timeout", type=int, default=60, help="Local embedding request timeout, 1..600 seconds")
    browse = commands.add_parser("browse", help="Browse sorting queues without a keyword; list every indexed location")
    browse.add_argument("--kind", choices=["all", "skill", "project", "document"], default="all")
    browse.add_argument("--queue", choices=QUEUES, default="all")
    browse.add_argument("--sort", choices=tuple(SORTS), default="name")
    browse.add_argument("--root")
    browse.add_argument("--project-type", choices=PROJECT_TYPES)
    browse.add_argument("--tag", action="append", default=[])
    browse.add_argument("--state", choices=sorted(STATES))
    browse.add_argument("--favorite", action="store_true")
    browse.add_argument("--limit", type=int, default=25)
    browse.add_argument("--offset", type=int, default=0)
    show = commands.add_parser("show", help="Read a complete skill and its resource manifest")
    show.add_argument("id")
    show.add_argument("--revision")
    show.add_argument("--json", action="store_true")
    read = commands.add_parser("read", help="Read a referenced text file with continuation")
    read.add_argument("id")
    read.add_argument("path")
    read.add_argument("--start-line", type=int, default=1)
    read.add_argument("--max-lines", type=int, default=200)
    read.add_argument("--max-chars", type=int, default=16000)
    read.add_argument("--revision")
    read.add_argument("--encoding", choices=ENCODINGS, help="Override the source's legacy text fallback")
    note = commands.add_parser("annotate", help="Set personal tags, note, review state and favorite")
    note.add_argument("id")
    note.add_argument("--tag", action="append", default=None)
    note.add_argument("--note")
    note.add_argument("--state", choices=["unreviewed", "to_try", "useful", "not_recommended"])
    note.add_argument("--favorite", action=argparse.BooleanOptionalAction, default=None)
    note.add_argument("--clear-tags", action="store_true")
    note.add_argument("--expected-revision", help="Require an unchanged annotation_revision from show/search/browse")
    batch = commands.add_parser("batch-annotate", help="Atomically update tags, state and favorites on 1..100 explicit ids; preserve notes")
    batch.add_argument("ids", nargs="+")
    batch.add_argument("--tag", action="append", default=None)
    batch.add_argument("--tag-mode", choices=["add", "remove", "replace", "clear"], default="add")
    batch.add_argument("--state", choices=sorted(STATES))
    batch.add_argument("--favorite", action=argparse.BooleanOptionalAction, default=None)
    batch.add_argument("--expected-versions", help="JSON file mapping every selected id to its annotation_revision")
    batch.add_argument("--preview", action="store_true", help="Read current annotation summaries without changing them")
    commands.add_parser("status", help="Show registered roots and index health")
    sources = commands.add_parser("sources", help="Detect source changes without changing the index")
    source_commands = sources.add_subparsers(dest="action", required=True)
    for action in ("check", "watch"):
        source = source_commands.add_parser(action)
        source.add_argument("--root", help="A registered source; omit to check all sources")
        source.add_argument("--verify", action="store_true", help="Hash unchanged candidates to catch preserved timestamps")
        if action == "watch":
            source.add_argument("--interval", type=int, default=60)
            source.add_argument("--refresh", action="store_true", help="Incrementally reindex changed sources after a complete check")
    doctor = commands.add_parser("doctor", help="Check Python, dependencies, SQLite and MCP launch without creating an index")
    doctor.add_argument("--check-index", action="store_true", help="Read-only quick_check of an existing index")
    commands.add_parser("history", help="Show local indexing and annotation operations")
    commands.add_parser("mcp", help="Serve read-only MCP tools over stdio")
    ui = commands.add_parser("ui", help="Serve the manual search UI on loopback until Ctrl+C")
    ui.add_argument("--port", type=int, default=8765)
    embed = commands.add_parser("embed", help="Build optional embeddings using an already installed local Ollama model")
    embed.add_argument("--model", required=True)
    embed.add_argument("--endpoint", default="http://127.0.0.1:11434")
    embed.add_argument("--timeout", type=int, default=60)
    embed.add_argument("--batch-size", type=int, default=16)
    embed.add_argument("--force", action="store_true", help="Rebuild matching vectors too, for model changes or damaged caches")
    records = commands.add_parser("records", help="Export review records and explicitly commit them to their own Git repository")
    record_commands = records.add_subparsers(dest="action", required=True)
    for name in ("init", "export", "preview", "log", "status"):
        record_commands.add_parser(name)
    snapshot = record_commands.add_parser("snapshot", help="Write a portable annotation snapshot as UTF-8 JSON")
    snapshot.add_argument("--output", help="Atomic .json output outside indexed sources; omit for stdout")
    snapshot.add_argument("--root")
    snapshot.add_argument("--annotated-only", action="store_true")
    snapshot.add_argument("--offset", type=int, default=0)
    snapshot.add_argument("--limit", type=int)
    for action in ("import", "migrate"):
        restore = record_commands.add_parser(action, help="Preview annotation restore/migration; --apply requires its token")
        if action == "import":
            restore.add_argument("snapshot")
            restore.add_argument("--root-map", help="JSON file mapping old roots to indexed new roots")
        else:
            restore.add_argument("from_root")
            restore.add_argument("to_root")
        restore.add_argument("--entry-map", help="JSON file mapping snapshot ids to explicit indexed target ids")
        restore.add_argument("--resolutions", help="JSON file mapping snapshot ids to keep/replace")
        restore.add_argument("--policy", choices=["keep", "replace"], default="keep")
        restore.add_argument("--match-content", action="store_true", help="Allow unique same-content matches for renamed entries")
        restore.add_argument("--apply", action="store_true")
        restore.add_argument("--preview-token")
        restore.add_argument("--offset", type=int, default=0)
        restore.add_argument("--limit", type=int, default=50)
    commit = record_commands.add_parser("commit")
    commit.add_argument("-m", "--message", required=True)
    commit.add_argument("--preview-token", help="Require the same snapshot and Git HEAD as a prior preview")
    evaluate = commands.add_parser("eval", help="Evaluate retrieval against a JSON task set")
    evaluate.add_argument("dataset")
    evaluate.add_argument("--k", type=int, default=5)
    evaluate.add_argument("--mode", choices=["lexical", "semantic", "hybrid"], default="lexical")
    evaluate.add_argument("--model", help="Explicitly selected installed local Ollama embedding model")
    evaluate.add_argument("--endpoint", default="http://127.0.0.1:11434")
    evaluate.add_argument("--timeout", type=int, default=60)
    return root


def output(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    watch_updates = 0
    try:
        library = Library(args.home)
        if args.command == "doctor":
            from .diagnostics import environment_report
            report = environment_report(args.home, check_index=args.check_index)
            output(report)
            return 0 if report["ready"] else 2
        elif args.command == "index":
            result = library.index(args.root, verify=args.verify, include_docs=args.include_docs,
                                 exclude=[] if args.clear_excludes else args.exclude, max_files=args.max_files, max_depth=args.max_depth, encoding=args.encoding,
                                 progress=(lambda value: print(json.dumps(value, ensure_ascii=False), file=sys.stderr, flush=True)) if args.progress else None)
            output(result)
            return 0 if result["complete"] else 3
        elif args.command == "browse":
            output(library.browse(kind=args.kind, queue=args.queue, sort=args.sort, root=args.root,
                project_type=args.project_type, tags=args.tag, state=args.state, favorite=args.favorite,
                limit=args.limit, offset=args.offset))
        elif args.command == "remove-root":
            output(library.remove_root(args.root))
        elif args.command == "sources":
            import time
            if args.action == "watch" and not 30 <= args.interval <= 86400:
                raise ValueError("interval must be 30..86400 seconds")
            attempted = {}
            while True:
                roots = [args.root] if args.root else [root["path"] for root in library.status()["roots"]]
                reports = []
                for root in roots:
                    report = library.check_source(root, verify=args.verify)
                    if report["complete"] and report["state"] == "clean":
                        attempted.pop(report["root"], None)
                    if args.action == "watch" and args.refresh and report["complete"] and report["state"] == "changed":
                        if attempted.get(report["root"]) == report["change_token"]:
                            report["refresh_suppressed"] = True
                        else:
                            attempted[report["root"]] = report["change_token"]
                            report["refresh"] = library.index(root, verify=args.verify, expected_source_epoch=report["source_epoch"])
                            watch_updates += 1
                    reports.append(report)
                output({"reports": reports, "complete": all(report["complete"] for report in reports)})
                if args.action == "check":
                    return 0 if all(report["complete"] for report in reports) else 3
                sys.stdout.flush()
                time.sleep(args.interval)
        elif args.command == "search":
            semantic = None
            if args.mode != "lexical":
                if not args.model:
                    raise ValueError("--model is required for semantic/hybrid search")
                from .semantic import OllamaEmbeddings
                semantic = OllamaEmbeddings(args.model, args.endpoint, timeout=args.timeout)
            result = library.search(args.query, kind=args.kind, limit=args.limit, offset=args.offset,
                root=args.root, tags=args.tag, favorite=args.favorite, state=args.state,
                max_chars=args.max_chars, mode=args.mode, semantic=semantic, project_type=args.project_type,
                queue=args.queue, required_terms=args.require_term)
            if args.json:
                output(result)
            else:
                for n, item in enumerate(result["results"], args.offset + 1):
                    print(f"{n}. {item['name']} [{item['kind']}]  {item['id']}")
                    print(f"   {item['description'][:220]}")
                    location = item.get("path")
                    if location:
                        suffix = str(item["evidence"]["line"]) if item["evidence"].get("field", "body") == "body" else item["evidence"]["field"]
                        print(f"   {location}:{suffix}")
                    else:
                        print(f"   Full details: sklib show {item['id']}")
                    print(f"   {item['evidence']['text']}")
                print(f"{result['returned']} results; {result['elapsed_ms']} ms")
                if result["index_empty"]:
                    print("Index is empty. Run sklib index <directory> first.")
        elif args.command == "show":
            result = library.get(args.id, expected_revision=args.revision)
            if args.json:
                output(result)
            else:
                if result["stale"]:
                    print("Source changed since indexing; displaying current content.", file=sys.stderr)
                print(result["content"])
        elif args.command == "read":
            output(library.read_file(args.id, args.path, start_line=args.start_line,
                   max_lines=args.max_lines, max_chars=args.max_chars, expected_revision=args.revision, encoding=args.encoding))
        elif args.command == "annotate":
            output(library.annotate(args.id, tags=[] if args.clear_tags else args.tag,
                                    note=args.note, state=args.state, favorite=args.favorite, expected_annotation_revision=args.expected_revision))
        elif args.command == "batch-annotate":
            if args.preview:
                output(library.annotation_states(args.ids))
            else:
                from .jsonutil import loads
                versions = loads(Path(args.expected_versions).read_bytes()) if args.expected_versions else None
                output(library.annotate_batch(args.ids, tags=args.tag, tag_mode=args.tag_mode, state=args.state,
                                             favorite=args.favorite, expected_revisions=versions))
        elif args.command == "status":
            output(library.status())
        elif args.command == "history":
            output(library.history())
        elif args.command == "records":
            if args.action == "snapshot":
                selection = {"root": args.root, "annotated_only": args.annotated_only, "offset": args.offset, "limit": args.limit}
                output(library.export_snapshot(args.output, **selection) if args.output else library.portable_snapshot(**selection))
                return 0
            if args.action in ("import", "migrate"):
                from .restoring import read_snapshot
                options = {"policy": args.policy, "match_content": args.match_content, "apply": args.apply,
                    "expected_preview": args.preview_token, "offset": args.offset, "limit": args.limit}
                for key in ("entry_map", "resolutions"):
                    if getattr(args, key):
                        options[key] = read_snapshot(getattr(args, key))
                if args.action == "import":
                    if args.root_map:
                        options["root_map"] = read_snapshot(args.root_map)
                    output(library.restore_annotations(read_snapshot(args.snapshot), **options))
                else:
                    output(library.migrate_annotations(args.from_root, args.to_root, **options))
                return 0
            records = Records(library)
            output(records.commit(args.message, expected_preview=args.preview_token) if args.action == "commit" else getattr(records, args.action)())
        elif args.command == "mcp":
            from .mcp import serve
            serve(library)
        elif args.command == "embed":
            from .semantic import OllamaEmbeddings, embed_library
            output(embed_library(library, OllamaEmbeddings(args.model, args.endpoint, timeout=args.timeout), args.batch_size, force=args.force))
        elif args.command == "eval":
            from .evaluation import evaluate
            provider = None
            if args.mode != "lexical":
                from .semantic import OllamaEmbeddings
                if not args.model:
                    raise ValueError("Semantic evaluation requires --model")
                provider = OllamaEmbeddings(args.model, args.endpoint, timeout=args.timeout)
            output(evaluate(library, args.dataset, args.k, mode=args.mode, semantic=provider))
        elif args.command == "ui":
            from .web import create_server
            server = create_server(library, args.port)
            print(f"http://127.0.0.1:{server.server_address[1]}", flush=True)
            try:
                server.serve_forever(poll_interval=0.2)
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
        return 0
    except KeyboardInterrupt as exc:
        if watch_updates:
            exc.outcome = "partial"
            exc.progress = {"completed_source_refreshes": watch_updates}
        print(json.dumps({"error": "Cancelled", "code": "cancelled", "operation": args.command,
            "outcome": getattr(exc, "outcome", "unknown" if args.command == "records" else "unchanged"),
            "progress": getattr(exc, "progress", None), "retryable": args.command != "records",
            "recovery": "检查状态后再继续；向量生成会保留已成功批次。Git 操作先检查提交历史。"}, ensure_ascii=False), file=sys.stderr)
        return 130
    except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
        print(json.dumps(failure_details(exc, args.command if args.command != "records" else "records." + args.action), ensure_ascii=False), file=sys.stderr)
        return 2
