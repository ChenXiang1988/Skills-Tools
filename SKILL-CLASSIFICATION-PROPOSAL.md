# Skill 分类与治理提案

> 目标：把 `skills/`（114 个 SKILL.md，约 20 个顶层目录）从「按来源随意堆放」收敛为「按领域分类、无重复、与规范一致」。
> 本文件是**提案，不改动任何现有文件**。所有删除/迁移动作列在第 4 节，待拍板后执行。

---

## 0. 结论前置（TL;DR）

| 项 | 现状 | 问题等级 |
|---|---|---|
| `pm-flow-kit` | `skills/pm-flow-kit/` + `packages/pm-flow-kit-codex/` + `packages/pm-flow-kit-workbuddy/` **三份完全同构** | 🔴 P0 违规重复 |
| `pm-html-presentation` | `skills/pm-html-presentation/` 与 `skills/presentation/pm-html-presentation/` **两份镜像** | 🔴 P0 重复 |
| `markitdown` | 同时存在于 `skills/markitdown-skill/` 与 `tools/doc-convert/batch-doc-convert/`（CONVENTIONS §7 已标记待确认） | 🟠 P1 |
| `superpowers` 系列 | 14 处分散（11 个 `superpowers-*` 顶层目录 + `skills/superpowers/` + `skills/meta/` 下 2 个） | 🟠 P1 碎片化 |
| 设计/前端/可视化类 | 9 个散落在 `design/`、`antd-skill/`、`archify`、`mermaid-diagram`、`ardot-ant-icons-import`、`code-first-design-system`、`style-dictionary-token-build`、`zhp-html-prototype`、`pm-html-presentation` | 🟠 P1 散落 |
| `INDEX.md` | 约 30+ 个 skill 未登记，pm-flow-kit 套件数/技能数均错，`_trash_flat_dups/` 残留未清 | 🟠 P2 文档脱节 |

**一句话建议**：先消三处重复副本（P0），再把 superpowers 与设计类各自归并为一个领域目录（P1），最后重写 INDEX.md 并清理回收站（P2）。

---

## 1. 现状盘点

### 1.1 数量
- `skills/` 下 SKILL.md：**114 个**（含 3 处重复副本中的 `skills/pm-flow-kit` 12 个、`pm-html-presentation` 双份 2 个）。
- `packages/` 下 SKILL.md：**24 个**（pm-flow-kit-codex 12 + pm-flow-kit-workbuddy 12）。
- 工作区 SKILL.md 合计约 **138 个**，去重后独立套件/skill 数更少（见第 2 节）。

### 1.2 当前 `skills/` 顶层分布（按位置粗分）

| 位置 | 数量 | 性质 |
|---|---|---|
| `pm/`（含 9 个中文子分类） | 68 | 产品管理知识库，分类清晰 ✅ |
| `supply-chain/` | 3 | 供应链，分类清晰 ✅ |
| `pm-flow-kit/`（skills 内副本） | 12 | ⚠️ 与 packages 重复（违规） |
| `superpowers/` + `superpowers-*`(11) + `meta/superpowers-*`(2) | 14 | ⚠️ 碎片 |
| `presentation/pm-html-presentation` | 1 | 演示（与 `pm-html-presentation` 重复） |
| `pm-html-presentation`（顶层） | 1 | ⚠️ 重复副本 |
| `antd-skill/` | 2 | 设计-组件库 |
| `design/pencil-design` | 1 | 设计 |
| `archify` | 1 | 架构图 |
| `mermaid-diagram` | 1 | 图 |
| `ardot-ant-icons-import` | 1 | 设计-Ardot 图标 |
| `code-first-design-system` | 1 | 设计系统 |
| `style-dictionary-token-build` | 1 | 设计 token |
| `zhp-html-prototype` | 1 | HTML 原型 |
| `markitdown-skill/` | 1 | 文档转换（另在 tools/ 有一份） |
| `teach` | 1 | 教学 |
| `web-access` | 1 | 联网 |
| `wiki-lint` | 1 | Wiki 检查 |
| `calicat-cli-operator` | 1 | CLI 操作 |

---

## 2. 六大结构性问题（带证据）

