# Ardot 设计系统交付 — 实操参考

## 节点 ID 与绑定名

- `mcp__ardot__batch_edit` 中 `I(parent, { ... })` 返回的绑定名（如 `root`、`header`）只在该次调用内有效。
- 跨 batch 引用时，必须用 `fetch_file_info` 或 `capture_layout` 拿到显式节点 ID（如 `"2:3"`、`"2:12"`）。
- 建议：每完成一块关键结构（如 header、色彩 section），用 `capture_layout` 取一次节点树，确认后续要引用的 ID。

## 颜色与填充

- 文本节点 `fill` 只接受 hex 字符串（如 `"#1677FF"`）。写 `rgba(...)` 会报错。
- 框架填充需要透明度时，用 `fills` 数组并指定 `opacity`：
  ```json
  {
    "fills": [{
      "type": "SOLID",
      "color": { "r": 0.0, "g": 0.0, "b": 0.0 },
      "opacity": 0.88,
      "visible": true,
      "blendMode": "NORMAL"
    }]
  }
  ```
- 不要写 `color: { r, g, b, a }`，`a` 会被忽略或报错。

## 布局属性

- `layout` 取值：`"vertical"` | `"horizontal"` | `"none"`。
- `primaryAxisAlignItems`：竖排时为竖轴对齐，横排时为横轴对齐。常用 `"SPACE_BETWEEN"`、`"CENTER"`。
- `counterAxisAlignItems` 只接受 `"MIN"` / `"MAX"` / `"CENTER"` / `"BASELINE"`。
- 文字水平对齐用 `textAlignHorizontal`：`"LEFT"` / `"RIGHT"` / `"CENTER"`。

## 阴影

- `effects` 数组中 `type: "DROP_SHADOW"`。
- 必须包含 `boundVariables: {}`，否则某些校验会失败。
- 示例：
  ```json
  {
    "effects": [{
      "type": "DROP_SHADOW",
      "color": { "r": 0, "g": 0, "b": 0, "a": 0.06 },
      "offset": { "x": 0, "y": 2 },
      "radius": 8,
      "spread": 0,
      "visible": true,
      "blendMode": "NORMAL",
      "showShadowBehindNode": true,
      "boundVariables": {}
    }]
  }
  ```

## 校验清单

- [ ] `capture_layout` `problemsOnly: true` 无异常。
- [ ] 关键区块已截图并人工核验。
- [ ] 文字未使用 rgba 字符串。
- [ ] 跨 batch 的绑定已替换为显式 ID。
- [ ] 设备相关主题切换正确（桌面亮色默认，PDA 暗色默认）。
- [ ] DESIGN.md 与 tokens.css 中的同一 token 值一致。
