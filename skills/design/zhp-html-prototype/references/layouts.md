# 布局规则（Layouts）

生成业务页时遵循以下布局约定，保证多页风格一致。

## 整体骨架
- 左侧 `sidebar`（深色 #001529，宽 220px）+ 右侧 `main`（header + content）。
- `header` 固定顶部，显示当前页标题与用户。
- `content` 最大宽度 1280px 居中。

## 卡片（.card）
- 查询区、表格区各自独立成卡。
- 卡片内边距：上下 16px、左右 24px。

## 查询/筛选区（.filter-bar）
- 每个筛选条件用 `.filter-item`（label 在上、控件在下）。
- 控件最小宽度 160px；多个条件横向排列、可换行。
- 操作按钮（查询/重置）靠右（`filter-actions` 的 `margin-left:auto`）。

## 表格（table.grid）
- 表头浅灰底 #fafafa，列左对齐，单元格上下 12px、左右 16px。
- 行 hover 浅灰；最后一行去底边线。
- 长文本列可用 `title` 属性提供完整值；状态列用 `.tag` 而非纯文字。

## 操作区
- 表格卡片右上放"新增"等主操作（`btn btn-primary`）；行内操作用 `btn-link`（编辑/查看）与 `btn-link danger`（删除）。

## 弹窗（.modal）
- 单一 `.modal-mask` + `.modal`，由 `openModal(mode)` 控制显隐。
- 表单字段纵向排列（`.form-row`：label 在上、控件在下）。
- 新增/编辑共用同一弹窗，靠 `mode` 切换标题。

## 禁止
- 禁止在页面内写 `<style>` 自创样式覆盖公共 CSS。
- 禁止引入外部 CDN（保证 `file://` 可直接打开）。
- 禁止自定颜色/圆角/间距数值——一律用 prototype.css 的类与 CSS 变量。
