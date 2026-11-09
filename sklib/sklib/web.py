"""On-demand loopback UI. No browser launch, daemon, CORS, or remote assets."""
from __future__ import annotations

import json
import secrets
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .records import Records
from .jsonutil import loads
from .failures import failure_details, OperationFailure
from .jobs import IndexJobs, UnavailableJobs, OPTIONS
from .monitor import SourceMonitor
from .restoring import MAX_SNAPSHOT_BYTES

STATIC = Path(__file__).parent / "static"


def create_server(library, port: int = 8765) -> ThreadingHTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("Invalid port")
    token = secrets.token_urlsafe(32)

    def index_options(data):
        if not isinstance(data.get("root"), str) or not data["root"].strip():
            raise ValueError("A source directory is required")
        options = {key: data[key] for key in OPTIONS if key in data}
        if "max_files" not in options:
            registered = any(row["path"] == str(Path(data["root"]).expanduser().resolve()) for row in library.status()["roots"])
            if not registered:
                options["max_files"] = 1000000
        return options

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(15)

        def log_message(self, format, *args):
            # Avoid logging queries, notes, paths or credentials.
            pass

        def _allowed(self) -> bool:
            actual_port = self.server.server_address[1]
            hosts = {f"127.0.0.1:{actual_port}", f"localhost:{actual_port}"}
            host = self.headers.get("Host", "")
            origin = self.headers.get("Origin")
            return host in hosts and (not origin or origin == "http://" + host) and self.headers.get("Sec-Fetch-Site") != "cross-site"

        def _send(self, code: int, data: bytes, content_type: str = "application/json; charset=utf-8") -> None:
            try:
                self.send_response(code)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
                self.end_headers()
                self.wfile.write(data)
            except (ConnectionError, TimeoutError):
                # The browser may abort during either headers or body. Stop
                # sending; a second error response cannot reach this connection.
                self.close_connection = True

        def _json(self, code: int, value: object) -> None:
            self._send(code, json.dumps(value, ensure_ascii=False).encode("utf-8"))

        def _failure(self, exc, operation):
            detail = failure_details(exc, operation)
            status = 503 if isinstance(exc, sqlite3.Error) or detail["code"] in {"jobs_unavailable", "jobs_stopping"} else 400
            self._json(status, detail)

        def _reject(self, status, message, code, recovery):
            self._json(status, failure_details(OperationFailure(message, code=code, recovery=recovery), "http"))

        def do_GET(self):
            if not self._allowed():
                self._reject(403, "Local origin required", "local_access_required", "使用本机服务显示的 loopback 地址打开界面。")
                return
            try:
                url = urlsplit(self.path)
                query = {key: values[-1] for key, values in parse_qs(url.query).items()}
                if url.path in {"/", "/app.js", "/drafts.js", "/management.js", "/styles.css"}:
                    name = "index.html" if url.path == "/" else url.path[1:]
                    content = (STATIC / name).read_bytes()
                    if name == "index.html":
                        content = content.replace(b"__TOKEN__", token.encode("ascii"))
                    mime = {"index.html": "text/html", "app.js": "text/javascript", "drafts.js": "text/javascript", "management.js": "text/javascript", "styles.css": "text/css"}[name]
                    self._send(200, content, mime + "; charset=utf-8")
                    return
                if url.path == "/api/status":
                    result = library.status()
                elif url.path == "/api/source-monitor":
                    result = self.server.source_monitor.status()
                elif url.path == "/api/records/snapshot":
                    result = library.snapshot()
                elif url.path == "/api/index-jobs":
                    result = self.server.index_jobs.list()
                elif url.path == "/api/index-job":
                    result = self.server.index_jobs.get(query.get("id", ""))
                elif url.path == "/api/search":
                    result = library.search(query.get("q", ""), kind=query.get("kind", "skill"),
                        limit=int(query.get("limit", "10")), offset=int(query.get("offset", "0")),
                        tags=[t.strip() for t in query.get("tags", "").split(",") if t.strip()] or None,
                        required_terms=[t.strip() for t in query.get("required_terms", "").split(",") if t.strip()] or None,
                        favorite=query.get("favorite") == "true", state=query.get("state") or None,
                        root=query.get("root") or None, project_type=query.get("project_type") or None,
                        queue=query.get("queue", "all"))
                elif url.path == "/api/browse":
                    result = library.browse(kind=query.get("kind", "all"), queue=query.get("queue", "all"),
                        sort=query.get("sort", "name"), limit=int(query.get("limit", "25")), offset=int(query.get("offset", "0")),
                        tags=[t.strip() for t in query.get("tags", "").split(",") if t.strip()] or None,
                        favorite=query.get("favorite") == "true", state=query.get("state") or None,
                        root=query.get("root") or None, project_type=query.get("project_type") or None)
                elif url.path == "/api/annotations":
                    result = library.annotation_states(query.get("ids", "").split(","))
                elif url.path == "/api/skill":
                    result = library.get(query.get("id", ""))
                elif url.path == "/api/file":
                    result = library.read_file(query.get("id", ""), query.get("path", ""),
                        start_line=int(query.get("start_line", "1")), expected_revision=query.get("revision"), encoding=query.get("encoding"))
                elif url.path == "/api/history":
                    result = library.history()
                elif url.path == "/api/records/log":
                    result = Records(library).log()
                elif url.path == "/api/records/status":
                    result = Records(library).status()
                else:
                    self._reject(404, "Not found", "unknown_endpoint", "检查接口路径与应用版本。")
                    return
                self._json(200, result)
            except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
                self._failure(exc, self.path.split("?", 1)[0].removeprefix("/api/").replace("/", "."))

        def do_POST(self):
            provided = self.headers.get("X-Sklib-Token", "")
            if not self._allowed() or not provided.isascii() or not secrets.compare_digest(provided, token):
                self._reject(403, "Local session token required", "local_access_required", "请从当前本地服务打开界面，刷新会话后重试；先保留未保存输入。")
                return
            try:
                if self.headers.get("Transfer-Encoding"):
                    raise ValueError("Chunked requests are not accepted")
                path = urlsplit(self.path).path
                size = int(self.headers.get("Content-Length", "0"))
                maximum = MAX_SNAPSHOT_BYTES + 65536 if path in {"/api/records/import-preview", "/api/records/import-apply"} else 65536
                if not 0 < size <= maximum:
                    raise ValueError(f"Request body must be 1..{maximum} bytes")
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("JSON body required")
                data = loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError("JSON body must be an object")
                path = urlsplit(self.path).path
                if path == "/api/source-monitor":
                    if set(data) - {"enabled", "auto_refresh", "interval_seconds", "check_now"}:
                        raise ValueError("Unknown source monitor fields")
                    result = self.server.source_monitor.configure(**data)
                elif path in {"/api/records/import-preview", "/api/records/import-apply", "/api/records/migrate-preview", "/api/records/migrate-apply"}:
                    common = {"policy", "resolutions", "entry_map", "match_content", "offset", "limit", "preview_token"}
                    migration = "/migrate-" in path
                    if set(data) - (common | ({"from_root", "to_root"} if migration else {"snapshot", "root_map"})):
                        raise ValueError("Unknown restore fields")
                    options = {key: data[key] for key in common - {"preview_token"} if key in data}
                    options.update(apply=path.endswith("-apply"), expected_preview=data.get("preview_token"))
                    if migration:
                        result = library.migrate_annotations(data.get("from_root"), data.get("to_root"), **options)
                    else:
                        result = library.restore_annotations(data.get("snapshot"), root_map=data.get("root_map"), **options)
                elif path == "/api/annotate":
                    allowed = {k: v for k, v in data.items() if k in {"tags", "note", "favorite", "state", "expected_annotation_revision"}}
                    result = library.annotate(data.get("id", ""), **allowed)
                elif path == "/api/annotate-batch":
                    if set(data) - {"ids", "tags", "tag_mode", "state", "favorite", "expected_revisions"}:
                        raise ValueError("Unknown batch annotation fields")
                    result = library.annotate_batch(data.get("ids"), **{key: value for key, value in data.items() if key != "ids"})
                elif path == "/api/index":
                    result = library.index(data["root"], **index_options(data))
                elif path == "/api/index-jobs":
                    if set(data) - (OPTIONS | {"root", "request_id"}):
                        raise ValueError("Unknown index job fields")
                    result = self.server.index_jobs.submit(data.get("root"), {key: data[key] for key in OPTIONS if key in data}, data.get("request_id"))
                elif path == "/api/index-jobs/cancel":
                    result = self.server.index_jobs.cancel(data.get("id", ""))
                elif path == "/api/remove-root":
                    if not isinstance(data.get("root"), str) or not data["root"].strip():
                        raise ValueError("A source directory is required")
                    result = library.remove_root(data["root"])
                elif path == "/api/records/init":
                    result = Records(library).init()
                elif path == "/api/records/preview":
                    result = Records(library).preview()
                elif path == "/api/records/commit":
                    if not isinstance(data.get("preview_token"), str):
                        raise ValueError("Preview records before committing")
                    result = Records(library).commit(data.get("message", ""), expected_preview=data["preview_token"])
                else:
                    self._reject(404, "Not found", "unknown_endpoint", "检查接口路径与应用版本。")
                    return
                self._json(200, result)
            except (ValueError, OSError, UnicodeError, sqlite3.Error) as exc:
                self._failure(exc, self.path.split("?", 1)[0].removeprefix("/api/").replace("/", "."))

    class LocalServer(ThreadingHTTPServer):
        index_jobs = None
        source_monitor = None

        def server_close(self):
            try:
                if self.source_monitor is not None:
                    self.source_monitor.close()
                if self.index_jobs is not None:
                    self.index_jobs.close()
            finally:
                super().server_close()

    server = LocalServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    try:
        server.index_jobs = IndexJobs(library)
    except (ValueError, OSError, sqlite3.Error) as exc:
        server.index_jobs = UnavailableJobs(exc)
    server.source_monitor = SourceMonitor(library, server.index_jobs)
    return server
