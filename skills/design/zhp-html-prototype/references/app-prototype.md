# 移动端 / PDA / H5 原型专属守则

> 适配自 huashu-design `references/app-prototype.md`，但**重写为企业功能型原型**：
> - 技术栈改为**纯 HTML + CSS + 原生 JS**（非 huashu 的 React + Babel），保持双击即开、离线可用、与本 skill 的 PC 模块同源。
> - 设计取向改为**高对比、大点击区、无装饰图**（仓库 PDA/手持终端场景），而非消费 App 的视觉化风格。
> - 设备框用 `device-frame.css`（纯 CSS 复刻 iPhone 15 Pro 精确规格），不引入 React 组件。

做移动端 / PDA / H5 原型时（触发：「app 原型」「移动端」「PDA」「H5」「手机页」「做个 app」），遵循以下规则。

---

## 0. 架构选型（默认单文件纯 HTML）

**默认：所有结构 / 样式 / 脚本写进一个 `.html`**，双击即开，不依赖 server、不依赖 CDN。
- 页面头部 `<link>` 引入三份本地 CSS：`prototype.css`（提供 design-tokens 变量）、`device-frame.css`（机身框）、`prototype-mobile.css`（移动布局）。
- 交互用原生 `<script>`（TabBar 切换、弹层开关、表单校验），不引第三方框架。
- 平铺多屏时，多台 iPhone 放在 `.device-gallery` 容器里横向并排，每台是一个独立的 `<div class="device-iphone">`，内部用各自的作用域 id 管理状态（参考 `template-mobile.html` 的 `App` 对象模式）。

> 仅在单文件 >1000 行难维护时，才把样式/脚本拆成同级 `*.css` / `*.js` 文件（仍走 `file://` 相对路径，不引 server）。

## 1. 设备框必须用 `device-frame.css` — 禁止手写刘海/灵动岛/状态栏

做 iPhone / Android mockup 时**硬性绑定** `device-frame.css` 的 `.device-iphone` / `.device-android`。规格已对齐 iPhone 15 Pro（393×852、灵动岛 124×36、状态栏高 54、home indicator 140×5）。

**禁止**在你的 HTML 里自己写：
- `.dynamic-island` / 居中的黑圆角矩形
- 手写的时间 / 信号 / 电池图标
- `.home-indicator` / 底部 home bar
- iPhone bezel 圆角外框 + 黑描边

自己写 99% 会撞位置 bug。用法严格三步：
1. 页面引入 `device-frame.css`
2. 套 `<div class="device-iphone"><div class="device-screen"> … <div class="device-content">你的 app</div> … </div></div>`
3. 你的 app 内容写在 `.device-content` 内（从顶部 54px 起渲染，底部 34px 留给 home indicator），**不碰** island / statusbar / home。

## 2. 交付形态：默认「平铺多屏 + 每屏可交互」

iOS / 移动端原型的**默认交付就一种**：平铺 4–6 个主界面（每台一台 iPhone 并排），且每台都能交互。一眼看全貌，又每台能点 tab 切换、开弹层、做基本操作。

| 维度 | 默认做法 |
|------|---------|
| 屏数 | 平铺 **4–6 个主界面**（覆盖核心功能面） |
| 布局 | 多台 iPhone 放 `.device-gallery` 横向 `flex-wrap` 并排，每台上方一行 italic 小字标签说明界面名 |
| 每台交互 | 每台独立状态机：TabBar 可切、按钮/卡片/开关可点、能弹 sheet——不是静态摆拍 |

**只有两种特例才偏离默认**（用户明确说了才走）：
- 用户说「只要静态截图 / 看 layout」→ 退回纯静态（不挂状态机）
- 用户说「只演示一条流程 / 单机 demo」→ 单台走完整 flow

## 3. 移动端布局原语（来自 `prototype-mobile.css`）

