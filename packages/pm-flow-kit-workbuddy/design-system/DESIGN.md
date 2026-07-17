# 云仓中后台设计系统 · DESIGN.md（AI 出码设计简报）

> 用途：本文件是给 AI 编码代理（Cursor / Claude Code / v0 等）看的**设计约束简报**。
> 团队走 code-first，产品直接出 HTML，无原型 / 视觉稿。本文件用于约束直出代码的视觉一致性，
> **替代不了 Ant Design 真实组件库**——能用 antd 组件就别手写。
> 所有取值锚定 **Ant Design v5** 公开 token，不臆造。

---

## 1. 设计哲学（为什么这么定）

- 数据密集型中后台（WMS / OMS / TMS / BMS），信息密度优先，扫读效率 > 装饰。
- 基底组件库 = **Ant Design v5**（真实可依赖，token 体系成熟、主题切换完善）。
- Token 双层：原始层（颜色 / 字号 / 间距的"原料"）与语义层（primary / error / success 等"用途"）分离，便于换肤。
- 亮 / 暗双主题；暗色用于大屏监控 / 夜间作业，统一走 `darkAlgorithm`，不手动调色。
- 颜色 / 字号 / 间距一律引用 `tokens.css` 的 `var(--xxx)`，**禁止硬编码魔法值**。

## 2. 色彩（Color）

### 2.1 语义主色（亮 / 暗）

| Token | 亮色 | 暗色 | 用途 |
|---|---|---|---|
| `--color-primary` | `#1677FF` | `#1668DC` | 主操作、选中、链接主色 |
| `--color-primary-hover` | `#4096FF` | `#3C89F2` | 主色 hover |
| `--color-primary-active` | `#0958D9` | `#1F5FB0` | 主色按下 |
| `--color-success` | `#52C41A` | `#49AA19` | 成功 / 已入库 / 正常 |
| `--color-warning` | `#FAAD14` | `#D89614` | 警告 / 待处理 |
| `--color-error` | `#FF4D4F` | `#FF4D4F` | 错误 / 失败 / 异常 |
| `--color-info` | `#1677FF` | `#1668DC` | 信息 |
| `--color-link` | `#1677FF` | `#1668DC` | 文字链接 |

### 2.2 中性色（文字 / 背景 / 边框）

| Token | 亮色 | 暗色 |
|---|---|---|
| `--color-text` | `rgba(0,0,0,0.88)` | `rgba(255,255,255,0.85)` |
| `--color-text-secondary` | `rgba(0,0,0,0.65)` | `rgba(255,255,255,0.65)` |
| `--color-text-tertiary` | `rgba(0,0,0,0.45)` | `rgba(255,255,255,0.45)` |
| `--color-text-quaternary` | `rgba(0,0,0,0.25)` | `rgba(255,255,255,0.30)` |
| `--color-bg-layout` | `#F5F5F5` | `#000000` |
| `--color-bg-container` | `#FFFFFF` | `#141414` |
| `--color-bg-elevated` | `#FFFFFF` | `#1F1F1F` |
| `--color-bg-mask` | `rgba(0,0,0,0.45)` | `rgba(0,0,0,0.45)` |
| `--color-border` | `#D9D9D9` | `#303030` |
| `--color-border-secondary` | `#F0F0F0` | `#2A2A2A` |
| `--color-fill` | `rgba(0,0,0,0.06)` | `rgba(255,255,255,0.18)` |
| `--color-fill-secondary` | `rgba(0,0,0,0.04)` | `rgba(255,255,255,0.12)` |

### 2.3 原始色阶（自定义时取用，不另造）

- Blue：`#E6F4FF` / `#BAE0FF` / `#91CAFF` / `#69B1FF` / `#4096FF` / `#1677FF` / `#0958D9` / `#003EB3`
- Red：`#FFCCC7` / `#FFA39E` / `#FF7875` / `#FF4D4F` / `#F5222D`
- Green：`#D9F7BE` / `#B7EB8F` / `#95DE64` / `#52C41A` / `#389E0D`
- Gold：`#FFF1B8` / `#FFE58F` / `#FFD666` / `#FAAD14` / `#D48806`

## 3. 字体排印（Typography）

