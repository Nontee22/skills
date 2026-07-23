# 🧠 Agent Skills Monorepo

一套面向 **VS Code Copilot Agent** 的领域技能（Skills）集合，覆盖简历改写、技术文章处理、前端设计品味三大方向。

每个 Skill 是一个自包含的 `SKILL.md` 文件（及配套参考资源），通过 Copilot Agent 的 `.github/copilot-instructions.md` 或 `AGENTS.md` 机制加载，使 Agent 在特定场景下获得深度领域知识。

---

## 📦 技能清单

### 一、简历改写类

| Skill | 说明 |
|-------|------|
| **[ai-resume-polish](./ai-resume-polish/)** | AI/大模型/Agent 方向简历项目描述改写 — 问题驱动 + 技术方案 + 量化成果 |
| **[java-resume-polish](./java-resume-polish/)** | Java 后端简历改写 — 架构思考 + 性能优化 + 分布式系统深度体现 |

### 二、文章处理类

| Skill | 说明 |
|-------|------|
| **[article-learning-pipeline](./article-learning-pipeline/)** | 通用技术文章学习管道 — 提取带来源追溯的 P-xxx 学习卡片，按学习顺序重组 |
| **[java-article-pipeline](./java-article-pipeline/)** | Java 技术文章学习管道 — 同通用架构 + Java 领域分类体系 |
| **[article-readability-enhancer](./article-readability-enhancer/)** | 文章可读性增强 — 结构重组 + 表达优化 + 排版增强，**不丢失任何原文内容** |

### 三、设计品味工具集 — [design-taste-toolkit](./design-taste-toolkit/)

一套对抗 AI 模板化设计的前端技能包，覆盖从设计方向推断到动效审查的全链路。

| Skill | 说明 |
|-------|------|
| **[design-direction-inference](./design-taste-toolkit/design-direction-inference/)** | 设计方向推断引擎 — 读取需求简报，反模板化生成高品质落地页/作品集/品牌站 |
| **[editorial-minimal-ui](./design-taste-toolkit/editorial-minimal-ui/)** | 编辑风极简 UI — 温暖单色调色板 + 排版对比 + 扁平便当网格 |
| **[premium-brand-ui](./design-taste-toolkit/premium-brand-ui/)** | 高端品牌 UI — 双边框嵌套 + 流体动效 + 磁吸悬停 + 毛玻璃浮岛导航 |
| **[elite-motion-design](./design-taste-toolkit/elite-motion-design/)** | 精英动效设计（Awwwards 级）— Python 真随机布局 + GSAP ScrollTrigger 高级编排 |
| **[industrial-terminal-ui](./design-taste-toolkit/industrial-terminal-ui/)** | 工业终端 UI — 瑞士排版 × 军用终端美学 × 模拟退化效果 |
| **[motion-craft-engine](./design-taste-toolkit/motion-craft-engine/)** | 动效工艺引擎 — Emil Kowalski 哲学：Spring 物理动画 + 帧率安全 + 组件构建原则 |
| **[animation-reviewer](./design-taste-toolkit/animation-reviewer/)** | 动画审查器 — 十条不可妥协标准，输出问题表 + 通过/阻止裁决 |
| **[animation-glossary](./design-taste-toolkit/animation-glossary/)** | 动画术语词典 — 反向查找：模糊描述 → 精确术语 |
| **[find-skills](./design-taste-toolkit/find-skills/)** | 技能发现器 — 搜索和安装开放 Agent Skills 生态中的技能包 |

---

## 🚀 使用方式

### 方式一：作为 Copilot Agent Instructions 加载

将本仓库克隆到本地后，在项目根目录创建 `.github/copilot-instructions.md`：

```markdown
> 参考 skills 仓库中的技能文件以获取领域知识。
```

或在 `AGENTS.md` / `.agent.md` 中为特定 Agent 指定 skills 路径。

### 方式二：单文件引用

将某个 `SKILL.md` 的内容复制到项目的 `.github/copilot-instructions.md` 中，或直接在对话中引用。

### 方式三：通过 find-skills 发现并安装

使用 `find-skills` 技能搜索开放生态中的其他技能包。

---

## 📁 项目结构

```
skills/
├── README.md                           # ← 本文件
├── skills-overview.md                  # 完整技能清单与用途说明
│
├── ai-resume-polish/                   # AI 简历改写
│   └── SKILL.md
│
├── java-resume-polish/                 # Java 简历改写
│   └── SKILL.md
│
├── article-learning-pipeline/          # 通用文章学习管道
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   │   ├── domain-taxonomy.md
│   │   ├── extraction-rules.md
│   │   └── output-template.md
│   └── scripts/
│       ├── prepare_article.py
│       └── recompose_markdown.py
│
├── java-article-pipeline/              # Java 文章学习管道
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   │   ├── extraction-rules.md
│   │   ├── java-taxonomy.md
│   │   └── output-template.md
│   └── scripts/
│       ├── prepare_article.py
│       └── recompose_markdown.py
│
├── article-readability-enhancer/       # 文章可读性增强
│   └── SKILL.md
│
└── design-taste-toolkit/               # 设计品味工具集
    ├── frontend-ui-rules.md
    ├── design-direction-inference/
    ├── editorial-minimal-ui/
    ├── premium-brand-ui/
    ├── elite-motion-design/
    ├── industrial-terminal-ui/
    ├── motion-craft-engine/
    ├── animation-reviewer/
    ├── animation-glossary/
    └── find-skills/
```

---

## 🧭 分类导航

### 适合谁用？

- **求职者** → `ai-resume-polish` / `java-resume-polish`
- **技术写作者 / 学习者** → `article-learning-pipeline` / `java-article-pipeline` / `article-readability-enhancer`
- **前端开发者 / 设计师** → `design-taste-toolkit` 全家桶

---

## ⚙️ 开发与贡献

每个 Skill 的核心约定：

- `SKILL.md` — YAML frontmatter + Markdown 正文。`name` 为技能标识，`description` 包含触发条件和用途说明。
- `references/` — 参考文件，如分类体系、提取规则、输出模板。
- `scripts/` — 辅助脚本（如有）。
- `agents/` — Agent 配置文件（如有）。

欢迎提交 Issue 或 PR 扩充技能库。

---

## 📄 License

本项目为个人技能积累库，仅供学习参考。