### 问题 1 — `pm-flow-kit` 三份完全重复（🔴 违反 CONVENTIONS §3）
- `skills/pm-flow-kit/skills/`：12 个（pm-flow, pm-boundary, pm-review, pm-metrics-definition, pm-research, pm-mermaid-diagram, pm-prd, pm-prototype-review, pm-requirement-analysis, pm-html-prototype, humanizer, pm-context-contract）
- `packages/pm-flow-kit-codex/skills/`：同 12 个（SKILL.md 内触发词为 "Codex"）
- `packages/pm-flow-kit-workbuddy/skills/`：同 12 个（SKILL.md 内触发词为 "you"）
- **冲突**：CONVENTIONS §3 明确「套件内已有的 skill，不在 `skills/` 另存独立副本」。`skills/pm-flow-kit/` 是赤裸裸的违规副本。
- **codex vs workbuddy 两版**：skills 清单一致，仅 SKILL.md 触发词不同，属「双平台变体套件」，**合法保留**。

### 问题 2 — `pm-html-presentation` 双份镜像（🔴）
- `skills/pm-html-presentation/` 与 `skills/presentation/pm-html-presentation/` 文件结构完全一致（均含 assets/docs/examples/references/scripts/SKILL.md）。
- 用户记忆确认工作副本在 `skills/presentation/pm-html-presentation/`（已优化的 pakco-html 改名版）。`skills/pm-html-presentation/` 是较早副本，应删除其一。

### 问题 3 — `markitdown` 双位置（🟠 CONVENTIONS §7 待确认）
- `skills/markitdown-skill/` 与 `tools/doc-convert/batch-doc-convert/` 均含完整 SKILL.md + `_skillhub_meta.json` + references + scripts，结构镜像。
- 按 CONVENTIONS §1/§2，带 SKILL.md 的本质是 skill，应归 `skills/`，`tools/` 只放非 skill 脚本。当前 `tools/doc-convert/` 下的副本应迁出或删除。

### 问题 4 — `superpowers` 碎片化（🟠）
- 14 处：11 个 `superpowers-*` 顶层目录（dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, verification-before-completion, writing-skills）+ `skills/superpowers/`（含 using-superpowers）+ `skills/meta/superpowers-brainstorming` + `skills/meta/superpowers-writing-plans`。
- 这是同一套 Anthropic「superpowers」方法论技能集被拆散，应收敛到一个目录。

### 问题 5 — 设计/前端/可视化类散落（🟠）
9 个相关 skill 分布在 5+ 个目录，无统一归属：
`design/pencil-design`、`antd-skill/`、`archify`、`mermaid-diagram`、`ardot-ant-icons-import`、`code-first-design-system`、`style-dictionary-token-build`、`zhp-html-prototype`、`pm-html-presentation`。

### 问题 6 — 索引与回收站（🟠）
- `INDEX.md` 未登记 archify / ardot-ant-icons-import / calicat-cli-operator / code-first-design-system / mermaid-diagram / style-dictionary-token-build / zhp-html-prototype / teach / web-access / wiki-lint / 全部 superpowers-* / markitdown-skill / skills/pm-flow-kit；且把 pm-flow-kit 套件数写成 9 个（实际 12）。
- `_trash_flat_dups/` 含 84 个文件（75 .md），是此前「拉平去重」操作的残留隔离区（里面是 pm/ 下 skill 的 SKILL.md 平铺副本）。当前 pm/ 下这些 skill 完好，**该目录属可回收残留**，但需谨慎（见第 4 节 P2）。

---

## 3. 推荐分类树（目标态）

在 CONVENTIONS §2 已有 `pm/ supply-chain/ meta/ design/ presentation/` 基础上，**扩展二级领域**，覆盖全部散落项：