| 组件 | class | 说明 |
|------|-------|------|
| 顶部导航栏 | `.app-topbar` / `.light` | 返回 + 居中标题 + 右侧操作；默认主色底，`.light` 为白底 |
| 内容区 | `.app-body` | 可滚动，默认 12px 内边距 |
| 搜索/扫码条 | `.app-search` / `.app-scan` | 扫码按钮用主色块，大点击区 |
| 统计卡 | `.app-stat-grid` / `.app-stat` | 2 列 KPI，`.v.danger/.success` 变红绿 |
| 卡片 / 列表 | `.app-card` / `.app-list` / `.app-list-item` | 列表项 14px 高度，右侧箭头 |
| 任务卡 | `.app-task` | 单号 + 元信息 + 操作按钮 |
| 表单 | `.app-field` / `.app-input` / `.app-select` | 输入框高 44px，适合手指 |
| 按钮 | `.app-btn` `.primary/.ghost/.danger` `.block/.sm` | 主按钮高 46px，`.block` 通栏 |
| 底部 TabBar | `.app-tabbar` / `.app-tab.active` | 4–5 个 tab，激活态主色 |
| 底部弹层 | `.app-sheet-mask.open` / `.app-sheet` | Action Sheet，从底部滑入 |
| 状态标签 | `.tag-blue/green/red/orange/gray` + `.dot-*` | 与 PC 版语义色一致 |

**交互约定**：TabBar 切换用 `data-tab` + 事件委托；弹层用 `.app-sheet-mask.open` 类切换显隐；所有可点元素加 `cursor:pointer`。每台设备用独立 `id` 作用域（如 `App1` / `App2`）避免状态串台。

## 4. 品位锚点（企业功能型，区别于消费 App）

| 维度 | 首选 | 避免 |
|------|------|------|
| 色彩 | 单一主色（默认 `#1677ff`）贯穿 + 语义色（红=异常/绿=成功） | 多色聚类、紫渐变装饰 |
| 字体 | 系统字体栈（`PingFang SC` / `Microsoft YaHei`）+ 大字号按钮 | 花哨衬线、全场 Inter |
| 信息密度 | **高密度、信息导向**（仓库场景需要一眼看到单号/数量/库位/状态） | 留白过度导致一屏看不完关键字段 |
| 图标 | 用 emoji 或 SVG 单色图标，仅表意不装饰 | 每卡片堆无意义 icon + tag + status dot |
| 真实数据 | 用贴近业务的**占位数据**（真实单号格式、真实库位编码如 `A-01-02-03`） | 写 "Lorem" / "测试数据" / 明显假数据 |

**反 AI slop**：不要给仓库 PDA 页配 Unsplash 风景图、不要紫色渐变背景、不要用 emoji 当主视觉。功能页的价值在于「字段准确、流程清楚」。

## 5. 交付前自测

静态截图只看 layout，交互 bug 要点过才发现。至少验证：
1. 每台 TabBar 切换后界面正确切换、状态不串台；
2. 列表项 / 任务卡点击能开弹层或跳转；
3. 弹层遮罩点击 / 取消能关闭；
4. 表单必填项为空时提交有提示。

无 server 时，至少在浏览器手动点过一遍上述路径；若本机有 Playwright，可跑最小点击测试（`pageerror` 为 0 再交付）。

## 与 huashu-design 的关键差异（务必知悉）

| 项 | huashu-design | 本 skill（移动端模块） |
|----|----------------|------------------------|
| 技术栈 | 单文件 inline React + Babel（CDN） | 纯 HTML + CSS + 原生 JS（零依赖、离线） |
| 适用场景 | 消费 App 高保真视觉 | 企业 WMS / PDA 功能原型 |
| 取图策略 | 主动抓真实图片填充 | 不配装饰图，用业务占位数据 |
| 设备框 | `ios_frame.jsx` React 组件 | `device-frame.css` 纯 CSS 结构 |
| 设计取向 | 视觉化、品位锚点（衬线/rust 橙） | 功能型、高对比、语义色 |

选择纯原生栈的原因：本 skill 的 PC 模块已是 vanilla，移动端保持一致可复用 design-tokens；且企业原型常在内网 / 离线评审，零依赖最稳。
