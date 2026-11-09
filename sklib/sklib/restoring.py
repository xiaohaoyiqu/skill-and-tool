"""Previewed, atomic annotation restore and path mapping; never writes sources."""
from __future__ import annotations

import hashlib
import codecs
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import json

from .annotations import values, validate, revision
from .failures import OperationFailure
from .indexer import now
from .jsonutil import loads
from .storage import dumps

MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024
MAX_RECORDS = 20000


def read_snapshot(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_SNAPSHOT_BYTES + 1)
    if len(raw) > MAX_SNAPSHOT_BYTES:
        raise ValueError("Snapshot exceeds 16 MiB")
    encoding = "utf-8-sig"
    for marker, name in ((codecs.BOM_UTF32_LE, "utf-32"), (codecs.BOM_UTF32_BE, "utf-32"),
                         (codecs.BOM_UTF16_LE, "utf-16"), (codecs.BOM_UTF16_BE, "utf-16")):
        if raw.startswith(marker):
            encoding = name
            break
    return loads(raw.decode(encoding))


def write_snapshot(path, snapshot):
    target = Path(path).expanduser().absolute()
    if target.suffix.lower() != ".json" or target.is_symlink():
        raise ValueError("Choose a non-symlink .json snapshot destination")
    target = target.resolve()
    data = (json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if len(data) > MAX_SNAPSHOT_BYTES:
        raise ValueError("Snapshot exceeds 16 MiB; export batches with records snapshot --root, --annotated-only or --offset/--limit")
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".sklib-snapshot-", dir=target.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"path": str(target), "size_bytes": len(data), "schema_version": 1}


def root_key(path):
    return os.path.normcase(path.replace("/", "\\").rstrip("\\")) if re.match(r"^[A-Za-z]:", path) else path.rstrip("/")


def validated(snapshot, root_map, entry_map, policy, resolutions, match_content):
    if not isinstance(snapshot, dict) or type(snapshot.get("schema_version")) is not int or snapshot["schema_version"] != 1:
        raise ValueError("Only annotation snapshot schema_version=1 is supported")
    if len(dumps(snapshot).encode("utf-8")) > MAX_SNAPSHOT_BYTES:
        raise ValueError("Snapshot exceeds 16 MiB")
    entries, orphans = snapshot.get("entries"), snapshot.get("orphaned_annotations", [])
    if not isinstance(entries, list) or not isinstance(orphans, list) or len(entries) + len(orphans) > MAX_RECORDS:
        raise ValueError("Snapshot must contain at most 20000 annotation records")
    if policy not in ("keep", "replace") or type(match_content) is not bool:
        raise ValueError("policy must be keep or replace; match_content must be boolean")
    maps = []
    for mapping in (root_map, entry_map, resolutions):
        mapping = {} if mapping is None else mapping
        if not isinstance(mapping, dict) or len(mapping) > MAX_RECORDS or any(
                not isinstance(key, str) or not key or len(key) > 32768 or not isinstance(value, str) or not value or len(value) > 32768
                for key, value in mapping.items()):
            raise ValueError("Mappings must contain nonempty string keys and values")
        maps.append(mapping)
    root_map, entry_map, resolutions = maps
    if any(choice not in ("keep", "replace") for choice in resolutions.values()):
        raise ValueError("Conflict resolutions must be keep or replace")
    records, seen = [], set()
    for entry, orphan in [(entry, False) for entry in entries] + [(entry, True) for entry in orphans]:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not 1 <= len(entry["id"]) <= 128:
            raise ValueError("Every annotation record needs a valid id")
        if entry["id"] in seen:
            raise ValueError("Snapshot contains duplicate annotation ids")
        seen.add(entry["id"])
        if not {"tags", "note", "favorite", "state"} <= entry.keys():
            raise ValueError("Every annotation record needs tags, note, favorite and state")
        if (not isinstance(entry["tags"], list) or not isinstance(entry["note"], str)
                or type(entry["favorite"]) is not bool or not isinstance(entry["state"], str)):
            raise ValueError("Annotation values must have explicit non-null types")
        validate(**{key: entry[key] for key in ("tags", "note", "favorite", "state")})
        incoming = {"tags": list(dict.fromkeys(tag.strip() for tag in entry["tags"])),
                    "note": entry["note"], "favorite": entry["favorite"], "state": entry["state"]}
        records.append({**({"id": entry["id"]} if orphan else entry), **incoming})
    for entry in entries:
        if (not isinstance(entry.get("root"), str) or not entry["root"] or len(entry["root"]) > 32768
                or not isinstance(entry.get("relative_path"), str) or not entry["relative_path"] or len(entry["relative_path"]) > 32768
                or entry.get("kind") not in ("skill", "project", "document")):
            raise ValueError("Snapshot entries require root, relative_path and kind")
        relative = PurePosixPath(entry["relative_path"].replace("\\", "/"))
        if not relative.parts or relative.is_absolute() or any(part in ("..", ".") or ":" in part for part in relative.parts):
            raise ValueError("Snapshot relative_path must stay within its source")
        if "revision" in entry and (not isinstance(entry["revision"], str) or not 1 <= len(entry["revision"]) <= 128):
            raise ValueError("Snapshot revision must be a string")
    if set(entry_map) - seen or set(resolutions) - seen:
        raise ValueError("Entry mappings and resolutions must refer to snapshot ids")
    roots = {root_key(entry["root"]) for entry in entries}
    if any(root_key(key) not in roots for key in root_map):
        raise ValueError("Root mapping does not refer to a snapshot source")
    return records, root_map, entry_map, resolutions


