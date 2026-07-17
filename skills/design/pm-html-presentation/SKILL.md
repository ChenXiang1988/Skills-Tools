---
name: pm-html-presentation
description: "HTML 演示/幻灯片生成 skill（fork of pakco-html）：生成静态 deck、网页、社媒卡片，并提供可视化风格选择器。单文件 / 内联 / 零外部依赖 / 响应式。"
---

# pm-html-presentation

> 本地命名：`pm-html-presentation`（与 `pm-html-prototype` 平行，统一 `pm-` 前缀）。
> 本 skill 是上游 **pakco-html**（`github.com/pakco77/pakco-html`）的 fork，本地改名为 `pm-html-presentation`，定位为 **HTML 演示 / 幻灯片生成** 类 skill，与「原型类」的 `pm-html-prototype` 互不混淆。

pm-html-presentation 是一个 local-first 的视觉审美菜单，用于 AI 生成的演示 deck。它帮用户不必从零描述审美：浏览可见风格、复制一份可执行 Prompt，让 Claude Code / Codex / Hermes 在稳定的视觉约束下生成 deck。

The underlying skill still authors professional HTML presentations as static files, with themes, full-deck taste cards, layouts, animations, and prompts. One theme file = one look. One layout file = one page type. One animation class = one entry effect.
All pages share a token-based design system in `assets/base.css`.

## Install

> **本目录（`Skills-Tools/skills/presentation/pm-html-presentation`）就是已交付的优化版**：字体 / 图表（charts.js）/ 代码高亮（code-hl.js）/ 图标 / 动效（motion）**全部内联，零外部依赖、零外网请求、响应式**。直接部署这个副本即可，**无需再从上游拉取**。

### WorkBuddy 本地部署（推荐，零依赖版）

把本目录软链或复制到用户级 skills 目录，运行时即可识别调用：

```bash
# 方式 A：软链（单一真源，Skills-Tools 里的改动即时生效，推荐）
ln -s "/Users/martin/Documents/Martinjob/Skills-Tools/skills/presentation/pm-html-presentation" \
      "/Users/martin/.workbuddy/skills/pm-html-presentation"

# 方式 B：复制（独立副本，与源断开联系）
cp -R "/Users/martin/Documents/Martinjob/Skills-Tools/skills/presentation/pm-html-presentation" \
      "/Users/martin/.workbuddy/skills/pm-html-presentation"
```

- 软链方式：无需重启，新开对话即可调用 `pm-html-presentation`。
- 复制方式：重启一次 WorkBuddy 让其重载 skills 目录。

### 项目级部署（可选）

放进具体项目的 `.workbuddy/skills/pm-html-presentation/`，仅对该项目生效，可随仓库提交共享给团队。

### 上游原版（fork 来源，**非本优化版**）

本 skill 是上游 **pakco-html**（`github.com/pakco77/pakco-html`）的 fork。若你确实想要**带 CDN 外链的原版**（与「零依赖」目标相反），才用以下方式安装：

**Codex**

```text
Install this skill from GitHub: https://github.com/pakco77/pakco-html
Use the repo root as the skill path and install it as pakco-html.
```

Terminal fallback:

```bash
curl -fsSL https://raw.githubusercontent.com/pakco77/pakco-html/refs/heads/main/scripts/install-codex.sh | bash
```

Restart Codex after installation so it reloads `~/.codex/skills/pakco-html`.

**Claude Code / AgentSkill CLI**

```bash
npx skills add https://github.com/pakco77/pakco-html
```

**Other AgentSkill agents**

```bash
npx skills add https://github.com/pakco77/pakco-html --agent kimi-code-cli
npx skills add https://github.com/pakco77/pakco-html --agent qwen-code
npx skills add https://github.com/pakco77/pakco-html --agent gemini-cli
```

For any agent that reads a local `SKILL.md` folder, use the generic installer:

```bash
curl -fsSL https://raw.githubusercontent.com/pakco77/pakco-html/refs/heads/main/scripts/install-agent.sh | bash -s -- workbuddy
curl -fsSL https://raw.githubusercontent.com/pakco77/pakco-html/refs/heads/main/scripts/install-agent.sh | bash -s -- ~/.some-agent/skills/pakco-html
```

No build. Pure static HTML/CSS/JS — **本优化版无任何 CDN 外链与 webfonts 依赖**。

