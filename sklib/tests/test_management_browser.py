"""Real browser source monitoring and preview/apply recovery workflows."""
from __future__ import annotations

import importlib.util
import json
import shutil
import unittest

import test_browser as browser_helpers
from test_library import Fixture, skill


@unittest.skipUnless(importlib.util.find_spec("playwright"), "Playwright is not installed")
class ManagementBrowserTests(Fixture):
    start_ui = browser_helpers.BrowserTests.start_ui
    browser_options = browser_helpers.BrowserTests.browser_options

    def test_source_detection_and_opt_in_automatic_refresh(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 390, "height": 844})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(base)
                page.locator('.nav[data-view="sources"]').click()
                expect(page.locator("#source-check")).to_be_visible()
                self.write("new/SKILL.md", skill("new", "New workflow"))
                page.locator("#source-check").click()
                expect(page.locator("#source-check-results")).to_contain_text("需要刷新")
                expect(page.locator("#source-check-results")).to_contain_text("新增 1")
                page.locator("#source-auto-check").check()
                page.locator("#source-auto-refresh").check()
                expect(page.locator("#summary")).to_contain_text("4 个技能", timeout=15000)
                self.assertEqual(self.lib.status()["documents"], 5)
                page.locator("#source-auto-check").uncheck()
                expect(page.locator("#source-auto-refresh")).not_to_be_checked()
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_snapshot_conflict_stale_preview_lost_response_and_download(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        identifier = self.pdf_id()
        self.lib.annotate(identifier, note="backup note", tags=["backup"])
        snapshot = self.lib.snapshot()
        self.lib.annotate(identifier, note="current note")
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(base)
                page.locator('.nav[data-view="records"]').click()
                page.locator("#restore-file").set_input_files({"name": "backup.json", "mimeType": "application/json",
                    "buffer": json.dumps(snapshot).encode("utf-8")})
                expect(page.locator("#restore-summary")).to_contain_text("快照已读取")
                page.locator("#restore-preview").click()
                expect(page.locator("#restore-summary")).to_contain_text("保留冲突 1")
                expect(page.locator("#restore-apply")).to_be_disabled()
                page.locator("#restore-policy").select_option("replace")
                page.locator("#restore-preview").click()
                expect(page.locator("#restore-apply")).to_be_enabled()
                self.lib.annotate(identifier, note="concurrent note")
                page.locator("#restore-apply").click()
                expect(page.locator("#notice")).to_contain_text("Restore preview is stale")
                self.assertEqual(self.lib.get(identifier)["annotation"]["note"], "concurrent note")
                page.locator("#restore-preview").click()
                expect(page.locator("#restore-apply")).to_be_enabled()
                requests = []
                def lose_response(route):
                    requests.append(route.request.method)
                    route.fetch()
                    route.abort("connectionfailed")
                page.route("**/api/records/import-apply", lose_response)
                page.locator("#restore-apply").click()
                expect(page.locator("#notice")).to_contain_text("结果尚未确认")
                self.assertEqual(requests, ["POST"])
                self.assertEqual(self.lib.get(identifier)["annotation"]["note"], "backup note")
                self.assertEqual(page.locator("#restore-file").evaluate("input => input.files.length"), 1)
                expect(page.locator("#restore-apply")).to_be_disabled()
                page.unroute("**/api/records/import-apply", lose_response)
                page.locator("#restore-preview").click()
                expect(page.locator("#restore-summary")).to_contain_text("相同 4")
                with page.expect_download() as downloading:
                    page.locator("#snapshot-download").click()
                destination = self.base / "downloaded.json"
                downloading.value.save_as(destination)
                self.assertTrue(any(entry["note"] == "backup note" for entry in json.loads(destination.read_text(encoding="utf-8"))["entries"]))
                page.set_viewport_size({"width": 390, "height": 844})
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
                self.assertEqual(errors, [])
            finally:
                browser.close()

    def test_path_migration_uses_existing_index_and_retains_original_note(self):
        from playwright.sync_api import sync_playwright, expect
        self.sample()
        original = self.pdf_id()
        self.lib.annotate(original, note="migrate me")
        copied = self.base / "copied"
        shutil.copytree(self.root, copied)
        self.lib.index(copied)
        server, base = self.start_ui()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**self.browser_options(playwright))
            try:
                page = browser.new_page()
                page.goto(base)
                page.locator('.nav[data-view="records"]').click()
                page.locator("#restore-tools details").first.locator("summary").click()
                page.locator("#migration-from").select_option(str(self.root.resolve()))
                page.locator("#migration-to").select_option(str(copied.resolve()))
                page.locator("#migration-preview").click()
                expect(page.locator("#restore-summary")).to_contain_text("新增 1")
                page.locator("#restore-apply").click()
                expect(page.locator("#restore-summary")).to_contain_text("已保存 1")
                self.assertEqual(self.lib.search("pdf", root=str(copied))["results"][0]["note"], "migrate me")
                self.assertEqual(self.lib.get(original)["annotation"]["note"], "migrate me")
            finally:
                browser.close()
