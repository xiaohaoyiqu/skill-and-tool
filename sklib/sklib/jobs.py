"""Durable index job records and one cooperative worker per application home.

Job status uses its own SQLite database so it remains readable while indexing
holds a write transaction. Restarted jobs are reported, never automatically run.
"""
from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
from queue import Queue, Empty
import re
import sqlite3
import threading
import uuid

from .failures import OperationFailure, failure_details
from .indexer import now, within
from .locking import exclusive
from .storage import dumps, source_epoch

ACTIVE = ("queued", "running", "cancelling")
OPTIONS = {"verify", "include_docs", "max_files", "max_depth", "exclude", "encoding"}


class IndexJobs:
    def __init__(self, library):
        self.library = library
        self.path = library.store.home / "jobs.sqlite3"
        self.guard = threading.RLock()
        self.stopping = threading.Event()
        self.queue = Queue()
        self.cancellations = {}
        self.fallback = {}
        self.lease = exclusive(library.store.home / "jobs.lock", timeout=0)
        try:
            self.lease.__enter__()
        except OperationFailure as exc:
            raise OperationFailure("This library already has an active UI job worker", code="jobs_busy",
                recovery="使用已启动的界面，或关闭它后再启动同一状态目录的服务；不要删除锁文件。") from exc
        try:
            with self.connect() as db:
                db.execute("PRAGMA journal_mode=WAL")
                version = db.execute("PRAGMA user_version").fetchone()[0]
                if version not in (0, 1):
                    raise ValueError(f"Unsupported job database schema {version}")
                db.execute("""CREATE TABLE IF NOT EXISTS jobs(
                    id TEXT PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, root TEXT NOT NULL, options TEXT NOT NULL,
                    state TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                    progress TEXT NOT NULL, report TEXT, error TEXT, cancel_requested INTEGER NOT NULL DEFAULT 0)""")
                db.execute("PRAGMA user_version=1")
                detail = failure_details(OperationFailure("Service stopped before the job outcome was recorded",
                    code="job_interrupted", outcome="unknown", recovery="先检查来源的最近扫描报告，确认是否已提交；需要时手动重新扫描，不会自动重放。"), "index.job")
                db.execute("UPDATE jobs SET state='interrupted',error=?,updated_at=? WHERE state IN('queued','running','cancelling')",
                           (dumps(detail), now()))
            self.worker = threading.Thread(target=self.run, name="sklib-index-worker", daemon=True)
            self.worker.start()
        except BaseException:
            self.lease.__exit__(None, None, None)
            raise

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=3)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def decode(row):
        value = dict(row)
        for key in ("options", "progress", "report", "error"):
            value[key] = json.loads(value[key]) if value[key] else None
        value["cancel_requested"] = bool(value["cancel_requested"])
        return value

    def get(self, identifier):
        if not isinstance(identifier, str) or not re.fullmatch(r"[0-9a-f]{32}", identifier):
            raise ValueError("A valid job id is required")
        with self.guard:
            if identifier in self.fallback:
                return dict(self.fallback[identifier])
            with self.connect() as db:
                row = db.execute("SELECT * FROM jobs WHERE id=?", (identifier,)).fetchone()
            if row is None:
                raise OperationFailure("Unknown index job", code="job_not_found",
                    recovery="刷新扫描任务列表。历史仅保留最近 200 个已结束任务。")
            return self.decode(row)

    def list(self):
        with self.guard:
            with self.connect() as db:
                rows = db.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT 30").fetchall()
            return {"jobs": [dict(self.fallback.get(row["id"], self.decode(row))) for row in rows]}

    def submit(self, root, options=None, request_id=None, *, expected_source_epoch=None):
        if not isinstance(root, str) or not root.strip():
            raise ValueError("A source directory is required")
        directory = Path(root).expanduser().resolve(strict=True)
        if expected_source_epoch is not None and (type(expected_source_epoch) is not int
                or directory != Path(root).expanduser().absolute()):
            raise OperationFailure("Source path changed after detection", code="source_conflict", retryable=True,
                recovery="来源路径在检测后发生变化。重新读取来源列表并检测，不会自动收录链接目标。")
        if not directory.is_dir() or within(directory, self.library.store.home):
            raise ValueError("A source directory outside application state is required")
        options = {} if options is None else options
        if not isinstance(options, dict) or set(options) - OPTIONS:
            raise ValueError("Unknown index options")
        request_id = uuid.uuid4().hex if request_id is None else request_id
        if not isinstance(request_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", request_id):
            raise ValueError("request_id must contain 1..80 letters, digits, underscores or hyphens")
        with self.guard:
            if self.stopping.is_set() or not self.worker.is_alive():
                raise OperationFailure("Index worker is stopping", code="jobs_stopping", recovery="等待服务停止后重新启动；先检查现有扫描任务。")
            with self.connect() as db:
                existing = db.execute("SELECT * FROM jobs WHERE request_id=?", (request_id,)).fetchone()
                if existing:
                    if existing["root"] != str(directory) or existing["options"] != dumps(options):
                        raise OperationFailure("request_id already belongs to a different scan", code="job_request_conflict",
                            recovery="先查询原请求对应的任务；不同扫描使用新的 request_id。")
                    return self.get(existing["id"])
                busy = db.execute("SELECT id FROM jobs WHERE root=? AND state IN('queued','running','cancelling')", (str(directory),)).fetchone()
                if busy:
                    if busy[0] in self.fallback and self.fallback[busy[0]]["state"] not in ACTIVE:
                        raise OperationFailure("The prior scan finished but its journal needs attention", code="job_status_unavailable",
                            recovery="先保留已完成任务的结果，检查任务日志和来源报告；修复后重启服务，再创建新扫描。")
                    raise OperationFailure("This source already has an active scan", code="job_source_busy",
                        recovery="查看现有任务并等待或取消；不会为同一来源重复入队。", progress={"job_id": busy[0]})
                if db.execute("SELECT count(*) FROM jobs WHERE state IN('queued','running','cancelling')").fetchone()[0] >= 10:
                    raise OperationFailure("Index queue is full", code="job_queue_full", recovery="最多有 10 个未结束任务。等待或取消已有任务后再添加。")
                identifier, timestamp = uuid.uuid4().hex, now()
                with self.library.store.connect() as index:
                    epoch = source_epoch(index, str(directory))
                    if expected_source_epoch is not None and (epoch != expected_source_epoch or not index.execute(
                            "SELECT 1 FROM roots WHERE path=?", (str(directory),)).fetchone()):
                        raise OperationFailure("Source changed after detection", code="source_conflict", retryable=True,
                            recovery="来源在检测后已重扫或移除。重新检测后再刷新。")
                db.execute("INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?,?,?)", (identifier, request_id, str(directory),
                    dumps(options), "queued", timestamp, timestamp, dumps({"phase": "queued", "source_epoch": epoch}), None, None, 0))
                db.execute("""DELETE FROM jobs WHERE id IN(SELECT id FROM jobs WHERE state NOT IN('queued','running','cancelling')
                           ORDER BY created_at DESC LIMIT -1 OFFSET 200)""")
            self.cancellations[identifier] = threading.Event()
            self.queue.put(identifier)
            try:
                return self.get(identifier)
            except (sqlite3.Error, OSError) as exc:
                raise OperationFailure("Scan was queued but its status could not be read", code="job_acceptance_unknown",
                    outcome="unknown", progress={"job_id": identifier}, recovery="任务可能已开始。先查询 job_id 或任务列表，不要重复创建扫描。") from exc

    def update(self, identifier, **values):
        fields = {**values, "updated_at": now()}
        for key in ("progress", "report", "error"):
            if key in fields and fields[key] is not None:
                fields[key] = dumps(fields[key])
        with self.connect() as db:
            db.execute("UPDATE jobs SET " + ",".join(key + "=?" for key in fields) + " WHERE id=?", [*fields.values(), identifier])

    def finish(self, job, **values):
        with self.guard:
            try:
                self.update(job["id"], **values)
            except (sqlite3.Error, OSError) as exc:
                # Preserve the actual index outcome in this process even when
                # the separate job journal cannot record the final result.
                self.fallback[job["id"]] = {**job, **values, "updated_at": now(),
                    "status_warning": {**failure_details(exc, "index.job_status"),
                        "outcome": "completed" if values.get("report") else "unknown",
                        "recovery": "任务状态未能持久化。保留结果并检查来源报告；修复任务日志后重启服务，再决定是否新建扫描。"}}

    def cancel(self, identifier):
        with self.guard:
            job = self.get(identifier)
            if job["state"] in ACTIVE:
                self.cancellations[identifier].set()
                if job["state"] == "queued":
                    detail = failure_details(OperationFailure("Queued scan cancelled", code="cancelled",
                        recovery="任务未执行，已有索引保持不变。"), "index.job")
                    self.finish(job, state="cancelled", error=detail, cancel_requested=1)
                else:
                    try:
                        self.update(identifier, state="cancelling", cancel_requested=1)
                    except (sqlite3.Error, OSError) as exc:
                        raise OperationFailure("Cancellation was signalled but its status could not be recorded",
                            code="job_cancel_unknown", outcome="unknown", progress={"job_id": identifier},
                            recovery="先查询扫描任务。取消信号已发出，不要据此启动重复扫描。") from exc
            return self.get(identifier)

    def run(self):
        try:
            while not self.stopping.is_set():
                try:
                    identifier = self.queue.get(timeout=.2)
                except Empty:
                    continue
                job = None
                try:
                    with self.guard:
                        job = self.get(identifier)
                        if job["state"] != "queued":
                            continue
                        self.update(identifier, state="running")
                        cancellation = self.cancellations[identifier]
                    def progress(value):
                        with self.guard:
                            self.update(identifier, progress=value)
                    options = dict(job["options"])
                    if "max_files" not in options and not any(row["path"] == job["root"] for row in self.library.status()["roots"]):
                        options["max_files"] = 1000000
                    report = self.library.index(job["root"], **options, progress=progress, cancelled=cancellation.is_set,
                                                expected_source_epoch=job["progress"]["source_epoch"])
                    self.finish(job, state="succeeded" if report["complete"] else "partial", report=report, error=None,
                                progress={"phase": "complete", "files_examined": report["files_examined"]})
                except BaseException as exc:
                    if job is not None:
                        if isinstance(exc, KeyboardInterrupt):
                            exc = OperationFailure("Scan interrupted", code="cancelled", outcome=getattr(exc, "outcome", "unchanged"), recovery="检查来源报告后再继续。")
                        if isinstance(exc, (ValueError, OSError, sqlite3.Error)):
                            detail = failure_details(exc, "index.job")
                        else:
                            detail = failure_details(OperationFailure("Unexpected index worker error: " + type(exc).__name__,
                                code="job_internal_error", outcome="unknown", recovery="先检查来源扫描报告和本地服务，再决定是否重试。"), "index.job")
                        self.finish(job, state="cancelled" if detail["code"] == "cancelled" else "failed", error=detail)
                finally:
                    with self.guard:
                        self.cancellations.pop(identifier, None)
        finally:
            self.lease.__exit__(None, None, None)

    def close(self):
        with self.guard:
            if self.stopping.is_set():
                return
            self.stopping.set()
            for identifier in list(self.cancellations):
                self.cancel(identifier)
        # Slow filesystem/Git calls stop at the next checkpoint. The worker
        # retains its OS lock until it really exits, even if this join expires.
        self.worker.join(timeout=5)


class UnavailableJobs:
    """Keep browsing available if the separate task journal cannot start."""
    def __init__(self, cause):
        self.detail = failure_details(cause, "index.jobs_startup")

    def unavailable(self, *args, **kwargs):
        raise OperationFailure("Background scans are unavailable: " + self.detail["error"], code="jobs_unavailable",
            recovery="检索和已有记录仍可使用。" + self.detail["recovery"] + " 修复后重新启动服务，不要删除任务记录。")

    submit = get = list = cancel = unavailable

    def close(self):
        pass
