# 云仓设计系统 · 说明

> code-first 团队设计系统。产品**直接出 HTML**，无原型 / 视觉稿阶段。本系统提供「可抄的 token + 组件片段 + 规格约束」，让 AI 直出 HTML 不跑偏、风格统一。

## 1. 适用范围

- 产品矩阵：云仓 **WMS / OMS / TMS / BMS**（中后台、数据密集型企业级）
- 两种形态：
  - **Web 端**——桌面中后台，基底 **Ant Design v5**
  - **PDA 端**——仓库现场手持终端（竖屏 / 暗色优先），基底**待重锚 Ant Design Mobile**

## 2. 文件地图

| 文件 | 端 | 作用 |
|---|---|---|
| `tokens.css` | Web | 唯一变量源（亮/暗双主题 CSS 变量 + 组件级 token） |
| `DESIGN.md` | Web | 设计简报 + §9 组件库规格索引 |
| `components.html` | Web | 组件画廊：17 个 P0 组件实例 + 全状态 + 可复制片段，暗/亮一键切换 |
| `pda/tokens.css` | PDA | PDA 设计 token（antd-mobile v5.42.2 真实值，暗色优先 + 亮色覆盖） |
| `pda/DESIGN.md` | PDA | PDA 设计简报（基底 = Ant Design Mobile） |
| `pda/components.html` | PDA | PDA 组件画廊：扫码入口/大触控按钮/任务列表/状态标签/TabBar/底部扫码栏/数字键盘/Toast/快捷入口，暗/亮切换 + 可复制片段 |

## 3. 怎么用（code-first 三步）

1. 页面 `<head>` 引 `tokens.css`（或把变量拷进你们的构建）。
2. 打开 `components.html` 找组件 → 点右上「复制」拿片段 → 粘进页面，改文案/数据。
3. 不确定用法 / 状态 / Do-Don't 时查 `DESIGN.md` 对应章节。

主题切换：Web 根节点加 `data-theme="dark"` 切暗色；PDA 默认暗色，加 `data-theme="light"` 切亮色。

## 4. 当前进度

- **Web 组件库 P0（已交付）**：Button / Input / InputNumber / Select / DatePicker / Checkbox&Radio / Switch / Table / Tag(业务状态) / Badge / Modal / Drawer / Alert / Progress / Tabs / Statistic(KPI) / 业务状态色板。
- **Web P1（规划中）**：Form / Tooltip / Dropdown / Menu / Steps / Pagination / Message / Notification / Descriptions / List / Empty / Avatar / Upload / Result。
- **PDA**：已重锚到 **Ant Design Mobile v5.42.2**（暗色优先，真实 `--adm-*` 变量值），组件库 `pda/components.html` 已交付：扫码入口卡 / 大触控按钮 / 任务列表行 / 状态标签 / TabBar / 底部扫码栏 / 数字键盘 / Toast / 圆形快捷入口，含状态 + 可复制片段。

## 5. 画布参考看板（ardot，可选）

- WMS 数据看板：`704274914685818`
- PDA 设计系统看板：`704278532183611`
- Web 组件库（空壳，未填组件）：`704365892284167`

> 看板是人工眼检 / 评审沟通物，**非代码来源**。PNG 导出需 ardot 连接正常时再补。

## 6. 核心约束（摘要）

- **不凭空造组件**：通用件优先引 AntD / antd-mobile 设计语言；只自建云仓特化件（扫码、任务卡、业务状态色）。
- **一套体系两种形态**：Web 与 PDA 共享 AntD 品牌 / 语义色，surface / 触控 / 字阶按端重写。
- **主色真值**：品牌蓝 `#1677FF` 为 Web / PDA 共享锚点；Web 暗色 `#1668DC`，PDA 暗色 `#3086FF`（antd-mobile 暗底提亮，属预期）。功能色：Web 锚 AntD v5（success `#52C41A` / warning `#FAAD14` / error `#FF4D4F`）；PDA 锚 antd-mobile（暗 success `#34B368` / warning `#FFA930` / danger `#FF4A58`）。

## 7. 维护

- 变量只改 `tokens.css`；组件片段只改 `components.html`；规格只改 `DESIGN.md`；PDA 对应改 `pda/` 下两份。
- 归档副本：`/Users/martin/Documents/Martinjob/designsys/`（与本项目 `design-system/` 同步）。
