# 项目长期记忆 (Skills-Tools)

## 工作区分类规范（2026-07-17 确立，见仓库 CONVENTIONS.md）
- 顶层桶：skills/（独立 skill）、packages/（套件）、tools/（通用脚本）、experts/（人设）、assets/（共享资源，字体→assets/fonts/）、intro/（HTML 介绍页）。
- 命名：全英文小写连字符（kebab-case）；禁止哈希目录名；skill 目录名 = `name` 字段。
- 套件优先：套件内已有的 skill 不在 skills/ 另存独立副本（删独立副本保套件版）。
- intro/ 强制：工作区 HTML 介绍/预览页统一放 intro/，skill 内部文档不进 intro/。
- 演示类两 skill 不混淆：pm-html-presentation（演示/幻灯片）vs pm-html-prototype（原型，在套件内）。
- 供应链两 PRD 保留区分：prd-writer（通用）vs supply-chain-prd-writer（四阶段门禁）。

## 已知待确认项
- markitdown-skill 的 SKILL.md 嵌套在 tools/doc-convert/batch-doc-convert/（本质是 skill 却不在 skills/），待决定是否迁入 skills/markitdown-skill/。
