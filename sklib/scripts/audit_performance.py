"""Repeatable, model-free load check using disposable files and an isolated index."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import math
import platform
from pathlib import Path
import sqlite3
import statistics
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sklib.service import Library


def timing(operation, repetitions):
    operation()  # warm the OS and SQLite caches
    elapsed = []
    for _ in range(repetitions):
        started = time.perf_counter()
        operation()
        elapsed.append((time.perf_counter() - started) * 1000)
    ordered = sorted(elapsed)
    return {"samples": len(ordered), "median_ms": round(statistics.median(ordered), 2),
            "p95_ms": round(ordered[math.ceil(.95 * len(ordered)) - 1], 2),
            "max_ms": round(max(ordered), 2)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entries", type=int, default=5000)
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 100 <= args.entries <= 50000 or not 5 <= args.repetitions <= 100:
        parser.error("entries must be 100..50000 and repetitions 5..100")
    with tempfile.TemporaryDirectory(prefix="sklib-audit-") as temporary:
        base = Path(temporary)
        root = base / "sources"
        root.mkdir()
        body = "Read references/guide.txt and validate the output.\n" * 30
        for number in range(args.entries):
            folder = root / str(number)
            folder.mkdir()
            # Every tenth location is an exact duplicate of its previous one.
            identity = number - 1 if number and number % 10 == 0 else number
            (folder / "SKILL.md").write_text(
                f"---\nname: workflow-{identity}\ndescription: PDF tables Vue performance 论文整理 {identity}\n---\n" + body,
                encoding="utf-8")
        library = Library(base / "state")
        started = time.perf_counter()
        first = library.index(root, max_files=args.entries + 100)
        first_s = time.perf_counter() - started
        print("Indexed fixture; measuring queries and concurrent operations.", file=sys.stderr, flush=True)
        started = time.perf_counter()
        second = library.index(root)
        second_s = time.perf_counter() - started
        assert first["complete"] and second["complete"] and second["unchanged"] == args.entries
        identifier = library.search("workflow-21")["results"][0]["id"]
        tasks = {
            "exact_search": lambda: library.search("workflow-21"),
            "broad_search": lambda: library.search("PDF tables"),
            "chinese_search": lambda: library.search("论文整理"),
            "browse_all": lambda: library.browse(),
            "browse_duplicates": lambda: library.browse(queue="duplicates"),
            "browse_recent": lambda: library.browse(sort="recent"),
            "get_skill": lambda: library.get(identifier),
        }
        measurements = {key: timing(operation, args.repetitions) for key, operation in tasks.items()}

        def mixed(number):
            started = time.perf_counter()
            if number % 10 == 0:
                library.annotate(identifier, note=f"concurrent note {number}", tags=["checked"])
            elif number % 2:
                library.search("PDF tables")
            else:
                library.browse(queue="needs_review", limit=10)
            return (time.perf_counter() - started) * 1000

        started = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as pool:
            mixed_times = list(pool.map(mixed, range(100)))
        mixed_s = time.perf_counter() - started
        with library.store.connect() as db:
            check = db.execute("PRAGMA quick_check").fetchone()[0]
            counts = [db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                      for table in ("documents", "documents_fts")]
            db.execute("INSERT INTO documents_fts(documents_fts) VALUES('integrity-check')")
        assert check == "ok" and counts == [args.entries, args.entries]
        report = {"environment": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                    "platform": platform.system(), "fixture_body_lines": 30, "warm_cache": True},
            "entries": args.entries, "first_index_s": round(first_s, 3),
            "unchanged_index_s": round(second_s, 3), "operations": measurements,
            "mixed_load": {"workers": 4, "operations": len(mixed_times), "writes": 10,
                "errors": 0, "elapsed_s": round(mixed_s, 3),
                "p95_ms": round(sorted(mixed_times)[math.ceil(.95 * len(mixed_times)) - 1], 2)},
            "integrity": {"sqlite": check, "fts": "ok", "document_rows": counts[0], "fts_rows": counts[1]},
            "database_bytes": library.store.database.stat().st_size,
            "limitations": "Synthetic short documents; warm cache; no real model, network, long-term soak or memory profile."}
        value = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(value + "\n", encoding="utf-8")
        print(value)


if __name__ == "__main__":
    main()
