"""Failure results shared by CLI, HTTP and MCP. Write requests are never replayed."""
from __future__ import annotations

import errno
import sqlite3
import urllib.error


class OperationFailure(ValueError):
    def __init__(self, message: str, *, code: str, recovery: str, retryable: bool = False,
                 outcome: str = "unchanged", progress: dict | None = None):
        super().__init__(message)
        self.code, self.recovery, self.retryable = code, recovery, retryable
        self.outcome, self.progress = outcome, progress


def failure_details(exc: Exception, operation: str = "request") -> dict:
    message = str(exc)
    code, retryable = "invalid_input", False
    # Export/staging can precede a later Git failure. Only explicit phase-aware
    # errors can promise that a commit request left managed state unchanged.
    outcome = "unknown" if operation == "records.commit" else "unchanged"
    recovery = "检查输入参数和当前状态，修正后重新操作。"
    progress = None
    if isinstance(exc, OperationFailure):
        code, retryable, outcome = exc.code, exc.retryable, exc.outcome
        recovery, progress = exc.recovery, exc.progress
    elif isinstance(exc, sqlite3.Error):
        if any(word in message.lower() for word in ("locked", "busy")):
            code, retryable = "database_busy", True
            recovery = "等待当前数据库写入完成后重试；不要删除状态库。"
        else:
            code = "database_unavailable"
            recovery = "检查状态目录、磁盘和数据库版本。保留数据库与记录仓库，备份后再诊断。"
    elif isinstance(exc, PermissionError):
        code = "permission_denied"
        recovery = "检查报错路径的访问权限或占用程序；修正后重试，现有记录保留。"
    elif isinstance(exc, FileNotFoundError):
        code = "git_unavailable" if operation.startswith("records") and exc.filename == "git" else "not_found"
        recovery = "检查文件或目录是否移动、删除；来源恢复后重新扫描。若缺少 Git，请先修正 Git 可执行程序路径。"
    elif isinstance(exc, urllib.error.HTTPError):
        code = "model_http_error"
        recovery = "检查本地模型服务和已安装的模型名称；本工具不会自动下载模型。"
    elif isinstance(exc, (TimeoutError, urllib.error.URLError)):
        code, retryable = "service_unavailable", True
        recovery = "检查本地模型服务是否启动及端点是否正确，服务恢复后重试。"
    elif isinstance(exc, ValueError) and operation == "embed":
        code = "model_response_invalid"
        recovery = "模型响应格式、数量或数值不符合要求。检查所选向量模型与本地服务响应后重试。"
    elif isinstance(exc, OSError):
        if operation == "embed" and exc.errno != errno.ENOSPC:
            code, retryable = "service_unavailable", True
            recovery = "检查本地模型服务与端点是否可连接，恢复服务后重试。"
        elif operation == "ui" and (exc.errno == errno.EADDRINUSE or getattr(exc, "winerror", None) == 10048):
            code = "port_in_use"
            recovery = "选择其他 --port，或确认并停止占用该端口的本地服务后重试。"
        else:
            code = "storage_full" if exc.errno == errno.ENOSPC else "io_error"
            recovery = "检查磁盘空间、路径和文件占用后重试；不要清空现有记录。"
    result = {"error": message, "code": code, "operation": operation,
              "retryable": retryable, "outcome": outcome, "recovery": recovery}
    if outcome == "unknown" and operation == "records.commit" and not isinstance(exc, OperationFailure):
        result["recovery"] += " 先查看 records status 与 records log，确认是否已导出、暂存或提交，再决定下一步。"
    if progress is not None:
        result["progress"] = progress
    return result
