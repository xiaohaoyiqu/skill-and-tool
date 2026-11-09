from __future__ import annotations

import json
import re
import sqlite3
import threading
import time
import urllib.request
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import test_library as fixtures
from sklib.failures import OperationFailure
from sklib.indexer import read_text
from sklib.jobs import IndexJobs, ACTIVE
from sklib.web import create_server


class ScanJobsTests(fixtures.Fixture):
    def manager(self):
        jobs = IndexJobs(self.lib)
        self.addCleanup(jobs.close)
        return jobs

    def terminal(self, jobs, identifier):
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            job = jobs.get(identifier)
            if job["state"] not in ACTIVE:
                return job
            time.sleep(.01)
        self.fail("Job did not finish: " + str(jobs.get(identifier)))

    def test_finished_job_persists_and_request_id_deduplicates(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        jobs = self.manager()
        job = jobs.submit(str(self.root), request_id="one-request")
        final = self.terminal(jobs, job["id"])
        self.assertEqual(final["state"], "succeeded")
        self.assertEqual(final["report"]["added"], 1)
        self.assertEqual(jobs.submit(str(self.root), request_id="one-request")["id"], job["id"])
        with self.assertRaisesRegex(ValueError, "different scan"):
            jobs.submit(str(self.root), {"verify": True}, "one-request")
        jobs.close()
        reopened = self.manager()
        self.assertEqual(reopened.get(job["id"])["report"], final["report"])
        self.assertEqual(len(reopened.list()["jobs"]), 1)

    def test_failed_job_does_not_stop_next_job(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        self.write("b/SKILL.md", fixtures.skill("b", "queue test"))
        jobs = self.manager()
        bad = jobs.submit(str(self.root), {"max_files": 1})
        failure = self.terminal(jobs, bad["id"])
        self.assertEqual(failure["state"], "failed")
        self.assertEqual(failure["error"]["code"], "scan_file_limit")
        self.assertEqual(self.lib.status()["documents"], 0)
        good = jobs.submit(str(self.root))
        self.assertEqual(self.terminal(jobs, good["id"])["state"], "succeeded")

    def test_cancel_during_write_rolls_back_documents_fts_and_reports(self):
        self.sample()
        with self.lib.store.connect() as db:
            before = [tuple(row) for row in db.execute("SELECT * FROM documents ORDER BY id")]
            events = db.execute("SELECT count(*) FROM events").fetchone()[0]
        self.write("pdf/skills/pdf-tables/SKILL.md", fixtures.skill("pdf-tables", "changed-only-newword"))
        cancelled = threading.Event()
        def cancel_after_read(path, **options):
            value = read_text(path, **options)
            cancelled.set()
            return value
        with patch("sklib.indexer.read_text", side_effect=cancel_after_read):
            with self.assertRaises(OperationFailure) as error:
                self.lib.index(self.root, verify=True, cancelled=cancelled.is_set)
        self.assertEqual(error.exception.code, "cancelled")
        with self.lib.store.connect() as db:
            self.assertEqual([tuple(row) for row in db.execute("SELECT * FROM documents ORDER BY id")], before)
            self.assertEqual(db.execute("SELECT count(*) FROM events").fetchone()[0], events)
            db.execute("INSERT INTO documents_fts(documents_fts) VALUES('integrity-check')")
        self.assertFalse(self.lib.search("changed-only-newword")["results"])

    def test_queued_cancel_busy_source_queue_limit_and_running_cancel(self):
        jobs = self.manager()
        started = threading.Event()
        def blocking_index(root, **options):
            started.set()
            while not options["cancelled"]():
                time.sleep(.005)
            raise OperationFailure("Cancelled", code="cancelled", recovery="Retry explicitly")
        with patch.object(self.lib, "index", side_effect=blocking_index):
            first = jobs.submit(str(self.root))
            self.assertTrue(started.wait(3))
            with self.assertRaisesRegex(ValueError, "already has an active"):
                jobs.submit(str(self.root))
            queued = []
            for number in range(9):
                root = self.base / f"extra-{number}"
                root.mkdir()
                queued.append(jobs.submit(str(root)))
            extra = self.base / "overflow"
            extra.mkdir()
            with self.assertRaisesRegex(ValueError, "queue is full"):
                jobs.submit(str(extra))
            for job in queued:
                self.assertEqual(jobs.cancel(job["id"])["state"], "cancelled")
            jobs.cancel(first["id"])
            self.assertEqual(self.terminal(jobs, first["id"])["error"]["outcome"], "unchanged")
            self.assertEqual(jobs.cancel(first["id"])["state"], "cancelled")
            self.assertEqual(self.lib.index.call_count, 1)

    def test_job_status_remains_available_while_index_transaction_is_open(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        entered, release = threading.Event(), threading.Event()
        jobs = self.manager()
        def slow_read(path, **options):
            entered.set()
            if not release.wait(5):
                raise TimeoutError("Fixture release timed out")
            return read_text(path, **options)
        with patch("sklib.indexer.read_text", side_effect=slow_read):
            job = jobs.submit(str(self.root))
            try:
                self.assertTrue(entered.wait(3))
                with ThreadPoolExecutor(max_workers=1) as pool:
                    status = pool.submit(jobs.get, job["id"]).result(timeout=2)
                self.assertEqual(status["state"], "running")
                self.assertEqual(status["progress"]["phase"], "index")
                jobs.cancel(job["id"])
            finally:
                release.set()
            self.assertEqual(self.terminal(jobs, job["id"])["state"], "cancelled")
        self.assertEqual(self.lib.status()["documents"], 0)

    def test_restart_marks_unrecorded_jobs_unknown_without_replaying(self):
        jobs = self.manager()
        job = jobs.submit(str(self.root))
        self.terminal(jobs, job["id"])
        jobs.close()
        with closing(sqlite3.connect(jobs.path)) as db:
            db.execute("UPDATE jobs SET state='running',report=NULL WHERE id=?", (job["id"],))
            db.commit()
        with patch.object(self.lib, "index") as index:
            reopened = self.manager()
            record = reopened.get(job["id"])
            self.assertEqual(record["state"], "interrupted")
            self.assertEqual(record["error"]["outcome"], "unknown")
            index.assert_not_called()

    def test_second_worker_is_rejected_until_first_releases_lock(self):
        jobs = self.manager()
        with self.assertRaises(OperationFailure) as error:
            IndexJobs(self.lib)
        self.assertEqual(error.exception.code, "jobs_busy")
        jobs.close()
        self.manager()

    def test_late_cancel_reports_committed_result(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        jobs = self.manager()
        original = jobs.update
        def cancel_when_committed(identifier, **values):
            original(identifier, **values)
            if values.get("progress", {}).get("phase") == "complete":
                jobs.cancel(identifier)
        with patch.object(jobs, "update", side_effect=cancel_when_committed):
            job = jobs.submit(str(self.root))
            result = self.terminal(jobs, job["id"])
        self.assertEqual(result["state"], "succeeded")
        self.assertTrue(result["cancel_requested"])
        self.assertEqual(self.lib.status()["documents"], 1)

    def test_post_commit_progress_database_error_preserves_success(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        jobs = self.manager()
        original = jobs.update
        def fail_complete(identifier, **values):
            if values.get("progress", {}).get("phase") == "complete" and "report" not in values:
                raise sqlite3.OperationalError("job progress write failed")
            return original(identifier, **values)
        with patch.object(jobs, "update", side_effect=fail_complete):
            job = jobs.submit(str(self.root))
            result = self.terminal(jobs, job["id"])
        self.assertEqual(result["state"], "succeeded")
        self.assertEqual(result["report"]["progress_warning"]["outcome"], "completed")

    def test_http_submit_read_and_cancel_preserve_session_checks(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        token = re.search(r'name="sklib-token" content="([^"]+)"', opener.open(base).read().decode())[1]
        def post(path, payload, session=token):
            request = urllib.request.Request(base + path, data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json", "X-Sklib-Token": session})
            return json.loads(opener.open(request, timeout=5).read())
        with self.assertRaises(urllib.error.HTTPError) as error:
            post("/api/index-jobs", {"root": str(self.root)}, "wrong")
        self.assertEqual(error.exception.code, 403)
        payload = {"root": str(self.root), "request_id": "http-once"}
        first = post("/api/index-jobs", payload)
        second = post("/api/index-jobs", payload)
        self.assertEqual(first["id"], second["id"])
        self.terminal(server.index_jobs, first["id"])
        self.assertEqual(post("/api/index-jobs", payload)["id"], first["id"])
        item = json.loads(opener.open(base + "/api/index-job?id=" + first["id"]).read())
        self.assertEqual(item["state"], "succeeded")
        self.assertEqual(post("/api/index-jobs/cancel", {"id": first["id"]})["state"], "succeeded")
        self.assertEqual(len(json.loads(opener.open(base + "/api/index-jobs").read())["jobs"]), 1)

    def test_corrupt_job_journal_keeps_existing_library_ui_available(self):
        self.sample()
        (self.lib.store.home / "jobs.sqlite3").write_bytes(b"corrupt job journal")
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.assertEqual(json.loads(opener.open(base + "/api/status").read())["documents"], 4)
        self.assertIn(b"SKLIB", opener.open(base).read())
        with self.assertRaises(urllib.error.HTTPError) as error:
            opener.open(base + "/api/index-jobs")
        self.assertEqual(error.exception.code, 503)
        self.assertEqual(json.loads(error.exception.read())["code"], "jobs_unavailable")

    def test_doctor_does_not_create_state_and_checks_existing_index_read_only(self):
        from sklib.diagnostics import environment_report
        missing = self.base / "not-created"
        report = environment_report(missing, check_index=True)
        self.assertTrue(report["sqlite"]["fts5"])
        self.assertFalse(missing.exists())
        self.sample()
        valid = environment_report(self.lib.store.home, check_index=True)
        self.assertTrue(valid["index"]["ok"])
        with closing(sqlite3.connect(self.lib.store.database)) as db:
            db.execute("PRAGMA user_version=99")
            db.commit()
        future = environment_report(self.lib.store.home, check_index=True)
        self.assertFalse(future["ready"])
        self.assertEqual(future["index"]["schema_version"], 99)

    def test_final_journal_failure_exposes_committed_result_in_memory(self):
        self.write("a/SKILL.md", fixtures.skill("a", "queue test"))
        jobs = self.manager()
        original = jobs.update
        def fail_final(identifier, **values):
            if values.get("state") == "succeeded":
                raise sqlite3.OperationalError("cannot record final job status")
            return original(identifier, **values)
        with patch.object(jobs, "update", side_effect=fail_final):
            job = jobs.submit(str(self.root), request_id="final-journal-check")
            result = self.terminal(jobs, job["id"])
        self.assertEqual(result["state"], "succeeded")
        self.assertEqual(result["status_warning"]["outcome"], "completed")
        self.assertEqual(jobs.list()["jobs"][0]["state"], "succeeded")
        self.assertEqual(jobs.submit(str(self.root), request_id="final-journal-check")["state"], "succeeded")
        with self.assertRaises(OperationFailure) as error:
            jobs.submit(str(self.root))
        self.assertEqual(error.exception.code, "job_status_unavailable")
        self.assertEqual(self.lib.status()["documents"], 1)

    def test_cancel_journal_failure_reports_unknown_then_recovers(self):
        jobs = self.manager()
        started = threading.Event()
        def blocking_index(root, **options):
            started.set()
            while not options["cancelled"]():
                time.sleep(.005)
            raise OperationFailure("Cancelled", code="cancelled", recovery="Existing index preserved")
        original = jobs.update
        def fail_cancel(identifier, **values):
            if values.get("state") == "cancelling":
                raise sqlite3.OperationalError("cannot record cancellation")
            return original(identifier, **values)
        with patch.object(self.lib, "index", side_effect=blocking_index), patch.object(jobs, "update", side_effect=fail_cancel):
            job = jobs.submit(str(self.root))
            self.assertTrue(started.wait(3))
            with self.assertRaises(OperationFailure) as error:
                jobs.cancel(job["id"])
            self.assertEqual(error.exception.outcome, "unknown")
            self.assertEqual(error.exception.code, "job_cancel_unknown")
            self.assertEqual(self.terminal(jobs, job["id"])["state"], "cancelled")

    def test_source_removed_while_queued_is_not_readded_by_old_job(self):
        self.sample()
        blocker = self.base / "blocking-source"
        blocker.mkdir()
        jobs = self.manager()
        entered, release = threading.Event(), threading.Event()
        original = self.lib.index
        def controlled(root, **options):
            if root == str(blocker.resolve()):
                entered.set()
                if not release.wait(5):
                    raise TimeoutError("Fixture release timed out")
            return original(root, **options)
        with patch.object(self.lib, "index", side_effect=controlled):
            first = jobs.submit(str(blocker))
            try:
                self.assertTrue(entered.wait(3))
                queued = jobs.submit(str(self.root))
                self.lib.remove_root(self.root)
            finally:
                release.set()
            self.assertEqual(self.terminal(jobs, first["id"])["state"], "succeeded")
            result = self.terminal(jobs, queued["id"])
        self.assertEqual(result["state"], "failed")
        self.assertEqual(result["error"]["code"], "source_conflict")
        self.assertEqual(self.lib.status()["documents"], 0)
        self.assertNotIn(str(self.root.resolve()), [row["path"] for row in self.lib.status()["roots"]])
