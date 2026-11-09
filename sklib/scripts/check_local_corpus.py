"""Read selected real sources into a temporary index; leave no persistent service.

Run from the project root: python scripts/check_local_corpus.py <source> [...]
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sklib.service import Library
from sklib.evaluation import evaluate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+")
    parser.add_argument("--evaluation")
    parser.add_argument("--compare-evaluation", help="Optional second dataset evaluated in the same temporary index")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-files", type=int, default=100000)
    parser.add_argument("--check-sorting", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="sklib-corpus-") as temporary:
        library = Library(temporary)
        scans = []
        for root in args.roots:
            start = time.perf_counter()
            report = library.index(root, max_files=args.max_files,
                progress=lambda value: print(json.dumps({"root": root, **value}, ensure_ascii=True), file=sys.stderr, flush=True))
            elapsed = time.perf_counter() - start
            second_start = time.perf_counter()
            second = library.index(root, max_files=args.max_files,
                progress=lambda value: print(json.dumps({"root": root, "pass": 2, **value}, ensure_ascii=True), file=sys.stderr, flush=True))
            scans.append({"root": root, "added": report["added"], "errors": report["errors"],
                          "elapsed_s": round(elapsed, 3), "files_examined": report["files_examined"],
                          "complete": report["complete"], "second_scan_s": round(time.perf_counter() - second_start, 3),
                          "unchanged_second_scan": second["unchanged"]})
        searches = []
        for query in ["PDF 表格提取", "Vue 页面性能优化", "文章改写去AI腔", "论文 文献", "浏览器 自动化", "Obsidian 笔记"]:
            data = library.search(query)
            searches.append({"query": query, "elapsed_ms": data["elapsed_ms"],
                             "names": [r["name"] for r in data["results"]]})
        report = {"scans": scans, "counts": library.status()["counts"], "queries": searches}
        if args.check_sorting:
            before = library.browse(kind="all", queue="unclassified", limit=5)
            if before["results"]:
                identifier = before["results"][0]["id"]
                library.annotate(identifier, tags=["sorting-check"], state="useful")
                after = library.browse(kind="all", queue="unclassified", limit=5)
                checked = library.browse(kind="all", tags=["sorting-check"])
                assert after["total"] == before["total"] - 1
                assert checked["total"] == 1 and checked["results"][0]["id"] == identifier
                report["sorting"] = {"counts_before": before["counts"], "counts_after": after["counts"],
                    "tagged_locations": checked["total"], "elapsed_ms": before["elapsed_ms"],
                    "passed": True, "temporary_annotations_only": True}
        if args.evaluation:
            report["evaluation"] = evaluate(library, args.evaluation)
        if args.compare_evaluation:
            report["comparison_evaluation"] = evaluate(library, args.compare_evaluation)
        sys.stdout.reconfigure(encoding="utf-8")
        value = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
        print(value)


if __name__ == "__main__":
    main()
