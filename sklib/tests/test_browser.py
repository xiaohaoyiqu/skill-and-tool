"""Real browser coverage. Optional when Playwright/Chromium are not installed."""
from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import subprocess
import threading
import unittest
from pathlib import Path

from test_library import Fixture
from sklib.web import create_server
from sklib.failures import OperationFailure
from unittest.mock import patch


@unittest.skipUnless(importlib.util.find_spec("playwright"), "Playwright is not installed")
class BrowserTests(Fixture):
    def test_required_terms_filter_and_standalone_search_on_mobile(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 390, "height": 844})
                page.goto(base)
                page.locator("#query").fill("performance")
                page.locator("#required-terms").fill("Flutter")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                expect(page.locator("#result-meta")).to_contain_text("0 项")
                expect(page.locator(".result")).to_have_count(0)
                page.locator("#query").fill("")
                page.locator("#required-terms").fill("PDF，tables")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                expect(page.locator("#result-meta")).to_contain_text("1 项")
                expect(page.locator(".result")).to_have_count(1)
                expect(page.locator(".result")).to_contain_text("pdf-tables")
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
            finally:
                browser.close()

    def start_ui(self):
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        return server, f"http://127.0.0.1:{server.server_address[1]}"

    def test_bulk_selection_across_pages_atomic_failure_conflict_and_lost_response(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        for number in range(9):
            self.write(f"s{number:02}/SKILL.md", f"---\nname: s{number:02}\ndescription: Selection sample\n---\nSteps.\n")
        self.lib.index(self.root)
        pdf = self.pdf_id()
        human = self.lib.search("humanize")["results"][0]["id"]
        vue = self.lib.search("vue-performance")["results"][0]["id"]
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.goto(base)
                page.locator(f'.bulk-pick[data-id="{pdf}"]').check()
                page.locator(f'.bulk-pick[data-id="{human}"]').check()
                page.locator("#next").click()
                page.locator(f'.bulk-pick[data-id="{vue}"]').check()
                expect(page.locator("#pick-count")).to_have_text("已选 3 项")
                page.locator("#batch-tags").fill("已复核")
                page.locator("#batch-state").select_option("useful")
                page.locator("#batch-favorite").select_option("true")
                with patch("sklib.service.refresh_fts", side_effect=sqlite3.OperationalError("database is locked")):
                    page.locator("#batch-apply").click()
                    expect(page.locator("#notice")).to_contain_text("database is locked")
                for identifier in (pdf, human, vue):
                    self.assertIsNone(self.lib.get(identifier)["annotation"])
                expect(page.locator("#pick-count")).to_have_text("已选 3 项")
                expect(page.locator("#batch-tags")).to_have_value("已复核")
                self.lib.annotate(pdf, note="他处的新笔记")
                page.locator("#batch-apply").click()
                expect(page.locator("#notice")).to_contain_text("Annotation changed")
                self.assertIsNone(self.lib.get(human)["annotation"])
                page.locator("#review-picks").click()
                expect(page.locator("#notice")).to_contain_text("已读取选中位置")
                page.locator("#batch-apply").click()
                expect(page.locator("#notice")).to_contain_text("更新 3 项")
                self.assertEqual(self.lib.get(pdf)["annotation"]["note"], "他处的新笔记")
                self.assertEqual(self.lib.browse(tags=["已复核"], favorite=True)["total"], 3)
                expect(page.locator("#pick-count")).to_have_text("已选 0 项")
                page.locator(f'.bulk-pick[data-id="{vue}"]').check()
                page.locator("#batch-tags").fill("结果待确认")
                requests = []
                def lose_response(route):
                    requests.append(route.request.method)
                    route.fetch()
                    route.abort("connectionfailed")
                page.route("**/api/annotate-batch", lose_response)
                page.locator("#batch-apply").click()
                expect(page.locator("#notice")).to_contain_text("操作结果尚未确认")
                expect(page.locator("#pick-count")).to_have_text("已选 1 项")
                self.assertEqual(requests, ["POST"])
                self.assertIn("结果待确认", json.loads(self.lib.get(vue)["annotation"]["tags"]))
                page.unroute("**/api/annotate-batch", lose_response)
                page.locator("#query").fill("different query")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                expect(page.locator("#pick-count")).to_have_text("已选 0 项")
                page.set_viewport_size({"width": 390, "height": 844})
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
            finally:
                browser.close()

    def test_persistent_draft_reload_new_page_removed_source_and_confirmed_save(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            context = browser.new_context(viewport={"width": 1440, "height": 1000})
            try:
                page = context.new_page()
                delayed_status = []
                page.route("**/api/status", lambda route: delayed_status.append(route))
                page.goto(base)
                page.locator("#query").fill("PDF")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                expect(page.locator("#note-text")).to_be_disabled()
                self.assertEqual(len(delayed_status), 1)
                delayed_status[0].continue_()
                page.unroute("**/api/status")
                expect(page.locator("#note-text")).to_be_enabled()
                page.locator("#note-tags").fill("未提交")
                page.locator("#note-text").fill("刷新后要还在")
                page.locator("#note-state").select_option("to_try")
                page.locator("#note-favorite").check()
                expect(page.locator("#draft-status")).to_contain_text("草稿已保存在此浏览器")
                self.assertIsNone(self.lib.get(self.pdf_id())["annotation"])
                page.reload()
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                expect(page.locator("#note-text")).to_have_value("刷新后要还在")
                expect(page.locator("#note-state")).to_have_value("to_try")
                expect(page.locator("#note-favorite")).to_be_checked()
                page.close()
                page = context.new_page()
                page.goto(base)
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                expect(page.locator("#note-text")).to_have_value("刷新后要还在")
                self.lib.remove_root(self.root)
                page.reload()
                page.locator("#drafts-toggle").click()
                expect(page.locator(".draft-card textarea")).to_have_value("刷新后要还在")
                with page.expect_download() as download_info:
                    page.locator("#drafts-export").click()
                exported = json.loads(Path(download_info.value.path()).read_text(encoding="utf-8"))
                self.assertTrue(any(record["values"]["note"] == "刷新后要还在" for record in exported["drafts"]))
                page.get_by_role("button", name="打开并恢复此副本").click()
                expect(page.locator("#notice")).to_contain_text("Unknown document id")
                self.lib.index(self.root)
                page.reload()
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                page.locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(page.locator("#notice")).to_contain_text("个人记录已保存")
                expect(page.locator("#drafts-toggle")).to_have_text("草稿箱 0")
                self.assertEqual(self.lib.get(self.pdf_id())["annotation"]["note"], "刷新后要还在")
            finally:
                context.close()
                browser.close()

    def test_two_pages_keep_drafts_and_reject_stale_note_save(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            context = browser.new_context(viewport={"width": 1440, "height": 1000})
            try:
                pages = [context.new_page(), context.new_page()]
                for page in pages:
                    page.goto(base)
                    page.locator(".result").filter(has_text="pdf-tables").click()
                    page.locator("#tab-notes").click()
                pages[0].locator("#note-text").fill("来自页面一")
                pages[1].locator("#note-text").fill("来自页面二")
                expect(pages[0].locator("#drafts-toggle")).to_have_text("草稿箱 2")
                pages[0].locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(pages[0].locator("#notice")).to_contain_text("个人记录已保存")
                pages[1].locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(pages[1].locator("#note-conflict")).to_be_visible()
                expect(pages[1].locator("#note-current")).to_contain_text("来自页面一")
                expect(pages[1].locator("#note-text")).to_have_value("来自页面二")
                self.assertEqual(self.lib.get(self.pdf_id())["annotation"]["note"], "来自页面一")
                pages[1].locator("#note-rebase").click()
                pages[1].locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(pages[1].locator("#notice")).to_contain_text("个人记录已保存")
                pages[0].locator("#note-text").fill("页面一后续修改")
                pages[0].locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(pages[0].locator("#note-conflict")).to_be_visible()
                expect(pages[0].locator("#note-text")).to_have_value("页面一后续修改")
                self.assertEqual(self.lib.get(self.pdf_id())["annotation"]["note"], "来自页面二")
                pages[0].reload()
                pages[0].locator(".result").filter(has_text="pdf-tables").click()
                pages[0].locator("#tab-notes").click()
                expect(pages[0].locator("#note-text")).to_have_value("来自页面二")
                expect(pages[0].locator("#draft-status")).to_contain_text("较早版本")
                pages[0].locator("#drafts-toggle").click()
                pages[0].get_by_role("button", name="打开并恢复此副本").click()
                expect(pages[0].locator("#note-text")).to_have_value("页面一后续修改")
                expect(pages[0].locator("#note-conflict")).to_be_visible()
                pages[0].get_by_role("button", name="删除此草稿副本").click()
                expect(pages[0].locator("#note-text")).to_have_value("来自页面二")
            finally:
                context.close()
                browser.close()

    def test_draft_storage_failure_keeps_input_and_exports_recovery_copy(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.add_init_script("const originalSetItem=Storage.prototype.setItem; Storage.prototype.setItem=function(key,value){if(String(key).startsWith('sklib.drafts'))throw new DOMException('Quota exceeded','QuotaExceededError'); return originalSetItem.call(this,key,value);};")
                page.goto(base)
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                page.locator("#note-text").fill("草稿不能丢")
                expect(page.locator("#draft-status")).to_contain_text("最新输入只保留在当前页面")
                expect(page.locator("#note-text")).to_have_value("草稿不能丢")
                self.assertIsNone(self.lib.get(self.pdf_id())["annotation"])
                page.locator("#drafts-toggle").click()
                with page.expect_download() as download_info:
                    page.locator("#drafts-export").click()
                exported = json.loads(Path(download_info.value.path()).read_text(encoding="utf-8"))
                self.assertTrue(any(record["values"]["note"] == "草稿不能丢" for record in exported["drafts"]))
                page.locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(page.locator("#notice")).to_contain_text("个人记录已保存")
                self.assertEqual(self.lib.get(self.pdf_id())["annotation"]["note"], "草稿不能丢")
            finally:
                browser.close()

    def browser_options(self, playwright):
        options = {"headless": True}
        if not Path(playwright.chromium.executable_path).exists():
            edge = Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Microsoft/Edge/Application/msedge.exe"
            if edge.exists():
                options["channel"] = "msedge"
            else:
                cache = Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"
                installed = sorted(cache.glob("chromium-*/chrome-win*/chrome.exe"), reverse=True)
                if not installed:
                    self.skipTest("No installed Chromium browser")
                options["executable_path"] = str(installed[0])
        else:
            options["channel"] = "chromium"
        return options

    def test_manual_search_read_annotate_and_git_commit(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        with sync_playwright() as playwright:
            # Reuse an existing browser; tests never download one.
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(f"http://127.0.0.1:{server.server_address[1]}")
                expect(page.locator("#summary")).to_contain_text("3 个技能")
                page.locator("#query").fill("PDF 表格提取")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                page.locator(".result").filter(has_text="pdf-tables").click()
                expect(page.locator("#content")).to_contain_text("Read references/guide.md")
                page.locator("#tab-files").click()
                page.get_by_role("button", name="references/guide.md", exact=True).click()
                expect(page.locator("#resource-content")).to_have_text("first\nsecond\nthird\n")
                page.locator("#tab-notes").click()
                page.locator("#note-tags").fill("办公,常用")
                page.locator("#note-text").fill("已试用，适合报销表格。<script>alert(1)</script>")
                page.locator("#note-favorite").check()
                page.locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(page.locator("#notice")).to_contain_text("个人记录已保存")
                page.get_by_role("button", name="记录与版本").click()
                page.locator("#records-init").click()
                expect(page.locator("#records-output")).to_contain_text('"initialized": true')
                records = self.lib.store.home / "records"
                for key, value in [("user.name", "Browser Fixture"), ("user.email", "browser@example.invalid")]:
                    subprocess.run(["git", "-C", str(records), "config", key, value], check=True, capture_output=True)
                page.locator("#records-preview").click()
                expect(page.locator("#commit-button")).to_be_enabled(timeout=15000)
                page.locator("#commit-message").fill("Review PDF skill")
                page.locator("#commit-button").click()
                expect(page.locator("#records-output")).to_contain_text('"committed": true')
                page.locator("#records-log").click()
                expect(page.locator("#records-output")).to_contain_text("Review PDF skill")
                # A second client changes annotations after this page's preview.
                self.lib.annotate(self.pdf_id(), note="Before preview")
                page.locator("#records-preview").click()
                expect(page.locator("#commit-button")).to_be_enabled(timeout=15000)
                self.lib.annotate(self.pdf_id(), note="Changed by another client")
                page.locator("#commit-message").fill("Reject stale preview")
                page.locator("#commit-button").click()
                expect(page.locator("#notice")).to_contain_text("changed since preview")
                expect(page.locator("#commit-button")).to_be_disabled()
                page.locator("#records-preview").click()
                expect(page.locator("#commit-button")).to_be_enabled(timeout=15000)
                page.locator("#commit-message").fill("Freshly reviewed records")
                page.locator("#commit-button").click()
                expect(page.locator("#notice")).to_contain_text("记录已提交到本地 Git")
                page.set_viewport_size({"width": 390, "height": 844})
                page.get_by_role("button", name="技能检索").click()
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
                self.assertEqual(errors, [])
            finally:
                browser.close()


    def test_project_filter_typed_files_encodings_and_saved_scan_options(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        self.write("app/package.json", '{"name":"javascript-sample"}')
        self.write("pdf/skills/pdf-tables/assets/image.png", "binary asset")
        self.write("pdf/skills/pdf-tables/utf16.txt", "").write_bytes("Unicode 参考文本".encode("utf-16"))
        self.write("pdf/skills/pdf-tables/legacy.txt", "").write_bytes("旧编码参考".encode("gb18030"))
        self.lib.index(self.root, include_docs=True, encoding="gb18030", max_files=500)
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(f"http://127.0.0.1:{server.server_address[1]}")
                page.locator("#query").fill("javascript-sample")
                page.locator("#project-type").select_option("javascript")
                expect(page.locator(".result")).to_have_count(1)
                expect(page.locator("#kind")).to_have_value("project")
                page.locator(".result").click()
                expect(page.locator("#content")).to_contain_text("javascript-sample")
                page.locator("#kind").select_option("skill")
                expect(page.locator("#project-type")).to_have_value("")
                page.locator("#query").fill("pdf-tables")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                page.locator(".result").click()
                page.locator("#tab-files").click()
                expect(page.get_by_role("button", name="assets/image.png", exact=True)).to_be_disabled()
                page.get_by_role("button", name="utf16.txt", exact=True).click()
                expect(page.locator("#resource-content")).to_have_text("Unicode 参考文本")
                page.get_by_role("button", name="legacy.txt", exact=True).click()
                expect(page.locator("#resource-content")).to_have_text("旧编码参考")
                page.locator("#resource-encoding").select_option("auto")
                expect(page.locator("#notice")).to_contain_text("Cannot decode")
                page.locator("#resource-encoding").select_option("gb18030")
                expect(page.locator("#resource-label")).to_contain_text("gb18030")
                page.get_by_role("button", name="资料来源").click()
                page.get_by_role("button", name="重新扫描", exact=True).click()
                expect(page.locator("#notice")).to_contain_text("扫描完成")
                expect(page.locator("#include-docs")).to_be_checked()
                expect(page.locator("#source-encoding")).to_have_value("gb18030")
                options = self.lib.status()["roots"][0]["last_report"]["options"]
                self.assertEqual(options["max_files"], 500)
                self.assertEqual(options["encoding"], "gb18030")
                self.assertTrue(options["include_docs"])
                page.set_viewport_size({"width": 390, "height": 844})
                page.get_by_role("button", name="技能检索").click()
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
                self.assertEqual(errors, [])
            finally:
                browser.close()


    def test_background_scan_reload_cancel_and_lost_response(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        extra = self.base / "extra source 中文"
        extra.mkdir()
        (extra / "SKILL.md").write_bytes(b"---\nname: queued-workflow\ndescription: Background scan sample\n---\nRead all steps.\n")
        release, started = threading.Event(), threading.Event()
        original = self.lib.index
        def controlled(root, **options):
            started.set()
            while not release.wait(.01):
                if options["cancelled"]():
                    raise OperationFailure("Scan cancelled", code="cancelled", recovery="Existing index preserved")
            return original(root, **options)
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (release.set(), server.shutdown(), server.server_close(), worker.join(timeout=5)))
        with patch.object(self.lib, "index", side_effect=controlled), sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                base = f"http://127.0.0.1:{server.server_address[1]}"
                page.goto(base)
                page.get_by_role("button", name="资料来源").click()
                page.locator("#source-root").fill(str(extra))
                page.locator("#index-form").get_by_role("button", name="扫描并更新索引").click()
                expect(page.locator('.index-job[data-state="running"]')).to_have_count(1)
                self.assertTrue(started.is_set())
                page.get_by_role("button", name="技能检索").click()
                page.locator("#query").fill("PDF")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                expect(page.locator(".result")).to_have_count(1)
                page.reload()
                page.get_by_role("button", name="资料来源").click()
                expect(page.locator('.index-job[data-state="running"]')).to_have_count(1)
                page.get_by_role("button", name="取消扫描", exact=True).click()
                expect(page.locator('.index-job[data-state="cancelled"]')).to_have_count(1)
                self.assertEqual(self.lib.status()["documents"], 4)
                writes = []
                def lose_acceptance(route):
                    if route.request.method != "POST":
                        route.continue_()
                        return
                    writes.append(route.request.url)
                    route.fetch()
                    route.abort("connectionfailed")
                page.route("**/api/index-jobs", lose_acceptance)
                page.locator("#source-root").fill(str(extra))
                page.locator("#index-form").get_by_role("button", name="扫描并更新索引").click()
                expect(page.locator("#notice")).to_contain_text("操作结果尚未确认")
                # The same URL also serves polling GET requests; only intercept
                # the one POST, then let the UI recover the accepted job.
                page.unroute("**/api/index-jobs", lose_acceptance)
                page.reload()
                page.get_by_role("button", name="资料来源").click()
                expect(page.locator('.index-job[data-state="running"]')).to_have_count(1)
                self.assertEqual(len(server.index_jobs.list()["jobs"]), 2)
                self.assertEqual(len(writes), 1)
                release.set()
                expect(page.locator('.index-job[data-state="succeeded"]')).to_have_count(1, timeout=15000)
                expect(page.locator("#summary")).to_contain_text("4 个技能")
                page.set_viewport_size({"width": 390, "height": 844})
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
                self.assertEqual(errors, [])
            finally:
                release.set()
                browser.close()

    def test_sorting_and_failed_or_uncertain_saves_preserve_input(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.goto(f"http://127.0.0.1:{server.server_address[1]}")
                expect(page.locator(".result")).to_have_count(3)
                page.locator("#queue").select_option("unclassified")
                expect(page.locator("#queue-summary")).to_contain_text("未分类 3")
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                page.locator("#note-tags").fill("tools")
                page.locator("#note-state").select_option("useful")
                page.locator("#note-text").fill("保留未确认的输入")
                def fail_save(route):
                    route.fulfill(status=503, content_type="application/json", body=json.dumps({"error":"database is locked", "recovery":"等待当前写入后重试", "code":"database_busy"}))
                page.route("**/api/annotate", fail_save)
                page.locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(page.locator("#notice")).to_contain_text("等待当前写入后重试")
                expect(page.locator("#note-text")).to_have_value("保留未确认的输入")
                self.assertIsNone(self.lib.get(self.pdf_id())["annotation"])
                page.locator(".result").filter(has_text="vue-performance").click()
                expect(page.locator("#detail-name")).to_have_text("vue-performance")
                page.locator(".result").filter(has_text="pdf-tables").click()
                page.locator("#tab-notes").click()
                expect(page.locator("#note-text")).to_have_value("保留未确认的输入")
                expect(page.locator("#note-tags")).to_have_value("tools")
                expect(page.locator("#note-state")).to_have_value("useful")
                page.unroute("**/api/annotate", fail_save)
                requests = []
                def lose_response(route):
                    requests.append(route.request.url)
                    route.fetch()
                    route.abort("connectionfailed")
                page.route("**/api/annotate", lose_response)
                page.locator("#notes-panel").get_by_role("button", name="保存记录").click()
                expect(page.locator("#notice")).to_contain_text("操作结果尚未确认")
                expect(page.locator("#note-text")).to_have_value("保留未确认的输入")
                self.assertEqual(self.lib.get(self.pdf_id())["annotation"]["note"], "保留未确认的输入")
                self.assertEqual(len(requests), 1)
                page.unroute("**/api/annotate", lose_response)
                page.locator("#search-form").get_by_role("button", name="检索").click()
                expect(page.locator(".result")).to_have_count(2)
                expect(page.locator("#queue-summary")).to_contain_text("未分类 2")
                def fail_search(route):
                    route.fulfill(status=503, content_type="application/json", body='{"error":"busy","recovery":"retry later"}')
                page.route("**/api/search?**", fail_search)
                page.locator("#query").fill("PDF")
                page.locator("#search-form").get_by_role("button", name="检索").click()
                expect(page.locator("#result-meta")).to_contain_text("仍显示上次结果")
                expect(page.locator("#next")).to_be_disabled()
                expect(page.locator(".result")).to_have_count(2)
                page.unroute("**/api/search?**", fail_search)
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
