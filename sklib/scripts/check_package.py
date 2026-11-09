"""Smoke-test a built wheel, without installing it globally or running a model."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    wheel = args.wheel.resolve(strict=True)
    with zipfile.ZipFile(wheel) as archive:
        for name in ("sklib/jobs.py", "sklib/diagnostics.py", "sklib/annotations.py", "sklib/static/index.html", "sklib/static/app.js", "sklib/static/drafts.js", "sklib/static/styles.css"):
            assert name in archive.namelist(), name
    with tempfile.TemporaryDirectory(prefix="sklib-package-") as temporary:
        base = Path(temporary)
        site = base / "package"
        subprocess.run([sys.executable, "-m", "pip", "--isolated", "install", "--disable-pip-version-check", "--no-index", "--no-deps",
                        "--target", str(site), str(wheel)], check=True, capture_output=True, timeout=60)
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(site)
        environment["PYTHONNOUSERSITE"] = "1"
        source = base / "source"
        source.mkdir()
        (source / "pyproject.toml").write_bytes(b'[project]\nname="wheel-project"\nversion="1.0"\n')
        state = base / "state"
        def cli(*arguments):
            result = subprocess.run([sys.executable, "-m", "sklib", "--home", str(state), *arguments],
                cwd=base, env=environment, capture_output=True, text=True, encoding="utf-8", timeout=30)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)
        index = cli("index", str(source))
        assert index["complete"] and index["added"] == 1
        search = cli("search", "wheel-project", "--kind", "project", "--json")
        assert search["results"][0]["name"] == "wheel-project"
        constrained = cli("search", "wheel-project", "--kind", "project", "--require-term", "wheel-project", "--json")
        assert constrained["results"][0]["name"] == "wheel-project"
        assert cli("search", "wheel-project", "--kind", "project", "--require-term", "Flutter", "--json")["returned"] == 0
        doctor = cli("doctor", "--check-index")
        assert doctor["ready"] and doctor["index"]["ok"]
        # This process imports the unpacked wheel before any editable checkout.
        smoke = '''import json, pathlib, sys, threading, urllib.request
import sklib
from sklib.service import Library
from sklib.web import create_server
module = pathlib.Path(sklib.__file__).resolve()
package_root = pathlib.Path(sys.argv[1]).resolve()
assert module.is_relative_to(package_root), str(module) + ' outside ' + str(package_root)
library = Library(sys.argv[2])
item = library.browse()['results'][0]
result = library.annotate_batch([item['id']], tags=['package-check'], expected_revisions={item['id']: item['annotation_revision']})
assert result['updated'] == 1
assert library.check_source(library.status()['roots'][0]['path'])['state'] == 'clean'
backup = library.snapshot()
library.annotate(item['id'], note='after backup')
preview = library.restore_annotations(backup, policy='replace')
restored = library.restore_annotations(backup, policy='replace', apply=True, expected_preview=preview['preview_token'])
assert restored['updated'] == 1
assert library.get(item['id'])['annotation']['note'] == ''
from sklib.mcp import TOOLS
assert len(TOOLS) == 5
server = create_server(library, 0)
worker = threading.Thread(target=server.serve_forever, daemon=True)
worker.start()
try:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    page = opener.open('http://127.0.0.1:' + str(server.server_address[1]), timeout=5).read().decode('utf-8')
    assert 'index-jobs' in page and '后台' in page and 'draft-box' in page and 'batch-form' in page and 'required-terms' in page
    script = opener.open('http://127.0.0.1:' + str(server.server_address[1]) + '/drafts.js', timeout=5).read()
    assert b'SklibDrafts' in script
    management = opener.open('http://127.0.0.1:' + str(server.server_address[1]) + '/management.js', timeout=5).read()
    assert b'restore-apply' in management and b'source-auto-refresh' in management
finally:
    server.shutdown()
    server.server_close()
    worker.join(timeout=5)
print(json.dumps({'wheel_import_used': True, 'static_ui': True, 'batch_annotation': True, 'draft_asset': True}))
'''
        result = subprocess.run([sys.executable, "-c", smoke, str(site), str(state)], cwd=base, env=environment,
            capture_output=True, text=True, encoding="utf-8", timeout=30)
        assert result.returncode == 0, result.stderr
        report = {"wheel": wheel.name, "passed": True, **json.loads(result.stdout),
                  "toml_project_indexed": True, "required_terms": True, "source_check": True, "annotation_restore": True,
                  "management_asset": True, "mcp_tools": 5, "doctor_ready": doctor["ready"], "global_install": False}
    value = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(value + "\n", encoding="utf-8", newline="\n")
    print(value)


if __name__ == "__main__":
    main()
