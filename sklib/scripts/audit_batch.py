"""Compare full FTS refresh with annotation-only refresh in the same temp index."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sklib.indexer import refresh_fts
from sklib.service import Library


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="sklib-batch-perf-") as temporary:
        base = Path(temporary)
        source = base / "source"
        body = "处理中文论文与 PDF tables; validate structured output and preserve sources.\n" * 150
        for number in range(50):
            folder = source / str(number)
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_bytes((f"---\nname: {number}\ndescription: Batch fixture\n---\n" + body).encode("utf-8"))
        lib = Library(base / "state")
        lib.index(source)
        identifiers = [item["id"] for item in lib.browse(limit=100, max_chars=100000)["results"]]
        assert len(identifiers) == 50
        timings = {"full_fts_refresh": [], "annotation_only": []}
        def full(db, identifier, **options):
            return refresh_fts(db, identifier)
        for round_number in range(6):
            for mode in ("full_fts_refresh", "annotation_only") if round_number % 2 == 0 else ("annotation_only", "full_fts_refresh"):
                with patch("sklib.service.refresh_fts", side_effect=full if mode == "full_fts_refresh" else refresh_fts):
                    started = time.perf_counter()
                    result = lib.annotate_batch(identifiers, tags=[f"round-{round_number}-{mode}"], tag_mode="replace")
                    assert result["updated"] == 50
                    if round_number:
                        timings[mode].append((time.perf_counter() - started) * 1000)
        with lib.store.connect() as db:
            db.execute("INSERT INTO documents_fts(documents_fts) VALUES('integrity-check')")
        report = {"entries": 50, "body_chars_each": len(body), "samples_each": 5, "warm_cache": True,
            "timings": {key: {"median_ms": round(statistics.median(values), 2), "max_ms": round(max(values), 2)} for key, values in timings.items()},
            "fts_integrity": "ok", "limitations": "Synthetic documents, alternating order, one machine; excludes browser and model latency."}
        value = json.dumps(report, indent=2)
        if args.output:
            args.output.write_text(value + "\n", encoding="utf-8")
        print(value)


if __name__ == "__main__":
    main()
