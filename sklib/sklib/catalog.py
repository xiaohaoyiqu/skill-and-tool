"""Virtual sorting of indexed locations, without keyword search or source moves."""
from __future__ import annotations

import json
import time
from pathlib import Path

from .projects import PROJECT_TYPES
from .storage import dumps
from .annotations import STATES, revision as annotation_revision

QUEUES = ("all", "unclassified", "needs_review", "warnings", "duplicates")
SORTS = {"name": "d.name COLLATE NOCASE,d.id", "recent": "d.indexed_at DESC,d.id", "source": "d.root,d.path,d.id"}
DUPLICATES = "d.kind='skill' AND d.revision IN(SELECT revision FROM documents WHERE kind='skill' GROUP BY revision HAVING count(*)>1)"
QUEUE_SQL = {"all": "1=1", "unclassified": "json_array_length(coalesce(a.tags,'[]'))=0",
             "needs_review": "coalesce(a.state,'unreviewed')='unreviewed'",
             "warnings": "json_array_length(d.warnings)>0", "duplicates": DUPLICATES}
JOIN = "FROM documents d LEFT JOIN annotations a ON a.document_id=d.id"


def queue_condition(queue: str) -> str:
    if not isinstance(queue, str) or queue not in QUEUES:
        raise ValueError("Unknown sorting queue")
    return QUEUE_SQL[queue]


def selection(*, kind="all", root=None, project_type=None, tags=None, favorite=False, state=None) -> tuple[str, list]:
    if not isinstance(kind, str) or kind not in {"all", "skill", "project", "document"}:
        raise ValueError("Unknown document kind")
    if root is not None and not isinstance(root, str):
        raise ValueError("root must be a directory string")
    if project_type is not None and (not isinstance(project_type, str) or project_type not in PROJECT_TYPES):
        raise ValueError("Unknown project type")
    if state is not None and (not isinstance(state, str) or state not in STATES):
        raise ValueError("Unknown review state")
    if type(favorite) is not bool:
        raise ValueError("favorite must be boolean")
    if tags is not None and (not isinstance(tags, list) or len(tags) > 30 or any(not isinstance(t, str) or not 1 <= len(t.strip()) <= 80 for t in tags)):
        raise ValueError("tags must be up to 30 nonempty strings of <=80 characters")
    clauses, args = ["1=1"], []
    if kind != "all":
        clauses.append("d.kind=?")
        args.append(kind)
    if root:
        clauses.append("d.root=?")
        args.append(str(Path(root).expanduser().resolve()))
    if project_type:
        clauses.append("d.kind='project' AND EXISTS(SELECT 1 FROM json_each(d.metadata,'$.project_types') WHERE value=?)")
        args.append(project_type)
    if favorite:
        clauses.append("a.favorite=1")
    if state:
        clauses.append("coalesce(a.state,'unreviewed')=?")
        args.append(state)
    for tag in tags or []:
        clauses.append("EXISTS(SELECT 1 FROM json_each(a.tags) WHERE value=?)")
        args.append(tag.strip())
    return " AND ".join(clauses), args


def browse(store, *, kind="all", queue="all", root=None, project_type=None, tags=None,
           favorite=False, state=None, sort="name", limit=25, offset=0, max_chars=24000) -> dict:
    started = time.perf_counter()
    condition, args = selection(kind=kind, root=root, project_type=project_type, tags=tags, favorite=favorite, state=state)
    queued = queue_condition(queue)
    if not isinstance(sort, str) or sort not in SORTS:
        raise ValueError("Unknown catalog sort order")
    if type(limit) is not int or not 1 <= limit <= 100 or type(offset) is not int or not 0 <= offset <= 100000:
        raise ValueError("limit must be 1..100 and offset must be 0..100000")
    if type(max_chars) is not int or not 1500 <= max_chars <= 100000:
        raise ValueError("max_chars must be 1500..100000")
    with store.connect() as db:
        db.execute("BEGIN")
        # Aggregate all queues in one pass over the same filtered snapshot.
        aggregates = ",".join(f"coalesce(sum(CASE WHEN ({predicate}) THEN 1 ELSE 0 END),0)" for predicate in QUEUE_SQL.values())
        counts = dict(zip(QUEUE_SQL, db.execute(f"SELECT {aggregates} {JOIN} WHERE {condition}", args).fetchone()))
        total = counts[queue]
        rows = db.execute(f"""SELECT d.id,d.kind,d.name,d.description,d.path,d.root,d.revision,d.metadata,d.warnings,
                a.tags,a.note,a.favorite,a.state,a.updated_at {JOIN} WHERE {condition} AND ({queued})
                ORDER BY {SORTS[sort]} LIMIT ? OFFSET ?""", [*args, limit, offset]).fetchall()
        revisions = list({row["revision"] for row in rows if row["kind"] == "skill"})
        duplicates = {}
        if revisions:
            placeholders = ",".join("?" for _ in revisions)
            duplicates = dict(db.execute(f"SELECT revision,count(*)-1 FROM documents WHERE kind='skill' AND revision IN({placeholders}) GROUP BY revision", revisions))
        items, used = [], 0
        for row in rows:
            metadata = json.loads(row["metadata"])
            item = {"id": row["id"], "kind": row["kind"], "name": row["name"][:200],
                    "description": row["description"][:600], "path": row["path"], "root": row["root"],
                    "revision": row["revision"], "annotation_revision": annotation_revision(row["id"], row), "tags": json.loads(row["tags"] or "[]"),
                    "favorite": bool(row["favorite"]), "state": row["state"] or "unreviewed",
                    "project_types": metadata.get("project_types", []) if row["kind"] == "project" else [], "warnings": json.loads(row["warnings"]),
                    "evidence": {"field": "name", "text": row["description"][:260], "line": 1},
                    "duplicate_count": 0, "next": {"tool": "get_skill", "id": row["id"]}}
            if row["kind"] == "skill":
                item["duplicate_count"] = duplicates.get(row["revision"], 0)
            size = len(dumps(item))
            if items and used + size > max_chars:
                break
            if size > max_chars:
                item = {key: value for key, value in item.items() if key not in {"path", "root", "warnings", "tags"}}
                item.update(tags=[], warnings=[], result_truncated=True)
                while len(dumps(item)) > max_chars:
                    for field in ("description", "name"):
                        item[field] = item[field][:max(1, len(item[field]) // 2)]
                    item["evidence"]["text"] = item["evidence"]["text"][:len(item["evidence"]["text"]) // 2]
            items.append(item)
            used += len(dumps(item))
        next_offset = offset + len(items)
        return {"results": items, "returned": len(items), "total": total, "counts": counts,
                "queue": queue, "sort": sort, "offset": offset,
                "next_offset": next_offset if next_offset < total and next_offset <= 100000 else None,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                "index_empty": db.execute("SELECT NOT EXISTS(SELECT 1 FROM documents)").fetchone()[0] == 1,
                "location_records": True}
