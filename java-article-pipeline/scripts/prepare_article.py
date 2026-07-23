#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)\s*([A-Za-z0-9_+.#-]*)?.*$")


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def read_text(path: Path, encoding: str) -> str:
    if encoding != "auto":
        return path.read_text(encoding=encoding)

    for candidate in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=candidate)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def unit_kind_suffix(kind: str, level: int | None = None) -> str:
    if kind == "heading":
        return f"H{level}"
    return {
        "paragraph": "P",
        "list": "LIST",
        "table": "TABLE",
        "code": "CODE",
    }[kind]


def make_unit(index: int, kind: str, content: str, level: int | None = None, lang: str = "") -> dict:
    suffix = unit_kind_suffix(kind, level)
    return {
        "id": f"S{index:04d}-{suffix}",
        "kind": kind,
        "level": level,
        "lang": lang,
        "content": content.strip("\n"),
    }


def flush_buffer(units: list[dict], buffer: list[str], kind: str, index: int) -> int:
    content = "\n".join(buffer).strip()
    if content:
        units.append(make_unit(index, kind, content))
        return index + 1
    return index


def parse_units(text: str) -> list[dict]:
    lines = normalize_newlines(text).split("\n")
    units: list[dict] = []
    buffer: list[str] = []
    buffer_kind = "paragraph"
    index = 1
    in_code = False
    code_fence = ""
    code_lang = ""
    code_buffer: list[str] = []

    for line in lines:
        fence_match = FENCE_RE.match(line)
        if in_code:
            code_buffer.append(line)
            if fence_match and fence_match.group(1).startswith(code_fence[0]):
                content = "\n".join(code_buffer)
                units.append(make_unit(index, "code", content, lang=code_lang))
                index += 1
                in_code = False
                code_fence = ""
                code_lang = ""
                code_buffer = []
            continue

        if fence_match:
            index = flush_buffer(units, buffer, buffer_kind, index)
            buffer = []
            buffer_kind = "paragraph"
            in_code = True
            code_fence = fence_match.group(1)
            code_lang = fence_match.group(2) or ""
            code_buffer = [line]
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            index = flush_buffer(units, buffer, buffer_kind, index)
            buffer = []
            buffer_kind = "paragraph"
            level = len(heading_match.group(1))
            units.append(make_unit(index, "heading", heading_match.group(2), level=level))
            index += 1
            continue

        if not line.strip():
            index = flush_buffer(units, buffer, buffer_kind, index)
            buffer = []
            buffer_kind = "paragraph"
            continue

        line_kind = "table" if line.lstrip().startswith("|") else "list" if LIST_RE.match(line) else "paragraph"
        if buffer and line_kind != buffer_kind:
            index = flush_buffer(units, buffer, buffer_kind, index)
            buffer = []
        buffer_kind = line_kind
        buffer.append(line)

    if in_code and code_buffer:
        units.append(make_unit(index, "code", "\n".join(code_buffer), lang=code_lang))
        index += 1

    flush_buffer(units, buffer, buffer_kind, index)
    return units


def render_unit(unit: dict) -> str:
    meta = unit["kind"].upper()
    if unit["kind"] == "heading":
        meta = f"HEADING level={unit['level']}"
    elif unit["kind"] == "code":
        meta = f"CODE lang={unit['lang'] or 'plain'}"

    return f"### [{unit['id']}] {meta}\n\n{unit['content']}\n"


def write_numbered(path: Path, source: Path, units: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        f"# Numbered Source: {source.name}",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Source path: `{source}`",
        f"- Source units: {len(units)}",
        "",
        "## Source Units",
        "",
    ]
    for unit in units:
        parts.append(render_unit(unit))
    path.write_text("\n".join(parts), encoding="utf-8")


def split_chunks(units: list[dict], max_chars: int) -> list[list[dict]]:
    chunks: list[list[dict]] = []
    current: list[dict] = []
    current_len = 0

    for unit in units:
        rendered_len = len(render_unit(unit))
        if current and current_len + rendered_len > max_chars:
            chunks.append(current)
            current = []
            current_len = 0
        current.append(unit)
        current_len += rendered_len

    if current:
        chunks.append(current)
    return chunks


def write_chunks(chunk_dir: Path, source: Path, units: list[dict], max_chars: int) -> list[dict]:
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunks = split_chunks(units, max_chars)
    manifest = []

    for idx, chunk_units in enumerate(chunks, start=1):
        start_id = chunk_units[0]["id"]
        end_id = chunk_units[-1]["id"]
        chunk_path = chunk_dir / f"chunk-{idx:03d}-{start_id}-to-{end_id}.md"
        parts = [
            f"# Chunk {idx:03d}: {source.name}",
            "",
            f"- Source range: {start_id} to {end_id}",
            f"- Unit count: {len(chunk_units)}",
            "",
        ]
        for unit in chunk_units:
            parts.append(render_unit(unit))
        chunk_path.write_text("\n".join(parts), encoding="utf-8")
        manifest.append(
            {
                "chunk": idx,
                "path": str(chunk_path),
                "start_id": start_id,
                "end_id": end_id,
                "unit_count": len(chunk_units),
            }
        )

    return manifest