## What the skill gives you

- **36 themes** (`assets/themes/*.css`) — minimal-white, editorial-serif, soft-pastel, sharp-mono, arctic-cool, sunset-warm, catppuccin-latte/mocha, dracula, tokyo-night, nord, solarized-light, gruvbox-dark, rose-pine, neo-brutalism, glassmorphism, bauhaus, swiss-grid, terminal-green, xiaohongshu-white, rainbow-gradient, aurora, blueprint, memphis-pop, cyberpunk-neon, y2k-chrome, retro-tv, japanese-minimal, vaporwave, midcentury, corporate-clean, academic-paper, news-broadcast, pitch-deck-vc, magazine-bold, engineering-whiteprint
- **24 deck taste cards** (`templates/full-decks/<name>/` + Guizang variants) — 15 native complete multi-slide decks with scoped `.tpl-<name>` CSS, plus 9 Guizang color variants. Native templates include 8 extracted looks (xhs-white-editorial, graphify-dark-graph, knowledge-arch-blueprint, hermes-cyber-terminal, obsidian-claude-gradient, testing-safety-alert, xhs-pastel-card, dir-key-nav-minimal) and 7 scenario scaffolds (pitch-deck, product-launch, tech-sharing, weekly-report, xhs-post 3:4, course-module, **presenter-mode-reveal** — 演讲者模式专用)
- **31 layouts** (`templates/single-page/*.html`) with realistic demo data
- **27 CSS animations** (`assets/animations/animations.css`) via `data-anim`
- **20 canvas FX animations** (`assets/animations/fx/*.js`) via `data-fx` — particle-burst, confetti-cannon, firework, starfield, matrix-rain, knowledge-graph (force-directed), neural-net (pulses), constellation, orbit-ring, galaxy-swirl, word-cascade, letter-explode, chain-react, magnetic-field, data-stream, gradient-blob, sparkle-trail, shockwave, typewriter-multi, counter-explosion
- **Keyboard runtime** (`assets/runtime.js`) — arrows, T (theme), A (anim), F/O, **S (presenter mode: magnetic-card popup with CURRENT / NEXT / SCRIPT / TIMER cards)**, N (notes drawer), R (reset timer in presenter)
- **FX runtime** (`assets/animations/fx-runtime.js`) — auto-inits `[data-fx]` on slide enter, cleans up on leave
- **Showcase decks** for themes / layouts / animations / full-decks gallery
- **Headless Chrome render script** for PNG export

## Opening the style picker

When the user asks to open/browse the style menu (e.g. "html来", "打开风格菜单", "打开 pm-html-presentation", "打开html风格", "看看有什么风格", "open the picker"), start a local server and open the picker in a browser:

```bash
cd ~/.codex/skills/pakco-html && python3 -m http.server 8000 &
# then open: http://localhost:8000/templates/style-picker.html
```

If you installed with Claude Code / AgentSkill CLI, use `~/.claude/skills/pakco-html` instead.

The picker shows 60+ live previews across 4 tabs (Skins / Templates / UI Taste / Social Cards). The user clicks a card to copy the prompt, then pastes it back to you.

## When to use

Use when the user asks for any kind of slide-based output or wants to turn
text/notes into a presentable deck. Prefer this over building from scratch.

### 🎤 Presenter Mode (演讲者模式 + 逐字稿)

If the user mentions any of: **演讲 / 分享 / 讲稿 / 逐字稿 / speaker notes / presenter view / 演讲者视图 / 提词器**, or says things like "我要去给团队讲 xxx", "要做一场技术分享", "怕讲不流畅", "想要一份带逐字稿的 PPT" — **use the `presenter-mode-reveal` full-deck template** and write 150–300 words of 逐字稿 in each slide's `<aside class="notes">`.

See [references/presenter-mode.md](references/presenter-mode.md) for the full authoring guide including the 3 rules of speaker script writing:
1. **不是讲稿，是提示信号** — 加粗核心词 + 过渡句独立成段
2. **每页 150–300 字** — 2–3 分钟/页的节奏
3. **用口语，不用书面语** — "因此"→"所以"，"该方案"→"这个方案"

