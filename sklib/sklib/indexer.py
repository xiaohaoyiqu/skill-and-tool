"""Bounded, incremental source indexing. Source directories are never written."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import stat as stat_module
import subprocess
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import yaml

from .gitutil import environment as git_environment
from .files import MAX_BYTES, DOCUMENT_SUFFIXES, is_readme, read_text_info, validate_encoding
from .projects import parser_signature, parse_project, project_type
from .failures import OperationFailure, failure_details
from .storage import Store, advance_source_epoch, dumps, source_epoch
from .text import content_hash, tokens

EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", "target", "dist", "build",
            ".sklib", ".zvec-grep", ".pytest_cache", ".cache", ".next", ".nuxt", ".tox",
            ".mypy_cache", ".ruff_cache", "coverage", "fixtures", "__fixtures__", "tests", "test",
            "bin", "obj", "vendor", ".gradle", ".dart_tool", ".pub-cache", ".swiftpm", ".build",
            ".idea", ".vs", ".svn", ".hg", ".terraform", "Pods", "DerivedData", ".audit-client"}


EXCLUDED_NORMALIZED = {os.path.normcase(value) for value in EXCLUDED}


def excluded_name(name: str) -> bool:
    return os.path.normcase(name) in EXCLUDED_NORMALIZED


def candidate_kind(name: str, directory: Path, root: Path, *, has_project: bool,
                   is_repository: bool, include_docs: bool) -> str | None:
    if name.lower() == "skill.md":
        return "skill"
    if project_type(name) or is_readme(name) and (
            directory == root or directory.parent == root or is_repository or has_project):
        return "project"
    return "document" if include_docs and Path(name).suffix.lower() in DOCUMENT_SUFFIXES else None


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def is_link(path: Path) -> bool:
    """One lstat detects POSIX links and Windows junctions/reparse points.

    Resolving every directory recursively costs many filesystem lookups on
    Windows; the directory itself exposes whether traversal would follow a link.
    """
    info = path.lstat()
    return stat_module.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat_module, "FILE_ATTRIBUTE_REPARSE_POINT", 1024))


def read_text(path: Path, max_bytes: int = MAX_BYTES, *, encoding: str = "auto") -> str:
    return read_text_info(path, max_bytes, encoding=encoding)[0]


def parse_skill(content: str, dirname: str) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    metadata: dict = {}
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            warnings.append("Unclosed YAML frontmatter")
        else:
            try:
                # SafeLoader avoids constructors; aliases are rejected to bound expansion.
                header = "\n".join(lines[1:end])
                if len(header) > 65536:
                    raise ValueError("Frontmatter exceeds 64 KiB")
                if any(isinstance(t, yaml.tokens.AliasToken) for t in yaml.scan(header)):
                    raise ValueError("YAML aliases are not supported")
                parsed = yaml.safe_load(header)
                if not isinstance(parsed, dict):
                    raise ValueError("Frontmatter must be a mapping")
                encoded = json.dumps(parsed, ensure_ascii=False, default=str, allow_nan=False)
                encoded.encode("utf-8")  # Reject lone surrogate escapes in YAML strings.
                metadata = json.loads(encoded)
            except (yaml.YAMLError, ValueError, TypeError, UnicodeError, RecursionError) as exc:
                warnings.append("Invalid YAML frontmatter: " + str(exc)[:240])
    else:
        warnings.append("Missing YAML frontmatter")
    for field in ("name", "description"):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            warnings.append(f"Missing or non-string {field}")
            metadata[field] = dirname if field == "name" else ""
    if metadata["name"] != dirname:
        warnings.append("Declared name differs from directory name")
    return metadata, warnings


def git_info(directory: Path, cancelled=None) -> dict:
    def run(*args: str) -> str:
        check_cancel(cancelled)
        try:
            result = subprocess.run(["git", "-C", str(directory), *args], capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=5, env=git_environment())
            return result.stdout.strip() if result.returncode == 0 else ""
        except (OSError, subprocess.TimeoutExpired):
            return ""
    remote = run("remote", "get-url", "origin")
    if "://" in remote:
        try:
            parsed = urllib.parse.urlsplit(remote)
            hostname = parsed.hostname or ""
            if ":" in hostname:
                hostname = "[" + hostname + "]"
            remote = urllib.parse.urlunsplit((parsed.scheme, hostname + (":" + str(parsed.port) if parsed.port else ""), parsed.path, "", ""))
        except ValueError:
            remote = "[invalid remote URL]"
    return {"repository": str(directory), "remote": remote,
            "commit": run("rev-parse", "HEAD"), "branch": run("branch", "--show-current")}


def check_cancel(cancelled) -> None:
    if cancelled and cancelled():
        raise OperationFailure("Index scan cancelled before commit", code="cancelled", outcome="unchanged",
            recovery="本轮未提交的索引已回滚，已有资料与笔记保留。需要时重新发起扫描。")


def refresh_fts(db, document_id: str, *, annotation_only: bool = False) -> None:
    columns = "rowid AS fts_rowid" if annotation_only else "rowid AS fts_rowid,*"
    row = db.execute(f"SELECT {columns} FROM documents WHERE id=?", (document_id,)).fetchone()
    if row is None:
        return
    annotation = db.execute("SELECT * FROM annotations WHERE document_id=?", (document_id,)).fetchone()
    extra = "" if annotation is None else " ".join(json.loads(annotation["tags"])) + " " + annotation["note"]
    if annotation_only:
        if db.execute("SELECT rowid FROM documents_fts WHERE rowid=?", (row["fts_rowid"],)).fetchone():
            db.execute("UPDATE documents_fts SET annotation=? WHERE rowid=?", (" ".join(tokens(extra)), row["fts_rowid"]))
            return
        # A missing row can be rebuilt from the authoritative document.
        refresh_fts(db, document_id)
        return
    # FTS5 does not index UNINDEXED document_id. Deleting by that field scans
    # every stored document on each insertion (quadratic over a large import).
    db.execute("DELETE FROM documents_fts WHERE rowid=?", (row["fts_rowid"],))
    db.execute("INSERT INTO documents_fts(rowid,document_id,name,description,body,annotation) VALUES(?,?,?,?,?,?)", (
        row["fts_rowid"], document_id, " ".join(tokens(row["name"] + " " + row["title"])),
        " ".join(tokens(row["description"])), " ".join(tokens(row["body"])), " ".join(tokens(extra))))


def index_root(store: Store, root: str | Path, *, verify: bool = False,
               include_docs: bool | None = None, max_files: int | None = None, max_depth: int | None = None,
               exclude: tuple[str, ...] | None = None, encoding: str | None = None,
               progress: Callable[[dict], None] | None = None,
               cancelled: Callable[[], bool] | None = None, expected_source_epoch: int | None = None) -> dict:
    check_cancel(cancelled)
    root = Path(root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Index root must be a directory")
    if within(root, store.home):
        raise ValueError("Cannot index the application's state directory")
    with store.connect() as db:
        expected_epoch = source_epoch(db, str(root))
        if expected_source_epoch is not None and expected_epoch != expected_source_epoch:
            raise OperationFailure("Source changed after this scan was queued", code="source_conflict", retryable=True,
                recovery="来源在排队后被移除或重新扫描。本任务没有写入；确认最新状态后手动重新发起。")
        prior_root = db.execute("SELECT last_report FROM roots WHERE path=?", (str(root),)).fetchone()
    previous_report = json.loads(prior_root[0]) if prior_root else {}
    previous_options = previous_report.get("options", {})
    include_docs = previous_options.get("include_docs", False) if include_docs is None else include_docs
    max_files = previous_options.get("max_files", 100000) if max_files is None else max_files
    max_depth = previous_options.get("max_depth", 30) if max_depth is None else max_depth
    exclude = previous_options.get("exclude", []) if exclude is None else exclude
    encoding = validate_encoding(previous_options.get("encoding", "auto") if encoding is None else encoding)
    if type(verify) is not bool or type(include_docs) is not bool:
        raise ValueError("verify and include_docs must be boolean")
    if not isinstance(exclude, (tuple, list)) or any(not isinstance(name, str) or not name or name in {".", ".."} or any(char in name for char in "/\\:") for name in exclude):
        raise ValueError("exclude must contain directory names")
    if type(max_files) is not int or type(max_depth) is not int or not 1 <= max_files <= 1000000 or not 1 <= max_depth <= 100:
        raise ValueError("Invalid scan limits")
    options = {"include_docs": include_docs, "max_files": max_files, "max_depth": max_depth,
               "exclude": sorted(set(exclude)), "encoding": encoding}
    signature = parser_signature()
    force_parse = previous_options.get("encoding") != encoding or previous_report.get("parser_version") != signature
    report = {"root": str(root), "added": 0, "updated": 0, "unchanged": 0,
              "removed": 0, "errors": [], "warnings": [], "files_examined": 0, "complete": True,
              "options": options, "parser_version": signature, "failures": [], "failure_count": 0,
              "errors_truncated": False}
    candidates: list[tuple[Path, str, os.stat_result]] = []
    seen: set[str] = set()
    repositories: dict[Path, dict] = {}
    errors: list[str] = report["errors"]
    excluded = {os.path.normcase(value) for value in EXCLUDED | set(exclude)}
    if progress:
        progress({"phase": "scan", "files_examined": 0})
    last_progress = time.monotonic()

    def onerror(exc: Exception, path=None, phase="scan") -> None:
        report["failure_count"] += 1
        if len(errors) < 200:
            errors.append(str(exc))
            report["failures"].append({**failure_details(exc, "index." + phase),
                "path": str(path or getattr(exc, "filename", "") or root), "outcome": "partial"})
        else:
            report["errors_truncated"] = True
        report["complete"] = False

    for base, dirs, files in os.walk(root, followlinks=False, onerror=onerror):
        check_cancel(cancelled)
        directory = Path(base)
        depth = len(directory.relative_to(root).parts)
        kept = []
        for name in sorted(dirs):
            check_cancel(cancelled)
            child = directory / name
            # Reparse attributes also identify Windows junctions.
            if os.path.normcase(name) in excluded:
                continue
            try:
                if is_link(child) or child == store.home:
                    continue
            except OSError as exc:
                onerror(exc)
                continue
            if depth >= max_depth:
                onerror(OperationFailure("Directory depth limit reached", code="scan_depth_limit",
                    recovery="提高 max_depth 后重新扫描；本次保留未确认缺失的旧条目。"), child)
                continue
            kept.append(name)
        dirs[:] = kept
        if (directory / ".git").exists():
            repositories[directory] = git_info(directory, cancelled) if cancelled else git_info(directory)
        has_project = any(project_type(name) for name in files)
        for name in sorted(files):
            check_cancel(cancelled)
            report["files_examined"] += 1
            if progress and (report["files_examined"] % 2000 == 0 or time.monotonic() - last_progress >= .5):
                progress({"phase": "scan", "files_examined": report["files_examined"], "candidates": len(candidates)})
                last_progress = time.monotonic()
            if report["files_examined"] > max_files:
                raise OperationFailure("Scan file limit reached; index was not changed. Increase --max-files.",
                    code="scan_file_limit", recovery="提高 --max-files 或缩小来源目录后重新扫描。本次索引未改变。")
            path = directory / name
            kind = candidate_kind(name, directory, root, has_project=has_project,
                                  is_repository=directory in repositories, include_docs=include_docs)
            if kind is None:
                continue
            try:
                if is_link(path):
                    continue
            except OSError as exc:
                onerror(exc, path)
                continue
            # root was resolved once; every ancestor was walked without links.
            # File names originate from scandir, so no per-file ancestor resolve
            # is needed to establish the lexical containment of this candidate.
            seen.add(str(path))
            try:
                stat = path.stat()
                if stat.st_size > MAX_BYTES:
                    raise OperationFailure("File exceeds 2 MiB", code="file_too_large",
                        recovery="文件超过读取上限。先在外部处理为较小的文本资料，再重新扫描。")
                candidates.append((path, kind, stat))
            except (OSError, ValueError) as exc:
                onerror(exc, path)

    check_cancel(cancelled)
    with store.connect() as db:
        db.execute("BEGIN IMMEDIATE")
        check_cancel(cancelled)
        if source_epoch(db, str(root)) != expected_epoch:
            raise OperationFailure("Source changed in the library during this scan; retry indexing",
                code="source_conflict", retryable=True, recovery="等待同一来源的其他操作完成，再重新扫描。")
        if progress:
            progress({"phase": "index", "candidates": len(candidates), "processed": 0, "files_examined": report["files_examined"]})
        last_progress = time.monotonic()
        # Overlapping roots make source ownership and pruning ambiguous.
        for registered in db.execute("SELECT path FROM roots"):
            other = Path(registered[0])
            if other != root and (within(root, other) or within(other, root)):
                raise ValueError(f"Root overlaps an existing root: {other}")
        previous = {r["path"]: r for r in db.execute("SELECT rowid AS fts_rowid,* FROM documents WHERE root=?", (str(root),))}
        for position, (path, kind, stat) in enumerate(candidates):
            check_cancel(cancelled)
            if progress and position and (position % 100 == 0 or time.monotonic() - last_progress >= .5):
                progress({"phase": "index", "candidates": len(candidates), "processed": position,
                          "files_examined": report["files_examined"], "added": report["added"],
                          "updated": report["updated"], "unchanged": report["unchanged"]})
                last_progress = time.monotonic()
                check_cancel(cancelled)
            prior = previous.get(str(path))
            repo_dirs = [p for p in repositories if within(path, p)]
            repo_dir = max(repo_dirs, key=lambda p: len(p.parts)) if repo_dirs else None
            source = repositories[repo_dir] if repo_dir else {}
            project = str(repo_dir) if repo_dir else str(root / path.relative_to(root).parts[0]) if len(path.relative_to(root).parts) > 1 else str(root)
            prior_decoding = json.loads(prior["metadata"]).get("_sklib", {}) if prior else {}
            prior_decoding = prior_decoding.get("encoding", "auto") if isinstance(prior_decoding, dict) else "auto"
            if prior and not verify and not force_parse and prior_decoding == encoding and prior["kind"] == kind and prior["project"] == project and prior["size"] == stat.st_size and prior["mtime_ns"] == stat.st_mtime_ns:
                # Provenance can change with a checkout even if the file did not.
                db.execute("UPDATE documents SET source=? WHERE id=?", (dumps(source), prior["id"]))
                report["unchanged"] += 1
                continue
            db.execute("SAVEPOINT index_item")
            try:
                body = read_text(path, encoding=encoding)
                metadata, warnings = (parse_skill(body, path.parent.name) if kind == "skill" else
                                      parse_project(body, path) if project_type(path.name) else ({}, []))
                metadata["_sklib"] = {"encoding": encoding}
                if kind == "skill" and path.name != "SKILL.md":
                    warnings.append("Nonstandard skill filename; prefer SKILL.md for agent compatibility")
                revision = content_hash(body)
                relative = path.relative_to(root).as_posix()
                identity = os.path.normcase(str(root)) + "/" + os.path.normcase(relative)
                document_id = "s_" + content_hash(identity)[:24]
                title_match = re.search(r"^#\s+(.+)$", body, re.M)
                title = title_match[1].strip() if title_match else metadata.get("name", path.parent.name)
                name = metadata.get("name", path.parent.name)
                description = metadata.get("description") or (" ".join(metadata.get("project_types", [])) + " project: " + path.name if project_type(path.name) else title)
                values = (document_id, str(root), relative, str(path), kind, name, title, description,
                          body, revision, stat.st_size, stat.st_mtime_ns, dumps(source), project,
                          dumps(metadata), dumps(warnings), now())
                db.execute("""INSERT INTO documents VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(id) DO UPDATE SET name=excluded.name,title=excluded.title,
                    description=excluded.description,body=excluded.body,revision=excluded.revision,
                    size=excluded.size,mtime_ns=excluded.mtime_ns,source=excluded.source,
                    project=excluded.project,metadata=excluded.metadata,warnings=excluded.warnings,
                    indexed_at=excluded.indexed_at,kind=excluded.kind""", values)
                refresh_fts(db, document_id)
                db.execute("RELEASE index_item")
                if prior is None:
                    report["added"] += 1
                elif prior["revision"] != revision:
                    report["updated"] += 1
                else:
                    report["unchanged"] += 1
            except (OSError, ValueError, UnicodeError, RecursionError) as exc:
                db.execute("ROLLBACK TO index_item")
                db.execute("RELEASE index_item")
                onerror(exc, path, "file")
                if len(report["warnings"]) < 200:
                    report["warnings"].append({"path": str(path), "message": str(exc)[:240]})
        if report["complete"]:
            for path, prior in previous.items():
                check_cancel(cancelled)
                if path not in seen:
                    db.execute("DELETE FROM documents WHERE id=?", (prior["id"],))
                    db.execute("DELETE FROM documents_fts WHERE rowid=?", (prior["fts_rowid"],))
                    db.execute("DELETE FROM vectors WHERE document_id=?", (prior["id"],))
                    report["removed"] += 1
        db.execute("INSERT INTO roots VALUES(?,?,?) ON CONFLICT(path) DO UPDATE SET scanned_at=excluded.scanned_at,last_report=excluded.last_report",
                   (str(root), now(), dumps(report)))
        advance_source_epoch(db, str(root))
        db.execute("INSERT INTO events(created_at,action,details) VALUES(?,?,?)", (now(), "index", dumps(report)))
        check_cancel(cancelled)
    if progress:
        try:
            progress({"phase": "complete", "added": report["added"], "updated": report["updated"], "unchanged": report["unchanged"],
                      "files_examined": report["files_examined"], "candidates": len(candidates), "processed": len(candidates)})
        except KeyboardInterrupt as exc:
            exc.outcome = "completed"
            raise
        except (OSError, ValueError, sqlite3.Error) as exc:
            # The commit already succeeded. A failing progress sink cannot undo it.
            report["progress_warning"] = {**failure_details(exc, "index.progress"), "outcome": "completed",
                "recovery": "索引已提交，进度通知失败。检查 status 即可，无需因此重复扫描。"}
    return report
