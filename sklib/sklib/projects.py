"""Static project markers and metadata. No imports, builds or script evaluation."""
from __future__ import annotations

import re
import configparser
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from .jsonutil import loads

try:
    import tomllib as TOML
except ImportError:
    try:
        import tomli as TOML
    except ImportError:
        TOML = None

PARSER_VERSION = 1
MARKERS = {
    "package.json": "javascript", "deno.json": "javascript", "deno.jsonc": "javascript",
    "pyproject.toml": "python", "setup.cfg": "python", "setup.py": "python",
    "cargo.toml": "rust", "go.mod": "go", "go.work": "go",
    "pom.xml": "jvm", "build.gradle": "jvm", "build.gradle.kts": "jvm",
    "cmakelists.txt": "cpp", "composer.json": "php", "pubspec.yaml": "dart",
    "gemfile": "ruby", "package.swift": "swift",
}
PROJECT_TYPES = tuple(sorted(set(MARKERS.values()) | {"dotnet"}))


def project_type(name: str) -> str | None:
    suffix = Path(name).suffix.lower()
    return MARKERS.get(name.lower()) or ("dotnet" if suffix in {".csproj", ".fsproj", ".vbproj", ".sln", ".slnx"} else "cpp" if suffix == ".vcxproj" else None)


def parser_signature() -> str:
    # An optional parser becoming available must refresh unchanged manifests.
    return f"{PARSER_VERSION}:toml={TOML is not None}"


def parse_project(content: str, path: Path) -> tuple[dict, list[str]]:
    family = project_type(path.name)
    metadata = {"name": path.parent.name, "description": "", "project_types": [family] if family else []}
    warnings = []
    if not family:
        return metadata, warnings
    values = {}
    try:
        lower = path.name.lower()
        if lower in {"package.json", "composer.json", "deno.json"}:
            values = loads(content)
            if not isinstance(values, dict):
                raise ValueError("Manifest must be an object")
        elif lower in {"pyproject.toml", "cargo.toml"}:
            if TOML is None:
                raise ValueError("TOML metadata needs the declared tomli dependency on Python 3.10")
            parsed = TOML.loads(content)
            tool = parsed.get("tool", {})
            values = parsed.get("package", {}) if family == "rust" else parsed.get("project", tool.get("poetry", {}) if isinstance(tool, dict) else {})
            if not isinstance(values, dict):
                raise ValueError("Project metadata must be a table")
        elif lower == "setup.cfg":
            parsed = configparser.ConfigParser(interpolation=None)
            parsed.read_string(content)
            values = dict(parsed["metadata"]) if parsed.has_section("metadata") else {}
        elif lower == "pubspec.yaml":
            if any(isinstance(token, yaml.tokens.AliasToken) for token in yaml.scan(content)):
                raise ValueError("YAML aliases are not supported")
            values = yaml.safe_load(content)
            if not isinstance(values, dict):
                raise ValueError("Manifest must be a mapping")
        elif lower == "pom.xml" or path.suffix.lower() in {".csproj", ".fsproj", ".vbproj", ".vcxproj", ".slnx"}:
            if re.search(r"<!\s*(?:DOCTYPE|ENTITY)", content, re.I):
                raise ValueError("XML DTD and entity declarations are not supported")
            tree = ET.fromstring(content)
            def value(tag):
                # Maven coordinates must come from the project, not a dependency.
                nodes = list(tree) if lower == "pom.xml" else list(tree.iter())
                return next((node.text.strip() for node in nodes if node.tag.split("}")[-1] == tag and node.text and node.text.strip()), "")
            values = {"name": value("name") or value("artifactId") if lower == "pom.xml" else value("PackageId") or value("AssemblyName"),
                      "description": value("description") if lower == "pom.xml" else value("Description")}
            if family == "dotnet":
                metadata["target_frameworks"] = value("TargetFrameworks") or value("TargetFramework")
        elif lower == "go.mod":
            match = re.search(r'^\s*module\s+(?:"([^"\n]+)"|([^\s/][^\s]*))', content, re.M)
            if match:
                values["name"] = match[1] or match[2]
        elif lower == "cmakelists.txt":
            match = re.search(r'^\s*project\s*\(\s*(?:"([^"\n]+)"|([^\s)]+))', content, re.I | re.M)
            if match:
                values["name"] = match[1] or match[2]
        # Gradle, Ruby, Swift, setup.py and go.work can contain executable/dynamic expressions.
        # Identify their family and retain raw text without evaluating values.
        for key in ("name", "description"):
            if isinstance(values.get(key), str) and values[key].strip():
                values[key].encode("utf-8")
                metadata[key] = values[key].strip()[:1000]
    except (ValueError, TypeError, UnicodeError, ET.ParseError, yaml.YAMLError, configparser.Error, RecursionError) as exc:
        warnings.append("Project metadata could not be parsed: " + str(exc)[:240])
    return metadata, warnings
