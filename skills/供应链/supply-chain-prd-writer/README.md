# supply-chain-prd-writer

供应链软件后台管理系统的需求分析、Plan、HTML 原型、PRD 全流程撰写 skill。

## 适用场景

- 供应链 WMS / OMS / TMS 系统的功能需求文档
- 所有需要输出可协同研发的管理后台 PRD 的项目
- 需要 HTML + Ant Design 静态原型的场景

## 文件结构

```
supply-chain-prd-writer/
├── SKILL.md                                  # skill 主文件（触发词、工作流、原则）
├── README.md                                 # 本文件（版本记录、使用说明）
├── _skillhub_meta.json                       # WorkBuddy skill 元数据
├── agents/
│   └── openai.yaml                          # 子 agent 配置
└── reference/
    ├── requirement-analysis-template.md      # 需求分析文档模板
    ├── plan-template.md                      # Plan 方案模板
    ├── prototype-template.md                 # HTML 原型模板
    └── prd-template.md                      # PRD 模板（10段式）
```

## 安装方式

### WorkBuddy 安装

有两种方式将本 skill 安装到 WorkBuddy：

**方式一：直接复制文件夹（推荐，适用于本地开发/调试）**

将 `supply-chain-prd-writer` 整个文件夹复制到 WorkBuddy 的本地 skill 目录：

```
# Windows
C:\Users\<你的用户名>\.workbuddy\skills\supply-chain-prd-writer

# macOS / Linux
~/.workbuddy/skills/supply-chain-prd-writer
```

复制完成后重启 WorkBuddy（或重新加载 session），输入 `/skills` 确认 `supply-chain-prd-writer` 已出现在列表中。

**方式二：通过 Skill 管理命令安装（适用于已打包的 skill）**

如果本 skill 已发布到内部市场或打包为 `.skill` 文件：

```
/skills
# 在 skill 管理界面中选择"安装 skill"，上传或选择 supply-chain-prd-writer
```

---

### Codex / OpenAI Codex 本地运行时安装

Codex 本地运行时（如通过 `codex` CLI 或 VS Code Codex 插件）加载 skill 的方式与 WorkBuddy 类似，将 skill 文件夹放置到 Codex 的 skill 搜索路径下：

**步骤：**

1. 找到 Codex 的 skill 目录（通常为以下路径之一）：
   ```
   # Windows
   C:\Users\<你的用户名>\.codex\skills\
   # macOS / Linux
   ~/.codex/skills/
   ```
   如果目录不存在，手动创建 `skills` 文件夹。

2. 将 `supply-chain-prd-writer` 整个文件夹复制到上述目录，确保目录结构如下：
   ```
   skills/
   └── supply-chain-prd-writer/
       ├── SKILL.md
       ├── README.md
       ├── _skillhub_meta.json
       ├── agents/
       └── reference/
   ```

3. 重启 Codex 会话，在对话中输入类似以下内容验证 skill 是否已加载：
   ```
   请使用 supply-chain-prd-writer skill 帮我写一份入库功能的 PRD
   ```

> **注意**：Codex 本地运行时对 skill 的支持取决于具体版本。如果 Codex 无法识别本地 skill 文件夹，可将 `SKILL.md` 的内容直接粘贴到对话上下文中作为 system prompt 补充使用。

---

## 版本记录

### v2.0（2026-06-21）

> 本次升级将 `supply-chain-prd-writer` 与 `supply-chain-prd-writer-copy` 合并为统一版本，并全面强化产品经理角色定位和专业性约束。

#### 新增 / 变更

