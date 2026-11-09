"""Strict JSON decoding for tool and HTTP input, including Unicode scalars."""
from __future__ import annotations

import json
import math


def loads(data: str | bytes) -> object:
    def reject_constant(value: str):
        raise ValueError(f"Invalid JSON numeric constant: {value}")
    try:
        value = json.loads(data, parse_constant=reject_constant)
    except RecursionError as exc:
        raise ValueError("JSON nesting is too deep") from exc
    pending = [(value, 0)]
    while pending:
        current, depth = pending.pop()
        if depth > 100:
            raise ValueError("JSON nesting exceeds 100 levels")
        if isinstance(current, str):
            current.encode("utf-8")
        elif isinstance(current, float) and not math.isfinite(current):
            raise ValueError("JSON numeric value is outside the finite range")
        elif isinstance(current, dict):
            pending.extend((key, depth + 1) for key in current)
            pending.extend((item, depth + 1) for item in current.values())
        elif isinstance(current, list):
            pending.extend((item, depth + 1) for item in current)
    return value
