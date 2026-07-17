# design-system · 来源 / 授权 / 接入说明

> 本目录是 **pm-flow-kit（WorkBuddy 适配版）的内置设计系统**，随套件一起打包提供（内部使用），**不依赖任何外部路径**。

## 1. 来源（Provenance）
- 原始归档：`/Users/martin/Documents/Martinjob/designsys/`
- 设计归属：云仓 WMS/OMS/TMS/BMS 产品矩阵（code-first 团队设计系统）。
- 基底：Web = **Ant Design v5** 公开 token；PDA = **Ant Design Mobile v5.42.2** 真实 `--adm-*` 变量值。
- 组件实现：手写 `.yc-*` 等价片段，仅用于「无框架 / 直出 HTML」场景；能用 antd 真实组件时应优先引 antd。

## 2. 使用范围（Usage Scope）⚠️
- 本 design-system 为云仓项目的**内部专有设计资产**。
- pm-flow-kit 整体为**内部使用套件**：不对外开放、不对外授权、不重新分发。
- design-system 随套件打包仅为「开箱即用」之便，不构成任何对第三方的授权。
- 禁止将 `design-system/` 或其内容对外分发；如确有对外需求，须获云仓项目所有权人授权。

## 3. Token 使用约定（Convention, not mandatory）⚠️
套件 `pm-html-prototype` 以本目录 `design-system/` 作为**唯一 token 来源**；脚手架会把它快照进每个原型，不再自带第二套 token：

| 项目类型 | 推荐 token 源 | 备注 |
|---|---|---|
| 云仓 WMS/OMS/TMS/BMS 或 AntD 系项目 | **本目录** `tokens.css` / `pda/tokens.css` + `.yc-*` 组件 | 视觉一致性最佳 |
| 非云仓 / 通用中后台原型 | 本目录 `tokens.css`（随脚手架快照进原型，通用兜底） | 视觉通用且一致 |
| 用户指定其他设计语言 | 用户/项目提供的规范 | 优先级最高 |

- 推荐：命中云仓/AntD 时，生成原型优先注入 `design-system/tokens.css`（PDA 用 `pda/tokens.css`），并引用 `components.html` 的 `.yc-*` 片段。
- 脚手架已将本目录快照进原型（`prototypes/assets/design-system/`），原型自身只引用这一套 token，不存在第二来源可混用。

## 4. 快照 vs 同步（Snapshot vs Sync）⚠️
- 本目录是 **2026-07-17 从 `designsys/` 复制的冻结快照**。
- `designsys/` 自述为「归档副本，与项目 `design-system/` 同步」——即上游仍会演进。
- 日后上游更新（新增 P1 组件、改 token 值）**不会自动回流**到本套件快照。
- 同步方式：重新从 `designsys/` 复制覆盖本目录，并复核 §3 优先级规则未被破坏。

## 5. 文件地图
| 文件 | 端 | 作用 |
|---|---|---|
| `tokens.css` | Web | 唯一变量源（亮/暗双主题 CSS 变量 + 组件级 token） |
| `DESIGN.md` | Web | 设计简报 + §9 组件库规格索引（给 AI 出码看） |
| `components.html` | Web | 组件画廊：17 个 P0 组件 + 全状态 + 可复制片段，暗/亮切换 |
| `README.md` | — | 设计系统总说明 |
| `pda/tokens.css` | PDA | PDA 设计 token（antd-mobile v5.42.2 真实值，暗色优先） |
| `pda/DESIGN.md` | PDA | PDA 设计简报 |
| `pda/components.html` | PDA | PDA 组件画廊（扫码/大触控/任务列表/TabBar/数字键盘…） |
