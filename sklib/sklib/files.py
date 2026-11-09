"""Deterministic file capabilities and bounded decoding; never execute a file."""
from __future__ import annotations

import codecs
import re
import stat
from pathlib import Path
from .failures import OperationFailure

MAX_BYTES = 2 * 1024 * 1024
ENCODINGS = ("auto", "utf-8", "gb18030", "cp1252", "shift_jis")
DOCUMENT_SUFFIXES = {".md", ".markdown", ".mdx", ".rst", ".txt", ".adoc", ".asciidoc"}
SOURCE_SUFFIXES = set(".py .pyi .js .mjs .cjs .ts .tsx .jsx .vue .svelte .html .htm .css .scss .sass .less .c .h .cc .cpp .cxx .hpp .cs .fs .vb .java .kt .kts .go .rs .rb .php .swift .m .mm .dart .r .R .jl .lua .pl .ps1 .psm1 .psd1 .sh .bash .zsh .fish .bat .cmd .sql .cmake .gradle".lower().split())
CONFIG_SUFFIXES = set(".json .jsonc .yaml .yml .toml .ini .cfg .conf .xml .properties .csv .tsv .csproj .fsproj .vbproj .vcxproj .sln .slnx".split())
BINARY_GROUPS = {
    "image": set(".png .jpg .jpeg .gif .webp .ico .bmp .tif .tiff .avif .heic .psd".split()),
    "document_binary": set(".pdf .doc .docx .xls .xlsx .ppt .pptx .odt .ods .epub".split()),
    "archive": set(".zip .gz .tgz .bz2 .xz .7z .rar .tar .whl .jar .nupkg".split()),
    "executable": set(".exe .dll .so .dylib .pyd .pyc .class .o .obj .a .lib .msi .wasm".split()),
    "media": set(".mp3 .wav .ogg .flac .mp4 .mov .mkv .avi .webm".split()),
    "data_binary": set(".db .sqlite .sqlite3 .bin .npy .npz .parquet .arrow .pkl .pickle .pt .pth .onnx .safetensors .gguf .ttf .woff .woff2".split()),
}


def validate_encoding(encoding: str) -> str:
    if not isinstance(encoding, str) or encoding not in ENCODINGS:
        raise ValueError("encoding must be one of: " + ", ".join(ENCODINGS))
    return encoding


def file_type(path: Path) -> tuple[str, bool]:
    suffix, name = path.suffix.lower(), path.name.lower()
    for category, extensions in BINARY_GROUPS.items():
        if suffix in extensions:
            return category, False
    if suffix == ".svg":
        return "image", True
    if suffix in DOCUMENT_SUFFIXES or name in {"readme", "license", "copying", "notice"}:
        return "document", True
    if suffix == ".ipynb":
        return "notebook", True
    if suffix in CONFIG_SUFFIXES or name in {"go.mod", "go.work", "gemfile", "makefile", "dockerfile", "cmakelists.txt"}:
        return "configuration", True
    if suffix in SOURCE_SUFFIXES:
        return "source", True
    return "unknown", True  # Actual decoding still rejects binary/invalid content.


def file_detail(path: Path, relative: str) -> dict:
    category, readable = file_type(path)
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("Resource must be a regular file")
    return {"path": relative, "category": category, "size_bytes": info.st_size,
            "text_readable": readable and info.st_size <= MAX_BYTES,
            "read_limit_bytes": MAX_BYTES}


def read_text_info(path: Path, max_bytes: int = MAX_BYTES, *, encoding: str = "auto") -> tuple[str, str]:
    validate_encoding(encoding)
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("Resource must be a regular text file")
    if not file_type(path)[1]:
        raise OperationFailure("Binary file type is not supported by the text reader: " + path.suffix.lower(),
            code="binary_file", recovery="查看资源清单中的类型和大小；该文件不能通过文本读取接口打开。")
    with path.open("rb") as stream:
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise OperationFailure(f"File exceeds {max_bytes} bytes: {path.name}", code="file_too_large",
            recovery="该文件超出文本读取上限。先在外部处理为较小的文本资料，再重新扫描。")
    # UTF-32 BOMs share the UTF-16 prefix, so test them first.
    decoder = next((codec for bom, codec in (
        (codecs.BOM_UTF32_LE, "utf-32"), (codecs.BOM_UTF32_BE, "utf-32"),
        (codecs.BOM_UTF16_LE, "utf-16"), (codecs.BOM_UTF16_BE, "utf-16"),
        (codecs.BOM_UTF8, "utf-8-sig")) if raw.startswith(bom)), "utf-8")
    try:
        content = raw.decode(decoder)
    except UnicodeDecodeError as exc:
        if decoder != "utf-8" or encoding in {"auto", "utf-8"}:
            raise OperationFailure("Cannot decode text; use an explicit legacy encoding for non-UTF files",
                code="encoding_error", recovery="确认文件编码，显式选择正确的来源编码或单文件 encoding 后重试。") from exc
        decoder = encoding
        try:
            content = raw.decode(decoder)
        except UnicodeDecodeError as fallback_error:
            raise OperationFailure("Cannot decode text with the selected encoding: " + decoder,
                code="encoding_error", recovery="所选旧编码仍无法读取；检查原文件编码或文件是否损坏。") from fallback_error
    if any(ord(char) < 32 and char not in "\t\n\r\f" for char in content):
        raise OperationFailure("Binary content is not a text resource", code="binary_file",
            recovery="文件包含二进制或非法控制字符。检查文件类型，使用对应程序查看。")
    return content, decoder


def text_lines(content: str, *, keepends: bool = False) -> list[str]:
    """Use physical CR/LF lines; U+2028 and other text remain on their line."""
    lines = re.findall(r"[^\r\n]*(?:\r\n|\r|\n|$)", content)
    if lines and not lines[-1]:
        lines.pop()
    return lines if keepends else [line.rstrip("\r\n") for line in lines]


def is_readme(name: str) -> bool:
    lower = name.lower()
    if lower == "readme":
        return True
    return (lower.startswith(("readme.", "readme_", "readme-"))
            and Path(lower).suffix in DOCUMENT_SUFFIXES)