- 字体栈：`--font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- 基准字号 14px，正文行高 `1.5714`（≈22px）。
- 字阶：

| 级别 | 字号 | 行高 | 字重 | 用途 |
|---|---|---|---|---|
| Display | 30px | 38px | 600 | 大屏页标题（慎用） |
| H1 | 24px | 32px | 600 | 页面标题 |
| H2 | 20px | 28px | 600 | 区块标题 |
| H3 | 16px | 24px | 600 | 卡片标题 |
| Body | 14px | 22px | 400 | 正文 / 表格 |
| Caption | 12px | 20px | 400 | 辅助说明 / 表格次要 |

- 数字 / 英文优先 `font-variant-numeric: tabular-nums`，保证数据列对齐（表格必备）。

## 4. 间距与栅格（Spacing & Grid）

- 基线 4px。主档：**4 / 8 / 12 / 16 / 20 / 24 / 32 / 48**（`--space-1`…`--space-12`）。
- 卡片内边距 16px（`--space-4`），区块间距 24px（`--space-6`）。
- 控件高度：默认 32px、大 40px、小 24px。
- 栅格：24 列，gutter 16px；断点 xs 480 / sm 576 / md 768 / lg 992 / xl 1200 / xxl 1600。

## 5. 圆角 / 描边 / 阴影（Radius / Border / Elevation）

- 圆角：默认 6px（`--radius-base`）、大 8px（`--radius-lg`）、小 4px（`--radius-sm`）、胶囊 999px。
- 描边：1px 实线，默认色 `--color-border`。
- 阴影（抬升）：

| Token | 值 | 用途 |
|---|---|---|
| `--shadow-1` | `0 6px 16px 0 rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12)` | 下拉 / 悬浮 |
| `--shadow-2` | `0 6px 16px 0 rgba(0,0,0,0.08), 0 9px 28px 0 rgba(0,0,0,0.05)` | 弹窗 / 卡片抬升 |
| `--shadow-3` | `0 6px 16px 0 rgba(0,0,0,0.08), 0 9px 28px 8px rgba(0,0,0,0.05)` | 通知 / 抽屉 |

## 6. 组件使用规则（Ant Design v5）

- 能用 antd 组件就用 antd，禁止手写替代：Button / Table / Form / Select / Tabs / Tag / Modal / Drawer / Message / Notification / Tooltip。
- 表格：密度默认 `middle`，大数据量用 `small`；状态列用 `Tag` 着色（success / warning / error 语义色）。
- 表单：校验态用 `--color-error` 描边 + 下方 12px 红色说明；必填走 `rules.required`。
- 操作按钮：主操作 ≤1 个 `primary`，其余 `default` / `text`；危险操作用 `danger`。
- 反馈：轻量用 `message`（自动消失），需停留 / 操作反馈用 `notification`。
- 暗色场景：通过 `ConfigProvider` 的 `theme.darkAlgorithm` 注入，勿手动改组件色。

## 7. 禁止项（Do / Don't）

- ❌ 不用纯黑 `#000` 作背景或文字（用 `rgba(0,0,0,0.88)`）。
- ❌ 不用荧光 / 过饱和装饰色。
- ❌ 不自创间距档位（只用 4 的倍数档）。
- ❌ 不手写组件替代 antd。
- ❌ 不把品牌蓝 `#1677FF` 当状态色（状态色见 §2.1）。
- ✅ 语义色驱动一切视觉状态。
- ✅ 暗色一律走 `darkAlgorithm`，不手动调色。

## 8. AI 出码约束（给编码代理看）

1. 所有颜色 / 字号 / 间距**优先 `var(--xxx)` 引用 `tokens.css`**，禁止硬编码魔法值。
2. 引入 `antd` v5 + `tokens.css`；根容器用 `ConfigProvider` 注入主题。
3. 主题切换：切换 `:root` 与 `[data-theme="dark"]` 两套变量即可，组件无需改。
4. 无法引用 CSS 变量时，至少使用 §2–§5 的真实 token 值，不得自创。
5. 业务语义色（如股票涨跌红绿）不在本规范内，单独遵循业务规范，不与语义状态色混淆。

---

## 9. 组件库（Component Library）

> 本系统走 code-first，组件**不画在画布上**，而是以「可抄的 HTML + CSS 片段」交付。
> 组件实现见 **`components.html`**（纯 HTML+CSS，引 `tokens.css`，暗/亮一键切换，每组件带复制片段）。
> 画布仅用于设计系统地基（token/配色/字体参考），不承载组件。
> 若团队使用 React，请直接引 **antd v5** 真实组件；本库是「无框架 / 直出 HTML」场景下的等价实现。

### 9.1 组件总索引（P0 已建）

