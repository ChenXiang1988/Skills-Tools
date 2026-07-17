# 原型目录初始化步骤

当用户要求"开始画原型""初始化原型目录""新建第一个页面"，且项目根目录尚无 `prototypes/` 时，执行以下初始化（把 skill 的 assets 复制到目标项目）：

1. 确定目标项目的原型根目录（默认项目根 `prototypes/`；若项目 `AGENTS.md` 指定了别的目录则遵循）。
2. 创建目录结构：
   ```
   mkdir -p prototypes/assets prototypes/shared
   ```
3. 复制共享资产（从本 skill 的 `assets/` 到目标的 `prototypes/`）：
   - `design-tokens.json` → `prototypes/assets/`
   - `prototype.css`      → `prototypes/assets/`（PC 后台）
   - `device-frame.css`   → `prototypes/assets/`（移动端设备框，**移动端必复制**）
   - `prototype-mobile.css`→ `prototypes/assets/`（移动端布局，**移动端必复制**）
   - `app-shell.js`       → `prototypes/shared/`
   - `menu-config.js`     → `prototypes/shared/`
   - `prototype-component-demo.html` → `prototypes/assets/`（控件视觉参考页，可选）
   - `validate_prototype.py` → `prototypes/assets/`（**必须**，校验脚本按自身位置推算根目录，放 assets/ 时 ROOT 正好等于 prototypes/）
4. 用 `template.html` 生成首个 `index.html`（工作台/入口页），并令其 `activeKey` 指向菜单第一项。
5. 创建 `shared/menu-config.js` 初始菜单（至少一项指向 `index.html`）。
6. 进入 `prototypes/` 目录，运行 `python3 assets/validate_prototype.py` 确认结构通过。
   ⚠️ 校验脚本必须放在 `prototypes/assets/` 下再运行；若放在 `prototypes/` 根目录，其根目录推算会跳到上一级（项目根），导致检查全部误报。

> 初始化后，新增页面只需：复制 `template.html` → 命名新页 → 填内容 → 在 `menu-config.js` 追加菜单项 → 重跑校验。
