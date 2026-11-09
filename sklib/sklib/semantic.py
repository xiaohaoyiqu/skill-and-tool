"""Optional, explicitly configured local Ollama embeddings; no model downloads."""
from __future__ import annotations

import array
import math
import sqlite3
import urllib.error
import urllib.parse
import urllib.request

from .storage import dumps
from .jsonutil import loads
from .failures import OperationFailure, failure_details


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Embedding redirects are disabled")


class OllamaEmbeddings:
    def __init__(self, model: str, endpoint: str = "http://127.0.0.1:11434", *, timeout: int = 60):
        url = urllib.parse.urlsplit(endpoint)
        if url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost", "::1"} or url.username or url.password or url.query or url.fragment:
            raise ValueError("Embeddings must use an explicitly configured loopback HTTP endpoint")
        if not isinstance(model, str) or not model.strip() or len(model) > 200:
            raise ValueError("A local embedding model is required")
        if type(timeout) is not int or not 1 <= timeout <= 600:
            raise ValueError("Embedding timeout must be 1..600 seconds")
        self.timeout = timeout
        self.endpoint = endpoint.rstrip("/")
        self.model = self.endpoint + "|" + model
        self.model_name = model
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def encode(self, texts: list[str]) -> list[list[float]]:
        data = dumps({"model": self.model_name, "input": texts, "truncate": True}).encode("utf-8")
        req = urllib.request.Request(self.endpoint + "/api/embed", data=data, headers={"Content-Type": "application/json"})
        with self.opener.open(req, timeout=self.timeout) as response:
            raw = response.read(16 * 1024 * 1024 + 1)
        if len(raw) > 16 * 1024 * 1024:
            raise ValueError("Embedding response exceeds 16 MiB")
        payload = loads(raw)
        if not isinstance(payload, dict) or not isinstance(payload.get("embeddings"), list):
            raise ValueError("Embedding response must contain an embeddings array")
        vectors = payload["embeddings"]
        if len(vectors) != len(texts):
            raise ValueError("Embedding count mismatch")
        result = []
        dimension = None
        for vector in vectors:
            if not isinstance(vector, list) or not 1 <= len(vector) <= 8192:
                raise ValueError("Invalid embedding dimension")
            if any(type(v) not in {int, float} or not math.isfinite(v) for v in vector):
                raise ValueError("Embedding contains non-finite values")
            if dimension is not None and len(vector) != dimension:
                raise ValueError("Embedding dimensions differ")
            dimension = len(vector)
            norm = math.sqrt(sum(v * v for v in vector))
            if not norm or not math.isfinite(norm):
                raise ValueError("Embedding has zero norm")
            result.append([v / norm for v in vector])
        return result

    @staticmethod
    def pack(vector: list[float]) -> bytes:
        return array.array("f", vector).tobytes()

    @staticmethod
    def similarity(query: list[float], blob: bytes, dimension: int) -> float:
        if len(query) != dimension:
            raise OperationFailure("Embedding dimension changed; rebuild the semantic index", code="embedding_incompatible",
                recovery="确认使用相同模型，再用 embed --force --model <模型名> 重建向量。词法检索仍可使用。")
        if not isinstance(blob, bytes) or len(blob) != dimension * array.array("f").itemsize:
            raise OperationFailure("Corrupt embedding", code="embedding_corrupt",
                recovery="使用 embed --force --model <模型名> 重建向量；词法索引和笔记保留。")
        vector = array.array("f")
        vector.frombytes(blob)
        if any(not math.isfinite(value) for value in vector):
            raise OperationFailure("Corrupt embedding", code="embedding_corrupt",
                recovery="使用 embed --force --model <模型名> 重建向量；词法索引和笔记保留。")
        return sum(a * b for a, b in zip(query, vector))


def embed_library(library, provider: OllamaEmbeddings, batch_size: int = 16, *, force: bool = False) -> dict:
    if type(batch_size) is not int or not 1 <= batch_size <= 64 or type(force) is not bool:
        raise ValueError("batch_size must be 1..64")
    # Release the DB before network calls. New revisions are rechecked on write.
    with library.store.connect() as db:
        rows = db.execute("""SELECT d.* FROM documents d LEFT JOIN vectors v ON v.document_id=d.id
            WHERE ? OR v.document_id IS NULL OR v.revision<>d.revision OR v.model<>? ORDER BY d.id""", (force, provider.model)).fetchall()
    updated, processed = 0, 0
    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        texts = [r["name"] + "\n" + r["description"] + "\n" + r["body"][:12000] for r in batch]
        try:
            vectors = provider.encode(texts)
            if not isinstance(vectors, list) or len(vectors) != len(batch):
                raise ValueError("Embedding count mismatch")
            if any(not isinstance(vector, list) or not 1 <= len(vector) <= 8192
                   or any(type(value) not in {int, float} or not math.isfinite(value) for value in vector) for vector in vectors):
                raise ValueError("Invalid embedding values")
            written = 0
            with library.store.connect() as db:
                db.execute("BEGIN IMMEDIATE")
                for row, vector in zip(batch, vectors):
                    current = db.execute("SELECT revision FROM documents WHERE id=?", (row["id"],)).fetchone()
                    if current is not None and current[0] == row["revision"]:
                        db.execute("INSERT OR REPLACE INTO vectors VALUES(?,?,?,?,?)", (
                            row["id"], row["revision"], provider.model, len(vector), provider.pack(vector)))
                        written += 1
            updated += written
            processed += len(batch)
        except KeyboardInterrupt as exc:
            exc.progress = {"embedded": updated, "processed": processed, "pending_at_start": len(rows)}
            exc.outcome = "partial" if updated else "unchanged"
            raise
        except (ValueError, OSError, sqlite3.Error, RecursionError, OverflowError) as exc:
            detail = failure_details(exc, "embed")
            raise OperationFailure(str(exc), code=detail["code"], retryable=detail["retryable"],
                recovery=detail["recovery"] + " 修正后重新运行 embed，会跳过已成功的匹配向量；强制重建需保留 --force。",
                outcome="partial" if updated else "unchanged",
                progress={"embedded": updated, "processed": processed, "pending_at_start": len(rows),
                          "remaining_at_failure": len(rows) - processed}) from exc
    return {"embedded": updated, "model": provider.model, "pending_at_start": len(rows), "skipped_changed": processed - updated}
