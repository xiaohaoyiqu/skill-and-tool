"""Application API shared by CLI, MCP and the manual UI."""
from __future__ import annotations

import hashlib
import heapq
import json
import math
import os
import time
from pathlib import Path, PurePosixPath

from .indexer import excluded_name, index_root, is_link, now, parse_skill, refresh_fts, within
from .files import file_detail, read_text_info, text_lines
from .projects import PROJECT_TYPES, parse_project, project_type as detect_project_type
from .catalog import STATES, browse, queue_condition, selection
from .failures import OperationFailure
from .storage import Store, advance_source_epoch, dumps
from .text import content_hash, match_expression, normalized, query_terms, required_expression, snippet, tokens
from .annotations import values as annotation_values, revision as annotation_revision, validate as validate_annotation, check_revision

SUMMARY_COLUMNS = ",".join("d." + name for name in (
    "id", "root", "path", "kind", "name", "title", "description", "revision", "source", "metadata", "warnings"))


class Library:
    def __init__(self, home: str | Path):
        self.store = Store(home)

    def index(self, root: str | Path, **options) -> dict:
        return index_root(self.store, root, **options)

    def browse(self, **options) -> dict:
        return browse(self.store, **options)

    def check_source(self, root: str, **options) -> dict:
        from .sources import check_source
        return check_source(self, root, **options)

    def restore_annotations(self, snapshot: dict, **options) -> dict:
        from .restoring import restore
        return restore(self, snapshot, **options)

    def portable_snapshot(self, *, root=None, annotated_only=False, offset=0, limit=None) -> dict:
        from .restoring import root_key
        if type(annotated_only) is not bool or type(offset) is not int or offset < 0 or (limit is not None and (type(limit) is not int or not 1 <= limit <= 20000)):
            raise ValueError("Invalid snapshot selection")
        if root is not None and (not isinstance(root, str) or not root.strip()):
            raise ValueError("Snapshot root must be a source path")
        snapshot = self.snapshot()
        if root is None and not annotated_only and offset == 0 and limit is None:
            return snapshot
        entries = snapshot["entries"]
        orphans = snapshot["orphaned_annotations"]
        if root is not None:
            canonical = root_key(str(Path(root).expanduser().resolve()))
            if not any(root_key(source["root"]) == canonical for source in snapshot["sources"]):
                raise ValueError("Snapshot source is not registered")
            entries = [entry for entry in entries if root_key(entry["root"]) == canonical]
            orphans = []
            snapshot["sources"] = [source for source in snapshot["sources"] if root_key(source["root"]) == canonical]
        records = [(False, entry) for entry in entries] + [(True, entry) for entry in orphans]
        if annotated_only:
            defaults = annotation_values()
            records = [(orphan, entry) for orphan, entry in records if annotation_values(entry) != defaults]
        chosen = records[offset:] if limit is None else records[offset:offset + limit]
        snapshot["entries"] = [entry for orphan, entry in chosen if not orphan]
        snapshot["orphaned_annotations"] = [entry for orphan, entry in chosen if orphan]
        end = offset + len(chosen)
        snapshot["selection"] = {"root": root, "annotated_only": annotated_only, "offset": offset,
            "total": len(records), "returned": len(chosen), "next_offset": end if end < len(records) else None}
        return snapshot

    def export_snapshot(self, destination: str, **options) -> dict:
        from .restoring import write_snapshot
        target = Path(destination).expanduser().resolve()
        if any(within(target, Path(source["path"])) for source in self.status()["roots"]):
            raise ValueError("Save annotation snapshots outside indexed source directories")
        snapshot = self.portable_snapshot(**options)
        return write_snapshot(destination, snapshot)

    def migrate_annotations(self, from_root: str, to_root: str, **options) -> dict:
        from .restoring import root_key
        if not isinstance(from_root, str) or not from_root.strip() or not isinstance(to_root, str) or not to_root.strip():
            raise ValueError("Source and target roots are required")
        snapshot = self.snapshot()
        canonical = root_key(str(Path(from_root).expanduser().resolve()))
        snapshot["entries"] = [entry for entry in snapshot["entries"] if root_key(entry["root"]) == canonical]
        if not snapshot["entries"]:
            raise ValueError("The original source has no indexed entries; import its saved snapshot instead")
        snapshot["orphaned_annotations"] = []
        return self.restore_annotations(snapshot, root_map={snapshot["entries"][0]["root"]: to_root}, **options)

    def remove_root(self, root: str | Path) -> dict:
        from .sources import registered_source
        if not isinstance(root, (str, Path)) or not str(root).strip():
            raise ValueError("A source path is required")
        with self.store.connect() as db:
            registered = registered_source(db, root)
            path = registered["path"] if registered else str(Path(root).expanduser().absolute())
            db.execute("BEGIN IMMEDIATE")
            count = db.execute("SELECT count(*) FROM documents WHERE root=?", (path,)).fetchone()[0]
            db.execute("DELETE FROM documents_fts WHERE rowid IN(SELECT rowid FROM documents WHERE root=?)", (path,))
            db.execute("DELETE FROM vectors WHERE document_id IN(SELECT id FROM documents WHERE root=?)", (path,))
            db.execute("DELETE FROM documents WHERE root=?", (path,))
            db.execute("DELETE FROM roots WHERE path=?", (path,))
            advance_source_epoch(db, path)
            result = {"root": path, "removed_from_index": count}
            db.execute("INSERT INTO events(created_at,action,details) VALUES(?,?,?)", (now(), "remove_root", dumps(result)))
            return result

    def status(self) -> dict:
        with self.store.connect() as db:
            return {"home": str(self.store.home), "documents": db.execute("SELECT count(*) FROM documents").fetchone()[0],
                    "counts": dict(db.execute("SELECT kind,count(*) FROM documents GROUP BY kind")),
                    "roots": [{"path": row["path"], "scanned_at": row["scanned_at"],
                               "last_report": json.loads(row["last_report"])} for row in db.execute("SELECT * FROM roots ORDER BY path")],
                    "vectors": db.execute("SELECT count(*) FROM vectors").fetchone()[0]}

    def search(self, query: str, *, kind: str = "skill", limit: int = 5, offset: int = 0,
               root: str | None = None, tags: list[str] | None = None, favorite: bool = False,
               state: str | None = None, max_chars: int = 16000, mode: str = "lexical",
               semantic=None, project_type: str | None = None, queue: str = "all",
               required_terms: list[str] | None = None) -> dict:
        if not isinstance(query, str) or not query.strip() or len(query) > 2048:
            raise ValueError("Query must contain 1..2048 characters")
        if not isinstance(kind, str) or kind not in {"skill", "project", "document", "all"}:
            raise ValueError("Unknown document kind")
        if type(limit) is not int or not 1 <= limit <= 50 or type(offset) is not int or not 0 <= offset <= 500:
            raise ValueError("limit must be 1..50 and offset must be 0..500")
        if type(max_chars) is not int or not 1500 <= max_chars <= 100000:
            raise ValueError("max_chars must be 1500..100000")
        if not isinstance(mode, str) or mode not in {"lexical", "semantic", "hybrid"}:
            raise ValueError("Unknown search mode")
        if state is not None and (not isinstance(state, str) or state not in STATES):
            raise ValueError("Unknown review state")
        if type(favorite) is not bool:
            raise ValueError("favorite must be boolean")
        if project_type is not None and (not isinstance(project_type, str) or project_type not in PROJECT_TYPES):
            raise ValueError("Unknown project type")
        if root is not None and not isinstance(root, str):
            raise ValueError("root must be a directory string")
        if tags is not None and (not isinstance(tags, list) or len(tags) > 30 or any(not isinstance(t, str) for t in tags)):
            raise ValueError("tags must be a list of up to 30 strings")
        if mode != "lexical" and semantic is None:
            raise ValueError("Semantic search requires an explicitly configured embedding provider")
        required = required_expression(required_terms)
        start = time.perf_counter()
        literal, expanded = query_terms(query)
        # In mixed-language task requests preserve explicit product identifiers.
        # Otherwise generic expansions such as "optimization" can hide the fact
        # that the requested framework is absent from the indexed collection.
        has_han = any("\u3400" <= char <= "\u9fff" for char in query)
        anchors = [term for term in literal if term.isascii() and len(term) >= 3] if has_han else []
        # Short document queries often include a collection name as context.
        # Require every anchor for multi-identifier document queries.
        strict_anchors = kind == "document" and len(anchors) >= 3
        anchor_expression = match_expression(anchors, all_terms=strict_anchors)
        condition, args = selection(kind=kind, root=root, project_type=project_type, tags=tags, favorite=favorite, state=state)
        condition += " AND (" + queue_condition(queue) + ")"
        if required:
            condition += " AND d.id IN (SELECT document_id FROM documents_fts WHERE documents_fts MATCH ?)"
            args.append(required)
        pool_size = max(200, offset + limit * 5)
        ranks: list[list[str]] = []
        by_id: dict[str, dict] = {}
        vector = semantic.encode([query])[0] if mode != "lexical" else None
        with self.store.connect() as db:
            # Every retrieval channel and the selected bodies use one WAL snapshot.
            db.execute("BEGIN")
            # Two lists keep exact identifiers competitive with expanded task words.
            for terms in (() if mode == "semantic" else (literal, expanded)):
                if not terms:
                    continue
                expression = match_expression(terms)
                if anchor_expression:
                    expression = "(" + expression + ") AND (" + anchor_expression + ")"
                rows = db.execute(f"""SELECT {SUMMARY_COLUMNS},a.tags,a.note,a.favorite,a.state,a.updated_at,
                    bm25(documents_fts,0,9,5,1,6) AS lexical_score FROM documents_fts
                    JOIN documents d ON d.id=documents_fts.document_id
                    LEFT JOIN annotations a ON a.document_id=d.id
                    WHERE documents_fts MATCH ? AND {condition}
                    ORDER BY lexical_score,d.id LIMIT ?""", [expression, *args, pool_size]).fetchall()
                order = []
                for row in rows:
                    by_id[row["id"]] = dict(row)
                    order.append(row["id"])
                ranks.append(order)
            semantic_count = 0
            if mode != "lexical":
                eligible = db.execute(f"""SELECT d.id,v.embedding,v.dimension
                    FROM vectors v JOIN documents d ON d.id=v.document_id
                    LEFT JOIN annotations a ON a.document_id=d.id
                    WHERE v.revision=d.revision AND v.model=? AND {condition}""", [semantic.model, *args])

                def scored_candidates():
                    nonlocal semantic_count
                    # Stream each vector; retain only the bounded ranking pool.
                    # Still validate every eligible vector, including low scores.
                    for row in eligible:
                        score = semantic.similarity(vector, row["embedding"], row["dimension"])
                        semantic_count += 1
                        yield score, row["id"]

                best = heapq.nsmallest(pool_size, scored_candidates(), key=lambda item: (-item[0], item[1]))
                semantic_rank = [item[1] for item in best]
                if semantic_rank:
                    placeholders = ",".join("?" for _ in semantic_rank)
                    rows = db.execute(f"""SELECT {SUMMARY_COLUMNS},a.tags,a.note,a.favorite,a.state,a.updated_at
                        FROM documents d LEFT JOIN annotations a ON a.document_id=d.id
                        WHERE d.id IN ({placeholders})""", semantic_rank)
                    for row in rows:
                        by_id[row["id"]] = dict(row)
                if mode == "semantic":
                    ranks = [semantic_rank]
                else:
                    ranks.append(semantic_rank)
            scores: dict[str, float] = {}
            for rank_index, order in enumerate(ranks):
                weight = 1.15 if rank_index == 0 else 1.0
                for position, document_id in enumerate(order, 1):
                    scores[document_id] = scores.get(document_id, 0) + weight / (60 + position)
            # Semantic-only diagnostics preserve dense ordering without lexical boosts.
            q = normalized(query.strip())
            for document_id in scores:
                if mode == "semantic":
                    continue
                row = by_id[document_id]
                name = normalized(row["name"])
                if q == name or q == normalized(row["title"]):
                    scores[document_id] += 0.1
                elif q in name:
                    scores[document_id] += 0.025
                if anchors and set(anchors).intersection(tokens(row["name"])):
                    # A skill actually named for the requested product should
                    # outrank a general workflow mentioning it in a reference.
                    scores[document_id] += 0.035
                name_terms = set(tokens(row["name"] + " " + row["description"]))
                coverage = sum(t in name_terms for t in literal) / max(1, len(literal))
                scores[document_id] += 0.012 * coverage

            ordered = sorted(scores, key=lambda key: (-scores[key], key))
            # Collapse exact-content copies, while retaining every location.
            groups: dict[tuple, list[str]] = {}
            for document_id in ordered:
                row = by_id[document_id]
                # Identical manifests in distinct projects remain separate entries.
                identity = row["revision"] if row["kind"] == "skill" else row["path"]
                groups.setdefault((row["kind"], identity), []).append(document_id)
            grouped = list(groups.values())
            results, used = [], 0
            for members in grouped[offset:offset + limit]:
                row = by_id[members[0]]
                body = db.execute("SELECT body FROM documents WHERE id=?", (row["id"],)).fetchone()[0]
                markdown = Path(row["path"]).suffix.lower() in {".md", ".markdown", ".mdx"}
                evidence = {"field": "body", **snippet(body, literal + expanded, markdown=markdown)}
                if evidence["match_count"] == 0 and "heading" not in evidence:
                    for field, content in (("annotation", (row["note"] or "") + " " + (row["tags"] or "")),
                                           ("name", row["name"])):
                        candidate = snippet(content, literal + expanded)
                        if candidate["match_count"]:
                            evidence = {"field": field, **candidate}
                            break
                metadata = json.loads(row["metadata"])
                item = {"id": row["id"], "kind": row["kind"], "name": row["name"][:200], "title": row["title"][:200],
                        "description": row["description"][:600], "path": row["path"], "root": row["root"],
                        "revision": row["revision"], "annotation_revision": annotation_revision(row["id"], row), "source": json.loads(row["source"]),
                        "score": round(scores[row["id"]], 6), "evidence": evidence,
                        "tags": json.loads(row["tags"] or "[]"), "note": (row["note"] or "")[:400],
                        "favorite": bool(row["favorite"]), "state": row["state"] or "unreviewed",
                        "compatibility": metadata.get("compatibility", "unknown"),
                        "project_types": metadata.get("project_types", []) if row["kind"] == "project" else [],
                        "warnings": json.loads(row["warnings"]),
                        "duplicate_count": len(members) - 1,
                        "other_locations": [{"id": key, "path": by_id[key]["path"]} for key in members[1:6]],
                        "next": {"tool": "get_skill", "id": row["id"]}}
                size = len(dumps(item))
                if results and used + size > max_chars:
                    break
                if size > max_chars:
                    # Keep the first candidate usable even with a tight budget.
                    # Full paths/metadata remain available through get_skill.
                    evidence.pop("heading", None)
                    item = {"id": row["id"], "kind": row["kind"], "name": row["name"][:120],
                            "description": row["description"][:200], "revision": row["revision"], "annotation_revision": annotation_revision(row["id"], row),
                            "score": round(scores[row["id"]], 6),
                            "evidence": {**evidence, "text": evidence["text"][:120], "truncated": True},
                            "tags": [], "favorite": bool(row["favorite"]), "duplicate_count": len(members) - 1,
                            "result_truncated": True, "next": {"tool": "get_skill", "id": row["id"]}}
                    while len(dumps(item)) > max_chars:
                        for field in ("description", "name"):
                            item[field] = item[field][:max(1, len(item[field]) // 2)]
                        item["evidence"]["text"] = item["evidence"]["text"][:len(item["evidence"]["text"]) // 2]
                results.append(item)
                used += len(dumps(item))
            next_offset = offset + len(results)
            return {"query": query, "mode": mode, "expanded_terms": expanded,
                    "required_terms": [term.strip() for term in required_terms or []], "results": results,
                    "returned": len(results), "candidate_groups": len(grouped),
                    "next_offset": next_offset if next_offset < len(grouped) and next_offset <= 500 else None,
                    "candidate_limit": pool_size, "semantic_coverage": semantic_count,
                    "elapsed_ms": round((time.perf_counter() - start) * 1000, 2),
                    "score_meaning": "relative ranking only; not probability or compatibility",
                    "index_empty": db.execute("SELECT NOT EXISTS(SELECT 1 FROM documents)").fetchone()[0] == 1}

    def _row(self, db, document_id: str):
        if not isinstance(document_id, str) or not 1 <= len(document_id) <= 128:
            raise ValueError("A valid document id is required")
        row = db.execute("SELECT * FROM documents WHERE id=?", (document_id,)).fetchone()
        if row is None:
            raise OperationFailure(f"Unknown document id: {document_id}", code="entry_not_found",
                recovery="条目可能已移出索引。检查来源，重新浏览或检索当前条目后再操作。")
        return row

    def get(self, document_id: str, *, expected_revision: str | None = None,
            start_char: int = 0, max_chars: int | None = None,
            expected_content_revision: str | None = None) -> dict:
        if type(start_char) is not int or start_char < 0:
            raise ValueError("start_char must be a nonnegative integer")
        if max_chars is not None and (type(max_chars) is not int or not 1500 <= max_chars <= 100000):
            raise ValueError("max_chars must be 1500..100000")
        if start_char and (not expected_revision or not expected_content_revision or max_chars is None):
            raise ValueError("Continuation requires expected_revision, expected_content_revision and max_chars")
        with self.store.connect() as db:
            row = self._row(db, document_id)
            path = Path(row["path"])
            root = Path(row["root"])
            if not within(path.resolve(), root) or path.resolve() != path.absolute() or is_link(path):
                raise ValueError("Source moved outside its registered root")
            indexed_metadata = json.loads(row["metadata"])
            decoding = indexed_metadata.get("_sklib", {})
            decoding = decoding.get("encoding", "auto") if isinstance(decoding, dict) else "auto"
            body, actual_encoding = read_text_info(path, encoding=decoding)
            actual_revision = content_hash(body)
            content_revision = hashlib.sha256(body.encode("utf-8")).hexdigest()
            if expected_revision and actual_revision != expected_revision:
                raise OperationFailure("Source changed since selection; reindex and search again", code="source_changed",
                    recovery="重新扫描来源并选择当前版本。此次没有读取所要求的旧版本。")
            if expected_content_revision and expected_content_revision != content_revision:
                raise OperationFailure("Source changed since previous page", code="source_changed",
                    recovery="正文或换行已改变。清空已拼接的内容，从 start_char=0 重新读取。")
            if start_char > len(body):
                raise ValueError("start_char is beyond end of file")
            content = body[start_char:] if max_chars is None else body[start_char:start_char + max_chars]
            end_char = start_char + len(content)
            files = []
            details = []
            manifest_truncated = False
            current_metadata, current_warnings = (parse_skill(body, path.parent.name) if row["kind"] == "skill" else
                parse_project(body, path) if detect_project_type(path.name) else (indexed_metadata, json.loads(row["warnings"])))
            if row["kind"] == "skill" and path.name != "SKILL.md":
                current_warnings.append("Nonstandard skill filename; prefer SKILL.md for agent compatibility")
            if row["kind"] == "skill":
                walk_errors = []
                for visited, (base, dirs, names) in enumerate(os.walk(path.parent, followlinks=False, onerror=walk_errors.append), 1):
                    if visited > 2000:
                        manifest_truncated = True
                        break
                    directory = Path(base)
                    kept = []
                    for name in sorted(dirs):
                        try:
                            if not name.startswith(".") and not excluded_name(name) and not is_link(directory / name):
                                kept.append(name)
                        except OSError as exc:
                            walk_errors.append(exc)
                    dirs[:] = kept
                    if len(directory.relative_to(path.parent).parts) >= 20:
                        manifest_truncated |= bool(dirs)
                        dirs[:] = []
                    for name in sorted(names):
                        resource = directory / name
                        try:
                            if not name.startswith(".") and not is_link(resource) and within(resource.resolve(), path.parent):
                                relative = resource.relative_to(path.parent).as_posix()
                                detail = file_detail(resource, relative)
                                files.append(relative)
                                details.append(detail)
                        except (OSError, ValueError) as exc:
                            walk_errors.append(exc)
                        if len(files) > 256:
                            files.pop()
                            details.pop()
                            manifest_truncated = True
                            break
                    if manifest_truncated and len(files) == 256:
                        break
                if walk_errors:
                    current_warnings.append("Some resource directories or files could not be listed")
                    manifest_truncated = True
            else:
                files = [path.name]
                details = [file_detail(path, path.name)]
            annotation = db.execute("SELECT * FROM annotations WHERE document_id=?", (document_id,)).fetchone()
            return {"id": document_id, "kind": row["kind"], "name": current_metadata.get("name", row["name"]), "path": str(path),
                    "skill_root": str(path.parent), "content": content, "revision": actual_revision,
                    "start_char": start_char, "total_chars": len(body), "content_truncated": end_char < len(body),
                    "content_revision": content_revision,
                    "next_start_char": end_char if end_char < len(body) else None,
                    "next": {"tool": "get_skill", "id": document_id, "expected_revision": actual_revision,
                             "expected_content_revision": content_revision,
                             "start_char": end_char, "max_chars": max_chars} if end_char < len(body) else None,
                    "indexed_revision": row["revision"], "stale": actual_revision != row["revision"],
                    "source": json.loads(row["source"]), "metadata": current_metadata,
                    "warnings": current_warnings, "files": files,
                    "file_details": details, "encoding": actual_encoding,
                    "file_list_truncated": manifest_truncated,
                    "annotation": dict(annotation) if annotation else None, "annotation_revision": annotation_revision(document_id, annotation),
                    "estimated_tokens": math.ceil(len(content) / 3)}

    def read_file(self, document_id: str, relative_path: str, *, start_line: int = 1,
                  max_lines: int = 200, max_chars: int = 16000, expected_revision: str | None = None,
                  encoding: str | None = None) -> dict:
        if type(start_line) is not int or start_line < 1 or type(max_lines) is not int or not 1 <= max_lines <= 1000:
            raise ValueError("Invalid line range")
        if type(max_chars) is not int or not 100 <= max_chars <= 100000:
            raise ValueError("max_chars must be 100..100000")
        if not isinstance(relative_path, str) or not 1 <= len(relative_path) <= 2000:
            raise ValueError("A resource relative path is required")
        relative = PurePosixPath(relative_path.replace("\\", "/"))
        if (relative.is_absolute() or not relative.parts
                or any(p == ".." or ":" in p or p.startswith(".") for p in relative.parts)
                or any(excluded_name(p) for p in relative.parts[:-1])):
            raise ValueError("Resource path must stay inside the skill directory")
        with self.store.connect() as db:
            row = self._row(db, document_id)
            folder = Path(row["path"]).parent
            if not within(folder.resolve(), Path(row["root"])) or folder.resolve() != folder.absolute():
                raise ValueError("Source moved outside its registered root")
            if row["kind"] != "skill" and relative.as_posix() != Path(row["path"]).name:
                raise ValueError("Non-skill records expose only their indexed document")
            target = folder / str(relative)
            if not within(target.resolve(), folder) or target.resolve() != target.absolute() or is_link(target):
                raise ValueError("Resource link escapes the skill directory")
            metadata = json.loads(row["metadata"])
            decoding = metadata.get("_sklib", {})
            decoding = decoding.get("encoding", "auto") if isinstance(decoding, dict) else "auto"
            content, actual_encoding = read_text_info(target, encoding=decoding if encoding is None else encoding)
            revision = content_hash(content)
            if expected_revision and revision != expected_revision:
                raise OperationFailure("Resource changed since previous read", code="resource_changed",
                    recovery="清空已拼接的片段，从第 1 行读取当前版本，避免混合新旧正文。")
            lines = text_lines(content, keepends=True)
            if start_line > len(lines) + 1:
                raise ValueError("start_line is beyond end of file")
            chosen, size = [], 0
            for line in lines[start_line - 1:start_line - 1 + max_lines]:
                if size + len(line) > max_chars:
                    if not chosen:
                        raise ValueError("One line exceeds max_chars; increase the character budget")
                    break
                chosen.append(line)
                size += len(line)
            end = start_line - 1 + len(chosen)
            return {"id": document_id, "relative_path": relative.as_posix(), "content": "".join(chosen),
                    "start_line": start_line, "end_line": end, "total_lines": len(lines),
                    "next_start_line": end + 1 if end < len(lines) else None, "revision": revision,
                    "encoding": actual_encoding}

    def annotate(self, document_id: str, *, tags: list[str] | None = None, note: str | None = None,
                 favorite: bool | None = None, state: str | None = None, expected_annotation_revision: str | None = None) -> dict:
        validate_annotation(tags, note, favorite, state)
        with self.store.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            self._row(db, document_id)
            old = db.execute("SELECT * FROM annotations WHERE document_id=?", (document_id,)).fetchone()
            check_revision(document_id, old, expected_annotation_revision)
            values = annotation_values(old)
            for key, value in {"tags": tags, "note": note, "favorite": favorite, "state": state}.items():
                if value is not None:
                    values[key] = list(dict.fromkeys(tag.strip() for tag in value)) if key == "tags" else value
            timestamp = now()
            self._write_annotation(db, document_id, values, timestamp)
            db.execute("INSERT INTO events(created_at,action,details) VALUES(?,?,?)", (timestamp, "annotate", dumps({"id": document_id})))
            return {"id": document_id, **values, "updated_at": timestamp,
                    "annotation_revision": annotation_revision(document_id, {**values, "updated_at": timestamp})}

    def _write_annotation(self, db, identifier, values, timestamp):
        db.execute("INSERT OR REPLACE INTO annotations VALUES(?,?,?,?,?,?)", (
            identifier, dumps(values["tags"]), values["note"], int(values["favorite"]), values["state"], timestamp))
        refresh_fts(db, identifier, annotation_only=True)

    def annotate_batch(self, ids, *, tags=None, tag_mode="add", state=None, favorite=None, expected_revisions=None):
        if not isinstance(ids, list) or not 1 <= len(ids) <= 100 or any(not isinstance(identifier, str) or not 1 <= len(identifier) <= 128 for identifier in ids) or len(set(ids)) != len(ids):
            raise ValueError("ids must contain 1..100 distinct document ids")
        if not isinstance(tag_mode, str) or tag_mode not in {"add", "remove", "replace", "clear"}:
            raise ValueError("Unknown tag mode")
        validate_annotation(tags=tags, state=state, favorite=favorite)
        if tag_mode == "clear" and tags:
            raise ValueError("Clear mode does not accept tag values")
        if tags is None and tag_mode != "clear" and state is None and favorite is None:
            raise ValueError("At least one batch change is required")
        if expected_revisions is not None and (not isinstance(expected_revisions, dict) or set(expected_revisions) != set(ids)
                or any(not isinstance(value, str) or len(value) != 64 for value in expected_revisions.values())):
            raise ValueError("expected_revisions must cover exactly the selected ids")
        with self.store.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            changes = []
            for identifier in ids:
                if not db.execute("SELECT 1 FROM documents WHERE id=?", (identifier,)).fetchone():
                    raise OperationFailure("Selected entry is no longer indexed: " + identifier, code="entry_not_found", recovery="保留选择，重新读取选中记录；移除失效项后再提交。")
                old = db.execute("SELECT * FROM annotations WHERE document_id=?", (identifier,)).fetchone()
                if expected_revisions is not None:
                    check_revision(identifier, old, expected_revisions[identifier])
                original = annotation_values(old)
                values = {**original, "tags": list(original["tags"])}
                if tag_mode == "clear":
                    values["tags"] = []
                elif tags is not None:
                    normalized_tags = list(dict.fromkeys(tag.strip() for tag in tags))
                    values["tags"] = (list(dict.fromkeys([*values["tags"], *normalized_tags])) if tag_mode == "add" else
                        [tag for tag in values["tags"] if tag not in normalized_tags] if tag_mode == "remove" else normalized_tags)
                for key, value in (("state", state), ("favorite", favorite)):
                    if value is not None:
                        values[key] = value
                validate_annotation(**values)
                changes.append((identifier, original, values, old))
            timestamp, updated, entries = now(), 0, []
            for identifier, original, values, old in changes:
                changed = values != original
                if changed:
                    self._write_annotation(db, identifier, values, timestamp)
                    updated += 1
                version = annotation_revision(identifier, {**values, "updated_at": timestamp}) if changed else annotation_revision(identifier, old)
                entries.append({"id": identifier, "tags": values["tags"], "favorite": values["favorite"], "state": values["state"], "annotation_revision": version})
            result = {"selected": len(ids), "updated": updated, "unchanged": len(ids) - updated, "entries": entries}
            if updated:
                db.execute("INSERT INTO events(created_at,action,details) VALUES(?,?,?)", (timestamp, "annotate.batch",
                    dumps({"ids": ids, "updated": updated, "tag_mode": tag_mode, "tags": tags, "state": state, "favorite": favorite})))
            return result

    def annotation_states(self, ids):
        if not isinstance(ids, list) or not 1 <= len(ids) <= 100 or any(not isinstance(identifier, str) or not 1 <= len(identifier) <= 128 for identifier in ids) or len(set(ids)) != len(ids):
            raise ValueError("ids must contain 1..100 distinct document ids")
        with self.store.connect() as db:
            db.execute("BEGIN")
            rows = db.execute("SELECT d.id,d.name,d.path,a.tags,a.note,a.favorite,a.state,a.updated_at FROM documents d "
                "LEFT JOIN annotations a ON a.document_id=d.id WHERE d.id IN(" + ",".join("?" for _ in ids) + ")", ids).fetchall()
            by_id = {row["id"]: row for row in rows}
            missing = [identifier for identifier in ids if identifier not in by_id]
            if missing:
                raise OperationFailure("Selected entries are no longer indexed", code="entry_not_found",
                    recovery="从选择中移除失效条目，或恢复来源后重新读取。", progress={"missing_ids": missing})
            return {"entries": [{"id": identifier, "name": by_id[identifier]["name"], "path": by_id[identifier]["path"],
                **{key: value for key, value in annotation_values(by_id[identifier]).items() if key != "note"},
                "annotation_revision": annotation_revision(identifier, by_id[identifier])} for identifier in ids]}

    def snapshot(self) -> dict:
        """Portable review records, never source bodies, SQLite or model caches."""
        with self.store.connect() as db:
            db.execute("BEGIN")
            entries = []
            for row in db.execute("""SELECT d.*,a.tags,a.note,a.favorite,a.state FROM documents d
                                    LEFT JOIN annotations a ON a.document_id=d.id ORDER BY d.path"""):
                entries.append({"id": row["id"], "relative_path": row["relative_path"], "root": row["root"],
                                "kind": row["kind"], "name": row["name"], "revision": row["revision"],
                                "source": json.loads(row["source"]), "warnings": json.loads(row["warnings"]),
                                "tags": json.loads(row["tags"] or "[]"), "note": row["note"] or "",
                                "favorite": bool(row["favorite"]), "state": row["state"] or "unreviewed"})
            orphaned = [{"id": row["document_id"], "tags": json.loads(row["tags"]),
                         "note": row["note"], "favorite": bool(row["favorite"]), "state": row["state"]}
                        for row in db.execute("""SELECT a.* FROM annotations a LEFT JOIN documents d
                            ON d.id=a.document_id WHERE d.id IS NULL ORDER BY a.document_id""")]
            sources = [{"root": row["path"], "options": json.loads(row["last_report"]).get("options", {})}
                       for row in db.execute("SELECT path,last_report FROM roots ORDER BY path")]
            return {"schema_version": 1, "entries": entries, "orphaned_annotations": orphaned, "sources": sources}

    def history(self, limit: int = 30) -> list[dict]:
        if not 1 <= limit <= 200:
            raise ValueError("History limit must be 1..200")
        with self.store.connect() as db:
            return [{**dict(row), "details": json.loads(row["details"])} for row in db.execute(
                "SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))]
