"""Explicit, local Git history for review records. Never pushes or commits sources."""
from __future__ import annotations

import json
import difflib
import hashlib
import os
import subprocess
import tempfile
import sqlite3
from pathlib import Path

from .indexer import is_link, now
from .gitutil import environment as git_environment
from .locking import exclusive
from .storage import dumps
from .failures import OperationFailure, failure_details

GIT_OPERATIONS = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply")


class Records:
    def __init__(self, library):
        self.library = library
        self.directory = library.store.home / "records"
        self.catalog = self.directory / "catalog.json"
        self.lock = library.store.home / "records.lock"

    def _check_paths(self) -> None:
        if self.directory.is_symlink() or self.directory.resolve() != self.directory.absolute():
            raise ValueError("Records directory must not be a link")
        if self.catalog.is_symlink():
            raise ValueError("Catalog must not be a link")
        git_directory = self.directory / ".git"
        if git_directory.exists() and is_link(git_directory):
            raise ValueError("Records Git metadata must not be a link")

    def export(self) -> dict:
        with exclusive(self.lock):
            return self._export(self._snapshot_bytes())

    def _snapshot_bytes(self) -> bytes:
        return (json.dumps(self.library.snapshot(), ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")

    def _export(self, data: bytes) -> dict:
        self._check_paths()
        self.directory.mkdir(parents=True, exist_ok=True)
        if self.catalog.exists() and self.catalog.read_bytes() == data:
            return {"path": str(self.catalog), "changed": False}
        fd, temporary = tempfile.mkstemp(prefix=".catalog-", dir=self.directory)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.catalog)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return {"path": str(self.catalog), "changed": True}

    def _git(self, *args: str, check: bool = True) -> str:
        self._check_paths()
        try:
            result = subprocess.run(["git", "-C", str(self.directory), *args], capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=30, env=git_environment())
        except subprocess.TimeoutExpired as exc:
            raise OperationFailure("Git timed out; inspect record status/history before retrying",
                code="git_outcome_unknown", outcome="unknown",
                recovery="先检查 records log 和记录仓库的 Git 状态，确认提交是否已完成，再决定下一步；不要直接重复提交。") from exc
        if check and result.returncode:
            message = result.stderr.strip() or result.stdout.strip() or "Git command failed"
            if args and args[0] == "commit":
                raise OperationFailure(message, code="git_commit_failed", outcome="unknown",
                    recovery="先查看 records log 与记录仓库的 Git 状态。catalog.json 可能已暂存；修正身份、钩子或锁问题后重新预览。")
            raise ValueError(message)
        return result.stdout.strip()

    def _repository(self) -> None:
        self._check_paths()
        if not (self.directory / ".git").is_dir():
            raise OperationFailure("Records Git repository is not initialized; run records init", code="records_not_initialized",
                recovery="运行 records init 或点击初始化记录仓库，再生成预览。")
        actual = self._git("rev-parse", "--show-toplevel")
        if Path(actual).resolve() != self.directory.resolve():
            raise ValueError("Refusing to operate on a parent/source Git repository")

    def init(self) -> dict:
        with exclusive(self.lock):
            return self._init()

    def _init(self) -> dict:
        self._check_paths()
        self.directory.mkdir(parents=True, exist_ok=True)
        if not (self.directory / ".git").exists():
            self._git("init")
        self._repository()
        return {"repository": str(self.directory), "initialized": True}

    def preview(self) -> dict:
        with exclusive(self.lock):
            self._repository()
            return self._preview(self._snapshot_bytes())

    def _preview_token(self, data: bytes) -> str:
        head = self._git("rev-parse", "--verify", "HEAD", check=False)
        return hashlib.sha256(data + b"\0" + head.encode("utf-8")).hexdigest()

    def _preview(self, data: bytes) -> dict:
        self._repository()
        export = self._export(data)
        head_exists = bool(self._git("rev-parse", "--verify", "HEAD", check=False))
        if head_exists:
            previous = self._git("show", "HEAD:catalog.json", check=False)
            changed = previous + "\n" != data.decode("utf-8")
            if previous:
                diff = self._git("diff", "--no-ext-diff", "--no-textconv", "HEAD", "--", "catalog.json")
            else:
                diff = "".join(difflib.unified_diff([], data.decode("utf-8").splitlines(keepends=True),
                                                 fromfile="HEAD/catalog.json", tofile="catalog.json"))
        else:
            changed = True
            diff = "".join(difflib.unified_diff([], data.decode("utf-8").splitlines(keepends=True),
                                             fromfile="HEAD/catalog.json", tofile="catalog.json"))
        return {**export, "repository": str(self.directory), "pending_changes": changed,
                "diff": diff[:100000], "diff_truncated": len(diff) > 100000,
                "status": self._git("status", "--short"), "committed_files": ["catalog.json"],
                "preview_token": self._preview_token(data)}

    def commit(self, message: str, expected_preview: str | None = None) -> dict:
        if not isinstance(message, str) or not message.strip() or len(message) > 1000 or "\x00" in message:
            raise ValueError("Commit message must contain 1..1000 characters")
        if expected_preview is not None and (not isinstance(expected_preview, str) or len(expected_preview) != 64):
            raise ValueError("Invalid preview token")
        with exclusive(self.lock):
            return self._commit(message, expected_preview)

    def _commit(self, message: str, expected_preview: str | None) -> dict:
        self._repository()
        # Refuse in-progress operations; never finish someone else's merge/rebase.
        for marker in GIT_OPERATIONS:
            if (self.directory / ".git" / marker).exists():
                raise OperationFailure("Records repository has an in-progress Git operation", code="git_operation_pending",
                    recovery="先人工检查并处理记录仓库中未完成的 Git 操作，再检查状态和生成新预览。")
        data = self._snapshot_bytes()
        if expected_preview is not None and expected_preview != self._preview_token(data):
            raise OperationFailure("Records or Git HEAD changed since preview; generate a new preview before committing",
                code="preview_stale", recovery="记录或 Git HEAD 已改变。重新生成预览、核对内容后再提交。")
        preview = self._preview(data)
        if not preview["pending_changes"]:
            return {"committed": False, "reason": "Records are unchanged"}
        # --only commits this managed file and preserves unrelated staged files.
        self._git("add", "--", "catalog.json")
        self._git("commit", "--only", "-m", message.strip(), "--", "catalog.json")
        try:
            revision = self._git("rev-parse", "HEAD")
        except (ValueError, OSError) as exc:
            raise OperationFailure("Git commit completed but its revision could not be read", code="git_outcome_unknown",
                outcome="unknown", recovery="提交命令已成功。先查看 records log / Git HEAD，确认提交后再继续。") from exc
        result = {"committed": True, "commit": revision, "repository": str(self.directory), "files": ["catalog.json"]}
        try:
            with self.library.store.connect() as db:
                db.execute("INSERT INTO events(created_at,action,details) VALUES(?,?,?)", (now(), "records.commit", dumps(result)))
        except (sqlite3.Error, OSError, ValueError) as exc:
            result["warnings"] = [{**failure_details(exc, "records.activity"), "code": "activity_log_failed",
                "outcome": "completed", "recovery": "Git 提交已经完成，活动日志写入失败。保留返回的提交号，无需重新提交。"}]
        return result

    def status(self) -> dict:
        """Inspect Git even if the application DB is unavailable; never export."""
        with exclusive(self.lock):
            self._repository()
            return {"repository": str(self.directory), "head": self._git("rev-parse", "--verify", "HEAD", check=False) or None,
                    "status": self._git("status", "--short"),
                    "in_progress": [marker for marker in GIT_OPERATIONS if (self.directory / ".git" / marker).exists()]}

    def log(self, limit: int = 20) -> dict:
        if not 1 <= limit <= 100:
            raise ValueError("Log limit must be 1..100")
        with exclusive(self.lock):
            return self._log(limit)

    def _log(self, limit: int) -> dict:
        self._repository()
        if not self._git("rev-parse", "--verify", "HEAD", check=False):
            return {"commits": []}
        text = self._git("log", f"-{limit}", "--format=%H%x00%aI%x00%s")
        return {"commits": [dict(zip(("commit", "date", "message"), line.split("\x00", 2))) for line in text.split("\n")]}
