# doc_to_md - Word 转 Markdown 工具

## 文件说明

- `doc_paths.txt`：待转换源路径列表，一行一个，支持文件或文件夹
- `output_dir.txt`：Markdown 输出目录，一行一个路径，支持绝对路径或仓库相对路径
- `processed_doc_paths.txt`：已转换文件记录，脚本自动维护
- `requirements.txt`：Python 依赖清单
- `doc_to_md.py`：转换脚本

## 依赖

```bash
python3 -m pip install -r requirements.txt
```

## 用法

在仓库根目录执行：

```bash
python tools/doc_to_md/doc_to_md.py
```

## 操作步骤

1. 打开 `tools/doc_to_md/doc_paths.txt`
2. 把需要转换的 `.doc` / `.docx` 文件路径写进去
3. 也可以直接写一个文件夹路径，脚本会递归扫描其中的 `.doc` / `.docx`
4. 打开 `tools/doc_to_md/output_dir.txt`
5. 写入 Markdown 输出目录
6. 运行脚本：
   ```bash
   python tools/doc_to_md/doc_to_md.py
   ```

## 路径规则

- `doc_paths.txt` 中的路径可以是绝对路径，也可以是仓库相对路径
- 相对路径会按仓库根目录解析
- 输出目录同样支持绝对路径或仓库相对路径
- 同名输出目录已存在时，脚本会自动追加 `-1`、`-2`，避免覆盖

## 处理规则

- 只处理 `.doc` 和 `.docx`
- `.ppt` / `.pptx` 会自动跳过
- 成功转换的文件会写入 `processed_doc_paths.txt`
- 下次运行时会自动跳过已处理文件
- 如果要重新转换某个文件，删除 `processed_doc_paths.txt` 中对应那一行即可

## 输出结构

每个 Word 文件会生成一个独立文件夹，里面包含：

- `document.md`
- `images/`（如果文档里有图片，图片会放这里）

## 转换引擎

- 在 macOS 上优先使用系统自带的 `textutil`
- 如果当前环境没有 `textutil`，脚本会尝试 `LibreOffice` 的命令行能力
- 文档结构越复杂，Markdown 结果和原始排版的差异越大，这是格式转换的正常限制

## 注意事项

- 这不是 Word 到 Word 的无损转换
- 表格、页眉页脚、批注、复杂文本框等内容，可能会有损失
- 如果源文件里有图片，脚本会尽量提取并放到输出目录下的 `images/`
- 目录输入模式下，脚本会递归扫描子目录
