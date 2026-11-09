"""Compatibility contracts for heterogeneous local projects and resources."""
from __future__ import annotations

import json
import codecs
import subprocess
import sys
import re
import threading
import urllib.request
from unittest.mock import patch

from test_library import Fixture, skill
from sklib.mcp import Session
from sklib.web import create_server


class CompatibilityTests(Fixture):
    def test_projects_without_readme_and_nested_workspace_packages(self):
        samples = {
            "web/package.json": '{"name":"@local/web","description":"Web interface"}',
            "web/packages/worker/package.json": '{"name":"queue-worker"}',
            "py/pyproject.toml": '[project]\nname = "python-tool"\ndescription = "Data utility"\n',
            "rust/Cargo.toml": '[package]\nname = "rust-tool"\nversion = "0.1.0"\n',
            "go/go.mod": 'module example.invalid/go-tool\n\ngo 1.23\n',
            "java/pom.xml": '<project xmlns="http://maven.apache.org/POM/4.0.0"><artifactId>java-tool</artifactId><description>Java server</description></project>',
            "net/App.csproj": '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><AssemblyName>dotnet-tool</AssemblyName><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>',
            "cpp/CMakeLists.txt": 'cmake_minimum_required(VERSION 3.20)\nproject(cpp-tool LANGUAGES CXX)\n',
            "php/composer.json": '{"name":"local/php-tool","description":"PHP utility"}',
            "dart/pubspec.yaml": 'name: dart_tool\ndescription: Dart mobile utility\n',
            "gradle/build.gradle.kts": 'plugins { kotlin("jvm") version "2.0" }\n',
            "ruby/Gemfile": 'source "https://rubygems.org"\ngem "rake"\n',
            "swift/Package.swift": 'import PackageDescription\nlet package = Package(name: "swift-tool")\n',
        }
        for path, body in samples.items():
            self.write(path, body)
        report = self.lib.index(self.root)
        self.assertTrue(report["complete"])
        self.assertEqual(self.lib.status()["counts"], {"project": len(samples)})
        for query in ["@local/web", "queue-worker", "python-tool", "rust-tool", "go-tool", "java-tool", "dotnet-tool", "cpp-tool", "php-tool", "dart_tool", "gradle", "ruby", "swift-tool"]:
            with self.subTest(query=query):
                self.assertGreater(self.lib.search(query, kind="project")["returned"], 0)
        entry = self.lib.search("queue-worker", kind="project")["results"][0]
        self.assertEqual(entry["project_types"], ["javascript"])
        dotnet = self.lib.search("dotnet-tool", kind="project")["results"][0]
        self.assertEqual(self.lib.get(dotnet["id"])["metadata"]["target_frameworks"], "net8.0")
        second = self.lib.index(self.root)
        self.assertEqual(second["unchanged"], len(samples))

    def test_readme_variants_and_optional_document_formats(self):
        for path in ["a/README", "b/README.rst", "c/README.zh-CN.md", "d/README.txt", "deep/mod/README.markdown"]:
            self.write(path, "Compatibility documentation\n")
        self.write("deep/mod/package.json", '{"name":"nested-mod"}')
        for extension in ["mdx", "rst", "txt", "adoc", "markdown"]:
            self.write("guide/usage." + extension, "Readability documentation " + extension)
        self.lib.index(self.root, include_docs=True)
        self.assertEqual(self.lib.status()["counts"], {"project": 6, "document": 5})

    def test_utf_bom_encodings_and_identical_decoded_revisions(self):
        value = skill("unicode", "Unicode 编码兼容")
        encodings = [("utf-8-sig", b""), ("utf-16", b""), ("utf-32", b""),
                     ("utf-16-be", codecs.BOM_UTF16_BE), ("utf-32-be", codecs.BOM_UTF32_BE)]
        for index, (encoding, prefix) in enumerate(encodings):
            path = self.write(f"v{index}/unicode/SKILL.md", "")
            path.write_bytes(prefix + value.encode(encoding))
        result = self.lib.index(self.root)
        self.assertTrue(result["complete"], result)
        self.assertEqual(result["added"], 5)
        found = self.lib.search("unicode")["results"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["duplicate_count"], 4)
        for location in [found[0], *found[0]["other_locations"]]:
            self.assertEqual(self.lib.get(location["id"])["content"], value)

    def test_explicit_legacy_encoding_persists_and_option_change_redecodes(self):
        path = self.write("legacy/SKILL.md", "")
        value = skill("legacy", "中文旧编码")
        path.write_bytes(value.encode("gb18030"))
        first = self.lib.index(self.root)
        self.assertFalse(first["complete"])
        result = self.lib.index(self.root, encoding="gb18030")
        self.assertEqual(result["added"], 1)
        identifier = self.lib.search("旧编码")["results"][0]["id"]
        self.assertEqual(self.lib.get(identifier)["content"], value)
        self.write("legacy/reference.txt", "").write_bytes("参考资料".encode("gb18030"))
        self.assertEqual(self.lib.read_file(identifier, "reference.txt")["content"], "参考资料")
        options = self.lib.status()["roots"][0]["last_report"]["options"]
        self.assertEqual(options["encoding"], "gb18030")
        self.assertFalse(self.lib.index(self.root, encoding="auto")["complete"])
        self.assertFalse(self.lib.index(self.root)["complete"])
        self.assertEqual(self.lib.status()["documents"], 1)
        for fallback, text in [("cp1252", "café"), ("shift_jis", "日本語")]:
            self.write("legacy/" + fallback + ".txt", "").write_bytes(text.encode(fallback))
            self.assertEqual(self.lib.read_file(identifier, fallback + ".txt", encoding=fallback)["content"], text)

    def test_file_type_manifest_and_binary_read_errors(self):
        self.write("bundle/SKILL.md", skill("bundle", "Mixed resources"))
        for name in ["scripts/a.py", "scripts/run.ps1", "scripts/run.cmd", "config/options.json", "references/guide.rst", "assets/icon.svg"]:
            self.write("bundle/" + name, "plain text\n")
        for name in ["assets/image.png", "assets/book.pdf", "app.exe", "archive.zip", "report.docx"]:
            self.write("bundle/" + name, "apparently text")
        self.write("bundle/.private/visible.txt", "private resource")
        self.lib.index(self.root)
        identifier = self.lib.search("bundle")["results"][0]["id"]
        record = self.lib.get(identifier)
        details = {item["path"]: item for item in record["file_details"]}
        self.assertEqual(details["scripts/a.py"]["category"], "source")
        self.assertEqual(details["config/options.json"]["category"], "configuration")
        self.assertEqual(details["assets/image.png"]["category"], "image")
        self.assertFalse(details["assets/image.png"]["text_readable"])
        self.assertNotIn(".private/visible.txt", record["files"])
        for name in ["assets/image.png", "assets/book.pdf", "app.exe", "archive.zip", "report.docx"]:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "text|binary|Binary"):
                self.lib.read_file(identifier, name)

    def test_hidden_and_excluded_resource_directories_not_readable(self):
        self.sample()
        identifier = self.pdf_id()
        self.write("pdf/skills/pdf-tables/node_modules/pkg/file.txt", "dependency")
        with self.assertRaisesRegex(ValueError, "excluded|Resource"):
            self.lib.read_file(identifier, "node_modules/pkg/file.txt")
        self.write("pdf/skills/pdf-tables/references/build", "an ordinary extensionless file")
        self.assertEqual(self.lib.read_file(identifier, "references/build")["content"], "an ordinary extensionless file")

    def test_build_output_excluded_but_agent_skill_dirs_kept(self):
        for directory in ["node_modules", "bin", "obj", "vendor", ".gradle", ".dart_tool", "__pycache__"]:
            self.write(f"app/{directory}/injected/SKILL.md", skill("injected", "Generated content"))
        self.write("app/.agents/skills/valid/SKILL.md", skill("valid", "Valid hidden agent directory"))
        self.lib.index(self.root)
        self.assertEqual(self.lib.status()["counts"], {"skill": 1})
        self.assertEqual(self.lib.search("valid")["returned"], 1)

    def test_invalid_manifests_are_isolated_without_evaluating_project_code(self):
        self.write("a/package.json", '{"name": NaN}')
        self.write("b/pom.xml", '<!DOCTYPE project [<!ENTITY a "expanded">]><project><name>&a;</name></project>')
        self.write("c/pyproject.toml", '[project\nname = invalid')
        self.write("d/setup.py", 'raise RuntimeError("must not execute")')
        self.write("valid/SKILL.md", skill("valid", "Healthy skill"))
        report = self.lib.index(self.root)
        self.assertTrue(report["complete"], report)
        with self.lib.store.connect() as db:
            rows = db.execute("SELECT kind,warnings FROM documents").fetchall()
        self.assertEqual(len(rows), 5)
        self.assertEqual(sum(bool(json.loads(row["warnings"])) for row in rows), 3)

    def test_source_options_reused_and_exported_to_records(self):
        self.write("guide/usage.rst", "Helpful documentation")
        self.write("extra/SKILL.md", skill("extra", "Excluded source"))
        self.lib.index(self.root, include_docs=True, max_files=300, max_depth=4, exclude=["extra"])
        report = self.lib.index(self.root)
        self.assertEqual(report["unchanged"], 1)
        self.assertEqual(report["options"]["max_files"], 300)
        self.assertEqual(report["options"]["exclude"], ["extra"])
        self.assertTrue(report["options"]["include_docs"])
        self.assertEqual(self.lib.snapshot()["sources"][0]["options"], report["options"])
        self.assertEqual(self.lib.index(self.root, include_docs=False)["removed"], 1)
        cleared = subprocess.run([sys.executable, "-m", "sklib", "--home", str(self.lib.store.home),
                                 "index", str(self.root), "--clear-excludes"],
                                capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(cleared.returncode, 0, cleared.stderr)
        self.assertEqual(json.loads(cleared.stdout)["options"]["exclude"], [])
        self.assertEqual(self.lib.search("extra")["returned"], 1)

    def test_project_filter_and_distinct_projects_not_collapsed(self):
        for folder in ["a", "b"]:
            self.write(folder + "/package.json", '{"private":true}')
        self.write("py/pyproject.toml", '[project]\nname="python-tool"\n')
        self.lib.index(self.root)
        result = self.lib.search("project", kind="project", project_type="javascript")
        self.assertEqual(result["returned"], 2)
        self.assertTrue(all(item["duplicate_count"] == 0 for item in result["results"]))
        self.assertEqual(self.lib.search("project", kind="all", project_type="python")["returned"], 1)
        with self.assertRaisesRegex(ValueError, "project type"):
            self.lib.search("project", project_type="unrecognized")

    def test_missing_toml_parser_is_reported_and_new_parser_refreshes(self):
        from sklib import projects
        parser = projects.TOML
        self.write("py/pyproject.toml", '[project]\nname="python-tool"\n')
        with patch.object(projects, "TOML", None):
            self.lib.index(self.root)
            identifier = self.lib.search("python-tool", kind="project")["results"][0]["id"]
            self.assertIn("tomli", str(self.lib.get(identifier)["warnings"]))
        if parser is not None:
            self.lib.index(self.root)
            self.assertEqual(self.lib.get(identifier)["name"], "python-tool")
            self.assertEqual(self.lib.get(identifier)["warnings"], [])

    def test_project_metadata_is_current_after_source_edit(self):
        path = self.write("app/package.json", '{"name":"old-name","description":"Before"}')
        self.lib.index(self.root)
        identifier = self.lib.search("old-name", kind="project")["results"][0]["id"]
        path.write_text('{"name":"new-name","description":"After"}', encoding="utf-8")
        result = self.lib.get(identifier)
        self.assertTrue(result["stale"])
        self.assertEqual(result["name"], "new-name")
        self.assertEqual(result["metadata"]["name"], "new-name")
        with self.assertRaises(ValueError):
            self.lib.read_file(identifier, "arbitrary-source.py")

    def test_resource_actual_newlines_preserve_unicode_separators(self):
        self.sample()
        identifier = self.pdf_id()
        value = "first\u2028still first\nsecond\r\nthird\rfinal"
        self.write("pdf/skills/pdf-tables/references/lines.txt", value)
        result = self.lib.read_file(identifier, "references/lines.txt", max_lines=1)
        self.assertEqual(result["content"], "first\u2028still first\n")
        self.assertEqual(result["total_lines"], 4)
        next_page = self.lib.read_file(identifier, "references/lines.txt", start_line=2, max_lines=3)
        self.assertEqual(result["content"] + next_page["content"], value)

    def test_cli_resource_encoding_and_source_options(self):
        self.sample()
        identifier = self.pdf_id()
        self.write("pdf/skills/pdf-tables/reference.txt", "").write_bytes("手动读取".encode("gb18030"))
        result = subprocess.run([sys.executable, "-m", "sklib", "--home", str(self.lib.store.home),
                                 "read", identifier, "reference.txt", "--encoding", "gb18030"],
                                capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["content"], "手动读取")

    def test_noncanonical_skill_filename_and_unicode_space_paths(self):
        self.write("有 空格 ' 目录/skill.md", skill("有 空格 ' 目录", "兼容路径"))
        self.lib.index(self.root)
        entry = self.lib.search("兼容路径")["results"][0]
        self.assertIn("Nonstandard", str(entry["warnings"]))
        self.write("有 空格 ' 目录/references/含 空格.txt", "路径读取正常")
        self.assertEqual(self.lib.read_file(entry["id"], "references\\含 空格.txt")["content"], "路径读取正常")

    def test_mcp_project_filter_file_details_and_legacy_encoding(self):
        self.sample()
        self.write("app/package.json", '{"name":"javascript-sample"}')
        self.write("pdf/skills/pdf-tables/legacy.txt", "").write_bytes("编码测试".encode("gb18030"))
        self.lib.index(self.root)
        session = Session(self.lib)
        session.initialized = session.ready = True
        def call(name, arguments):
            response = session.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}})
            self.assertFalse(response["result"].get("isError"), response)
            return response["result"]["structuredContent"]
        result = call("search_skills", {"query": "javascript-sample", "kind": "project", "project_type": "javascript"})
        self.assertEqual(result["returned"], 1)
        identifier = self.pdf_id()
        self.assertIn("file_details", call("get_skill", {"id": identifier}))
        self.assertEqual(call("read_skill_file", {"id": identifier, "relative_path": "legacy.txt", "encoding": "gb18030"})["content"], "编码测试")

    def test_http_source_settings_reused_and_project_filter(self):
        self.write("app/package.json", '{"name":"javascript-sample"}')
        self.write("guide/usage.rst", "Guide document")
        server = create_server(self.lib, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close(), worker.join(timeout=5)))
        base = f"http://127.0.0.1:{server.server_address[1]}"
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        token = re.search(r'name="sklib-token" content="([^"]+)"', opener.open(base).read().decode())[1]
        def post(payload):
            request = urllib.request.Request(base + "/api/index", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "X-Sklib-Token": token})
            return json.loads(opener.open(request).read())
        first = post({"root": str(self.root), "include_docs": True, "max_files": 500, "encoding": "gb18030"})
        second = post({"root": str(self.root)})
        self.assertEqual(first["options"], second["options"])
        self.assertEqual(second["unchanged"], 2)
        result = json.loads(opener.open(base + "/api/search?q=javascript-sample&kind=project&project_type=javascript").read())
        self.assertEqual(result["returned"], 1)


if __name__ == "__main__":
    import unittest
    unittest.main()
