# HTML 原型规范说明

> Plan 方案经用户确认后，才能输出 HTML 原型。HTML 原型未经用户确认，不得进入 PRD 阶段。
> HTML 原型是可直接在浏览器中打开预览的**轻交互 HTML 页面**，使用 Ant Design 组件渲染。每个页面对应一个 HTML 文件，必须可直接渲染，并包含轻量 JS 交互（页面跳转、弹窗/抽屉开关、Tab 切换、表单校验、列表筛选）。

## 0. 文档信息

| 字段 | 内容 |
|------|------|
| 标题 | <!-- @PROJECT_NAME --> HTML 原型规范 |
| 文档类型 | HTML 原型规范说明 |
| 版本 | v1.0 |
| 日期 | <!-- @DATE --> |
| 作者 | <!-- @AUTHOR --> |
| 相关方 | <!-- @STAKEHOLDERS --> |

## 一、原型定义

本规范定义的 HTML 原型为**轻交互原型**，具备以下能力：

| 交互类型 | 实现方式 | 示例 |
|---------|---------|------|
| 页面跳转 | `<a href>` 或 `location.href` | 列表页 → 详情页 |
| 弹窗/抽屉开关 | Ant Design Modal/Drawer API | 点击"审核"按钮 → 打开 Modal |
| Tab / 折叠切换 | `display` 切换 或 Ant Design Tabs | 详情页 Tab 切换 |
| 表单校验提示 | Ant Design Form 校验规则 | 必填项未填 → 红色提示 |
| 列表筛选（前端 Mock） | JS 数组 `filter` | 输入单号 → 列表过滤 |

**不要求**：后端数据联动、复杂状态管理、权限控制逻辑。

## 二、HTML 模板文件（强制使用）

原型生成时，**必须从以下模板文件读取并填充**，不得从零手写 HTML 结构。

| 模板文件 | 适用页面类型 | 文件路径 |
|---------|------------|---------|
| `list-page.html` | 列表页（含查询区、Table、分页） | `reference/prototype-html/list-page.html` |
| `detail-page.html` | 详情页（含 Descriptions、Tab、关联表） | `reference/prototype-html/detail-page.html` |
| `form-page.html` | 新建/编辑表单页（含 Form、校验、提交） | `reference/prototype-html/form-page.html` |
| `drawer-modal.html` | 抽屉/弹窗组件参考（嵌入其他页面使用） | `reference/prototype-html/drawer-modal.html` |

**使用方式**：读取对应模板 → 替换 `<!-- @PLACEHOLDER -->` 占位符 → 补充 Mock 数据 → 输出到 `./prototype/` 目录。

## 三、技术与样式规范

### 3.1 技术栈

| 项目 | 规范 |
|------|------|
| UI 框架 | Ant Design 5.x（React UMD CDN） |
| CDN 地址 | `https://unpkg.com/antd@5/dist/antd.min.js` |
| React CDN | `https://unpkg.com/react@18/umd/react.production.min.js` |
| JS 方言 | Babel standalone（`<script type="text/babel">`） |
| 流程图 | Mermaid 10.x CDN |
| 品牌色 | 泓湖主色 `#C4171C`，主色悬浮态 `#E64A4F` |

### 3.2 泓湖品牌色 CSS 变量（强制注入每个 HTML 文件）

```css
:root {
    --hhong-primary: #C4171C;
    --hhong-primary-hover: #E64A4F;
    --hhong-primary-light: #FFF1F0;
    --hhong-gold: #D4A017;
    --hhong-gold-light: #FFF7E6;
}
/* Ant Design 主色覆盖 */
.ant-btn-primary { background-color: var(--hhong-primary) !important; border-color: var(--hhong-primary) !important; }
```

### 3.3 页面基础结构

每个 HTML 文件必须包含：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title><!-- @PAGE_TITLE --></title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/antd@5/dist/reset.css">
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/antd@5/dist/antd.min.js"></script>
    <script crossorigin src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- 泓湖品牌色 CSS 变量 -->
    <style>/* ... */</style>
</head>
<body>
    <div id="root"><!-- Ant Design 组件渲染区 --></div>
    <script type="text/babel">
        // 轻交互 JS + Mock 数据
    </script>
</body>
</html>
```

## 四、原型范围

- **对应 Plan**：<!-- @PLAN_DOC_LINK -->
- **覆盖页面**：（按 `prototype-html/` 模板类型列出）

| 页面编号 | HTML 文件名 | 页面类型 | 使用角色 | 对应 UC |
|---------|------------|---------|---------|---------|
| P-001 | `prototype-p001-xxx.html` | 列表页 | <!-- @ROLE --> | <!-- @UC_ID --> |

- **不覆盖内容**：<!-- @OUT_OF_SCOPE -->
- **原型目标**：<!-- @PROTOTYPE_GOAL -->

## 五、Mock 数据规范

每个 HTML 原型文件必须包含至少 **3 条 Mock 数据**，且覆盖不同状态（如：启用/停用、已审核/待审核）。

```js
// Mock 数据示例（在 HTML 文件的 <script> 中定义）
const mockData = [
    { id: '001', name: '示例A', status: 'enabled', statusLabel: '启用', statusColor: 'green' },
    { id: '002', name: '示例B', status: 'disabled', statusLabel: '停用', statusColor: 'red' },
    { id: '003', name: '示例C', status: 'enabled', statusLabel: '启用', statusColor: 'green' },
];
```

## 六、轻交互 JS 规范

### 6.1 页面跳转

```js
function navigateTo(url) { window.location.href = url; }
```

### 6.2 弹窗/抽屉

```js
// 确认弹窗
antd.Modal.confirm({ title: '确认操作', content: '确认执行？', onOk: () => { /* ... */ } });

// 详情抽屉
antd.Drawer.confirm({ title: '详情', width: 520, content: '...' });
```

### 6.3 表单校验

使用 Ant Design Form 的 `rules` 属性，必填项未填时显示红色提示文字，不得提交。

### 6.4 列表筛选

在"查询"按钮的 `onClick` 回调中，对 Mock 数据执行 `Array.filter()`，然后重新渲染 Table。

## 七、页面流转说明（Mermaid）

> 页面流转图必须以"页面"为节点，不能以"操作"为节点。

```mermaid
graph TD
    A[P-001 列表页] -->|点击"新增"| B[P-002 新建页]
    B -->|提交成功| A
    A -->|点击"查看"| C[P-003 详情页]
```

## 八、异常与空状态

| 场景 | Ant Design 组件 | 说明 |
|------|----------------|------|
| 列表无数据 | `Empty` | 展示"暂无数据"图标 + 文案 |
| 操作失败 | `Modal.confirm` 或 `message.error` | 弹出错误提示 |
| 表单校验失败 | Form 校验提示 | 字段下方红色文字 |

## 九、HTML 文件命名规范

| 规则 | 说明 |
|------|------|
| 管理后台页面 | `prototype-p{三位数编号}-{页面名称}.html`，如 `prototype-p001-客户管理列表页.html` |
| PDA/移动端页面 | `prototype-m{三位数编号}-{页面名称}.html`，如 `prototype-m001-拣货任务页.html` |
| 目录位置 | `./prototype/` 目录下 |

## 十、确认结论

- HTML 原型是否确认：<!-- @CONFIRMED: 待用户确认 / 已确认 -->
- 进入下一阶段条件：用户明确确认所有 HTML 原型文件后，才生成 PRD。
