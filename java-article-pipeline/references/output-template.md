# Output Template

Write the final output in Chinese unless the user asks for another language.

Do not output a separate core point table, source-code deep-dive table, code/configuration table, or coverage matrix. Keep the omission audit internally, but make the visible result centered on copy-pasteable AI prompt cards.

## 1. 文章学习地图

State the article topic in 3-5 sentences. Explain what the learner should understand after studying it.

Include:

- main topic;
- prerequisite knowledge;
- important mechanisms;
- highest-value sections;
- suggested learning order.

## 2. 分章节详细拆解与 AI 深挖提示卡（核心输出）

For each major article section, output every article-derived knowledge point as one AI deep-dive prompt card. Do not only create cards for high-priority points. Every `P-xxx` point must appear in this form.

Each point card has two parts:

1. a compact metadata table for quick scanning;
2. a copy-pasteable prompt text block that converts the table content into a question another AI can answer directly.

Use this exact shape:

````markdown
### 章节：<section title>

#### AI 深挖提示卡：P-001 <topic>

| 字段 | 内容 |
|---|---|
| 结论 | <one atomic article-derived conclusion> |
| 来源 | <source IDs> |
| 类型 / 分类 | <point type; Java taxonomy category> |
| 为什么重要 | <learning, mechanism, production, or interview value> |
| 学习时要追问 | <questions the learner should ask next> |
| 常见误区 | <misunderstanding, boundary, or failure condition; write 无 if none> |
| 和其他知识的关系 | <related mechanisms, prerequisites, or follow-up topics> |
| 源码入口 | <classes / methods / call chain to inspect; use 无 if not source-code-worthy; prefix 外部建议 when not stated by the article> |
| 深挖方向 | <what to inspect in the mechanism or source code; include the details that would otherwise have been in a separate deep-dive checklist> |
| 面试追问角度 | <basic / mechanism / source / scenario angle> |
| 证据等级 | direct / synthesized / inferred |

可复制提问文本：

```text
我在学习 Java 技术栈中的「<topic>」。

文章中的核心结论是：<conclusion>。
这个点来自文章位置：<source IDs>。
它的重要性是：<why it matters>。

请你围绕下面方向深入讲解：
1. 这个机制或概念解决了什么问题；
2. 它的执行流程、关键条件和边界情况是什么；
3. 如果涉及源码，请按关键类 / 方法 / 调用链讲解；
4. 建议源码入口：<source-code entry, or 无>；
5. 深挖方向：<deep-dive direction>；
6. 常见失败场景、误区或生产风险是什么；
7. 面试中可能如何追问；
8. 给一个最小示例帮助理解。

请不要只做概念总结，要按机制、源码入口、边界条件和面试追问展开。
```
````

Rules:

- The prompt text must repeat the important table content, so the user can copy only the text block and still keep the full context.
- Source-code entry points and deep-dive directions belong inside each card, not in a separate table.
- If a source-code entry or deep-dive direction is not explicitly stated by the article, mark it as `外部建议`.
- Do not paste raw code/configuration snippets as a standalone output. If a code block or configuration item carries a core learning point, turn it into a `P-xxx` card and describe the mechanism, risk, and source/deep-dive direction.

## 3. 面试追问清单

Group questions by difficulty:

```markdown
### 基础确认
- ...

### 机制追问
- ...

### 源码追问
- ...

### 场景题
- ...
```

Questions should be answerable from the extracted cards plus clearly labeled extension knowledge.

## 4. 补充建议 AI 提示卡（非原文内容）

Only include this section when related, important, and current supplemental points were identified. These items are not article-derived points and must not be mixed into `P-xxx` cards.

Use `SUP-xxx` cards, not a table:

````markdown
#### AI 深挖提示卡：SUP-001 <topic>

| 字段 | 内容 |
|---|---|
| 补充建议 | <concise supplemental learning point> |
| 关联原文 | <related P IDs or source units> |
| 为什么补充 | <why this fills a learning blind spot> |
| 时效状态 | stable / verified-current / needs-verification |
| 验证说明 | <official source/date when checked, or why stable> |
| 学习 / 面试价值 | <how it helps learning, source-code reading, or interviews> |
| 源码入口 | <classes / methods / call chain, if useful; otherwise 无> |
| 深挖方向 | <what another AI should explain> |

可复制提问文本：

```text
我在学习 Java 技术栈中的「<topic>」。

这不是原文直接覆盖的内容，而是与原文 <related P IDs> 相关的补充建议。
补充点是：<supplemental point>。
为什么需要补充：<why it matters>。
时效状态：<stable / verified-current / needs-verification>。
验证说明：<verification note>。

请你从以下角度深入讲解：
1. 为什么这个补充点和原文主题相关；
2. 当前主流版本或实践是否仍然适用；
3. 如果涉及源码，请说明关键类 / 方法 / 调用链；
4. 它如何补足原文没有讲到的学习盲区；
5. 面试中可能如何追问。
```
````

Rules:

- Use `SUP-xxx` IDs.
- Use related `P-xxx` IDs or source units for `关联原文`, not as evidence for the supplement.
- If the supplement is version-sensitive and not verified, move it to "低置信 / 需人工确认项" instead of presenting it as confirmed.

## 5. 低置信 / 需人工确认项

List:

- article statements that are ambiguous;
- inferred points that need confirmation;
- source-code suggestions not directly stated by the article;
- supplemental suggestion candidates whose currentness could not be verified;
- possible version-specific claims.

If there are no such items, write `无明显低置信项。`
