---
name: java-article-pipeline
description: End-to-end article learning pipeline for Java technology articles and template-shaped Markdown study documents. Use when Codex needs to extract source-traceable P-xxx AI deep-dive prompt cards from a long Java .txt/.md article, write the result with output-template.md, optionally split an already template-formatted Markdown by "### 建议学习顺序", dispatch chapter workers, preserve P-xxx/SUP-xxx/interview/low-confidence sections, and merge the chapters into a learning-order final document.
---

# Article Learning Pipeline

## Overview

Use this skill as a two-stage learning-material pipeline:

1. **Extract** a raw Java technology article into a complete `output-template.md` style digest with source-traceable `P-xxx` cards.
2. **Recompose** an already template-shaped digest by parsing `### 建议学习顺序`, splitting chapters, optionally dispatching chapter workers, and merging the chapter outputs by learning order.

The two stages can be used separately or together.

## Choose The Mode

- **Raw Java article input**: use extraction mode.
- **Existing template-formatted Markdown input**: use recomposition mode.
- **Raw article plus requested chapter-level learning-order output**: run extraction first, then run recomposition on the generated digest.

Do not run extraction mode on a document that already contains complete `P-xxx` cards unless the user explicitly asks for re-extraction.

## Extraction Mode

Use this mode for long Java `.txt` or `.md` articles.

1. Load required references before extraction:
   - `references/extraction-rules.md`;
   - `references/java-taxonomy.md`;
   - `references/output-template.md`.
2. Prepare a numbered source:

```bash
python java-article-pipeline/scripts/prepare_article.py <article-path>
```

3. Use the generated numbered Markdown, chunk files, manifest, and draft result path.
4. Extract atomic article-derived points section by section. Every `P-xxx` point must have source IDs and evidence level.
5. Keep extension separated:
   - `P-xxx` for article-derived points only;
   - `SUP-xxx` for supplemental suggestions;
   - low-confidence items for inferred/version-sensitive claims.
6. Write the complete result to the manifest `result_path` or to `<article directory>/结果.md`.

Required extraction output:

- `## 1. 文章学习地图`;
- `## 2. 分章节详细拆解与 AI 深挖提示卡（核心输出）`;
- `## 3. 面试追问清单`;
- `## 4. 补充建议 AI 提示卡（非原文内容）`;
- `## 5. 低置信 / 需人工确认项`.

Do not output standalone core-point tables, source-code deep-dive tables, code/config tables, or printed coverage matrices. Fold source-code entries and deep-dive directions into each card.

## Recomposition Mode

Use this mode for a Markdown document that already follows `references/output-template.md` and contains `### 建议学习顺序`.

1. Prepare chapter slices:

```bash
python java-article-pipeline/scripts/recompose_markdown.py prepare <digest.md> --template java-article-pipeline/references/output-template.md --workdir .recomposer
```

2. Inspect `.recomposer/index/chapters.json`:
   - confirm all suggested-order chapters are present;
   - confirm S-ID ranges if present;
   - confirm each chapter has a slice and output path;
   - confirm every source `P-xxx` appears in exactly one chapter.
3. Spawn one worker per chapter when subagent tools are available. Respect concurrency limits.
4. Give each worker only its own `.recomposer/slices/chapter-XX.md` and output path `.recomposer/chapters/chapter-XX.md`.
5. Merge the generated chapter outputs:

```bash
python java-article-pipeline/scripts/recompose_markdown.py merge --workdir .recomposer --output res.md
```

6. Validate when desired:

```bash
python java-article-pipeline/scripts/recompose_markdown.py validate --workdir .recomposer --output res.md
```

## Worker Contract

Each recomposition worker must:

- read only its assigned slice;
- write only its assigned chapter output;
- preserve every `P-xxx` card in metadata-table plus copyable-prompt form;
- rebuild the chapter in the five output-template sections;
- write a chapter-level micro learning map, not a pasted global map;
- include relevant interview questions grouped by difficulty;
- include only chapter-related `SUP-xxx` cards;
- include chapter-related low-confidence items and inference notes;
- write `无...` when a section has no matching content.

Use this worker prompt shape:

```text
Read <slice_path>. Generate a complete Markdown chapter at <chapter_output_path>.
Do not modify other files. Preserve every P-xxx card in the slice. Rebuild the
chapter in the five output-template sections. Add a chapter-level learning map
with mechanism linkage and at least one practical deepening angle. Use the
slice's interview questions, SUP cards, and low-confidence items. If a section
has no matching content, write a clear "无..." sentence.
```

## Routing And Evidence Rules

- Treat `### 建议学习顺序` as canonical final order even if source chapter order differs.
- Match source chapter blocks by S-ID range first, then by chapter title.
- Match `SUP-xxx` by explicit `P-xxx` references. Avoid matching the `P-xxx` substring inside `SUP-xxx`.
- If interview questions have no S-ID/P-ID references, infer with narrow keywords and label the result as inferred.
- If no direct interview question matches a chapter, add a clearly labeled fallback question or write `无直接匹配追问。`.
- Keep all source-code entries labeled `外部建议` when they are not directly stated by the article.
- Treat version-sensitive framework claims as low-confidence unless verified against official docs or source code.

## Quality Bar

- Preserve every article-derived `P-xxx` point.
- Keep supplemental knowledge out of article-derived cards.
- Keep final output in Chinese unless the user asks for another language.
- For local-file extraction, write a result file; do not leave the final artifact only in chat.
- For recomposition, merge from chapter files and check the final output contains every expected `P-xxx`.
