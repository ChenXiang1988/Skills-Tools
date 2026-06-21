# md_to_docx - Markdown 批量转 Word 工具

## 文件说明

- `md_paths.txt`：待转换 Markdown 路径列表，一行一个，支持 `#` 注释
- `output_dir.txt`：Word 输出目录，一行一个路径，支持绝对路径或仓库相对路径
- `processed_md_paths.txt`：已转换路径记录，脚本自动维护
- `requirements.txt`：Python 依赖清单
- `package.json` / `package-lock.json`：本地 Mermaid 渲染依赖（`@mermaid-js/mermaid-cli`、`sharp`）
- `md_to_docx.py`：转换脚本

## 依赖

```bash
python3 -m pip install -r requirements.txt
```

再进入 `tools/md_to_docx` 执行：

```bash
npm install
```

## 用法

在仓库根目录执行：

```bash
python tools/md_to_docx/md_to_docx.py
```

## 操作步骤

1. 打开 `tools/md_to_docx/md_paths.txt`，把需要转换的 Markdown 路径按行写进去。
2. 打开 `tools/md_to_docx/output_dir.txt`，写入 `.docx` 输出目录。
3. 运行脚本：
   ```bash
   python tools/md_to_docx/md_to_docx.py
   ```
4. 查看输出目录中的 `.docx` 文件。

## 路径规则

- `md_paths.txt` 中的路径可以是绝对路径，也可以是仓库相对路径
- 相对路径会按仓库根目录解析
- `output_dir.txt` 同样支持绝对路径或仓库相对路径
- 如果同名 `.docx` 已存在，脚本会自动追加 `-1`、`-2` 以避免覆盖

## 已处理记录

- 脚本会把成功转换的 Markdown 绝对路径写入 `processed_md_paths.txt`
- 下次运行时会自动跳过
- 如果要重新转换某个文件，删除 `processed_md_paths.txt` 里对应那一行即可

## 图片处理

- Markdown 中的相对路径图片会按输入文件所在目录解析
- 例如 `![图](images/a.png)`
- 远程图片链接会保留为文本提示，不会自动下载
- Markdown 里的 HTML 注释块（`<!-- ... -->`）会被忽略，不会写入 Word
- Mermaid 代码块会先渲染成图片，再写入 Word

## 注意事项

- 这是批量转换工具，不需要每次手动输入路径
- Word 字体在不同系统上会有差异，中文字体会尽量自动适配
- 如果 Markdown 里有复杂嵌套表格、脚注、数学公式，渲染效果可能不完全一致
