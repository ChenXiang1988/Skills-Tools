# 云仓 PDA 设计系统 — DESIGN.md

> 适用对象：WMS / OMS / TMS / BMS 现场作业端（手持 PDA / 盘点机）  
> 设计基底：**Ant Design Mobile（antd-mobile）v5.42.2** 真实设计语言  
> 适配层：在 antd-mobile 之上叠加 PDA 工业件（扫码 / 任务卡 / 底部 CTA / 手套触控）  
> 设计模式：竖屏 / 暗色优先 / 扫描优先 / 单任务流  
> 注：antd-mobile 是 React 组件库，本系统仅借其**设计语言（变量 / 规范）**，组件按 HTML 自写（code-first）

---

## 1. 设计目标

PDA 不是“桌面后台缩小版”，而是另一套交互形态：

- **扫描优先**：实体扫码键 + 屏幕扫码入口是主交互，触点是辅助。
- **手套触控**：所有可点击区域 ≥ 48px，主操作 56px，扫码 CTA 64px。
- **一次一事**：单屏只完成一个任务（收货 / 上架 / 拣货 / 盘点），不堆信息。
- **暗色优先**：仓库强光、反光、省电；antd-mobile 暗色为原生支持（实验性），PDA 封为默认。
- **与桌面后台同源**：品牌蓝 `#1677FF` 与 Web 端 Ant Design v5 完全一致；语义色遵循 antd-mobile 真实值。

---

## 2. 色彩（antd-mobile v5.42.2 真实值）

### 2.1 品牌 / 主色

| Token | 暗色（PDA 默认） | 亮色 | 用途 |
|-------|------|------|------|
| `--pda-primary` | `#3086FF` | `#1677FF` | 主按钮、扫码入口描边、链接、图标 |
| 来源 | `--adm-color-primary`（theme-dark） | `--adm-color-primary`（theme-default） | antd-mobile 在暗底将主色提亮至 `#3086FF` 以保对比 |

> 品牌蓝 `#1677FF` 是 Web（AntD v5）与 PDA（antd-mobile）的**共享锚点**；暗色下 antd-mobile 自动提亮到 `#3086FF`，属正常对比优化，非偏差。

### 2.2 语义色

| 语义 | 暗色（默认） | 亮色 | 用途 |
|------|------|------|------|
| success | `#34B368` | `#00B578` | 成功、完成、通过 |
| warning | `#FFA930` | `#FF8F1F` | 警告、待处理、注意 |
| danger / error | `#FF4A58` | `#FF3141` | 异常、失败、删除 |
| 浅蓝底（选中） | `#0D2543` | `#E7F1FF` | 选中行 / 高亮背景（`--pda-wathet`） |

> 语义色遵循 antd-mobile 真实调色板；与 Web 端 AntD v5 桌面语义色为**近亲**（同一套设计体系），暗色下各自微调对比，属预期。

### 2.3 Surface（暗色默认）

| Token | 暗色 | 亮色 | 用途 |
|-------|------|------|------|
| `--pda-surface-1` / `--pda-bg` | `#1A1A1A` | `#FFFFFF` | 页面最底层背景 |
| `--pda-surface-2` | `#242424` | `#F5F5F5` | 卡片、列表行、底部栏 |
| `--pda-surface-3` | `#2F2F2F` | `#EBEBEB` | 抬升面板、操作抽屉、按压态 |
| `--pda-surface-sunken` / `--pda-box` | `#0A0A0A` | `#F0F0F0` | 输入框、凹陷区、分隔块 |
| `--pda-border` | `#2B2B2B` | `#EEEEEE` | 描边、分隔线 |

> `--pda-bg` / `--pda-box` / `--pda-border` 直接取自 antd-mobile；surface-2 / surface-3 为 PDA 卡片分层补充（antd-mobile 未单独定义）。

### 2.4 文字（暗色）

| Token | 暗色 | 亮色 | 用途 |
|-------|------|------|------|
| `--pda-text` | `#E6E6E6` | `#333333` | 正文、标题 |
| `--pda-text-secondary` | `#B3B3B3` | `#666666` | 副标题、辅助信息 |
| `--pda-text-weak` | `#808080` | `#999999` | 占位、禁用说明 |

> **禁止**：暗色背景上禁用 `#FFFFFF` 纯白正文，刺眼且反白。正文一律用 `--pda-text`（`#E6E6E6`）。

---

## 3. 字体与字阶

- 字体栈（antd-mobile 真实）：`-apple-system, BlinkMacSystemFont, "Helvetica Neue", …, "PingFang SC", "Microsoft YaHei", …`
- 基准字号：**16px**（PDA 因手套 + 户外可视距离放大；antd-mobile 默认 main 为 13px，此处按 PDA 覆盖）
- 行高：1.5
- antd-mobile 字号阶梯参考：`--pda-fs-1..10` = 9 / 10 / 11 / 12 / 13 / 14 / 15 / 16 / 17 / 18px

| 层级 | 字号 | 字重 | 用途 |
|------|------|------|------|
| Title L | 20px | 600 | 页面标题 |
| Title M | 18px | 600 | 卡片标题 |
| Body | 16px | 400 | 正文、按钮 |
| Body Strong | 16px | 500 | 强调 |
| Caption | 13px | 400 | 辅助说明 |
| Caption S | 12px | 400 | 系统信息、时间 |

---

## 4. 间距与触控