All full-deck templates support the S key presenter mode (it's built into `runtime.js`). **S opens a new popup window with 4 magnetic cards**:
- 🔵 **CURRENT** — pixel-perfect iframe preview of the current slide
- 🟣 **NEXT** — pixel-perfect iframe preview of the next slide
- 🟠 **SPEAKER SCRIPT** — large-font 逐字稿 (scrollable)
- 🟢 **TIMER** — elapsed time + slide counter + prev/next/reset buttons

Each card is **draggable by its header** and **resizable by the bottom-right corner handle**. Card positions/sizes persist to `localStorage` per deck. A "Reset layout" button restores the default arrangement.

**Why the previews are pixel-perfect**: each preview is an `<iframe>` that loads the actual deck HTML with a `?preview=N` query param; `runtime.js` detects this and renders only slide N with no chrome. So the preview uses the **same CSS, theme, fonts, and viewport as the audience view** — colors and layout are guaranteed identical.

**Smooth navigation**: on slide change, the presenter window sends `postMessage({type:'preview-goto', idx:N})` to each iframe. The iframe just toggles `.is-active` between slides — **no reload, no flicker**. The two windows also stay in sync via `BroadcastChannel`.

Only `presenter-mode-reveal` is designed from the ground up around the feature with proper example 逐字稿 on every slide.

Keyboard in presenter window: `← →` navigate (syncs audience) · `R` reset timer · `Esc` close popup.
Keyboard in audience window: `S` open presenter · `T` cycle theme · `← →` navigate (syncs presenter) · `F` fullscreen · `O` overview.

### 📱 网页模式（Webpage Mode）

If the user says any of: **网页 / 网页版 / 网页形态 / 做个网页 / 生成网页 / web page / webpage / 长页面 / 上下滑 / 手机看的 / 发链接给别人看**, or the content is meant for **阅读、传播、存档** rather than live presentation — **use the webpage template** instead of a deck.

Webpage mode produces a vertically scrolling HTML page with no slide boundaries. Key differences from deck:

| | Deck | Webpage |
|---|---|---|
| 交互 | 键盘/手势翻页 | 浏览器原生滚动 |
| 布局 | 全屏 16:9 slide | 720px 居中自适应 |
| JS | 需要 runtime.js | 不需要 |
| body class | (none) | `webpage` |
| 结构 | `.deck > .slide` | `.page > section` |
| 适合 | 演讲、分享会、Keynote | 阅读、传播、发链接 |

**How to scaffold:**
```html
<body class="webpage">
<div class="page">
  <section class="hero">...</section>
  <div class="section-break"></div>
  <section>...</section>
  ...
  <div class="page-footer">...</div>
</div>
</body>
```

Starter template: `templates/webpage.html`. Copy it to start a new webpage.
All design tokens (themes, `.card`, `.grid`, `.pill`, `.gradient-text`, etc.) work in both modes.
Do NOT include `runtime.js` in webpage mode — it's not needed.

## Before you author anything — ALWAYS ask or recommend

**Do not start writing slides until you understand three things.** Either ask
the user directly, or — if they already handed you rich content — propose a
tasteful default and confirm.

1. **Content & audience.** What's the deck about, how many slides, who's
   watching (engineers / execs / 小红书读者 / 学生 / VC)?
2. **Style / theme.** Which of the 36 themes fits? If unsure, recommend 2-3
   candidates based on tone:
   - Business / investor pitch → `pitch-deck-vc`, `corporate-clean`, `swiss-grid`
   - Tech sharing / engineering → `tokyo-night`, `dracula`, `catppuccin-mocha`,
     `terminal-green`, `blueprint`
   - 小红书图文 → `xiaohongshu-white`, `soft-pastel`, `rainbow-gradient`,
     `magazine-bold`
   - Academic / report → `academic-paper`, `editorial-serif`, `minimal-white`
   - Edgy / cyber / launch → `cyberpunk-neon`, `vaporwave`, `y2k-chrome`,
     `neo-brutalism`
3. **Starting point.** One of the 15 native full-deck templates, 9 Guizang variants, or scratch? Point
   to the closest `templates/full-decks/<name>/` and ask if it fits. If the
   user's content suggests something obvious (e.g. "我要做产品发布会" →
   `product-launch`), propose it confidently instead of asking blindly.

A good opening message looks like:

