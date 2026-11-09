"""Offline semantic retrieval comparison on one temporary synthetic index."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc
import types

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from sklib.service import Library
from sklib.semantic import OllamaEmbeddings


class Provider:
    model = "audit:deterministic"
    pack = staticmethod(OllamaEmbeddings.pack)
    similarity = staticmethod(OllamaEmbeddings.similarity)

    def __init__(self, dimension):
        self.dimension = dimension

    def encode(self, texts):
        return [[1 / math.sqrt(self.dimension)] * self.dimension for _ in texts]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entries", type=int, default=3000)
    parser.add_argument("--dimension", type=int, default=256)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--baseline-ref", help="Optional trusted local Git revision; executes its historical service.py for comparison")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 1 <= args.entries <= 10000 or not 1 <= args.dimension <= 1024 or not 1 <= args.repetitions <= 20:
        parser.error("entries must be 1..10000, dimension 1..1024, repetitions 1..20")
    classes = {"optimized": Library}
    if args.baseline_ref:
        historical = subprocess.run(["git", "show", args.baseline_ref + ":sklib/service.py"], cwd=PROJECT,
            check=True, capture_output=True, encoding="utf-8", timeout=10).stdout
        module = types.ModuleType("sklib._audit_baseline")
        module.__package__ = "sklib"
        exec(compile(historical, "<trusted Git baseline service.py>", "exec"), module.__dict__)
        classes = {"baseline": module.Library, **classes}
    provider = Provider(args.dimension)
    with tempfile.TemporaryDirectory(prefix="sklib-semantic-audit-") as temporary:
        base = Path(temporary)
        source = base / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: seed\ndescription: Audit seed\n---\nFixture body\n", encoding="utf-8")
        library = Library(base / "state")
        library.index(source)
        with library.store.connect() as db:
            template = dict(db.execute("SELECT * FROM documents").fetchone())
            columns = list(template)
            insert = f"INSERT INTO documents ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})"
            for number in range(args.entries):
                identifier = f"audit-{number:05}"
                row = {**template, "id": identifier, "path": str(source / identifier / "SKILL.md"),
                       "relative_path": identifier + "/SKILL.md", "name": identifier, "title": identifier,
                       "revision": identifier, "description": "Synthetic semantic audit. " * 20}
                db.execute(insert, [row[key] for key in columns])
                vector = [((number * 13 + position * 7) % 101 + 1) / 102 for position in range(args.dimension)]
                norm = math.sqrt(sum(value * value for value in vector))
                db.execute("INSERT INTO vectors VALUES(?,?,?,?,?)", (identifier, identifier, provider.model,
                           args.dimension, provider.pack([value / norm for value in vector])))
                db.execute("INSERT INTO annotations(document_id,note,updated_at) VALUES(?,?,?)",
                           (identifier, "Synthetic personal note. " * 40, "2026-01-01T00:00:00Z"))
        libraries = {name: implementation(library.store.home) for name, implementation in classes.items()}
        timings = {name: [] for name in libraries}
        reference = None
        def query(instance):
            nonlocal reference
            result = instance.search("semantic audit", mode="semantic", semantic=provider)
            actual = [(item["id"], item["score"]) for item in result["results"]]
            if reference is None:
                reference = actual
            assert actual == reference, "Ranking differs from baseline"
            assert result["semantic_coverage"] == args.entries
            return result
        for instance in libraries.values():
            query(instance)  # Warm up separately from timings and allocations.
        for number in range(args.repetitions):
            order = list(libraries) if number % 2 == 0 else list(reversed(libraries))
            for name in order:
                started = time.perf_counter()
                query(libraries[name])
                timings[name].append((time.perf_counter() - started) * 1000)
        peaks = {}
        for name, instance in libraries.items():
            tracemalloc.start()
            query(instance)
            peaks[name] = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
        report = {"entries": args.entries, "dimension": args.dimension, "samples_each": args.repetitions,
            "baseline_ref": args.baseline_ref, "warm_cache": True, "ranking_equal": len(classes) > 1,
            "measurements": {name: {"median_ms": round(statistics.median(values), 2),
                "max_ms": round(max(values), 2), "python_peak_bytes": peaks[name]} for name, values in timings.items()},
            "limitations": "One synthetic index; fake query embedding; no model/network/browser latency. Python allocations exclude SQLite/native/model memory. Still scans all eligible vectors."}
        value = json.dumps(report, indent=2)
        if args.output:
            args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
        print(value)


if __name__ == "__main__":
    main()
