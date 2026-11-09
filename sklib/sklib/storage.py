from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = 2
SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS roots(path TEXT PRIMARY KEY, scanned_at TEXT, last_report TEXT);
CREATE TABLE IF NOT EXISTS documents(
 id TEXT PRIMARY KEY, root TEXT NOT NULL, relative_path TEXT NOT NULL, path TEXT NOT NULL UNIQUE,
 kind TEXT NOT NULL, name TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL,
 body TEXT NOT NULL, revision TEXT NOT NULL, size INTEGER NOT NULL, mtime_ns INTEGER NOT NULL,
 source TEXT NOT NULL, project TEXT NOT NULL, metadata TEXT NOT NULL, warnings TEXT NOT NULL,
 indexed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS documents_root ON documents(root);
CREATE INDEX IF NOT EXISTS documents_kind ON documents(kind);
CREATE TABLE IF NOT EXISTS annotations(
 document_id TEXT PRIMARY KEY, tags TEXT NOT NULL DEFAULT '[]', note TEXT NOT NULL DEFAULT '',
 favorite INTEGER NOT NULL DEFAULT 0, state TEXT NOT NULL DEFAULT 'unreviewed', updated_at TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
 document_id UNINDEXED, name, description, body, annotation, tokenize='unicode61'
);
CREATE TABLE IF NOT EXISTS vectors(
 document_id TEXT PRIMARY KEY, revision TEXT NOT NULL, model TEXT NOT NULL,
 dimension INTEGER NOT NULL, embedding BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS events(
 id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL
);
"""


class Store:
    def __init__(self, home: str | Path):
        self.home = Path(home).expanduser().resolve()
        self.database = self.home / "index.sqlite3"

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        self.home.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.database, timeout=20)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA busy_timeout=20000")
            for attempt in range(7):
                try:
                    # journal_mode changes can return BUSY immediately during
                    # simultaneous first opens, regardless of busy_timeout.
                    if db.execute("PRAGMA journal_mode").fetchone()[0] != "wal":
                        db.execute("PRAGMA journal_mode=WAL")
                    # Do not silently open a future schema with old code.
                    version = db.execute("PRAGMA user_version").fetchone()[0]
                    if version not in (0, SCHEMA_VERSION):
                        raise ValueError(f"Unsupported database schema {version}")
                    if version == 0:
                        db.executescript(SCHEMA)
                        db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
                    break
                except sqlite3.OperationalError as exc:
                    if attempt == 6 or not any(word in str(exc).lower() for word in ("locked", "busy")):
                        raise
                    db.rollback()
                    time.sleep(.01 * 2**attempt)
            with db:
                yield db
        finally:
            db.close()


def dumps(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def source_epoch(db: sqlite3.Connection, root: str) -> int:
    row = db.execute("SELECT value FROM meta WHERE key=?", ("source_epoch:" + root,)).fetchone()
    return int(row[0]) if row else 0


def advance_source_epoch(db: sqlite3.Connection, root: str) -> None:
    db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (
        "source_epoch:" + root, str(source_epoch(db, root) + 1)))
