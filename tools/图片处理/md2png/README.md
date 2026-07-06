# Markdown 转高清 PNG 图片

将 Markdown 文件渲染为高清 PNG 图片（3x 视网膜级画质）。

## 功能

- 支持中文排版（Noto Sans CJK SC / PingFang SC）
- Mermaid 图表自动渲染为矢量图嵌入
- Frontmatter 元数据（title / author）
- 表格、代码块、任务列表、删除线、高亮
- 本地图片自动嵌入（base64）
- 批处理 + 增量记录，避免重复转换

---

## 安装

### 1. Python 依赖（直接装在系统中，不要 venv）

```bash
cd tools/md2png
pip3 install -r requirements.txt
```

### 2. Playwright Chromium 浏览器（只装一次，约 130 MB）

```bash
python3 -m playwright install chromium
```

### 3. Node.js 依赖（Mermaid 渲染）

```bash
cd tools/md2png
npm install
```

---

## 使用

### 配置

| 文件 | 作用 |
|------|------|
| `md_paths.txt` | 要转换的 `.md` 文件路径，每行一个 |
| `output_dir.txt` | PNG 输出目录，一行 |
| `processed_md_paths.txt` | 自动追加已转换记录，可清空重置 |

### 运行

```bash
cd 仓库根目录
python3 tools/md2png/md2png.py
```

### 画质配置

在 `md2png.py` 顶部可调整：

```python
SCALE_FACTOR = 3       # 3x 高清（约 288 DPI）
VIEWPORT_WIDTH = 1200  # 视口宽度
```

---

## 故障排查

### `pip3: command not found`
macOS 上用 `pip3` 或者 Python 3 自带的 pip。

### playwright 找不到
确认已安装：`python3 -m playwright install chromium`

### Mermaid 渲染失败
确认在 `tools/md2png` 目录下执行过 `npm install`
