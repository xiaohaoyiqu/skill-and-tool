"""Keep Git's directory/index environment from leaking across repositories."""
from __future__ import annotations

import os


def environment() -> dict[str, str]:
    value = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        value.pop(name, None)
    return value
