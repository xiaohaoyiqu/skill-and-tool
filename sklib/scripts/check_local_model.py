"""Evaluate an explicitly selected installed Ollama model on a temporary index."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sklib.evaluation import evaluate
from sklib.semantic import OllamaEmbeddings, embed_library
from sklib.service import Library


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--root", action="append", default=[])
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.root and not args.dataset:
        parser.error("--root requires --dataset")
    with tempfile.TemporaryDirectory(prefix="sklib-real-model-") as temporary:
        base = Path(temporary)
        roots = args.root
        dataset = args.dataset
        if not roots:
            source = base / "source"
            cases = []
            examples = [
                ("pdf-tables", "Extract PDF tables to spreadsheets. 从 PDF 文档提取表格并导出 Excel。", "PDF 表格提取", "extract PDF tables"),
                ("vue-performance", "Profile Vue component rendering performance. 排查 Vue 组件渲染性能。", "Vue 页面性能优化", "profile Vue rendering"),
                ("humanizer-zh", "Rewrite prose to remove formulaic AI writing. 修改中文文章，减少模板化 AI 腔。", "文章改写去AI腔", "rewrite formulaic AI prose"),
                ("obsidian-markdown", "Manage Obsidian Markdown notes, properties and backlinks. 管理双向链接与笔记属性。", "Obsidian 笔记", "Obsidian note backlinks"),
                ("literature-review", "Search scientific literature and validate paper citations. 检索科研文献，检查论文引用。", "论文 文献", "research paper literature review"),
            ]
            for name, body, chinese, english in examples:
                folder = source / name
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {body}\n---\n{body}\n", encoding="utf-8")
                cases.extend({"query": query, "relevant": [name]} for query in (chinese, english))
            dataset = base / "cases.json"
            dataset.write_text(json.dumps(cases), encoding="utf-8")
            roots = [str(source)]
        library = Library(base / "state")
        scans = [library.index(root) for root in roots]
        assert all(scan["complete"] for scan in scans), "A source scan was incomplete"
        class Provider(OllamaEmbeddings):
            batches = 0
            def encode(self, texts):
                self.batches += 1
                print(json.dumps({"phase": "embedding", "batch": self.batches, "texts": len(texts)}), file=sys.stderr, flush=True)
                return super().encode(texts)
        provider = Provider(args.model, args.endpoint, timeout=args.timeout)
        started = time.perf_counter()
        embedded = embed_library(library, provider, batch_size=args.batch_size)
        elapsed = round(time.perf_counter() - started, 3)
        assert embed_library(library, provider)["embedded"] == 0
        evaluations = {mode: evaluate(library, dataset, mode=mode, semantic=provider if mode != "lexical" else None)
                       for mode in ("lexical", "semantic", "hybrid")}
        with library.store.connect() as db:
            dimensions = [row[0] for row in db.execute("SELECT DISTINCT dimension FROM vectors")]
        report = {"model": provider.model_name, "endpoint": provider.endpoint, "real_model_inference": True,
            "source_counts": library.status()["counts"], "source_roots": roots if args.root else ["synthetic bilingual fixtures"],
            "embedding": embedded, "embedding_seconds": elapsed, "dimensions": dimensions,
            "incremental_cache_passed": True, "integration_passed": True, "evaluations": evaluations,
            "limitations": "Small labelled development dataset; labels are not exhaustive. Host LLM execution is tested separately."}
        value = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
        print(value)


if __name__ == "__main__":
    main()