```
skills/
├── pm/                      # 产品管理（68 个，保持现有 9 个中文子分类）✅
├── supply-chain/            # 供应链（3 个，保持）✅
├── design/                  # 设计/原型/可视化/前端（整合 9 个散落项）
│   ├── antd-skill/          # 套件：ant-design, antd
│   ├── pencil-design        # 原 design/pencil-design
│   ├── archify
│   ├── mermaid-diagram
│   ├── ardot-ant-icons-import
│   ├── code-first-design-system
│   ├── style-dictionary-token-build
│   ├── zhp-html-prototype
│   └── pm-html-presentation # 去重后保留 1 份（建议 presentation/ 那份）
├── engineering/             # 工程/开发方法论（整合 superpowers 14 个）
│   └── superpowers/         # 收敛：using-superpowers + 11 个 superpowers-* + meta 下 2 个
├── agent-ops/               # 智能体自身运作/系统工具（4 个）
│   ├── teach
│   ├── web-access
│   ├── wiki-lint
│   └── calicat-cli-operator
└── content/                 # 文档/内容处理
    └── markitdown-skill     # 从 tools/doc-convert 迁回（CONVENTIONS §7）
```

**关于 `presentation/` 平级的两种处理（待选）：**
- **方案 A（推荐）**：并入 `design/`，因为 presentation 与 prototype、mermaid、archify 同属「设计产物/可视化」，且 pm-flow-kit 内已有 `pm-html-prototype`，分散在 design 与 presentation 会造成不一致。
- **方案 B**：保留 `presentation/` 作为 `design/` 的平级二级（更贴近 CONVENTIONS 现状），仅做去重。

---

## 4. 去重 / 迁移动作清单（按优先级）

### P0 — 立即、低风险（消违规重复）
1. **删除 `skills/pm-flow-kit/`**（违规套件副本，CONVENTIONS §3）。packages 双套件仍在，功能不受影响。
2. **合并 `pm-html-presentation` 双份**：保留 `skills/presentation/pm-html-presentation/`（用户确认工作副本），删除 `skills/pm-html-presentation/`。
3. **markitdown 去重**：保留 `skills/markitdown-skill/`，删除 `tools/doc-convert/batch-doc-convert/` 内的 SKILL.md 副本（或整体迁出；见 §7）。

### P1 — 归并碎片化
4. **superpowers 收敛**：在 `skills/engineering/superpowers/` 下收口 14 个 superpowers-*（移动目录，不改内容）；`skills/meta/` 可退役或留空。
5. **设计类归并**：按第 3 节 `design/` 树移动 9 个 skill（纯目录移动）。

### P2 — 文档与回收站
6. **重写 INDEX.md**：补全全部 skill、修正 pm-flow-kit 套件数（12）、标注 packages 双平台套件、标注 `_trash_flat_dups` 状态。
7. **清理 `_trash_flat_dups/`**：经确认 pm/ 下 skill 完好后，将该残留隔离区移入系统回收站（**非 rm**），并记入 CONVENTIONS 待确认项已解决。

> ⚠️ 所有移动/删除均先备份、分批（≤10/批）、走回收站，不 `rm -rf`。P0 步骤执行前建议再确认一遍。

---

## 5. 对 CONVENTIONS.md / INDEX.md 的修订建议

- **CONVENTIONS §2**：把建议的二级领域从 `pm/ supply-chain/ meta/ design/ presentation/` 扩展为 `pm/ supply-chain/ design/ engineering/ agent-ops/ content/`，并说明 `meta/` 退役。
- **CONVENTIONS §3**：补充「`skills/` 下禁止出现与 `packages/` 同构的套件副本（如 pm-flow-kit）」的显式禁令，并明确「双平台变体套件（codex/workbuddy）允许并存于 packages/」。
- **CONVENTIONS §7**：markitdown 处置结论落定——统一到 `skills/markitdown-skill/`，`tools/doc-convert` 仅保留纯脚本。
- **INDEX.md**：全量重生成（建议脚本化：遍历所有 SKILL.md 自动产出表格，避免再次脱节）。

---

## 6. 待 Martin 拍板的问题

1. `pm-html-presentation` 删除哪一份？我倾向删 `skills/pm-html-presentation/`（保留 `presentation/` 那份工作副本）——是否同意？
2. `presentation/` 并入 `design/`（方案 A）还是保留平级（方案 B）？
3. `superpowers` 收敛到 `engineering/superpowers/` 还是保留 `meta/superpowers/` 命名？
4. P0 三步是否现在执行（我会先备份再走回收站）？
