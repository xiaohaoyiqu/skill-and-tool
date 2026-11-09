"""Annotation values and opaque versions shared by retrieval and editing."""
from __future__ import annotations

import hashlib
import json
import re

from .failures import OperationFailure
from .storage import dumps

STATES = {"unreviewed", "to_try", "useful", "not_recommended"}


def values(row=None):
    row = dict(row) if row is not None else {}
    tags = row.get("tags") or []
    return {"tags": json.loads(tags) if isinstance(tags, str) else tags,
            "note": row.get("note") or "", "favorite": bool(row.get("favorite")),
            "state": row.get("state") or "unreviewed"}


def revision(identifier, row=None):
    row = dict(row) if row is not None else {}
    return hashlib.sha256(dumps({"id": identifier, **values(row), "updated_at": row.get("updated_at")}).encode("utf-8")).hexdigest()


def validate(tags=None, note=None, favorite=None, state=None):
    if tags is not None and (not isinstance(tags, list) or len(tags) > 30 or any(not isinstance(t, str) or not 1 <= len(t.strip()) <= 80 for t in tags)):
        raise ValueError("tags must be up to 30 nonempty strings of <=80 characters")
    if note is not None and (not isinstance(note, str) or len(note) > 10000):
        raise ValueError("Note must be at most 10000 characters")
    if favorite is not None and type(favorite) is not bool:
        raise ValueError("favorite must be boolean")
    if state is not None and (not isinstance(state, str) or state not in STATES):
        raise ValueError("Unknown review state")


def check_revision(identifier, row, expected):
    if expected is None:
        return
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Invalid annotation revision")
    if revision(identifier, row) != expected:
        raise OperationFailure("Annotation changed since it was loaded", code="annotation_conflict",
            recovery="当前记录已更新。保留草稿或批量选择，重新读取并核对当前记录，再基于最新版本提交。",
            progress={"id": identifier})
