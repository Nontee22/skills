#!/usr/bin/env python3
"""Prepare, merge, and validate template-shaped Markdown recomposition tasks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


GROUP_ORDER = ["基础确认", "机制追问", "源码追问", "场景题"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="parse source and create chapter slices")
    prepare.add_argument("source", type=Path)
    prepare.add_argument("--template", type=Path, default=Path("output-template.md"))
    prepare.add_argument("--workdir", type=Path, default=Path(".recomposer"))

    merge = sub.add_parser("merge", help="merge generated chapter files")
    merge.add_argument("--workdir", type=Path, default=Path(".recomposer"))
    merge.add_argument("--output", type=Path, default=Path("res.md"))
    merge.add_argument("--title", default=None)

    validate = sub.add_parser("validate", help="validate slices, chapter files, and merged output")
    validate.add_argument("--workdir", type=Path, default=Path(".recomposer"))
    validate.add_argument("--output", type=Path, default=Path("res.md"))

    args = parser.parse_args()
    if args.command == "prepare":
        prepare_task(args.source, args.template, args.workdir)
    elif args.command == "merge":
        merge_task(args.workdir, args.output, args.title)
    elif args.command == "validate":
        validate_task(args.workdir, args.output)


def prepare_task(source: Path, template: Path, workdir: Path) -> None:
    source_text = source.read_text(encoding="utf-8")
    template_text = template.read_text(encoding="utf-8")

    chapters = parse_suggested_order(source_text)
    attach_chapter_blocks(source_text, chapters)
    global_map = extract_block(source_text, r"^## 1\. 文章学习地图\s*$", r"^## 2\. ")
    question_groups = parse_interview_questions(source_text)
    sup_cards = parse_cards(source_text, "SUP", r"^## 4\. 补充建议 AI 提示卡", r"^## 5\. ")
    low_items = parse_low_confidence_items(source_text)

    route_questions(chapters, question_groups)
    route_sup_and_low(chapters, sup_cards, low_items)

    for rel in ["slices", "chapters", "index", "prompts"]:
        (workdir / rel).mkdir(parents=True, exist_ok=True)

    summary = []
    for chapter in chapters:
        slug = f"chapter-{chapter['order']:02d}"
        slice_path = workdir / "slices" / f"{slug}.md"
        output_path = workdir / "chapters" / f"{slug}.md"
        prompt_path = workdir / "prompts" / f"{slug}.txt"

        payload = chapter_payload(chapter, slice_path, output_path, prompt_path)
        summary.append(payload)
        slice_path.write_text(render_slice(chapter, payload, template_text, global_map), encoding="utf-8")
        prompt_path.write_text(render_worker_prompt(payload), encoding="utf-8")

    (workdir / "index" / "chapters.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (workdir / "index" / "global-map.md").write_text(global_map, encoding="utf-8")
    print(f"Prepared {len(summary)} chapter slices in {workdir}")


def merge_task(workdir: Path, output: Path, title: str | None) -> None:
    chapters = load_chapters(workdir)
    global_map = (workdir / "index" / "global-map.md").read_text(encoding="utf-8").strip()
    missing = [c["chapter_output_path"] for c in chapters if not Path(c["chapter_output_path"]).exists()]
    if missing:
        raise SystemExit("Missing chapter outputs:\n" + "\n".join(missing))

    doc_title = title or "按建议学习顺序重组输出文档"
    parts = [
        f"# {doc_title}",
        "",
        "> 本文档由章节切片并行编排后合并生成，顺序以源文档 `### 建议学习顺序` 为准。",
        "",
        "## 文档头部总述",
        "",
        global_map,
        "",
        "### 章节总览学习地图",
        "",
    ]
    for c in chapters:
        parts.append(f"{c['order']}. **{c['title_short']}**（{c['source_range']}）→ {c.get('goal') or '按章节卡片学习'}")
    parts.extend(["", "---", ""])

    for c in chapters:
        parts.append(Path(c["chapter_output_path"]).read_text(encoding="utf-8").strip())
        parts.extend(["", "---", ""])

    output.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Merged {len(chapters)} chapters into {output}")


def validate_task(workdir: Path, output: Path) -> None:
    chapters = load_chapters(workdir)
    problems: list[str] = []
    if not output.exists():
        problems.append(f"missing output file: {output}")
    output_text = output.read_text(encoding="utf-8") if output.exists() else ""

    expected_pids = []
    for c in chapters:
        chapter_path = Path(c["chapter_output_path"])
        if not chapter_path.exists():
            problems.append(f"missing chapter output: {chapter_path}")
            continue
        chapter_text = chapter_path.read_text(encoding="utf-8")
        for heading in [
            "## 1. 文章学习地图",
            "## 2. 分章节详细拆解与 AI 深挖提示卡",
            "## 3. 面试追问清单",
            "## 4. 补充建议 AI 提示卡",
            "## 5. 低置信 / 需人工确认项",
        ]:
            if heading not in chapter_text:
                problems.append(f"{chapter_path} missing heading: {heading}")
        expected_pids.extend(c.get("p_ids", []))

    for pid in expected_pids:
        if output_text.count(pid) == 0:
            problems.append(f"merged output missing {pid}")

    if problems:
        raise SystemExit("Validation failed:\n" + "\n".join(problems))
    print(f"Validation passed: {len(chapters)} chapters, {len(expected_pids)} P cards")


def parse_suggested_order(text: str) -> list[dict]:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "### 建议学习顺序")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("---") or lines[i].startswith("## "))
    chapters = []
    for line in lines[start + 1 : end]:
        match = re.match(
            r"\s*(\d+)\.\s*\*\*(.+?)\*\*(?:（S-(\d+)\s*~\s*S-(\d+)）)?(?:\s*→\s*(.*))?",
            line,
        )
        if not match:
            continue
        order, title, s_start, s_end, goal = match.groups()
        chapters.append(
            {
                "order": int(order),
                "title_short": title.strip(),
                "s_start": int(s_start) if s_start else None,
                "s_end": int(s_end) if s_end else None,
                "source_range": f"S-{int(s_start):02d} ~ S-{int(s_end):02d}" if s_start and s_end else "无显式 S-ID 范围",
                "goal": (goal or "").strip(),
            }
        )
    return chapters


def attach_chapter_blocks(text: str, chapters: list[dict]) -> None:
    matches = list(re.finditer(r"^### 章节：(.+?)\s*$", text, flags=re.M))
    section3 = re.search(r"^## 3\. 面试追问清单\s*$", text, flags=re.M)
    if not section3:
        raise ValueError("Cannot find section: ## 3. 面试追问清单")
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else section3.start()
        block = text[start:end].strip()
        title = match.group(1).strip()
        p_cards = re.findall(r"#### AI 深挖提示卡：(P-\d{3})\s+(.+)", block)
        s_ids = sorted({int(n) for n in re.findall(r"S-(\d+)", block)})
        first_s = min(s_ids) if s_ids else None
        target = find_chapter(chapters, title, first_s)
        if not target:
            continue
        target["source_title"] = title
        target["chapter_block"] = block
        target["p_ids"] = [pid for pid, _ in p_cards]
        target["p_topics"] = {pid: topic.strip() for pid, topic in p_cards}
        if target.get("s_start") is not None:
            target["actual_s_ids"] = [sid for sid in s_ids if target["s_start"] <= sid <= target["s_end"]]
        else:
            target["actual_s_ids"] = s_ids


def find_chapter(chapters: list[dict], title: str, first_s: int | None) -> dict | None:
    for c in chapters:
        if first_s is not None and c.get("s_start") is not None and c["s_start"] <= first_s <= c["s_end"]:
            return c
    for c in chapters:
        if c["title_short"] in title or title.endswith(c["title_short"]):
            return c
    return None


def extract_block(text: str, start_pattern: str, end_pattern: str) -> str:
    start = re.search(start_pattern, text, flags=re.M)
    if not start:
        raise ValueError(f"Cannot find start pattern: {start_pattern}")
    end = re.search(end_pattern, text[start.end() :], flags=re.M)
    if not end:
        raise ValueError(f"Cannot find end pattern: {end_pattern}")
    return text[start.start() : start.end() + end.start()].strip()


def parse_interview_questions(text: str) -> dict[str, list[str]]:
    try:
        block = extract_block(text, r"^## 3\. 面试追问清单\s*$", r"^## 4\. ")
    except ValueError:
        return {group: [] for group in GROUP_ORDER}
    groups: dict[str, list[str]] = {}
    current = None
    for line in block.splitlines():
        heading = re.match(r"^###\s+(.+)$", line)
        if heading:
            current = heading.group(1).strip()
            groups[current] = []
        elif current and line.startswith("- "):
            groups[current].append(line[2:].strip())
    return groups


def parse_cards(text: str, prefix: str, start_pattern: str, end_pattern: str) -> list[dict]:
    try:
        block = extract_block(text, start_pattern, end_pattern)
    except ValueError:
        return []
    pattern = rf"^#### AI 深挖提示卡：({prefix}-\d{{3}})\s+(.+?)\s*$"
    matches = list(re.finditer(pattern, block, flags=re.M))
    cards = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(block)
        card = block[start:end].strip()
        cards.append(
            {
                "id": match.group(1),
                "topic": match.group(2).strip(),
                "refs": re.findall(r"\bP-\d{3}", card),
                "block": card,
            }
        )
    return cards


def parse_low_confidence_items(text: str) -> list[str]:
    start = re.search(r"^## 5\. 低置信 / 需人工确认项\s*$", text, flags=re.M)
    if not start:
        return []
    return [line[2:].strip() for line in text[start.start() :].splitlines() if line.startswith("- ")]


def route_questions(chapters: list[dict], groups: dict[str, list[str]]) -> None:
    for c in chapters:
        c["interview_questions"] = {group: [] for group in GROUP_ORDER}
        keywords = build_keywords(c)
        for group, questions in groups.items():
            for question in questions:
                if any(keyword in question for keyword in keywords):
                    c["interview_questions"].setdefault(group, []).append({"question": question, "match": "推断关联"})
        if not any(c["interview_questions"].values()):
            c["interview_questions"]["机制追问"].append(
                {
                    "question": f"请围绕 {c['title_short']} 的 {c['source_range']} 解释核心机制、边界条件和源码入口。",
                    "match": "章节兜底",
                }
            )


def build_keywords(chapter: dict) -> list[str]:
    words = []
    for topic in chapter.get("p_topics", {}).values():
        for token in re.split(r"[\s/（）()、，,与和的]+", topic):
            if len(token) >= 3 and token not in {"Vue", "Java", "Agent", "核心", "区别", "原理", "作用"}:
                words.append(token)
    manual = {
        "基础": ["核心思想", "数据驱动", "组件化", "MVVM", "ViewModel", "data 必须", "v-bind", "v-model 的区别"],
        "生命周期": ["生命周期", "created", "mounted", "父子组件的生命周期"],
        "响应式": ["响应式", "Object.defineProperty", "Proxy", "nextTick", "异步更新", "computed", "watch", "$set", "Dep.target"],
        "组件通信": ["自定义组件", "多个 v-model", "provide/inject", "props", "插槽"],
        "状态管理": ["Vuex", "Pinia", "状态管理"],
        "Router": ["路由", "动态 import", "返回按钮", "权限"],
        "Vue 3": ["Vue 3", "ref", "reactive", "Teleport", "Patch Flags", "Block Tree", "Composition API"],
        "性能": ["性能", "首屏", "v-for", "key", "index", "虚拟滚动", "SSR", "预渲染", "SEO"],
        "源码": ["Observer", "Dep", "Watcher", "diff", "源码", "调用链"],
        "实战": ["后台管理", "购物车", "弹窗", "表单页", "大型表格", "SPA", "Select", "内存泄漏"],
        "小程序": ["小程序", "页面生命周期", "组件生命周期", "setData", "分包", "WXML", "WXSS", "云开发", "登录", "授权"],
        "微信": ["小程序", "页面生命周期", "组件生命周期", "setData", "分包", "WXML", "WXSS", "云开发", "登录", "授权"],
        "Agent": ["Agent", "工具调用", "function calling", "规划", "记忆", "RAG", "检索", "评测", "多智能体", "上下文"],
        "智能体": ["Agent", "工具调用", "规划", "记忆", "RAG", "检索", "评测", "多智能体", "上下文"],
        "Java": ["JVM", "Spring", "Spring Boot", "并发", "事务", "MyBatis", "Redis", "线程池", "GC", "类加载"],
    }
    for key, extra in manual.items():
        if key in chapter["title_short"] or key in chapter.get("source_title", ""):
            words.extend(extra)
    return sorted(set(words), key=len, reverse=True)


def route_sup_and_low(chapters: list[dict], sup_cards: list[dict], low_items: list[str]) -> None:
    for c in chapters:
        pset = set(c.get("p_ids", []))
        c["sup_blocks"] = [card for card in sup_cards if pset.intersection(card["refs"])]
        c["low_items"] = [
            item
            for item in low_items
            if any(pid in item for pid in pset) or any(card["id"] in item for card in c["sup_blocks"])
        ]
        if any('"外部建议"' in item or "外部建议" in item for item in low_items):
            c["low_items"].append("本章中标记为“外部建议”的源码入口需按实际项目依赖的技术版本验证。")
        inferred = any(q.get("match") == "推断关联" for qs in c["interview_questions"].values() for q in qs)
        fallback = any(q.get("match") == "章节兜底" for qs in c["interview_questions"].values() for q in qs)
        if inferred:
            c["low_items"].append("本章面试追问由总追问清单按关键词推断关联，源追问未显式标注 S-ID/P-ID。")
        if fallback:
            c["low_items"].append("本章存在章节兜底追问；源文档总追问清单未提供直接匹配题。")


def chapter_payload(chapter: dict, slice_path: Path, output_path: Path, prompt_path: Path) -> dict:
    return {
        "order": chapter["order"],
        "title_short": chapter["title_short"],
        "source_title": chapter.get("source_title"),
        "source_range": chapter["source_range"],
        "goal": chapter.get("goal", ""),
        "p_ids": chapter.get("p_ids", []),
        "p_topics": chapter.get("p_topics", {}),
        "actual_s_ids": chapter.get("actual_s_ids", []),
        "interview_questions": chapter["interview_questions"],
        "sup_ids": [card["id"] for card in chapter["sup_blocks"]],
        "low_count": len(chapter["low_items"]),
        "slice_path": str(slice_path),
        "chapter_output_path": str(output_path),
        "prompt_path": str(prompt_path),
    }


def render_slice(chapter: dict, payload: dict, template: str, global_map: str) -> str:
    parts = [
        f"# 章节切片：{chapter['order']}. {chapter['title_short']}",
        "",
        "## 章节元数据",
        "",
        "```json",
        json.dumps(payload, ensure_ascii=False, indent=2),
        "```",
        "",
        "## output-template.md",
        "",
        template.strip(),
        "",
        "## 源文档全局学习地图",
        "",
        global_map.strip(),
        "",
        "## 本章节原文内容范围",
        "",
        chapter.get("chapter_block", "").strip(),
        "",
        "## 本章节相关面试追问",
        "",
    ]
    for group in GROUP_ORDER:
        parts.extend([f"### {group}", ""])
        questions = chapter["interview_questions"].get(group, [])
        parts.extend([f"- {q['question']}（{q['match']}）" for q in questions] or ["- 无"])
        parts.append("")
    parts.extend(["## 本章节相关补充建议卡片", ""])
    parts.extend([card["block"] for card in chapter["sup_blocks"]] or ["无"])
    parts.extend(["", "## 本章节相关低置信 / 需人工确认项", ""])
    parts.extend([f"- {item}" for item in chapter["low_items"]] or ["无明显低置信项。"])
    return "\n".join(parts).rstrip() + "\n"


def render_worker_prompt(payload: dict) -> str:
    return f"""Read `{payload['slice_path']}` and generate a complete Markdown chapter at `{payload['chapter_output_path']}`.

Do not modify other files. Preserve every P-xxx card in the slice.
Use the five output-template sections exactly. Add a chapter-level learning map
with mechanism linkage and one practical deepening angle. Use the slice's
interview questions, SUP cards, and low-confidence items. If a section has no
matching content, write a clear "无..." sentence.

Chapter: {payload['order']}. {payload['title_short']} ({payload['source_range']})
P IDs: {', '.join(payload['p_ids'])}
"""


def load_chapters(workdir: Path) -> list[dict]:
    path = workdir / "index" / "chapters.json"
    chapters = json.loads(path.read_text(encoding="utf-8"))
    return sorted(chapters, key=lambda c: c["order"])


if __name__ == "__main__":
    main()
