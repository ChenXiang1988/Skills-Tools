---
name: pencil-design
description: >
  Create high-quality visual designs — websites, app screens, dashboards, slides, marketing materials, social media graphics — using the Pencil CLI tool. Use this skill whenever the user wants to create, generate, or visualize any kind of UI design, mockup, wireframe, layout, webpage, app screen, presentation slide, poster, banner, or marketing asset. Also use it when the user says things like "design me a...", "make a visual for...", "create a mockup of...", "what would X look like?", or wants to turn an idea into a visual. Even if the user doesn't mention "Pencil" or "design tool" explicitly — if they want something visual created, this is the skill to use.
---

# Pencil Design

Create professional visual designs from natural language descriptions using the Pencil CLI. Pencil is a headless design tool that generates `.pen` files (a structured JSON design format) and can export them as images.

> **中文说明：** 使用 Pencil CLI 根据自然语言描述创建专业视觉设计。Pencil 是一款无界面设计工具，可生成 `.pen` 文件（一种结构化 JSON 设计格式），并能将其导出为图片。

## Setup

Before designing, make sure the Pencil CLI is available.

> **中文说明：** 在开始设计之前，请确保 Pencil CLI 已可用。

### Check installation

```bash
which pencil || npx pencil version
```

If `pencil` is not found, install it:

```bash
npm install -g @pencil.dev/cli
```

If global install fails due to permissions, install locally instead:

```bash
npm install @pencil.dev/cli
```

Then run it via `npx pencil` (or `./node_modules/.bin/pencil`) instead of `pencil`.
You can learn about the available commands via the `pencil --help` command.

> **中文说明：**
> 如果找不到 `pencil` 命令，请执行全局安装。若因权限问题全局安装失败，则改为本地安装，之后通过 `npx pencil`（或 `./node_modules/.bin/pencil`）来运行。可通过 `pencil --help` 查看所有可用命令。

### Authentication

#### Pencil user

To use the CLI, an authenticated user logged in to Pencil is required. First, check
the current user configuration on the machine with the `pencil status` command.

If not logged in, there are the following options:

- use `pencil signup --email you@example.com --username johndoe --name "John Doe"` command, to create a new user.
- use `pencil login --email you@example.com [--code abc123]` to authenticate an existing or newly created user.
- optionally, the `PENCIL_CLI_KEY` env var can also be used for authentication if its set in your session.

> **中文说明（Pencil 用户）：**
> 使用 CLI 需要一个已登录 Pencil 的认证用户。首先使用 `pencil status` 命令检查当前机器上的用户配置。
> 如果尚未登录，可选择以下方式：
> - 使用 `pencil signup` 命令创建新用户；
> - 使用 `pencil login` 命令对已有用户进行身份验证；
> - 也可在会话中设置环境变量 `PENCIL_CLI_KEY` 来完成认证。

#### Claude Code agent

The CLI needs auth to run its AI agent for which Claude Code is required. For that
there needs to be an authenticated Claude Code user set in the system configuration
either via env var or a user subscription.

If none of these are available, tell the user what options they have and help them set one up.

> **中文说明（Claude Code Agent）：**
> CLI 运行 AI Agent 需要 Claude Code 的授权。系统配置中必须存在一个已认证的 Claude Code 用户（通过环境变量或用户订阅均可）。
> 如果两者都不可用，请告知用户有哪些选项，并协助其完成配置。

### Staying up to date

This skill stays in sync with the **Pencil CLI npm package** (`@pencil.dev/cli`). The published package includes `SKILL.md` at its root; the package version is the skill version.

**Check for a newer CLI / skill**

- Latest version on the registry: `npm view @pencil.dev/cli version`
- Installed CLI: `pencil version`, or `npm list -g @pencil.dev/cli` (global) / `npm list @pencil.dev/cli` (project)

**Upgrade the CLI**, then refresh your copied skill file (agents do not auto-update skill files you placed in config folders):

```bash
npm install -g @pencil.dev/cli
```

**Where to copy the skill from after installing**

- From a dependency tree: `node_modules/@pencil.dev/cli/SKILL.md` (path is the same for global and local installs; resolve from your project root or global `node_modules` prefix).

**Fetch the same file without cloning the repo** (mirrors the npm tarball; optional third-party CDNs):

- `https://unpkg.com/@pencil.dev/cli@latest/SKILL.md`
- `https://cdn.jsdelivr.net/npm/@pencil.dev/cli@latest/SKILL.md`

Use `@latest` for the newest publish, or pin (e.g. `@0.2.4`) for a reproducible snapshot.

**If you don't know where skills live on this machine**

Agents don't always get the skills directory from context. When the path isn't obvious:

- **Ask the user** where their agent or IDE loads skills from, or where they want this skill installed.
- **Check the product's docs** for "skills", "agent skills", or "plugins" — paths differ by tool and version.
- You can still **use the skill content without installing**: fetch or open the **`SKILL.md` URL above** (unpkg/jsDelivr) in the session so guidance applies even when the on-disk path is unknown. For a persistent install, copy the fetched file into the path the user or docs specify.