> 我可以给你做这份 PPT！先确认三件事：
> 1. 大致内容 / 页数 / 观众是谁？
> 2. 风格偏好？我建议从这 3 个主题里选一个：`tokyo-night`（技术分享默认好看）、`xiaohongshu-white`（小红书风）、`corporate-clean`（正式汇报）。
> 3. 要不要用我现成的 `tech-sharing` 全 deck 模板打底？

Only after those are clear, scaffold the deck and start writing.

## Update (更新)

When the user says "更新 pakco-html", "update pakco-html", "升级", or "拉最新版", run:

```bash
bash ~/.codex/skills/pakco-html/scripts/update.sh
```

For Claude Code installs, run `bash ~/.claude/skills/pakco-html/scripts/update.sh`.

If `scripts/update.sh` doesn't exist yet (old install), run the equivalent inline:

```bash
TMP=$(mktemp -d) && git clone --depth 1 https://github.com/pakco77/pakco-html.git "$TMP/r" 2>/dev/null && mkdir -p ~/.codex/skills/pakco-html && cp -r "$TMP/r/assets" "$TMP/r/templates" "$TMP/r/references" "$TMP/r/scripts" ~/.codex/skills/pakco-html/ && cp "$TMP/r/SKILL.md" ~/.codex/skills/pakco-html/ && rm -rf "$TMP" && echo "✅ 更新完成"
```

All existing decks that reference `assets/` via relative paths will automatically get the latest features (themes, layouts, mobile support, bug fixes) — no HTML changes needed.

## Quick start

1. **Scaffold a new deck.** From the repo root:
   ```bash
   ./scripts/new-deck.sh my-talk
   open examples/my-talk/index.html
   ```
2. **Pick a theme.** Open the deck and press `T` to cycle. Or hard-code it:
   ```html
   <link rel="stylesheet" id="theme-link" href="../assets/themes/aurora.css">
   ```
   Catalog in [references/themes.md](references/themes.md).
3. **Pick layouts.** Copy `<section class="slide">...</section>` blocks out of
   files in `templates/single-page/` into your deck. Replace the demo data.
   Catalog in [references/layouts.md](references/layouts.md).
4. **Add animations.** Put `data-anim="fade-up"` (or `class="anim-fade-up"`) on
   any element. On `<ul>`/grids, use `anim-stagger-list` for sequenced reveals.
   For canvas FX, use `<div data-fx="knowledge-graph">...</div>` and include
   `<script src="../assets/animations/fx-runtime.js"></script>`.
   Catalog in [references/animations.md](references/animations.md).
5. **Use a full-deck template.** Copy `templates/full-decks/<name>/` into
   `examples/my-talk/` as a starting point. Each folder is self-contained with
   scoped CSS. Catalog in [references/full-decks.md](references/full-decks.md)
   and gallery at `templates/full-decks-index.html`.
6. **Render to PNG.**
   ```bash
   ./scripts/render.sh templates/theme-showcase.html       # one shot
   ./scripts/render.sh examples/my-talk/index.html 12      # 12 slides
   ```

## Authoring rules (important)

- **Always start from a template.** Don't author slides from scratch — copy the
  closest layout from `templates/single-page/` first, then replace content.
- **Use tokens, not literal colors.** Every color, radius, shadow should come
  from CSS variables defined in `assets/base.css` and overridden by a theme.
  Good: `color: var(--text-1)`. Bad: `color: #111`.
- **Don't invent new layout files.** Prefer composing existing ones. Only add
  a new `templates/single-page/*.html` if none of the 31 fit.
- **Respect chrome slots.** `.deck-header`, `.deck-footer`, `.slide-number`
  and the progress bar are provided by `assets/base.css` + `runtime.js`.
- **Keyboard-first.** Always include `<script src="../assets/runtime.js"></script>`
  so the deck supports ← → / T / A / F / S / O / hash deep-links.
- **One `.slide` per logical page.** `runtime.js` makes `.slide.is-active`
  visible; all others are hidden.
- **Supply notes.** Wrap speaker notes in `<div class="notes">…</div>` inside
  each slide. Press S to open the overlay.
- **NEVER put presenter-only text on the slide itself.** Descriptive text like
  "这一页展示了……" or "Speaker: 这里可以补充……" or small explanatory captions
  aimed at the presenter MUST go inside `<div class="notes">`, NOT as visible
  `<p>` / `<span>` elements on the slide. The `.notes` class is `display:none`
  by default — it only appears in the S overlay. Slides should contain ONLY
  audience-facing content (titles, bullet points, data, charts, images).

