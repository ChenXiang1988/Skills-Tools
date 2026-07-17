# 工作区规范 (CONVENTIONS)

本仓库统一遵循以下分类与命名规范。结构总览见 [INDEX.md](./INDEX.md)。

## 1. 顶层按"制品类型"分桶

| 桶 | 含义 | 说明 |
|---|---|---|
| `skills/` | 独立 skill（最小可调用单元） | 每个子目录 = 一个 skill，目录名须等于其 `SKILL.md` 的 `name` 字段 |
| `packages/` | 多 skill 套件（含 manifest/KIT.md） | 套件内 skill 随套件走，整包管理 |
| `tools/` | 通用脚本 / CLI（非 skill 形态） | 文档转换、图片处理等独立脚本 |
| `experts/` | 角色 / 专家人设定义 | `.md` 文件 |
| `assets/` | 共享二进制资源 | 字体等；字体统一放 `assets/fonts/` |
| `intro/` | 工作区 HTML 介绍 / 预览页 | 见第 4 条 |

## 2. 命名约定

- 目录与文件：**全英文、小写、连字符**（`kebab-case`）。
  - 例：`supply-chain`、`pm-html-presentation`、`batch-doc-convert`。
- **禁止**哈希 / 随机 ID 作为目录名（如 `skill_2053083553754644480` → 改为语义名）。
- skill 目录名 = 其 `SKILL.md` 中 `name:` 字段的值。
- `skills/` 下按**领域**建二级分类目录（当前：`agent-ops/`、`content/`、`design/`、`engineering/`、`pm/`、`supply-chain/`）；通用/未归类 skill 可平铺在 `skills/` 下。

## 3. 套件优先（去重规则）

- **套件（`packages/`）内已有的 skill，不在 `skills/` 另存独立副本。**
- 若发现同名 skill 同时存在于 `packages/<kit>/skills/` 与 `skills/`，**删除 `skills/` 中的独立副本，保留套件版**。
- `packages/` 内部一律不手动改动（增删/重命名其内部 skill 由套件自身版本管理决定）。
- 例：`pm-prd`、`pm-flow`、`humanizer`、`pm-html-prototype`、`pm-mermaid-diagram` 等已随套件保留，`skills/` 中对应独立副本已删除。

## 4. intro/ 介绍页规范（本工作区强制）

- 所有**工作区级 HTML 介绍 / 预览 /  landing 页**统一放入 `intro/`，建议命名 `<名称>.html`。
- skill / 套件**自身内部**的使用文档（如 `pakco-html/docs/readme/*.html`、套件 `assets/`）仍随制品存放，**不**进 `intro/`。
- 套件自带的对外介绍页如需作为工作区统一入口，可**迁移**至 `intro/`（如 `pm-flow-kit.html`）。

## 5. 资源与依赖

- 共享字体放 `assets/fonts/`。
- 各 skill / 套件内部尽量**零外部依赖**（系统字体栈、内联资源优先）。
- Python 依赖隔离在虚拟环境，不污染用户环境；`__pycache__/`、编译产物不入库。

## 6. 已知平级约束

- 两个演示类 skill **互不复用、不可混淆**：
  - `pm-html-presentation`（上游 `pakco-html`，本地改名，现位于 `skills/design/pm-html-presentation/`）—— HTML 演示 / 幻灯片生成。
  - `pm-html-prototype`（位于 `packages/pm-flow-kit-*/skills/`）—— HTML 原型。
- 两个供应链 PRD skill **保留并明确区分**：
  - `prd-writer`（通用 10 段式 PRD）—— `skills/supply-chain/PRD-writer`。
  - `supply-chain-prd-writer`（供应链四阶段门禁 PRD，面向 WMS/OMS/TMS）—— `skills/supply-chain/supply-chain-prd-writer`。

## 7. 待确认事项（已知例外）

- `markitdown-skill` 已落定：统一到 `skills/content/markitdown-skill/`（带 SKILL.md 的本质是 skill，归 `skills/`）；`tools/doc-convert/batch-doc-convert/` 副本已移入回收站，`tools/doc-convert/` 仅保留纯脚本（`doc_to_md`、`md_to_docx`、`wx2md`）。