def write_result_draft(
    path: Path,
    source: Path,
    numbered_path: Path,
    manifest_path: Path,
    units: list[dict],
    chunks: list[dict],
    overwrite: bool = False,
) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return False

    parts = [
        f"# Java 长文核心知识提取结果：{source.name}",
        "",
        "> 状态：待完成。此文件由准备脚本创建，最终提取完成前必须替换为完整结果。",
        "",
        "## 输入与中间产物",
        "",
        f"- 原文：`{source}`",
        f"- 编号源文件：`{numbered_path}`",
        f"- Manifest：`{manifest_path}`",
        f"- 原文单元数：{len(units)}",
        f"- Chunk 数：{len(chunks)}",
        "",
        "## 写作要求",
        "",
        "- 按 `references/output-template.md` 写完整结果。",
        "- 每个原文派生点必须带来源 ID，并以 AI 深挖提示卡呈现。",
        "- 每张卡必须包含可复制粘贴给其他 AI 的提问文本。",
        "- 源码入口和深挖方向合并到对应卡片中，不输出单独的源码深挖清单表。",
        "- 不输出核心点总表、代码与配置点表或覆盖矩阵。",
        "- 完成前确认内部覆盖 ledger 不存在 `not-covered-risk`。",
        "",
        "## 分批写入要求",
        "",
        "- 如果结果很长，不要等全部分析结束后一次性写入。",
        "- 按 chunk 或文章主要章节分批写入本文件。",
        "- 每批写入后记录已覆盖的 source ID 范围和 point ID 范围。",
        "- `P-xxx` 编号必须全局连续，不能在每个批次重新从 `P-001` 开始。",
        "- 可以临时创建 `<结果文件名>.part-001.md` 等分批文件，但最终必须合并回本文件。",
        "- 不要用 shell heredoc 追加大段 Markdown；内容里的 `$` 和反引号可能被 shell 解释。",
        "- 不要用 Edit 猜测文件尾部内容；Edit 需要 old_string 与文件内容逐字节匹配。",
        "- 优先使用直接文件写入或短 Python helper 以 UTF-8 读写结果文件，写完后回读文件尾部确认。",
    ]
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return True


def write_manifest(
    path: Path,
    source: Path,
    numbered_path: Path,
    result_path: Path,
    result_draft_created: bool,
    units: list[dict],
    chunks: list[dict],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": str(source),
        "numbered_source": str(numbered_path),
        "result_path": str(result_path),
        "result_draft_created": result_draft_created,
        "unit_count": len(units),
        "kind_counts": {},
        "chunks": chunks,
    }
    for unit in units:
        payload["kind_counts"][unit["kind"]] = payload["kind_counts"].get(unit["kind"], 0) + 1

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def default_result_path(article: Path) -> Path:
    candidate = article.with_name("结果.md")
    if candidate == article:
        return article.with_name(f"{article.stem}.结果.md")
    return candidate


def main() -> int:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Number a Java article for source-traceable extraction.")
    parser.add_argument("article", type=Path, help="Input .txt or .md article")
    parser.add_argument("--out", type=Path, help="Output numbered markdown path")
    parser.add_argument("--chunk-dir", type=Path, help="Directory for chunk files")
    parser.add_argument("--manifest", type=Path, help="Output manifest JSON path")
    parser.add_argument("--result", type=Path, help="Final result markdown path, default: <article-dir>/结果.md")
    parser.add_argument("--force-result", action="store_true", help="Overwrite an existing result draft")
    parser.add_argument("--max-chars", type=int, default=8000, help="Approximate max characters per chunk")
    parser.add_argument("--encoding", default="auto", help="Input encoding, default: auto")
    args = parser.parse_args()

    article = args.article.resolve()
    if article.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise SystemExit("Only .txt, .md, and .markdown files are supported.")
    if not article.exists():
        raise SystemExit(f"Input file not found: {article}")

    text = read_text(article, args.encoding)
    units = parse_units(text)
    if not units:
        raise SystemExit("No source units were parsed from the article.")

    numbered_path = args.out.resolve() if args.out else article.with_name(f"{article.stem}.numbered.md")
    chunk_dir = args.chunk_dir.resolve() if args.chunk_dir else article.with_name(f"{article.stem}.chunks")
    manifest_path = args.manifest.resolve() if args.manifest else article.with_name(f"{article.stem}.manifest.json")
    result_path = args.result.resolve() if args.result else default_result_path(article)

    write_numbered(numbered_path, article, units)
    chunks = write_chunks(chunk_dir, article, units, args.max_chars)
    result_draft_created = write_result_draft(
        result_path,
        article,
        numbered_path,
        manifest_path,
        units,
        chunks,
        overwrite=args.force_result,
    )
    write_manifest(manifest_path, article, numbered_path, result_path, result_draft_created, units, chunks)

    print(f"Numbered source: {numbered_path}")
    print(f"Chunk directory: {chunk_dir}")
    print(f"Manifest: {manifest_path}")
    print(f"Result file: {result_path}")
    print(f"Result draft: {'created' if result_draft_created else 'exists'}")
    print(f"Source units: {len(units)}")
    print(f"Chunks: {len(chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