**Typical skill locations** (confirm with your tool's current docs — layouts change):

| Environment | Where to put `SKILL.md` |
|-------------|-------------------------|
| **Cursor** | Project: `.cursor/skills/pencil-design/SKILL.md`; user-level: under `~/.cursor/skills/` |
| **Claude Code** | Often `.claude/skills/pencil-design/SKILL.md` or user-level under `~/.claude/` |
| **OpenClaw** | Often `~/.openclaw/skills/`, workspace `.agents/skills/`, or paths in [OpenClaw skills docs](https://docs.openclaw.ai/skills/) — verify for the user's setup |
| **Other agents (Codex, etc.)** | Use the directory your product uses for skills or prompts |

Example (adjust the destination path to match your agent):

```bash
curl -fsSL "https://unpkg.com/@pencil.dev/cli@latest/SKILL.md" -o .cursor/skills/pencil-design/SKILL.md
```

**When to check for an update**

- **Early in the session**, before the first Pencil design run (compare `npm view @pencil.dev/cli version` to the installed CLI), so you aren't following stale instructions.
- **Again** if the user says they upgraded the CLI, or if behavior doesn't match this doc (flags, auth, timing).
- **Not** before every single command — once per session is enough unless something changed or errors suggest a version mismatch.

> **中文说明（保持最新版本）：**
> 本 Skill 与 **Pencil CLI npm 包**（`@pencil.dev/cli`）保持同步。已发布的包在根目录包含 `SKILL.md`；包版本即为 Skill 版本。
>
> **检查是否有新版 CLI / Skill：**
> - 注册表上的最新版本：`npm view @pencil.dev/cli version`
> - 已安装的 CLI：`pencil version`，或 `npm list -g @pencil.dev/cli`（全局）/ `npm list @pencil.dev/cli`（项目）
>
> **升级 CLI** 后，还需刷新你复制的 Skill 文件（Agent 不会自动更新你放在配置目录中的 Skill 文件）：
> ```bash
> npm install -g @pencil.dev/cli
> ```
>
> **安装后从哪里复制 Skill 文件：**
> - 从依赖树中：`node_modules/@pencil.dev/cli/SKILL.md`（全局和本地安装路径相同，从项目根目录或全局 `node_modules` 前缀解析）。
>
> **不克隆仓库也能获取该文件**（镜像 npm tarball；可选第三方 CDN）：
> - `https://unpkg.com/@pencil.dev/cli@latest/SKILL.md`
> - `https://cdn.jsdelivr.net/npm/@pencil.dev/cli@latest/SKILL.md`
>
> 使用 `@latest` 获取最新发布，或固定版本号（如 `@0.2.4`）以获得可复现的快照。
>
> **如果不知道 Skill 文件在本机的位置：**
> Agent 不总是能从上下文中获取 Skill 目录路径。路径不明显时：
> - **询问用户**，其 Agent 或 IDE 从哪里加载 Skill，或希望将 Skill 安装到哪里；
> - **查阅产品文档**中关于"skills"、"agent skills"或"plugins"的说明——不同工具和版本路径各异；
> - 即使不安装，也可以**直接使用 Skill 内容**：在会话中获取或打开上方的 `SKILL.md` URL（unpkg/jsDelivr），使指导内容生效。若要持久化安装，将获取的文件复制到用户或文档指定的路径。
>
> **典型 Skill 位置**（请以工具当前文档为准——目录结构可能变化）：
>
> | 环境 | `SKILL.md` 放置位置 |
> |------|---------------------|
> | **Cursor** | 项目级：`.cursor/skills/pencil-design/SKILL.md`；用户级：`~/.cursor/skills/` |
> | **Claude Code** | 通常为 `.claude/skills/pencil-design/SKILL.md` 或用户级 `~/.claude/` |
> | **OpenClaw** | 通常为 `~/.openclaw/skills/`、工作区 `.agents/skills/`，或参考 [OpenClaw skills 文档](https://docs.openclaw.ai/skills/)——请根据用户配置确认 |
> | **其他 Agent（Codex 等）** | 使用你的产品用于存放 Skill 或提示词的目录 |
>
> **何时检查更新：**
> - **每次会话初期**，在第一次运行 Pencil 设计之前（对比 `npm view @pencil.dev/cli version` 与已安装 CLI 版本），以免遵循过时的说明；
> - **再次检查**：当用户表示已升级 CLI，或行为与本文档不符时（标志、认证、耗时等）；
> - **无需**在每条命令前都检查——每个会话检查一次即可，除非出现变更或错误提示版本不匹配。

## Creating a Design

The core command:

```bash
pencil --out <output.pen> --prompt "<design description>" --export <output.png> --export-scale 2
```

Key flags:
- `--out, -o` — where to save the `.pen` file (required)
- `--prompt, -p` — what to design (required)
- `--prompt-file, -f` — attach an image or text file to send with the prompt (repeatable). Same idea as attaching reference images in the Pencil editor chat; not for loading the prompt text from a file.
- `--export, -e` — export an image of the result
- `--export-scale` — image resolution multiplier (use 2 for crisp output)
- `--export-type` — format: `png` (default), `jpeg`, `webp`, `pdf`
- `--in, -i` — start from an existing `.pen` file (for iteration)
- `--model, -m` — Claude model to use (defaults to Opus)

> **中文说明（创建设计）：**
> 核心命令如上所示。
>
> 主要参数说明：
> - `--out, -o`：`.pen` 文件的保存路径（必填）
> - `--prompt, -p`：设计内容描述（必填）
> - `--prompt-file, -f`：附加图片或文本文件随提示词一起发送（可重复使用）。与在 Pencil 编辑器对话中附加参考图片的用途相同；不用于从文件加载提示词文本。
> - `--export, -e`：将结果导出为图片
> - `--export-scale`：图片分辨率倍数（建议使用 2 以获得清晰输出）
> - `--export-type`：格式，可选 `png`（默认）、`jpeg`、`webp`、`pdf`
> - `--in, -i`：从已有 `.pen` 文件开始（用于迭代修改）
> - `--model, -m`：使用的 Claude 模型（默认为 Opus）

### Passing the Prompt

Pass the user's request directly as the prompt — do not expand, or add detail beyond what the user actually said. The Pencil CLI has its own AI designer agent that handles creative decisions like layout structure, color palettes, typography, spacing, and content. Adding your own design specifics on top of the user's request will conflict with the CLI agent's own judgment and produce worse results.

If the user says "make me a landing page for a coffee shop", the prompt should be exactly that — not a paragraph with hero sections, color palettes, and font choices you invented.

> **中文说明（传递提示词）：**
> 将用户的原始请求直接作为提示词传入——不要扩展或添加用户未提及的细节。Pencil CLI 内置 AI 设计师 Agent，会自己处理布局结构、配色方案、字体排版、间距和内容等创意决策。在用户请求之上叠加你自己的设计细节，会与 CLI Agent 的判断产生冲突，导致效果变差。
>
> 如果用户说"帮我做一个咖啡店落地页"，提示词就应该是这句话本身——而不是你自行补充的包含 Hero 区块、配色和字体选择的长段描述。

### Timing Expectations

Design generation is not instant — the CLI runs an AI agent that plans the layout, creates each element, and validates the result visually. Expect:

- **Simple designs** (a card, a single component): 1-2 minutes
- **Medium designs** (an app screen, a landing page section): 2-3 minutes
- **Complex designs** (full landing page, detailed dashboard): 3-5+ minutes

Let the user know upfront that generation will take a few minutes so they're not left wondering. Use a generous timeout (at least 600000ms / 10 minutes) when running the command.

> **中文说明（时间预期）：**
> 设计生成不是即时完成的——CLI 会运行一个 AI Agent 来规划布局、创建每个元素并进行视觉验证。预计耗时如下：
>
> - **简单设计**（卡片、单个组件）：1-2 分钟
> - **中等设计**（应用页面、落地页某个区块）：2-3 分钟
> - **复杂设计**（完整落地页、详细仪表板）：3-5 分钟以上
>
> 请提前告知用户生成需要几分钟，避免用户等待时感到困惑。运行命令时请设置较大的超时时间（至少 600000ms / 10 分钟）。

### Showing the Result

After the command completes, read the exported image to show it to the user:

```bash
# The command exports to the path you specified
pencil --out design.pen --prompt "..." --export design.png --export-scale 2
```

Then use the Read tool on the exported PNG — it will render visually since you're a multimodal model.

Always show the image to the user after creating it. This is the whole point — they want to see the visual.

> **中文说明（展示结果）：**
> 命令执行完成后，读取导出的图片并展示给用户。对导出的 PNG 使用 Read 工具——由于你是多模态模型，图片将以可视化方式渲染。
>
> 创建完成后务必将图片展示给用户，这才是重点——用户希望看到视觉效果。

## Iterating on a Design

When the user wants changes to an existing design, use the `--in` flag to load the previous `.pen` file:

```bash
pencil --in design.pen --out design-v2.pen --prompt "Make the header larger and change the accent color to green" --export design-v2.png --export-scale 2
```

The agent will read the existing design and apply modifications rather than starting from scratch.

For quick successive iterations, keep a consistent naming pattern:
- `design.pen` → `design-v2.pen` → `design-v3.pen`
- Or use a single file: `--in design.pen --out design.pen` (overwrites)

> **中文说明（迭代设计）：**
> 当用户希望修改已有设计时，使用 `--in` 标志加载之前的 `.pen` 文件。Agent 会读取现有设计并应用修改，而不是从头开始。
>
> 快速连续迭代时，建议保持一致的命名规则：
> - `design.pen` → `design-v2.pen` → `design-v3.pen`
> - 或使用单一文件：`--in design.pen --out design.pen`（会覆盖原文件）

## Working Directory

Save design files in the user's current working directory or a subdirectory like `designs/`. Don't use temp directories — the user will want to find and iterate on these files later.

> **中文说明（工作目录）：**
> 将设计文件保存在用户当前工作目录或其子目录（如 `designs/`）中。不要使用临时目录——用户后续需要找到这些文件并进行迭代修改。
