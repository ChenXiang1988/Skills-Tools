---
name: zhp-html-prototype
description: 生成静态 HTML
  产品原型页面，用于需求评审与方案沟通。触发条件（写给模型看，不是写给人看）：用户要求'生成原型页面'、'画原型'、'出原型'、'根据业务描述生成页面'、'维护原型目录'、'新增原型页面'、'做低保真/高保真原型'、'用
  HTML 出原型'、'Axure/墨刀替代'、'需求阶段原型'、'移动端原型'、'PDA 原型'、'H5 原型'、'手机页'、'app 原型'、'做个
  app'、'iOS 原型'、'Android 原型'。产出统一放在项目 prototypes/ 目录，复用公共
  CSS、设计令牌(design-tokens.json)、共享菜单(menu-config.js)与页面模板(template.html /
  template-mobile.html)，生成后必须运行 validate_prototype.py 校验。支持双端：PC
  后台管理（侧边菜单+表格+弹窗）与移动端/PDA/H5（设备框+顶栏+TabBar+卡片列表+表单+底部弹层），移动端参考
  references/app-prototype.md。适用于后台管理系统、WMS/仓储系统、数据看板、配置页、仓库手持终端(PDA)等场景。当用户提供截图或旧系统页面作为参考时，只提取业务信息（字段、筛选、表格列、按钮、状态、流程），不得复刻对方视觉风格（颜色/字体/圆角/阴影/间距）。
version: 1.0.0
author: 参考码农胖大海《原型页面生成 Skill 实战总结》实现
disable: true
---

# zhp-html-prototype · 静态 HTML 原型生成 Skill

让 AI 按**团队约定的原型体系**生成页面，而不是每次重新发明一套风格。

核心价值：需求人员描述业务场景、页面字段、交互规则，AI 快速生成**可评审的静态 HTML 原型**，降低原型制作成本，让需求沟通更快进入具体页面与流程。

## 一、Skill 职责边界

- ✅ 生成/维护**静态 HTML 原型**（用于需求评审、方案沟通、草稿确认）。
- ✅ 复用统一的设计令牌、公共样式、模板、共享菜单。
- ✅ 当用户给截图/旧系统页面：只提取**业务信息**，不作为视觉规范。
- ❌ 不生成生产级前端工程（Vue/React 等）——那是后续技术栈阶段的事。
- ❌ 不自由发挥视觉风格——一律走公共样式 + 设计令牌。

## 二、何时触发（已写入 description，模型自动识别）

用户提到：生成原型页面 / 画原型 / 出原型 / 根据业务描述生成页面 / 维护原型目录 / 新增原型页面 / 做低保真原型 / 用 HTML 出原型 / Axure 墨刀替代 / 需求阶段原型 / 移动端原型 / PDA 原型 / H5 原型 / 手机页 / app 原型 / iOS 原型 / Android 原型。

## 二·五、双端分流（生成前先判定）

| 用户意图信号 | 走哪套 | 资源 |
|------|------|------|
| 后台 / 管理端 / Web 系统 / 看板 / 配置页 / 表格页 | **PC 后台** | `template.html` + `prototype.css` + `menu-config.js`（侧边菜单） |
| 手机 / 移动端 / PDA / H5 / app / iOS / Android / 手持终端 | **移动端** | `template-mobile.html` + `device-frame.css` + `prototype-mobile.css` + `references/app-prototype.md` |

- 同一业务常需双端（如 WMS：PC 运营后台 + PDA 采集终端）。两端**并存、互不干扰**，各自独立页面，可分别平铺评审。
- 移动端默认「平铺 4–6 台 iPhone 可交互」（详见 `references/app-prototype.md`），不要问用户"要平铺还是可操作"——默认两者都要。

## 三、标准工作流（每次生成都走完）