| # | 组件 | antd v5 对应 | 关键状态 | `components.html` 锚点 |
|---|---|---|---|---|
| 1 | Button 按钮 | Button | default/hover/active/disabled/loading + lg/sm | `#btn` |
| 2 | Input 输入框 | Input | default/focus/disabled/error + 前后缀 | `#input` |
| 3 | InputNumber 数字 | InputNumber | −/+ 步进 | `#inputnumber` |
| 4 | Select 下拉 | Select | closed/open/active | `#select` |
| 5 | DatePicker 日期 | DatePicker | 面板展开/选中/今日 | `#datepicker` |
| 6 | Checkbox / Radio | Checkbox / Radio | 选中/禁用 | `#checkradio` |
| 7 | Switch 开关 | Switch | on/off/disabled | `#switch` |
| 8 | Table 表格 | Table | middle 密度、状态列 Tag、数字右对齐 | `#table` |
| 9 | Tag 标签 | Tag | default/success/processing/warning/error + 业务语义 | `#tag` |
| 10 | Badge 徽标 | Badge | 数字/圆点/成功色 | `#badge` |
| 11 | Modal 弹窗 | Modal | mask + 卡片 | `#modal` |
| 12 | Drawer 抽屉 | Drawer | 右侧滑出 | `#drawer` |
| 13 | Alert 警告 | Alert | success/info/warning/error | `#alert` |
| 14 | Progress 进度 | Progress | line/circle + success/exception | `#progress` |
| 15 | Tabs 选项卡 | Tabs | active 下划线 | `#tabs` |
| 16 | Statistic KPI | Statistic + Card | 大字号 tabular-nums + 趋势 | `#stat` |
| 17 | 业务状态色板 | —（云仓专用） | 待收货/收货中/已上架/异常 | `#palette` |

### 9.2 各组件规格（速查）

**Button** — 主操作 ≤1 个 `yc-btn-primary`；危险用 `yc-btn-danger`；次要 `default`/`dashed`/`text`。高度 32/40/24，圆角 6px，过渡 0.1s。
**Input** — focus：`--color-primary` 描边 + 2px 同色光晕；错误 `is-error` + 下方 12px `--color-error` 说明；占位符用 `--color-text-quaternary`。
**Select / DatePicker** — 展开面板 `--shadow-1` 抬升、`z-index: dropdown`；选中项 `--blue-1` 底 + 主色字。
**Checkbox / Radio / Switch** — 选中态一律 `--color-primary` 填充；Switch 关闭用 `rgba(0,0,0,0.25)`。
**Table** — 密度 `middle`（行高 ≈ 22+padding）；状态列用 `yc-tag` 语义色；数字列 `class="num"` 右对齐 + `tabular-nums`；hover 行 `--color-fill-secondary`。
**Tag** — 通用五态见 §9.1；**业务语义**：待收货=`--blue-1`底+主色字，收货中=`#FFFBE6`底+warning字，已上架=`#F6FFED`底+success字，异常=`#FFF1F0`底+error字。
**Modal / Drawer** — 遮罩 `--color-bg-mask`；Modal 卡片 `--shadow-2`，Drawer `--shadow-3`；底部操作区右对齐。
**Alert** — 四语义背景/边框/文字配色固定（success `#F6FFED`/`#B7EB8F`/`#389E0D` 等），带图标。
**Progress** — line：`--color-fill-secondary` 轨道 + `--color-primary` 填充；circle 用 SVG `stroke-dasharray`；success/exception 换填充色。
**Statistic** — 标签 `--color-text-tertiary`，值 `30px/600` + `tabular-nums`，趋势 up=`--color-success` / down=`--color-error`。

### 9.3 使用规则（给编码代理）

1. 组件一律引 `components.html` 的 `.yc-*` 类 + `tokens.css` 变量，**禁止硬编码色值/尺寸**。
2. 暗色：仅切 `html[data-theme="dark"]`，组件无需改；勿手动调组件色。
3. 业务状态色只用于「仓库业务语义」（待收货/收货中/已上架/异常），**不与品牌蓝 `#1677FF` 混用**。
4. 数字列强制 `tabular-nums` 对齐（表格/统计卡/KPI 必备）。
5. 能用 antd 真实组件就用 antd；本库是「直出 HTML」场景的兜底等价实现。

### 9.4 规划中（P1，后续补）

Form 表单布局 / Tooltip 提示 / Popconfirm 气泡确认 / Dropdown 下拉菜单 / Menu 菜单 / Breadcrumb 面包屑 / Steps 步骤条 / Pagination 分页 / Message 轻提示 / Notification 通知 / Descriptions 描述 / List 列表 / Empty 空态 / Avatar 头像 / Upload 上传 / Result 结果页。

