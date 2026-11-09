"""Read-only environment checks, including an optional existing index check."""
from __future__ import annotations

from importlib import metadata
from pathlib import Path
import shutil
import sqlite3
import sys

from .storage import SCHEMA_VERSION


def environment_report(home, *, check_index=False):
    dependencies = []
    for name, required in (("PyYAML", True), ("tomli", sys.version_info < (3, 11))):
        try:
            version = metadata.version(name)
        except metadata.PackageNotFoundError:
            version = None
        major = int(version.split(".", 1)[0]) if version else None
        supported = major == (6 if name == "PyYAML" else 2)
        dependencies.append({"name": name, "version": version, "required": required, "ok": supported or not required})
    sqlite = {"version": sqlite3.sqlite_version, "fts5": False, "json": False}
    db = sqlite3.connect(":memory:")
    try:
        for name, sql in (("fts5", "CREATE VIRTUAL TABLE check_fts USING fts5(body)"),
                          ("json", "SELECT json_array_length('[1,2]')")):
            try:
                db.execute(sql)
                sqlite[name] = True
            except sqlite3.Error as exc:
                sqlite[name + "_error"] = str(exc)
    finally:
        db.close()
    directory = Path(home).expanduser().resolve()
    database = directory / "index.sqlite3"
    index = {"path": str(database), "exists": database.exists(), "checked": False}
    if check_index and database.exists():
        try:
            connection = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True, timeout=2)
            try:
                result = connection.execute("PRAGMA quick_check").fetchone()[0]
                version = connection.execute("PRAGMA user_version").fetchone()[0]
                index.update(checked=True, ok=result == "ok" and version == SCHEMA_VERSION, result=result,
                             schema_version=version, expected_schema_version=SCHEMA_VERSION)
            finally:
                connection.close()
        except sqlite3.Error as exc:
            index.update(checked=True, ok=False, error=str(exc), recovery="保留现有状态目录，备份后诊断；此检查没有修复或删除文件。")
    try:
        package_version = metadata.version("sklib-local")
    except metadata.PackageNotFoundError:
        package_version = None
    warnings = []
    if not shutil.which("git"):
        warnings.append("未找到 Git；检索仍可用，Git 记录功能需要准备 Git。")
    if not package_version:
        warnings.append("当前解释器未安装项目；从其他工作目录接入时使用绝对源码启动器路径，或在独立环境安装项目。")
    ready = sys.version_info >= (3, 10) and all(item["ok"] for item in dependencies) and sqlite["fts5"] and sqlite["json"] and index.get("ok", True)
    return {"ready": ready, "runtime": {"python": sys.version.split()[0], "executable": sys.executable,
                "isolated_environment": sys.prefix != sys.base_prefix, "installed_version": package_version},
            "dependencies": dependencies, "sqlite": sqlite, "home": str(directory), "index": index,
            "mcp": {"transport": "stdio", "command": sys.executable,
                "args": ["-m", "sklib", "--home", str(directory), "mcp"], "installed_launch_ready": package_version is not None},
            "warnings": warnings, "recovery": None if ready else (
                "索引检查未通过。保留状态目录，按 index 字段诊断数据库或 schema；不要直接删除重建。"
                if not index.get("ok", True) else "使用项目 .venv 安装声明依赖；检查上方失败项后重试。")}