| # | 变更内容 | 影响范围 | 说明 |
|---|---------|---------|------|
| 1 | **YAML 描述重写** | SKILL.md 头部 | 明确"扮演专业供应链产品经理"，终点交付物是 PRD，不关心技术实现 |
| 2 | **新增「角色定位」章节** | SKILL.md | 明确关注什么（业务目标/场景/功能边界/验收标准）和不关心什么（表结构/API/算法/技术选型）；明确 PRD 只回答"做什么"和"为什么做" |
| 3 | **新增「专业性体现」三句话约束** | SKILL.md「角色定位」内 | ① 异常优先于正常流程；② 实际作业角色优先于管理员视角；③ 库存责任归属是需求前置项 |
| 4 | **「北极星目标」重写** | SKILL.md | 从"训练业务人员"改为"扮演专业供应链产品经理"；输出目标从"研发评审、接口联调"改为"产品评审、研发估算、测试设计" |
| 5 | **新增原则第13条：原型阶段强制 HTML + Ant Design** | SKILL.md 原则第13条 | 原型必须是可直接在浏览器中预览的 HTML 静态页面稿；禁止以 Markdown 描述替代 |
| 6 | **新增原则第14条：Ant Design Pro 组件语言强制规范** | SKILL.md 原则第14条（新增） | PRD/Plan/原型描述界面时必须使用 Ant Design Pro 标准组件名（Table、Form、Select 等），不得使用通用提法；适用于所有管理后台项目 |
| 7 | **新增原则第15条：Skill 版本发布日志强制规则** | SKILL.md 原则第15条（新增） | 每次升级必须在 README.md 版本记录中追加更新说明；README.md 是唯一版本发布日志 |
| 8 | **新增原则第16条：异常优先于正常流程** | SKILL.md 原则第16条（新增） | 异常分支和边界情况覆盖必须完整，篇幅不得少于正常流程；只写正常流程视为 PRD 未完成 |
| 9 | **新增原则第17条：实际作业角色强制** | SKILL.md 原则第17条（新增） | 必须明确每个操作的实际执行角色（仓管员/拣货员/复核员/客服等），不得笼统写为"管理员" |
| 10 | **新增原则第18条：库存责任归属前置澄清** | SKILL.md 原则第18条（修改强化） | 涉及库存变动的需求，库存责任归属未厘清前不得进入需求分析阶段 |
| 11 | **新增原则第19条：接受已有阶段产物并继续** | SKILL.md 原则第19条（新增） | 用户提供已有需求分析/Plan/原型时，必须先按模板逐条校验，输出校验报告，通过后才能继续 |
| 12 | **Plan 阶段描述修改** | SKILL.md 阶段2 | "映射到研发可执行对象"改为"映射到产品可验收的交付范围"（功能模块/页面/业务数据对象/状态流转/UC/验收标准） |
| 13 | **PRD 模板第五章新增 UI 规范强制说明** | reference/prd-template.md §5 | 在"页面交互"开头新增强制规范块，未按规范描述视为 PRD 未完成 |
| 14 | **PRD §6.4 改为"操作触发的系统行为"** | reference/prd-template.md §6.4 | 原"后端写入"更名为"操作触发的系统行为"，禁止写入表名/字段名/API 等技术细节 |
| 15 | **PRD §10.4 字段清单改为必填项** | reference/prd-template.md §10.4 | 供应链系统字段清单为必填；只能包含业务级定义，不得包含技术列 |
| 16 | **PRD 新增第十一章"确认结论"** | reference/prd-template.md §11（新增） | 每个 PRD 末尾必须包含确认结论 |
| 17 | **原型模板全面重构为 HTML 原型模板** | reference/prototype-template.md（全面重写） | 原 Markdown 低保真模板全面重写为 HTML 原型模板；明确文件命名规则和 Ant Design CDN 渲染要求 |
| 18 | **新增使用示例场景4：接受已有需求分析文档** | SKILL.md 使用示例 | 用户提供已有需求分析文档时，先校验完整性，通过后继续输出 Plan |
| 19 | **新增使用示例场景5：接受已有 Plan 方案** | SKILL.md 使用示例 | 用户提供已有 Plan 方案时，先校验完整性，通过后继续输出原型和 PRD |
| 20 | **所有"原型"提法统一为"HTML 原型"** | SKILL.md 全文 | 明确交付物形态，避免歧义 |

#### 删除

| # | 删除内容 | 原位置 | 原因 |
|---|---------|-------|------|
| 1 | "原型默认使用 Markdown 多页静态稿" | SKILL.md 阶段3说明 | 原型强制为 HTML，不再提供 Markdown 作为默认格式 |
| 2 | "Markdown 原型用于快速对齐" | SKILL.md 阶段3说明 | Markdown 仅可作为临时讨论格式，不得作为最终交付物 |
| 3 | §10.4"如需字段级细化，再补充"（条件式表述） | reference/prd-template.md | 供应链系统字段清单为必填，不得条件式省略 |
| 4 | "把普通供应链业务人员训练成能站在产品总监视角" | SKILL.md 北极星目标 | 角色定位改为"扮演专业供应链产品经理"，更准确 |