## Writing guide

See [references/authoring-guide.md](references/authoring-guide.md) for a
step-by-step walkthrough: file structure, naming, how to transform an outline
into a deck, how to choose layouts and themes per audience, how to do a
Chinese + English deck, and how to export.

## Catalogs (load when needed)

- [references/themes.md](references/themes.md) — all 36 themes with when-to-use.
- [references/layouts.md](references/layouts.md) — all 31 layout types.
- [references/animations.md](references/animations.md) — 27 CSS + 20 canvas FX animations.
- [references/full-decks.md](references/full-decks.md) — 15 native full-deck templates + 9 Guizang picker variants.
- [references/presenter-mode.md](references/presenter-mode.md) — **演讲者模式 + 逐字稿编写指南（技术分享/演讲必看）**.
- [references/authoring-guide.md](references/authoring-guide.md) — full workflow.

## File structure

```
pm-html-presentation/
├── SKILL.md                 (this file)
├── references/              (detailed catalogs, load as needed)
├── assets/
│   ├── base.css             (tokens + primitives — do not edit per deck)
│   ├── fonts.css            (webfont imports)
│   ├── runtime.js           (keyboard + presenter + overview + theme cycle)
│   ├── themes/*.css         (36 token overrides, one per theme)
│   └── animations/
│       ├── animations.css   (27 named CSS entry animations)
│       ├── fx-runtime.js    (auto-init [data-fx] on slide enter)
│       └── fx/*.js          (20 canvas FX modules: particles/graph/fireworks…)
├── templates/
│   ├── deck.html                  (minimal 6-slide starter)
│   ├── webpage.html               (webpage mode starter — vertical scroll, no slides)
│   ├── theme-showcase.html        (36 slides, iframe-isolated per theme)
│   ├── layout-showcase.html       (iframe tour of all 31 layouts)
│   ├── animation-showcase.html    (20 FX + 27 CSS animation slides)
│   ├── full-decks-index.html      (gallery of all 15 native full-deck templates)
│   ├── full-decks/<name>/         (17 deck folders: 15 native + 2 Guizang bases)
│   └── single-page/*.html         (31 layout files with demo data)
├── scripts/
│   ├── new-deck.sh                (scaffold a deck from deck.html)
│   └── render.sh                  (headless Chrome → PNG)
└── examples/demo-deck/            (complete working deck)
```

## Rendering to PNG

`scripts/render.sh` wraps headless Chrome at
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. For multi-slide
capture, runtime.js exposes `#/N` deep-links, and render.sh iterates 1..N.

```bash
./scripts/render.sh templates/single-page/kpi-grid.html        # single page
./scripts/render.sh examples/demo-deck/index.html 8 out-dir    # 8 slides, custom dir
```

## Keyboard cheat sheet

```
←  →  Space  PgUp  PgDn  Home  End    navigate
F                                       fullscreen
S                                       open presenter window (magnetic cards: current/next/script/timer)
N                                       quick notes drawer (bottom overlay)
R                                       reset timer (in presenter window)
?preview=N                              URL param — force preview-only mode (single slide, no chrome)
O                                       slide overview grid
T                                       cycle themes (reads data-themes attr)
A                                       cycle demo animation on current slide
#/N in URL                              deep-link to slide N
Esc                                     close all overlays
```

## 单文件 / 内联模式（本优化版新增）

目标：把生成的 deck 打包成**一个自包含 HTML**——内联全部 CSS/JS、无 `../assets` 相对路径、无外网请求，符合「单文件 + 内联 + 零外部依赖 + 响应式」偏好。

### 字体已改零依赖
`assets/fonts.css` 原 8 个 Google Fonts `@import` 已删除；`assets/base.css` 的 `--font-*` 与各主题 `--font-*` 均已内置中文系统字体栈（PingFang SC / Microsoft YaHei / Songti SC / SimSun）。**离线即可渲染，不连任何外网。**