- 栅格基线：4px（antd-mobile 以 8px 为主，PDA 保留 4px 细档用于紧凑布局）
- 主档：4 / 8 / 12 / 16 / 24 / 32px
- 触控热区（手套作业下限）：
  - 最小：`48px`
  - 主操作：`56px`
  - 底部扫码 CTA：`64px`
- 列表行高：`56px`
- 圆角（antd-mobile 真实）：小 `4px` / 中 `8px` / 大 `12px`；胶囊 `999px`

---

## 5. 圆角与阴影

- 圆角（`--adm-radius-s/m/l`）：卡片 / 按钮 `8px`，大面板 / 底部抽屉 `12px`，胶囊 / 主按钮 `999px`。
- 暗色抬升靠 **阴影 + 1px 描边** 双重表达：
  - shadow-1：`0 1px 4px rgba(0,0,0,0.4)`
  - shadow-2：`0 2px 8px rgba(0,0,0,0.45)`
  - shadow-3：`0 4px 16px rgba(0,0,0,0.5)`

---

## 6. PDA 组件规则（对应 antd-mobile 组件 + 工业件）

### 6.1 顶部栏 NavBar（antd-mobile `NavBar`）

- 高度 44px，左返回 / 中标题 / 右操作。
- 背景 `--pda-surface-1`，底 1px `--pda-border`。
- 标题 17px 居中，操作区图标 24px。

### 6.2 扫码入口卡（工业件，antd-mobile 无）

- 大点击区（≥ 120px 高），带扫码图标 + 文案。
- 默认容器 `--pda-surface-2`，描边 `--pda-primary`。
- 必须支持实体扫码键直接触发，屏幕点击仅作兜底。

### 6.3 任务列表行（antd-mobile `List.Item` 适配）

- 行高 56px（`--pda-list-row-h`）。
- 左侧图标 / 头像 32px，`--pda-surface-3` 背景。
- 主标题 16px，副标题 13px 灰色（`--pda-text-secondary`）。
- 右侧状态胶囊标签（语义色驱动，见 6.7）。

### 6.4 底部标签栏 TabBar（antd-mobile `TabBar`）

- 固定底部，高 50px，`--pda-surface-1` + 1px 顶描边。
- 每个 item：图标 24px + 文字 12px；选中态图标 / 文字用 `--pda-primary`。

### 6.5 底部扫码栏（工业件，antd-mobile 无）

- 固定底部，高 72px（`--pda-bottom-bar-h`），`--pda-surface-2` + 1px 顶描边。
- 单一主操作：全宽胶囊按钮，高 64px（`--pda-touch-cta`），`--pda-primary` 填充。
- 按钮内文字 18px semibold，“扫 码”中间留空隙，便于扫描枪误触后仍可读。

### 6.6 大触控按钮（antd-mobile `Button` 适配）

- 主操作高 56px，全宽；CTA 高 64px。
- 含 default / active（按下，提亮）/ disabled（降透明度）/ loading（转圈）四态。

### 6.7 状态标签（antd-mobile `Tag` 适配）

- 胶囊，高 24px，padding 10px。
- 暗色背景使用语义色低透明度（~18%），文字用对应亮色调：
  - 成功 → 背景 `rgba(52,179,104,0.18)` + 文字 `--pda-success-light`（`#4CD389`）
  - 警告 → 背景 `rgba(255,169,48,0.18)` + 文字 `--pda-warning-light`
  - 异常 → 背景 `rgba(255,74,88,0.18)` + 文字 `--pda-danger-light`

### 6.8 数字键盘（工业件，antd-mobile 无）

- 按键 56px（`--pda-key-size`），`--pda-surface-3` 背景，`--pda-border` 描边。
- 数字 20px `--pda-text`；删除、小数点用 `--pda-text-weak`。
- 行列间距 8px；输入框上方实时显示当前值。

### 6.9 Toast / 反馈（antd-mobile `Toast`）

- 暗色：`--pda-surface-3` 背景，`--pda-border` 描边，左图标语义色。
- 文字 14px，居中偏左，不阻断操作。
- 错误类 Toast 可配合震动反馈（如设备支持）。

---

## 7. 禁止项

- 不要把桌面密集表格直接搬到 PDA。
- 不要在暗底用纯白正文。
- 不要出现 < 44px 的触控热区（PDA 下限 48px）。
- 不要在一屏内放多个主按钮。
- 不要一次给用户多项任务。
- 不要默认亮色（仓库强光下反光严重）。

---

## 8. 出码约束

- 使用 `tokens.css` 中的 CSS 变量，**禁止硬编码魔法值**。
- 组件尺寸用 `var(--pda-touch-*)` / `var(--pda-space-*)` / `var(--pda-list-row-h)`。
- 颜色用 `var(--pda-color-*)` / `--pda-*` 语义变量；暗色 / 亮色切换通过 `<html data-theme="light">` 覆盖（默认暗）。
- 字体用 `var(--pda-font-family)`。
- 扫码按钮必须可被实体键和屏幕同时触发。
- 所有状态文案用语义色 token，不直接写 `green` / `red`。
- 设计语言锚 antd-mobile v5.42.2；通用移动组件（NavBar / TabBar / List / Toast）优先参考其规范，仅自建云仓特化工业件（扫码 / 任务卡 / 底部 CTA / 数字键盘）。

---

## 9. 组件库（可抄片段）

见同目录 **`components.html`**：暗色优先组件画廊，每组件含实例 + 状态 + 可复制 HTML/CSS 片段，支持暗 / 亮一键切换。