---

### v2.1（2026-06-21）

> 本次升级新增 PDA/移动端原型设计规范，与管理后台的 Ant Design Pro 规范形成完整覆盖。

#### 新增 / 变更

| # | 变更内容 | 影响范围 | 说明 |
|---|---------|---------|------|
| 1 | **新增原则第15条：Ant Design Mobile 组件语言强制规范** | SKILL.md 原则第15条（新增） | PDA/移动端原型及 PRD 描述界面时必须使用 Ant Design Mobile 标准组件名（NavBar、TabBar、List、Picker 等），不得使用通用提法；参考 https://mobile.ant.design/ |
| 2 | **原则第14条后插入新第15条，后续规则重新编号** | SKILL.md 原则第15–20条 | 原第15–19条重新编号为第16–20条，新增 Ant Design Mobile 规范为第15条 |
| 3 | **阶段3原型说明区分 PC 端和 PDA/移动端** | SKILL.md 阶段3 | 管理后台/PC 端原型使用 Ant Design（文件命名 `prototype-p001-*.html`）；PDA/移动端原型使用 Ant Design Mobile（文件命名 `prototype-m001-*.html`）；分别列出各自必须覆盖的组件清单 |

#### 删除

（无）

---

### v2.2（2026-06-21）

> 本次升级将原型从"静态页面稿"升级为"轻交互原型"，并新增 HTML 模板文件强制规范，原型生成从"按描述手写"变为"读取模板填充"。

#### 新增 / 变更

| # | 变更内容 | 影响范围 | 说明 |
|---|---------|---------|------|
| 1 | **废除"静态页面稿"约束，原型升级为轻交互原型** | SKILL.md 原则第13条、阶段3 | 原型默认包含轻量 JS 交互（页面跳转、弹窗/抽屉开关、Tab 切换、表单校验、列表前端 Mock 筛选）；不要求后端数据联动或复杂状态管理 |
| 2 | **新增 `reference/prototype-html/` 目录及 4 个 HTML 模板文件** | reference/prototype-html/（新建） | 新增 `list-page.html`（列表页）、`detail-page.html`（详情页）、`form-page.html`（表单页）、`drawer-modal.html`（抽屉/弹窗组件参考）；skill 生成原型时必须从模板读取并填充占位符，不得从零手写 HTML 结构 |
| 3 | **原则第4条更新：原型强制使用 HTML 模板文件** | SKILL.md 原则第4条 | 原型生成时必须先读取 `reference/prototype-template.md`（原型规范说明），再从 `reference/prototype-html/` 读取对应页面类型的 HTML 模板文件，填充业务数据后输出 |
| 4 | **阶段3原型说明全面更新** | SKILL.md 阶段3 | 删除"不要求可点击模拟（无 JS 交互逻辑）"；新增轻交互能力清单；新增 HTML 模板引用说明；新增"必须从 prototype-html/ 读取模板"强制规则 |
| 5 | **`reference/prototype-template.md` 全面重写** | reference/prototype-template.md | 从"描述性文档（描述原型应该长什么样）"改写为"原型规范说明文档（定义原型标准、模板文件、轻交互规范、Mock 数据规范、品牌色规范）" |
| 6 | **使用示例中的原型生成步骤更新** | SKILL.md 使用示例场景1、场景5 | 原型生成步骤从"按 prototype-template.md 输出"更新为"按 prototype-template.md（规范）并从 prototype-html/ 读取模板输出" |

#### 删除

| # | 删除内容 | 原位置 | 原因 |
|---|---------|-------|------|
| 1 | "不要求可点击模拟（无 JS 交互逻辑）" | SKILL.md 原原则第13条、阶段3说明 | 原型升级为轻交互原型，该约束已废除 |
| 2 | "静态页面稿"提法 | SKILL.md 阶段3 | 原型不再是静态稿，准确提法为"轻交互 HTML 原型页面" |

---

### v1.0（初始版本）

- 四阶段门禁工作流：需求分析 → Plan → HTML 原型 → PRD
- 10段式 PRD 模板
- Mermaid 流程图强制
- 供应链系统边界澄清规则
