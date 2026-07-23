# 前端 UI 开发规范 & AI 使用指南

## 为什么需要这套规则

我本地安装了 5 个前端 UI 视觉风格技能 + 3 个动效质量技能。视觉风格技能各自定义了不同的设计语言，如果没有统一调度，AI 可能会随机混搭（比如 Bento 网格配上 CRT 终端扫描线），输出四不像。动效技能作为跨风格通用层，确保无论选择哪种视觉风格，动效质量都保持高水平。

**核心原则：** 每次只走一条设计路线，不能混搭多种风格。动效层与风格层是叠加关系，不冲突。

---

## AI 工作流（按此顺序执行）

### Step 1 — 判断需求，选主技能

接到前端 UI 任务后，先分析需求属于哪种类型，激活对应的**主技能**：

| 需求类型 | 激活的主技能 | 适合场景 |
|---------|------------|---------|
| 高端品牌/SaaS/Agency 官网 | `premium-brand-ui` | 产品 Landing Page、品牌展示、Awwwards 级页面 |
| 极简编辑风/工具型产品 | `editorial-minimal-ui` | 文档站、SaaS 后台、个人博客、Notion/Linear 风格 |
| 竞赛级/强动效/创意展示 | `elite-motion-design` | Awwwards 参赛作品、创意工作室、强交互页面 |
| 工业风/军事终端/数据看板 | `industrial-terminal-ui` | 数据仪表盘、技术文档、军事/航空风格界面 |
| **不确定/需要推理** | `design-direction-inference`（总控制器） | 它会自动推断设计方向，再委派给具体风格 |

> **默认选择：** 如果不确定走什么风格，先激活 `design-direction-inference`，它会输出一行"Design Read"告诉你它推断的方向，你确认后再继续。

### Step 2 — 禁用其他风格规则

选定一个主技能后，**忽略其他所有风格技能的具体规则**，只遵循当前主技能的指令。

例如：
- 选了 `editorial-minimal-ui` → 不遵循 `premium-brand-ui` 的双嵌套边框规则
- 选了 `premium-brand-ui` → 不遵循 `editorial-minimal-ui` 的禁渐变规则
- 选了 `industrial-terminal-ui` → 不遵循其他任何技能的圆角/阴影规则

### Step 3 — 技术栈统一

所有前端 UI 任务默认使用：
- **框架：** React / Next.js
- **样式：** Tailwind CSS
- **动效：** Motion（motion/react），GSAP 用于复杂 ScrollTrigger
- **图标：** @phosphor-icons/react

### Step 4 — 输出前检查

对照所选主技能的 Pre-Flight Check（如果有的话），确保没有违反该风格的禁忌规则。

### Step 5 — 动效质量（跨风格通用层）

选好视觉风格后，所有动效/交互代码必须遵循以下 3 个动效技能的质量标准（与视觉风格不冲突，叠加使用）：

| 技能 | 用途 | 何时用 |
|------|------|--------|
| `motion-craft-engine` | 动效哲学基础 — easing 曲线、时长规范、spring 参数 | 编写任何动画/过渡代码时 |
| `animation-reviewer` | 动效审查 — 按 10 条硬标准严格审查动效代码 | 动效代码完成后，输出前 |
| `animation-glossary` | 动效术语表 — 将模糊描述映射为精确术语 | 不确定动效名称时（如"弹出来的那个效果叫什么"） |

> motion-craft-engine 的核心理念来自 Emil Kowalski（Vercel/Linear 设计师）：动效不是"能用就行"，而是"感觉对才行"。animation-reviewer 引用 STANDARDS.md 中的精确数值（easing 曲线表、时长预算表、spring 配置等）。

---

## 常见错误（AI 不要犯）

| 错误 | 正确做法 |
|------|---------|
| 选了 `editorial-minimal-ui` 却加了玻璃拟态效果 | editorial-minimal-ui 禁止渐变和玻璃效果 |
| 选了 `premium-brand-ui` 却用 Inter 字体 | 它明确禁止 Inter/Roboto/Arial |
| 选了 `industrial-terminal-ui` 却用圆角 | 它要求所有角落 90° 直角 |
| 混用多个技能的规则 | 一次只能用一个主技能 |
| 用 `design-direction-inference` 推理后跳过确认 | 输出 Design Read 后等用户确认再动手 |

---

## 快速参考

```
用户说 "做个官网" → 激活 design-direction-inference → 输出 Design Read → 等确认 → 动效层激活 motion-craft-engine
用户说 "Linear 风格" → 激活 editorial-minimal-ui → 动效层激活 motion-craft-engine
用户说 "高端品牌站" → 激活 premium-brand-ui → 动效层激活 motion-craft-engine
用户说 "很炫的动效" → 激活 elite-motion-design → 动效层叠加 motion-craft-engine + animation-reviewer
用户说 "工业风"    → 激活 industrial-terminal-ui → 动效层激活 motion-craft-engine
用户说 "审查动效"  → 激活 animation-reviewer（独立使用）
```
