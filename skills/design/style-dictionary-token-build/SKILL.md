---
name: style-dictionary-token-build
description: 用 style-dictionary v5 把单一 Token 源编译到 CSS/SCSS/JS/JSON 等多端。覆盖 v5 的
  ESM-only、显式 {value} 格式、usesDtcg、本地 node_modules 解析等踩坑点。当用户要做设计系统 Token
  多端分发、Design Token 编译、style-dictionary 配置时调用。
disable: true
---

# style-dictionary v5 多端 Token 编译

把一份 Token 源（JSON）编译成 CSS 变量 / SCSS 变量 / JS 常量 / 扁平 JSON，供 Web / 小程序 / 原生 App 共用。

## 关键事实（v5 已踩坑，必看）

1. **v5 是 ESM-only 包**（`"type":"module"`）。不要 `require()`，用 `.mjs` + `import StyleDictionary from 'style-dictionary'`。
2. **Token 源必须显式 `{value:...}`**，v5 不认 legacy shorthand（`"600":"#0052D9"` 会被当普通字符串/忽略，allTokens 为空 → "No tokens"）。
   - 正确：`"600": { "value": "#0052D9" }`
   - 引用语法不变：`"primary": { "value": "{global.color.brand.600}" }`，在 build 阶段展开。
3. **legacy 格式要显式 `usesDtcg:false`**（否则 v5 默认按 DTCG `{ "$value" }` 解析，你的 `{value}` 会失败）。
4. **ESM 裸导入只认 node_modules 可达路径**：`import 'style-dictionary'` 需要脚本所在目录向上能找到 `node_modules/style-dictionary`（软链或 `npm i -D style-dictionary` 均可）。`NODE_PATH` 对 ESM 无效。CLI `bin/index.js` 因传递依赖不在同一 node_modules 而失败，别用。
5. **运行前必须 `cd` 到项目目录**：config 的 `source` 相对 cwd 解析。
6. v5 实例无 `transformGroup`/`format` 实例属性属正常，built-in 在 build 时内部生效。

## 最小可用结构

```
design-system/
├── tokens/tokens.json     # 单一真源，显式 {value}
├── sd.config.json         # source + platforms
├── build-tokens.mjs       # 构建脚本
├── package.json           # devDependencies: style-dictionary ^5
└── node_modules/style-dictionary -> 托管环境安装(软链)
```

### tokens/tokens.json（节选）
```json
{
  "global": { "color": { "brand": { "600": { "value": "#0052D9" } } } },
  "semantic": { "light": { "color": { "brand": { "primary": { "value": "{global.color.brand.600}" } } } } }
}
```

### sd.config.json
```json
{
  "source": ["tokens/tokens.json"],
  "usesDtcg": false,
  "platforms": {
    "css":  { "transformGroup": "css",  "buildPath": "dist/css/",  "files": [{ "destination": "tokens.css",  "format": "css/variables" }] },
    "scss": { "transformGroup": "scss", "buildPath": "dist/scss/", "files": [{ "destination": "tokens.scss", "format": "scss/variables" }] },
    "js":   { "transformGroup": "js",   "buildPath": "dist/js/",   "files": [{ "destination": "tokens.js",   "format": "javascript/es6" }] },
    "json": { "transformGroup": "js",   "buildPath": "dist/json/", "files": [{ "destination": "tokens.flat.json", "format": "json/flat" }] }
  }
}
```

### build-tokens.mjs
```js
import StyleDictionary from 'style-dictionary';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const dir = fileURLToPath(new URL('.', import.meta.url));
const cfg = JSON.parse(readFileSync(dir + 'sd.config.json', 'utf8'));
const sd = new StyleDictionary(cfg);
await sd.buildAllPlatforms();
console.log('tokens 编译完成 -> dist/{css,scss,js,json}');
```

## 运行
```bash
cd design-system
node build-tokens.mjs
```
输出：`dist/css/tokens.css`（`--semantic-light-color-brand-primary: #0052D9` 等，引用已展开）、`tokens.scss`、`tokens.js`、`tokens.flat.json`。

## 调试清单（"No tokens" 时）
- [ ] 每个叶子是否 `{ "value": ... }`（非 shorthand）
- [ ] config 是否 `usesDtcg:false`（legacy 格式）
- [ ] `cd` 到项目目录再运行（source 相对 cwd）
- [ ] `node_modules/style-dictionary` 可达（软链或 npm i）
- [ ] 用 `.mjs` 而非 `.js`（ESM）

## 扩展多端
- 小程序 WXSS / 原生：新增 platform，`format: "css/variables"` 改文件后缀，或自定义 format 输出平台专属语法。
- 换肤：多套 `semantic` 映射（light/dark/pda-highcontrast），改 Token 一处重跑即全端同步。