def make_plan(db, records, root_map, entry_map, policy, resolutions, match_content, offset=0, limit=50):
    documents = [dict(row) for row in db.execute("SELECT id,root,relative_path,path,kind,name,revision FROM documents")]
    by_id = {row["id"]: row for row in documents}
    by_path = {(root_key(row["root"]), os.path.normcase(row["relative_path"].replace("\\", "/"))): row for row in documents}
    registered = {root_key(row[0]): row[0] for row in db.execute("SELECT path FROM roots")}
    mapped_roots = {}
    for old, target in root_map.items():
        canonical = root_key(str(Path(target).expanduser().resolve()))
        if canonical not in registered:
            raise ValueError("A mapping target must be an already indexed source: " + target)
        if root_key(old) in mapped_roots:
            raise ValueError("Duplicate root mapping")
        mapped_roots[root_key(old)] = canonical
    by_content = {}
    if match_content:
        for row in documents:
            by_content.setdefault((row["kind"], row["revision"]), []).append(row)
    plan, targets = [], set()
    for entry in records:
        source_id = entry["id"]
        target, match, reason = None, "orphan", None
        mapped_root = mapped_roots.get(root_key(entry["root"])) if "root" in entry else None
        if source_id in entry_map:
            target = by_id.get(entry_map[source_id])
            if target is None:
                raise ValueError("Explicit target is not indexed: " + entry_map[source_id])
            match = "explicit_id"
        elif mapped_root:
            relative = os.path.normcase(entry["relative_path"].replace("\\", "/"))
            target = by_path.get((mapped_root, relative))
            match = "mapped_path" if target else "orphan"
        elif source_id in by_id:
            target, match = by_id[source_id], "id"
        elif "root" in entry:
            target = by_path.get((root_key(entry["root"]), os.path.normcase(entry["relative_path"].replace("\\", "/"))))
            match = "path" if target else "orphan"
        if target is None and match_content and entry.get("revision"):
            candidates = by_content.get((entry.get("kind"), entry["revision"]), [])
            if mapped_root:
                candidates = [row for row in candidates if root_key(row["root"]) == mapped_root]
            if len(candidates) == 1:
                target, match = candidates[0], "unique_content"
            elif candidates:
                reason = "ambiguous_content"
        if target is not None and entry.get("kind", target["kind"]) != target["kind"]:
            raise ValueError("Cannot map an annotation to a different document kind")
        target_id = target["id"] if target else source_id
        if target_id in targets:
            raise ValueError("Multiple snapshot records map to the same target: " + target_id)
        targets.add(target_id)
        old = db.execute("SELECT * FROM annotations WHERE document_id=?", (target_id,)).fetchone()
        incoming = {key: entry[key] for key in ("tags", "note", "favorite", "state")}
        before = values(old)
        choice = resolutions.get(source_id, policy)
        if before == incoming:
            action = "unchanged"
        elif old is not None and choice == "keep":
            action = "conflict"
        else:
            action = "replace" if old is not None else "insert"
        plan.append({"source_id": source_id, "target_id": target_id, "match": match,
            "reason": reason, "orphan": target is None, "name": str(entry.get("name", source_id))[:200],
            "source_root": entry.get("root"), "source_relative_path": entry.get("relative_path"),
            "target_path": target["path"] if target else None, "target_revision": target["revision"] if target else None,
            "annotation_revision": revision(target_id, old), "policy": choice, "action": action,
            "before": before if old is not None and offset <= len(plan) < offset + limit else None, "incoming": incoming})
    digest = hashlib.sha256()
    for item in plan:
        # The opaque revision covers the full current values. Retain full old
        # notes only for the displayed page, without changing the plan token.
        digest.update(dumps({key: value for key, value in item.items() if key != "before"}).encode("utf-8"))
        digest.update(b"\n")
    token = digest.hexdigest()
    counts = {action: sum(item["action"] == action for item in plan) for action in ("insert", "replace", "conflict", "unchanged")}
    counts.update({"total": len(plan), "orphans": sum(item["orphan"] for item in plan),
                   "ambiguous": sum(item["reason"] == "ambiguous_content" for item in plan)})
    return plan, token, counts


def restore(library, snapshot, *, root_map=None, entry_map=None, policy="keep", resolutions=None,
            match_content=False, expected_preview=None, apply=False, offset=0, limit=50):
    if type(apply) is not bool or type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("Invalid restore preview paging")
    if apply and (not isinstance(expected_preview, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_preview)):
        raise ValueError("Applying annotations requires a valid preview token")
    records, root_map, entry_map, resolutions = validated(snapshot, root_map, entry_map, policy, resolutions, match_content)
    with library.store.connect() as db:
        db.execute("BEGIN IMMEDIATE" if apply else "BEGIN")
        plan, token, counts = make_plan(db, records, root_map, entry_map, policy, resolutions, match_content, offset, limit)
        if apply and token != expected_preview:
            raise OperationFailure("Restore preview is stale", code="restore_preview_stale",
                recovery="目标条目、整理记录或导入选项已变化。保留导入文件与映射，重新预览核对后再导入。")
        if apply:
            timestamp = now()
            for item in plan:
                if item["action"] in ("insert", "replace"):
                    library._write_annotation(db, item["target_id"], item["incoming"], timestamp)
            updated = counts["insert"] + counts["replace"]
            if updated:
                db.execute("INSERT INTO events(created_at,action,details) VALUES(?,?,?)", (
                    timestamp, "annotations.restore", dumps({"counts": counts, "preview_token": token})))
            return {"applied": True, "updated": updated, "counts": counts, "preview_token": token,
                    "source_annotations_retained": True}
        return {"applied": False, "counts": counts, "preview_token": token, "offset": offset,
            "entries": plan[offset:offset + limit], "next_offset": offset + limit if offset + limit < len(plan) else None,
            "source_annotations_retained": True}