### 打包器 `scripts/inline.sh`
```bash
./scripts/inline.sh examples/my-talk/index.html            # 产出 index-single.html
./scripts/inline.sh examples/my-talk/index.html out.html   # 指定输出
```
四件事：
1. 内联 `<link>` 样式：base.css / fonts.css / animations.css；
2. 内联主题：当前 `theme-link` + `data-themes` 全部候选，各成 `<style data-pm-theme="X" [disabled]>`；并改写 inlined runtime.js 的 `applyTheme`，让 **T 键换肤在单文件版照样可用**（切 `<style>` 的 `disabled`，不再去拉 `.css` 文件）；
3. 内联 `<script>`：runtime.js / fx-runtime.js / charts.js（自托管 SVG 图表引擎）/ code-hl.js（零依赖代码高亮）；
4. 剥离外部字体：删 `@import url(http...)`、内联 `<link href="https://fonts.googleapis...">`、惰性属性 `data-theme-base`。

产物：一个 `.html`，浏览器直接开，无相对路径、无外网请求。

### 外部库已替换为零依赖内联实现（第二批｜已完成）
原 4 个 CDN `<script>` 库已全部干掉，改用自托管零依赖实现，**`inline.sh` 可一并内联，单文件版彻底无外网**：

- **Chart.js → `assets/charts.js`**：自托管 SVG/CSS 图表引擎，暴露 `window.PmChart.render(el, cfg)`。
  - 支持类型：`'bar' | 'line' | 'radar' | 'doughnut' | 'pie'`，调用签名兼容 `new Chart(canvas, cfg)` → 直接换成 `PmChart.render(div, cfg)`（`el` 可为 `<canvas>` 自动替换为 `<div>`，或本身就是 `<div class="pm-chart">`）。
  - 取色读 CSS 变量（`cssVar(name, fb)`），零硬编码；折线用 Catmull-Rom 样条光滑；雷达/饼图安全读取 `options.scales.r`（用 `dig()` 防 undefined）。
  - 模板 `templates/single-page/chart-*.html` 与 `examples/demo-deck/index.html` 已切到 `PmChart.render`，0 处 `chart.js` CDN 残留。
- **highlight.js → `assets/code-hl.js`**：零依赖正则分词高亮，暴露 `window.PmHL.highlight(el, lang)` 与 `PmHL.highlightAll()`。
  - 类：`tok-com / tok-str / tok-num / tok-kw / tok-fn / tok-p / tok-w`，默认 tokyo-night 调色板（写在模板 `<head>` 里的 `<style>`）。
  - 模板 `templates/single-page/code.html` 已删 3 个 highlight.js 外链，改用 `PmHL.highlightAll()`。
- **lucide / motion（guizang 模板）→ 内联 SVG / 现有 CSS 动效**：
  - guizang 模板图标本就是手写的 inline SVG，原 `lucide.createIcons()` 是 no-op，故直接删 `lucide@latest` CDN `<script>` 即可，**无需 lucide-shim.js 兜底**（这也是 `inline.sh` 脚本清单里去掉 `lucide-shim.js` 的原因）。
  - guizang-magazine / guizang-swiss 已删 3 个 googleapis 字体外链 + `lucide` 外链；字体变量改系统栈（`--mono` / `--serif-*` / `--sans-zh`）。
  - `motion.min.js` 本就是本地 `./assets/`，但原代码有 jsDelivr CDN 兜底 `catch(e2){…}`——已删兜底，加载失败静默退化为「无入场动画、内容完整可见」，零外部请求。

`inline.sh` 外部计数已修正为 `https?://(?!www\.w3\.org)`（SVG 命名空间 `w3.org` 非网络请求，不计），并打印真实外部数。

最终验证（全部经 Node DOM-mock + inline.sh 冒烟）：
- `demo-deck`：0 外部 http、charts.js 已内联、0 处 `../assets`
- `code.html`：0 外部 http、code-hl.js 已内联
- `guizang-magazine` + `guizang-swiss`：0 真实外部（不含 w3.org）、0 处 `../assets`

产物：一个 `.html`，浏览器直接开，**无相对路径、无外网请求、图表/代码高亮/字体/动效全离线可用**。

### 响应式
`assets/base.css` 已加 `@media (max-width:820px / 520px)` 收敛内边距与标题字号，窄屏/手机不裁切。

## License & author

MIT. Copyright (c) 2026 lewis &lt;sudolewis@gmail.com&gt;.

This is a fork of [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill).
Fork maintainer: [@pakco77](https://github.com/pakco77) — adds an interactive
style-picker WebUI, Guizang deck variant integration, and presenter-mode stability
fixes on top of the upstream work.
