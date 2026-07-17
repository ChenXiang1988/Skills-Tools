# 交互模式（Interactions）

原型阶段只做**轻量、可演示**的交互，不写复杂业务逻辑。以下为约定模式。

## 菜单导航
- 由 `shared/app-shell.js` 的 `renderShell({activeKey})` 渲染。
- 页面切换 = 跳转 `href`（整页刷新即可，原型无需 SPA 路由）。
- 当前页 `activeKey` 与 `menu-config.js` 的 `key` 对应，高亮左侧菜单。

## 弹窗
- 新增：`onclick="openModal('add')"` → 标题"新增"。
- 编辑：`onclick="openModal('edit')"` → 标题"编辑"。
- 关闭：取消按钮、`closeModal()`、或点击遮罩。
- 确定：原型阶段用 `closeModal()` 关闭即可（不接后端）。

## 查询/重置
- 原型阶段查询按钮可仅 `alert` 或刷新视觉；不必接真实数据。
- 重置按钮清空表单控件。

## 删除确认
- 行内删除用 `confirm('确认删除？')` 或 `alert` 演示；不真删数据。

## 分页
- 用 `.pagination` 渲染页码，当前页 `.active`。
- 原型阶段页码为静态展示。

## 状态标签
- 用 `.tag` + 修饰类表达状态，不写行内 color：
  - 启用/在线/成功 → `.tag-success`
  - 停用/离线/告警 → `.tag-warning` / `.tag-error`
  - 待处理/未知 → `.tag-info` / `.tag-default`

## 原则
- 交互只为"让评审者看懂流程"，用最少的 JS（app-shell.js 已提供菜单/弹窗基础设施）。
- 不引入框架（Vue/React），保持单文件 + 原生 JS。
