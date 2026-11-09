"""Bounded read-only source change detection using the indexer's discovery rules."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import stat
import time

from .failures import OperationFailure, failure_details
from .files import MAX_BYTES, read_text_info
from .indexer import EXCLUDED, candidate_kind, is_link, now, within
from .projects import parser_signature, project_type
from .storage import source_epoch, dumps
from .text import content_hash


def registered_source(db, root):
    requested = os.path.normcase(os.path.abspath(os.path.expanduser(str(root))))
    roots = list(db.execute("SELECT * FROM roots"))
    registered = next((row for row in roots if os.path.normcase(row["path"]) == requested), None)
    if registered is None:
        # Expand Windows 8.3 aliases without accepting a replaced junction as
        # another registered source. Exact registered names never resolve links.
        alias = Path(root).expanduser().absolute()
        try:
            linked = any(is_link(part) for part in (alias, *alias.parents) if os.path.lexists(part))
            if not linked:
                resolved = os.path.normcase(str(alias.resolve()))
                registered = next((row for row in roots if os.path.normcase(row["path"]) == resolved), None)
        except (OSError, RuntimeError):
            pass
    return registered


def check_source(library, root: str, *, verify: bool = False, max_changes: int = 20, cancelled=None) -> dict:
    if not isinstance(root, str) or not root.strip() or len(root) > 32768 or type(verify) is not bool:
        raise ValueError("A registered root and boolean verify are required")
    if type(max_changes) is not int or not 1 <= max_changes <= 100:
        raise ValueError("max_changes must be 1..100")
    # Match the registered lexical path first: resolving a replaced junction
    # would silently turn this into a check of a different directory.
    with library.store.connect() as db:
        db.execute("BEGIN")
        registered = registered_source(db, root)
        if registered is None:
            raise OperationFailure("Source is not registered", code="source_not_found",
                recovery="重新读取来源列表，选择已登记的目录；新目录应先扫描。")
        directory = Path(registered["path"])
        report = json.loads(registered["last_report"])
        epoch = source_epoch(db, str(directory))
        previous = {row["path"]: dict(row) for row in db.execute(
            "SELECT path,kind,size,mtime_ns,revision FROM documents WHERE root=?", (str(directory),))}
    options = report.get("options", {})
    fingerprint = hashlib.sha256(dumps({"options": options, "parser": parser_signature()}).encode("utf-8"))
    started = time.perf_counter()
    result = {"root": str(directory), "checked_at": now(), "verify": verify, "complete": True,
        "state": "clean", "added": 0, "modified": 0, "removed": 0, "files_examined": 0,
        "changes": [], "changes_truncated": False, "failures": [], "failure_count": 0,
        "requires_reindex": report.get("parser_version") != parser_signature() or not report.get("complete", False),
        "source_epoch": epoch, "refresh_job": None}
    def fail(exc, path=None):
        result["complete"] = False
        result["failure_count"] += 1
        if len(result["failures"]) < 20:
            result["failures"].append({**failure_details(exc, "source.check"), "path": str(path or directory)})
    def changed(kind, path):
        result[kind] += 1
        if len(result["changes"]) < max_changes:
            result["changes"].append({"change": kind, "path": str(path)})
        else:
            result["changes_truncated"] = True
    def check_cancel():
        if cancelled and cancelled():
            raise OperationFailure("Source check cancelled", code="cancelled", recovery="来源检查未修改索引，必要时重新检测。")
    seen = set()
    try:
        check_cancel()
        if is_link(directory) or directory.resolve() != directory.absolute():
            raise ValueError("Registered source became a link")
        if not directory.is_dir():
            raise FileNotFoundError(str(directory))
        excluded = {os.path.normcase(value) for value in EXCLUDED | set(options.get("exclude", []))}
        for base, dirs, files in os.walk(directory, followlinks=False, onerror=fail):
            check_cancel()
            current = Path(base)
            depth = len(current.relative_to(directory).parts)
            kept = []
            for name in sorted(dirs):
                if os.path.normcase(name) in excluded:
                    continue
                child = current / name
                try:
                    if is_link(child) or within(child, library.store.home):
                        continue
                    if depth >= options.get("max_depth", 30):
                        raise OperationFailure("Directory depth limit reached", code="scan_depth_limit",
                            recovery="提高来源的 max_depth 后重新扫描；本次检查不能确认所有未见条目已删除。")
                    kept.append(name)
                except OSError as exc:
                    fail(exc, child)
                except ValueError as exc:
                    fail(exc, child)
            dirs[:] = kept
            has_project = any(project_type(name) for name in files)
            is_repository = (current / ".git").exists()
            for name in sorted(files):
                check_cancel()
                result["files_examined"] += 1
                if result["files_examined"] > options.get("max_files", 100000):
                    raise OperationFailure("Source check file limit reached", code="scan_file_limit",
                        recovery="提高来源扫描上限或缩小目录后重新检测；本次不会推断未见条目已删除。")
                kind = candidate_kind(name, current, directory, has_project=has_project,
                    is_repository=is_repository, include_docs=options.get("include_docs", False))
                if kind is None:
                    continue
                path = current / name
                try:
                    if is_link(path):
                        continue
                    info = path.stat()
                    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                        raise ValueError("Source candidate is not a regular text file within 2 MiB")
                    seen.add(str(path))
                    fingerprint.update(dumps([str(path), kind, info.st_size, info.st_mtime_ns]).encode("utf-8"))
                    current_hash = content_hash(read_text_info(path, encoding=options.get("encoding", "auto"))[0]) if verify else None
                    if current_hash:
                        fingerprint.update(current_hash.encode("ascii"))
                    old = previous.get(str(path))
                    if old is None:
                        changed("added", path)
                    elif old["kind"] != kind or old["size"] != info.st_size or old["mtime_ns"] != info.st_mtime_ns:
                        changed("modified", path)
                    elif verify and current_hash != old["revision"]:
                        changed("modified", path)
                except (OSError, ValueError) as exc:
                    fail(exc, path)
        if result["complete"]:
            for path in sorted(previous.keys() - seen):
                changed("removed", path)
    except OperationFailure as exc:
        if exc.code == "cancelled":
            raise
        fail(exc)
    except (OSError, ValueError) as exc:
        fail(exc)
    with library.store.connect() as db:
        if source_epoch(db, str(directory)) != epoch:
            result["stale"] = True
            fail(OperationFailure("Source changed during check", code="source_conflict", retryable=True,
                recovery="来源在检测期间已重扫或移除；重新读取来源列表再检测。"))
    dirty = result["requires_reindex"] or any(result[key] for key in ("added", "modified", "removed"))
    result["state"] = "attention" if not result["complete"] else "changed" if dirty else "clean"
    result["change_token"] = fingerprint.hexdigest()
    result["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 2)
    return result
