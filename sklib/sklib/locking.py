"""Process-safe advisory lock for application-owned record operations."""
from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path

from .indexer import is_link
from .failures import OperationFailure


@contextmanager
def exclusive(path: Path, timeout: float = 10):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if is_link(path):
            raise ValueError("Record lock must not be a link")
    except FileNotFoundError:
        pass
    with path.open("a+b") as stream:
        if os.fstat(stream.fileno()).st_size == 0:
            stream.write(b"\0")
            stream.flush()
        deadline = time.monotonic() + timeout
        while True:
            try:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as exc:
                if time.monotonic() >= deadline:
                    raise OperationFailure("Records are busy; retry after the current operation finishes", code="records_busy",
                        retryable=True, recovery="等待当前记录操作结束后重试；不要删除锁文件或重建记录仓库。") from exc
                time.sleep(.02)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
