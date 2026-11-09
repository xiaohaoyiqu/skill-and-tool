"""Deterministic multilingual lexical retrieval primitives."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from .files import text_lines

# Query expansion is explicit and inspectable; it is not claimed as semantic AI.
ALIASES = {
    "表格": "table spreadsheet excel csv", "提取": "extract extraction parse",
    "性能": "performance profiling optimization", "优化": "optimize optimization",
    "前端": "frontend ui web", "后端": "backend server api",
    "测试": "test testing unittest pytest", "调试": "debug debugging troubleshoot",
    "代码审查": "code review", "重构": "refactor refactoring",
    "论文": "paper research scientific", "科研": "research scientific",
    "文献": "literature citation bibliography", "搜索": "search retrieval",
    "浏览器": "browser automation", "自动化": "automation workflow",
    "截图": "screenshot capture", "音频": "audio speech", "转文字": "transcribe transcription stt",
    "语音": "speech voice tts", "视频": "video ffmpeg", "音乐": "music audio",
    "写作": "writing prose", "改写": "rewrite editing humanize",
    "AI腔": "humanizer humanize writing", "去AI": "humanizer humanize",
    "去ai": "humanizer humanize", "数据库": "database sql",
    "安全": "security audit", "部署": "deploy deployment",
    "图表": "chart visualization plot", "绘图": "plot diagram visualization",
    "图片": "image picture", "设计": "design ui ux", "笔记": "notes obsidian",
    "专利": "patent disclosure", "翻译": "translation translate",
}
STOP = {"the", "a", "an", "and", "or", "to", "of", "in", "for", "with", "is", "how", "can", "i", "my"}
WORD = re.compile(r"[a-z0-9]+(?:[._+#-][a-z0-9]+)*|[\u3400-\u9fff]+", re.I)
CJK = re.compile(r"^[\u3400-\u9fff]+$")


def normalized(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def tokens(text: str) -> list[str]:
    output: list[str] = []
    for word in WORD.findall(normalized(text)):
        if CJK.match(word):
            # Bigrams find two-character Chinese words on older SQLite versions.
            output.extend(word[i:i + 2] for i in range(len(word) - 1))
            output.extend(word)  # Single-character queries remain possible.
        else:
            output.append(word)
            if any(c in word for c in "-._"):
                output.extend(re.split(r"[-._]", word))
    return output


def query_terms(query: str) -> tuple[list[str], list[str]]:
    literal = list(dict.fromkeys(t for t in tokens(query) if t not in STOP))[:64]
    # Single Han characters make long task descriptions too broad.
    if len(literal) > 1:
        literal = [t for t in literal if not (len(t) == 1 and CJK.match(t))] or literal
    expanded = []
    lowered = normalized(query)
    for alias, terms in ALIASES.items():
        if normalized(alias) in lowered:
            expanded.extend(tokens(terms))
    return literal, list(dict.fromkeys(expanded))[:64]


def match_expression(terms: list[str]) -> str:
    # Never pass user syntax to MATCH. Tokens are individually quoted literals.
    return " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)


def required_expression(terms: list[str] | None) -> str | None:
    """Validate explicit constraints; all literal tokens must match, no aliases."""
    if terms is None:
        return None
    if not isinstance(terms, list) or len(terms) > 8:
        raise ValueError("required_terms must be a list of up to 8 strings")
    words = []
    for term in terms:
        if not isinstance(term, str) or not term.strip() or not 1 <= len(term) <= 80:
            raise ValueError("Each required_terms entry must contain 1..80 characters")
        literal, _ = query_terms(term)
        if not literal:
            raise ValueError("Each required_terms entry must contain searchable words")
        words.extend(literal)
    return " AND ".join(match_expression([word]) for word in dict.fromkeys(words)) or None


def content_hash(content: str) -> str:
    return hashlib.sha256(content.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def snippet(content: str, terms: list[str], width: int = 260) -> dict:
    lines = text_lines(content) or [""]
    words = list(dict.fromkeys(normalized(t) for t in terms))
    score, n, line, low = -1, 0, lines[0], normalized(lines[0])
    for index, current in enumerate(lines):
        lowered = normalized(current)
        matches = sum(t in lowered for t in words)
        if matches > score:
            score, n, line, low = matches, index, current, lowered
        if words and score == len(words):
            break
    positions = [low.find(t) for t in words if t in low]
    start = max(0, min(positions, default=0) - 70)
    return {"text": line[start:start + width], "line": n + 1,
            "truncated": start > 0 or len(line) > start + width, "match_count": max(score, 0)}
