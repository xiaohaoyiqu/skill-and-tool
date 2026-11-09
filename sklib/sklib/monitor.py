"""One opt-in source checker per UI, with bounded results and normal index jobs."""
from __future__ import annotations

import threading
import sqlite3

from .failures import failure_details, OperationFailure


class SourceMonitor:
    def __init__(self, library, jobs):
        self.library, self.jobs = library, jobs
        self.guard = threading.RLock()
        self.wake = threading.Event()
        self.stopping = threading.Event()
        self.enabled = self.auto_refresh = self.running = False
        self.interval = 60
        self.reports = {}
        self.attempted = {}
        self.refresh_jobs = {}
        self.error = None
        self.worker = threading.Thread(target=self.run, name="sklib-source-checker", daemon=True)
        self.worker.start()

    def status(self):
        with self.guard:
            return {"enabled": self.enabled, "auto_refresh": self.auto_refresh, "running": self.running,
                "interval_seconds": self.interval, "reports": list(self.reports.values()), "error": self.error}

    def configure(self, *, enabled=None, auto_refresh=None, interval_seconds=None, check_now=False):
        if any(value is not None and type(value) is not bool for value in (enabled, auto_refresh)) or type(check_now) is not bool:
            raise ValueError("Monitor switches must be boolean")
        if interval_seconds is not None and (type(interval_seconds) is not int or not 30 <= interval_seconds <= 86400):
            raise ValueError("interval_seconds must be 30..86400")
        with self.guard:
            if self.stopping.is_set():
                raise ValueError("Source monitor is stopping")
            if enabled is not None:
                self.enabled = enabled
            if auto_refresh is not None:
                self.auto_refresh = auto_refresh
            if interval_seconds is not None:
                self.interval = interval_seconds
            if self.auto_refresh and not self.enabled:
                self.auto_refresh = False
            if self.enabled or check_now:
                self.wake.set()
            return self.status()

    def run(self):
        while not self.stopping.is_set():
            with self.guard:
                timeout = self.interval if self.enabled else None
            triggered = self.wake.wait(timeout)
            self.wake.clear()
            if self.stopping.is_set():
                break
            with self.guard:
                if not triggered and not self.enabled:
                    continue
                self.running, self.error = True, None
            try:
                roots = self.library.status()["roots"]
                valid = {item["path"] for item in roots}
                with self.guard:
                    self.reports = {key: report for key, report in self.reports.items() if key in valid}
                    self.attempted = {key: token for key, token in self.attempted.items() if key in valid}
                    self.refresh_jobs = {key: job for key, job in self.refresh_jobs.items() if key in valid}
                for item in roots:
                    if self.stopping.is_set():
                        break
                    report = self.library.check_source(item["path"], cancelled=self.stopping.is_set)
                    with self.guard:
                        refresh = self.enabled and self.auto_refresh and not self.stopping.is_set()
                    if report["complete"] and report["state"] == "clean":
                        self.attempted.pop(item["path"], None)
                    suppressed = self.attempted.get(item["path"]) == report["change_token"]
                    if refresh and report["complete"] and report["state"] == "changed" and suppressed:
                        report["refresh_suppressed"] = True
                    if refresh and report["complete"] and report["state"] == "changed" and not suppressed:
                        try:
                            job = self.jobs.submit(item["path"], request_id=None, expected_source_epoch=report["source_epoch"])
                            report["refresh_job"] = job["id"]
                            self.refresh_jobs[item["path"]] = job["id"]
                            self.attempted[item["path"]] = report["change_token"]
                        except (ValueError, OSError, sqlite3.Error) as exc:
                            report["refresh_error"] = failure_details(exc, "source.refresh")
                            if isinstance(exc, OperationFailure) and exc.outcome == "unknown":
                                self.attempted[item["path"]] = report["change_token"]
                                if exc.progress and exc.progress.get("job_id"):
                                    self.refresh_jobs[item["path"]] = exc.progress["job_id"]
                    if item["path"] in self.refresh_jobs:
                        report["refresh_job"] = self.refresh_jobs[item["path"]]
                    with self.guard:
                        self.reports[item["path"]] = report
            except Exception as exc:
                if not self.stopping.is_set():
                    with self.guard:
                        self.error = failure_details(exc, "source.monitor")
            finally:
                with self.guard:
                    self.running = False

    def close(self):
        self.stopping.set()
        self.wake.set()
        self.worker.join(timeout=5)
