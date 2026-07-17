---
name: code-first-design-system
description: 用于为 code-first（产品直接出 HTML / AI 生成 UI）团队交付设计系统。产出包含：Ardot 画布规范看板、给
  AI 编码代理看的 DESIGN.md 设计简报、以及 tokens.css 变量文件。需锚定真实开源组件库（Ant Design / TDesign
  等），不凭空造值。
agent_created: true
disable: true
---

# Code-First 设计系统交付

## 概述

本 skill 用于把「设计系统」交付给**不画原型、直接写 HTML / 由 AI 生成代码**的团队。交付物包含三部分：

1. **画布规范看板**（Ardot）：可视化对齐与人工眼检闸门，给不读代码的人看。
2. **DESIGN.md**：给 AI 编码代理（Cursor / Claude Code / v0）看的设计约束简报，防止风格漂移。
3. **tokens.css**：双主题 CSS 变量，作为代码层的硬约束。

这套流程的核心思想是：**先锚定真实可引用的设计系统（Ant Design / TDesign / Carbon 等），再在画布上把 token 和组件样本打样，最后把约束写成 md + css 喂给代码代理。**

## 何时使用

出现以下任一请求时触发：

- "给我设计系统" / "输出设计系统" / "设计系统方案"
- "产品直接出 HTML，还要设计系统吗？"（回答是，并给出这套流程）
- "DESIGN.md / tokens.css / 组件库" 相关交付
- 团队是 code-first，需要把视觉一致性落到代码侧

## 前置问题（必须确认）

动手前先确认 3 个分叉点，避免返工：

1. **设备形态**：桌面后台 / 手持 PDA / 移动端？这会重写间距、触控热区、字阶。
2. **主题默认**：亮色优先 / 暗色优先 / 双主题？PDA 通常暗色优先，桌面后台通常亮色优先。
3. **组件基底**：Ant Design v5 / TDesign / 其他？直接决定色值、圆角、字号、栅格。
4. **交付范围**：画布看板 / DESIGN.md / tokens.css 三件套，还是只要其中某几项？

## 工作流

### Step 1：锚定真实参考

- 如果用户没指定，先搜索互联网上的真实设计系统（Ant Design / TDesign / Semi / Arco / IBM Carbon / Salesforce SLDS）。
- 记录关键真实值：主色、语义色、圆角、字号、栅格、行高。禁止臆造。
- 与桌面后台 / PDA 的差异化需求区分开：同品牌色，但 surface / 触控 / 字阶可重写。

### Step 2：创建画布规范看板

1. 使用 `mcp__ardot__create_design` 创建新文件。
2. 文件加载后，使用 `mcp__ardot__fetch_file_info` 确认 fileId，使用 `mcp__ardot__locate_available_space` 定位空位。
3. 用 `mcp__ardot__batch_edit` 搭建 8 个板块：
   - Header（标题 + 组件基底 + 亮/暗双主题说明）
   - 色彩 Token（品牌色阶、语义色、surface、文字）
   - 字体排印（字阶、字重、行高、字体族）
   - 间距栅格（4px 基线 + 主档）
   - 圆角与阴影（sm/base/lg/pill + 三级抬升）
   - 组件矩阵-暗（或主题默认色下的组件样本）
   - 组件矩阵-亮（对照主题）
   - 禁止项 Do / Don't
4. 每个 batch 操作不超过 25 个；若跨 batch 引用节点，必须使用显式节点 ID（上一批的绑定名会失效）。

### Step 3：编写 DESIGN.md

- 文件放在项目目录的 `design-system/DESIGN.md`（或按设备分子目录如 `design-system/pda/DESIGN.md`）。
- 必须包含：设计目标、色彩、字体、间距/触控、圆角/阴影、组件规则、禁止项、出码约束。
- 所有色值/字号/圆角必须对应 `tokens.css` 中的变量，禁止写不一致的硬编码。

### Step 4：编写 tokens.css

- 文件与 DESIGN.md 同目录。
- 默认主题根据设备形态选择：
  - 桌面后台：`:root` 为亮色，`[data-theme="dark"]` 覆盖暗色。
  - PDA：`:root` 为暗色，`[data-theme="light"]` 覆盖亮色。
- 变量分层：品牌色阶、语义色、surface、文字、字体、间距、触控热区、圆角、阴影、组件尺寸。
- 组件必须引用变量，不能写死。

### Step 5：校验

1. `mcp__ardot__capture_layout`（`problemsOnly: true`）检查重叠、裁剪、行高异常。
2. `mcp__ardot__capture_screenshot` 对关键区块截图，人工核验视觉。
3. 每区最多修复 2 次；≤4px 的渲染抖动可忽略。

### Step 6：交付

- 向用户呈现：Ardot 文件 URL、DESIGN.md 路径、tokens.css 路径。
- 说明画布看板 vs DESIGN.md 的分工：看板是可视化闸门，DESIGN.md + CSS 是代码层硬约束。

## Ardot 实操陷阱

本流程已多次踩坑，务必注意：

- **编辑工具**：使用 `mcp__ardot__batch_edit`。`mcp__ardot-design__batch_edit` 可能报 `NO_ADAPTER`（适配器未连）。
- **透明度**：`fills` 的颜色对象**不接受 `a` 键**，alpha 必须放在 fill 条目的 `opacity` 字段。例如：
  ```json
  { "type": "SOLID", "color": { "r": 0, "g": 0, "b": 0 }, "opacity": 0.88, "visible": true, "blendMode": "NORMAL" }
  ```
- **对齐属性**：`counterAxisAlignItems` 只接受 `MIN` / `MAX` / `CENTER` / `BASELINE`，不接受 `START` / `END`。
- **绑定名失效**：`I("2:3", ...)` 返回的绑定名只在**当前 batch 内**有效；下一批必须改用显式节点 ID（如 `"2:12"`）。
- **文字颜色**：`fill` 不支持 `rgba()` 字符串，必须传 hex。
- **SVG 文本**：`<text>` 在 Ardot 中解析不稳定，中心文字建议用 Ardot 文本节点覆盖，而非 SVG 内文字。

## 推荐文件结构

```
design-system/
├── DESIGN.md          # 桌面/通用设计简报
├── tokens.css         # 桌面/通用 CSS 变量
└── pda/
    ├── DESIGN.md      # PDA 手持终端设计简报
    └── tokens.css     # PDA CSS 变量（暗色默认）
```

## 相关 skill

- `ardot-design-core`：画布编辑与校验工具。
- `ardot-ui-design`：组件与布局最佳实践。
- 如用户要求安装/引用其他组件库，先搜索 `find-skills` 或 marketplace。
