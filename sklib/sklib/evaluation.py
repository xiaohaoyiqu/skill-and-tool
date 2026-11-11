"""Task-level retrieval evaluation, including irrelevant results and empty cases."""
from __future__ import annotations

import math
from pathlib import Path
from .files import read_text_info
from .jsonutil import loads
from .text import normalized, required_expression


def evaluate(library, dataset: str | Path, k: int = 5, *, mode: str = "lexical", semantic=None) -> dict:
    if type(k) is not int or not 1 <= k <= 50:
        raise ValueError("k must be 1..50")
    if not isinstance(mode, str) or mode not in {"lexical", "semantic", "hybrid"}:
        raise ValueError("Unknown search mode")
    if mode != "lexical" and semantic is None:
        raise ValueError("Semantic evaluation requires an explicitly configured embedding provider")
    cases = loads(read_text_info(Path(dataset))[0])
    if not isinstance(cases, list) or not 1 <= len(cases) <= 1000:
        raise ValueError("Evaluation set must contain 1..1000 cases")
    # Validate the entire set before issuing any retrieval request.
    for case in cases:
        if (not isinstance(case, dict) or not isinstance(case.get("query"), str) or not case["query"].strip() or not 1 <= len(case["query"]) <= 2048
                or not isinstance(case.get("relevant"), list) or len(case["relevant"]) > 1000
                or any(not isinstance(item, str) or not item.strip() or not 1 <= len(item) <= 1000 for item in case["relevant"])):
            raise ValueError("Each case needs a query and relevant names, titles or ids as strings; use [] for an expected empty result")
        if not isinstance(case.get("kind", "skill"), str) or case.get("kind", "skill") not in {"skill", "project", "document", "all"}:
            raise ValueError("Unknown evaluation document kind")
        required_expression(case.get("required_terms"))
        if "evidence_contains" in case:
            terms = case["evidence_contains"]
            if (not case["relevant"] or not isinstance(terms, list) or not 1 <= len(terms) <= 8
                    or any(not isinstance(term, str) or not term.strip() or len(term) > 260 for term in terms)):
                raise ValueError("evidence_contains requires a positive case and 1..8 non-empty strings of up to 260 characters")
    details = []
    for case in cases:
        # Increase the result budget for measurement. Explicitly expose any
        # remaining budget cutoff rather than presenting it as a ranking miss.
        result = library.search(case["query"], limit=k, kind=case.get("kind", "skill"),
                                max_chars=100000, mode=mode, semantic=semantic,
                                required_terms=case.get("required_terms"))
        expected = set(case["relevant"])
        matches, found, excerpts = [], set(), []
        for rank, item in enumerate(result["results"], 1):
            labels = expected.intersection((item["name"], item["id"], item.get("title")))
            if labels:
                matches.append(rank)
                found.update(labels)
                evidence = item.get("evidence", {})
                if evidence.get("field") == "body":
                    excerpts.append(normalized(evidence["text"]))
        terms = [normalized(term.strip()) for term in case.get("evidence_contains", [])]
        evidence_hit = any(all(term in excerpt for term in terms) for excerpt in excerpts) if terms else None
        returned = len(result["results"])
        details.append({"query": case["query"], "kind": case.get("kind", "skill"),
                        "required_terms": case.get("required_terms") or [],
                        "expected_empty": not expected, "relevant": sorted(expected), "hit": bool(matches),
                        "evidence_contains": case.get("evidence_contains", []), "evidence_hit": evidence_hit,
                        "reciprocal_rank": (1 / matches[0] if matches else 0) if expected else None,
                        "recall": len(found) / len(expected) if expected else None,
                        "precision": len(matches) / k if expected else None,
                        "returned_precision": len(matches) / returned if returned and expected else (0 if expected else None),
                        "false_positive": bool(returned) if not expected else None,
                        "budget_limited": returned < k and result.get("next_offset") is not None,
                        "elapsed_ms": result["elapsed_ms"],
                        "returned": [item["name"] for item in result["results"]],
                        "returned_titles": [item.get("title") or item["name"] for item in result["results"]],
                        "returned_ids": [item["id"] for item in result["results"]]})
    count = len(details)
    latencies = sorted(d["elapsed_ms"] for d in details)
    positive = [d for d in details if not d["expected_empty"]]
    negative = [d for d in details if d["expected_empty"]]
    evidence_cases = [d for d in details if d["evidence_hit"] is not None]
    def average(rows, field):
        return sum(d[field] for d in rows) / len(rows) if rows else None
    false_positive_rate = average(negative, "false_positive")
    return {"queries": count, "positive_queries": len(positive), "negative_queries": len(negative),
            "k": k, "mode": mode, "max_chars": 100000,
            "hit_at_k": average(positive, "hit"), "mrr_at_k": average(positive, "reciprocal_rank"),
            "evidence_queries": len(evidence_cases), "evidence_hit_at_k": average(evidence_cases, "evidence_hit"),
            "recall_at_k": average(positive, "recall"), "precision_at_k": average(positive, "precision"),
            "returned_precision": average(positive, "returned_precision"),
            "false_positive_rate": false_positive_rate,
            "correct_empty_rate": 1 - false_positive_rate if negative else None,
            "budget_limited_queries": sum(d["budget_limited"] for d in details),
            "p95_ms": latencies[math.ceil(count * .95) - 1], "details": details}