1. **初始化目录**：若项目根目录无 `prototypes/`，先读 `references/prototype-init.md` 并按其步骤初始化（复制 assets 到 `prototypes/assets`、`prototypes/shared`）。
2. **读取约束资产**（按需、渐进披露，不要一次性全读）：
   - `assets/design-tokens.json` — 颜色/圆角/间距/字号，禁止自创值。
   - **PC 后台**：`assets/prototype.css`（布局/表单/表格/按钮/弹窗/标签）、`assets/template.html`（骨架）、`assets/menu-config.js`（侧边菜单项）。
   - **移动端/PDA/H5**：`assets/device-frame.css`（iPhone/Android 机身框）、`assets/prototype-mobile.css`（顶栏/TabBar/卡片列表/表单/弹层）、`assets/template-mobile.html`（骨架）；规范读 `references/app-prototype.md`。
   - 需要布局规则读 `references/layouts.md`；需要交互模式读 `references/interactions.md`。
3. **基于模板生成业务页**：在 `template.html` 基础上填充：页面标题、查询区、操作区、表格列、状态标签、弹窗字段、脚本逻辑。
4. **只提取业务信息**：若用户给了截图/参考页，提取字段/筛选/表格列/按钮/状态/流程，**不要**照搬颜色/字体/圆角/阴影/间距。
5. **同步菜单与入口页**：新增页面后，更新 `prototypes/shared/menu-config.js` 与 `prototypes/index.html`，保证统一入口可访问。
6. **运行校验**：进入 `prototypes/` 目录，执行 `python3 assets/validate_prototype.py`。脚本检查目录结构、公共资源、页面引用、菜单配置、入口同步。
   ⚠️ 校验脚本必须位于 `prototypes/assets/validate_prototype.py`（随初始化一同复制），否则根目录推算错误、检查全部误报。
7. **交付**：提示用户用浏览器打开 `prototypes/<page>.html` 查看；若有校验失败项，先修复再交付。

## 四、目录结构（生成结果落点）

```
prototypes/
├── assets/
│   ├── design-tokens.json      # 设计令牌（约束颜色/间距/圆角/字号，PC/移动共用）
│   ├── prototype.css           # PC 后台公共样式（骨架/表单/表格/按钮/弹窗/标签）
│   ├── device-frame.css        # 移动端设备框（iPhone/Android 纯 CSS，复刻 15 Pro 规格）
│   ├── prototype-mobile.css    # 移动端布局（顶栏/TabBar/卡片列表/表单/弹层）
│   ├── template.html           # PC 业务页骨架
│   ├── template-mobile.html   # 移动端单台 iPhone 骨架
│   └── validate_prototype.py  # 校验脚本（须置于 assets/ 下运行）
├── shared/
│   ├── app-shell.js            # 共享外壳：渲染侧边菜单、激活态、基础交互
│   └── menu-config.js          # 菜单配置（新增页面必须同步）
├── index.html                  # 原型集合入口页
├── <page-pc>.html             # PC 后台页面
├── <page-mobile>.html         # 移动端/PDA 页面（平铺多台 iPhone）
└── ...
```

## 五、关键原则（写进 skill 的原因）

1. **补充模型默认不知道的东西**：通用 HTML/CSS 写法不必重复；要写的是团队规则——目录放哪、页面长啥样、菜单怎么维护、截图怎么处理、完成怎么校验。
2. **约束目标，不写死路径**：要求"必须复用公共样式""新增页面必须同步菜单""截图只提取业务信息""完成必须跑校验"，具体排布保留灵活。
3. **稳定能力沉淀成脚本**：校验/初始化/复制模板/同步目录用脚本保证确定性，而非只靠提示词。
4. **渐进披露**：SKILL.md 只留核心流程；布局规则→`references/layouts.md`；交互模式→`references/interactions.md`；初始化→`references/prototype-init.md`；移动端/PDA 规范→`references/app-prototype.md`；控件视觉参考→`assets/prototype-component-demo.html`。模型按需读取，省 token。

## 六、定制方式

- **项目级覆盖**：在原型所在项目根目录添加 `AGENTS.md`/`CLAUDE.md`，覆盖局部规则（如"新页面放 `prototypes/v2` 目录"）。
- **换风格**：修改 `design-tokens.json` 与 `prototype.css`，或让 AI 重新生成 `assets/prototype-component-demo.html`（如改为 Ant Design 风格），再据其更新公共样式与规则。

## 七、依赖

- 校验脚本 `validate_prototype.py` 仅用 Python 标准库，**无需 pip 安装任何包**。
- 生成的 HTML 全部使用**相对路径**、**无外部 CDN**，可直接 `file://` 打开。
