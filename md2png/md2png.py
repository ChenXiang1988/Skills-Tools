#!/usr/bin/env python3
"""
批量将 Markdown 文件转换为高清 PNG 图片。

相关文件：
  - md_paths.txt
  - output_dir.txt
  - processed_md_paths.txt

依赖安装：
  python3 -m pip install -r requirements.txt
  python3 -m playwright install chromium   # 首次安装浏览器
  npm install  # 在 tools/md2png 目录下，用于 Mermaid 渲染

使用方式：
  python tools/md2png/md2png.py

`md_paths.txt` 中每一行非空内容都会被当作一个 Markdown 路径。
以 `#` 开头的行会被忽略。输出目录从 `output_dir.txt` 读取，
如果目录不存在会自动创建。
"""

from __future__ import annotations

import asyncio
import base64
import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path

try:
    import markdown
    from bs4 import BeautifulSoup, Comment, NavigableString, Tag
    from playwright.async_api import async_playwright
except ImportError as exc:  # pragma: no cover
    print(f"Missing dependency: {exc}")
    print(
        "Install requirements with: "
        "python3 -m pip install playwright markdown beautifulsoup4"
    )
    print("Then install Chromium: python3 -m playwright install chromium")
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
MD_PATHS_FILE = BASE_DIR / "md_paths.txt"
OUTPUT_DIR_FILE = BASE_DIR / "output_dir.txt"
PROCESSED_FILE = BASE_DIR / "processed_md_paths.txt"

# PNG 输出配置
SCALE_FACTOR = 3      # 3x 高清（相当于 288 DPI）
VIEWPORT_WIDTH = 1200  # 视口宽度（像素）
JPEG_QUALITY = None    # PNG 无损；如需 JPEG 设为 95 等

# Markdown 扩展
MARKDOWN_EXTENSIONS = [
    "extra",
    "codehilite",
    "toc",
    "sane_lists",
    "pymdownx.tasklist",
    "pymdownx.tilde",
    "pymdownx.superfences",
    "pymdownx.mark",
]

MARKDOWN_EXTENSION_CONFIGS = {
    "codehilite": {"linenums": False, "guess_lang": True},
    "toc": {"permalink": False, "title": "目录"},
    "pymdownx.tasklist": {"custom_checkbox": True},
}

# ------------------------------- CSS 样式 -------------------------------

DEFAULT_CSS = """
@font-face {
    font-family: "Noto Sans CJK SC";
    src: local("Noto Sans CJK SC"), local("NotoSansCJK-Regular"),
         local("PingFang SC"), local("Microsoft YaHei"),
         local("SimSun");
    font-weight: normal;
    font-style: normal;
}
@font-face {
    font-family: "Noto Sans CJK SC";
    src: local("Noto Sans CJK SC Bold"), local("NotoSansCJK-Bold"),
         local("PingFang SC Semibold");
    font-weight: bold;
    font-style: normal;
}
@font-face {
    font-family: "Courier New";
    src: local("Courier New"), local("Menlo"), local("Consolas");
    font-weight: normal;
    font-style: normal;
}

body {
    font-family: "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif;
    line-height: 1.8;
    font-size: 14pt;
    color: #333;
    margin: 0;
    padding: 40px 50px;
    max-width: 960px;
    background: #fff;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
    font-family: "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif;
}
h1 { font-size: 22pt; border-bottom: 2px solid #eee; padding-bottom: 0.3em; }
h2 { font-size: 18pt; border-bottom: 1px solid #eee; padding-bottom: 0.2em; }
h3 { font-size: 15pt; }

p { margin: 0.8em 0; text-align: justify; text-justify: inter-ideograph; }
blockquote {
    border-left: 4px solid #ddd;
    padding: 0.5em 1em;
    color: #666;
    background-color: #f9f9f9;
    margin: 1em 0;
}
hr { border: none; border-top: 1px solid #eee; margin: 2em 0; }
a { color: #3498db; text-decoration: none; }

code {
    font-family: "Courier New", Menlo, Monaco, monospace;
    background-color: #f5f5f5;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 0.9em;
}
pre {
    background-color: #f8f8f8;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    padding: 12px;
    overflow-x: auto;
    margin: 1em 0;
    font-family: "Courier New", Menlo, Monaco, monospace;
    font-size: 12pt;
    line-height: 1.5;
}
pre code { background: none; padding: 0; font-size: 12pt; }

table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 13pt; }
table, th, td { border: 1px solid #ddd; }
th, td { padding: 8px 14px; text-align: left; }
th { background-color: #f5f5f5; font-weight: 600; }
tr:nth-child(even) { background-color: #fafafa; }

ul, ol { margin: 0.8em 0; padding-left: 2em; }
li { margin: 0.4em 0; }

img { max-width: 100%; height: auto; display: block; margin: 1em auto; }
"""


def clean_user_path(raw: str) -> Path:
    value = raw.strip().strip('"').strip("'")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    else:
        path = path.resolve()
    return path


def read_list_file(path: Path) -> list[str]:
    if not path.exists():
        return []

    items: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            items.append(stripped)
    return items


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    name = name.strip().strip(".")
    return name or "document"


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return {}, text

    meta: dict[str, str] = {}
    for line in lines[1:end_idx]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip('"').strip("'")

    body = "\n".join(lines[end_idx + 1:]).lstrip("\n")
    return meta, body


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def load_processed_paths() -> set[str]:
    processed: set[str] = set()
    if not PROCESSED_FILE.exists():
        return processed
    for raw_path in read_list_file(PROCESSED_FILE):
        processed.add(str(clean_user_path(raw_path)))
    return processed


def append_processed_path(source_path: Path) -> None:
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_FILE.open("a", encoding="utf-8") as f:
        f.write(str(source_path.resolve()) + "\n")


def image_to_data_uri(image_path: Path) -> str:
    """将本地图片转为 base64 data URI，避免 file:// 跨域问题。"""
    ext = image_path.suffix.lower().lstrip(".")
    mime_map = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "svg": "image/svg+xml",
        "webp": "image/webp",
        "bmp": "image/bmp",
    }
    mime = mime_map.get(ext, "image/png")
    data = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


class MarkdownToPng:
    """将单个 Markdown 文件转为高清 PNG 图片。"""

    def __init__(
        self,
        source_path: Path,
        output_dir: Path,
        browser,
    ) -> None:
        self.source_path = source_path
        self.source_dir = source_path.parent
        self.output_dir = output_dir
        self.browser = browser
        self.meta: dict[str, str] = {}
        self.temp_images: list[Path] = []

    # ---------- Step 1: 读取 ----------

    def load_markdown(self) -> str:
        raw = self.source_path.read_text(encoding="utf-8")
        self.meta, body = split_frontmatter(raw)
        return normalize_text(body)

    # ---------- Step 2: Markdown → HTML ----------

    def convert(self, markdown_text: str) -> str:
        html_body = markdown.markdown(
            markdown_text,
            extensions=MARKDOWN_EXTENSIONS,
            extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        )
        soup = BeautifulSoup(html_body, "html.parser")
        self._remove_html_comments(soup)
        self._render_mermaid_blocks(soup)
        self._fix_image_paths(soup)
        return self._build_full_html(soup)

    # ---------- 内部辅助 ----------

    def _remove_html_comments(self, soup: BeautifulSoup) -> None:
        for comment in soup.find_all(
            string=lambda text: isinstance(text, Comment)
        ):
            comment.extract()

    def _render_mermaid_blocks(self, soup: BeautifulSoup) -> None:
        for pre in soup.find_all("pre"):
            code_tag = pre.find("code")
            if code_tag is None:
                continue
            classes = code_tag.get("class", [])
            if isinstance(classes, str):
                classes = [classes]
            if not any(
                cls in {"language-mermaid", "mermaid"} for cls in classes
            ):
                continue

            code = code_tag.get_text()
            if not code.strip():
                continue

            with tempfile.TemporaryDirectory(prefix="md2png_mermaid_") as tmp_dir:
                tmp_path = Path(tmp_dir)
                input_path = tmp_path / "diagram.mmd"
                output_path = tmp_path / "diagram.png"
                input_path.write_text(code + "\n", encoding="utf-8")
                self._run_mermaid_renderer(input_path, output_path)

                if output_path.exists() and output_path.stat().st_size > 0:
                    data_uri = image_to_data_uri(output_path)
                    img_tag = soup.new_tag("img", src=data_uri)
                    img_tag["alt"] = "Mermaid diagram"
                    pre.replace_with(img_tag)
                else:
                    p = soup.new_tag("p")
                    p.string = "[Mermaid render failed]"
                    pre.replace_with(p)

    def _run_mermaid_renderer(self, input_path: Path, output_path: Path) -> None:
        renderer = BASE_DIR / "render_mermaid.mjs"
        if not renderer.exists():
            raise FileNotFoundError(
                f"Mermaid renderer not found: {renderer}\n"
                "Run `npm install` in tools/md2png first."
            )

        command = ["node", str(renderer), str(input_path), str(output_path)]
        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Mermaid render timed out (30s).")
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "Node.js not found. "
                "Please install Node.js to render Mermaid diagrams."
            ) from exc
        except subprocess.CalledProcessError as exc:
            message = (exc.stderr or exc.stdout or str(exc)).strip()
            raise RuntimeError(f"Mermaid render failed: {message}") from exc

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise RuntimeError("Mermaid render did not produce an image.")

    def _fix_image_paths(self, soup: BeautifulSoup) -> None:
        """将本地图片转为 base64 data URI，彻底规避 file:// 跨域限制。"""
        for img in soup.find_all("img"):
            src = img.get("src", "").strip()
            if not src or is_url(src):
                # 网络图片保留原 URL
                continue
            # 已经是 data URI 就跳过（Mermaid 渲染的图）
            if src.startswith("data:"):
                continue
            img_path = Path(src)
            if not img_path.is_absolute():
                img_path = (self.source_dir / img_path).resolve()
            if img_path.exists():
                try:
                    data_uri = image_to_data_uri(img_path)
                    img["src"] = data_uri
                except Exception:
                    img["alt"] = f"[Failed to load: {img.get('alt', '')}]"
                    img["src"] = ""
            else:
                img["alt"] = f"[Missing: {img.get('alt', '')}]"
                img["src"] = ""

    def _build_full_html(self, soup: BeautifulSoup) -> str:
        title = self.meta.get("title", self.source_path.stem)
        author = self.meta.get("author", "")

        doc = BeautifulSoup(
            '<!doctype html><html><head></head><body></body></html>',
            "html.parser",
        )
        head = doc.head
        body = doc.body

        title_tag = doc.new_tag("title")
        title_tag.string = title
        head.append(title_tag)

        if author:
            meta_tag = doc.new_tag("meta")
            meta_tag["name"] = "author"
            meta_tag["content"] = author
            head.append(meta_tag)

        style_tag = doc.new_tag("style")
        style_tag.string = DEFAULT_CSS
        head.append(style_tag)

        for child in soup.children:
            body.append(child)

        return str(doc)

    # ---------- Step 3: HTML → PNG ----------

    async def save(self, html_content: str) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = self._next_available_output_path()

        page = None
        try:
            page = await self.browser.new_page(
                viewport={"width": VIEWPORT_WIDTH, "height": 800},
                device_scale_factor=SCALE_FACTOR,
            )
            # 直接用 data URI 加载，避免文件系统依赖
            data_uri = (
                "data:text/html;charset=utf-8,"
                + html_content.replace("#", "%23")
            )
            await page.goto(data_uri, wait_until="networkidle")
            # 等待渲染完成
            await page.wait_for_timeout(800)

            # 全页截图
            screenshot_opts = {
                "path": str(out_path),
                "full_page": True,
                "type": "png",
            }
            if JPEG_QUALITY is not None and out_path.suffix.lower() in (".jpg", ".jpeg"):
                screenshot_opts["type"] = "jpeg"
                screenshot_opts["quality"] = JPEG_QUALITY

            await page.screenshot(**screenshot_opts)

        finally:
            if page is not None:
                await page.close()

        return out_path

    def _next_available_output_path(self) -> Path:
        base_name = sanitize_filename(self.source_path.stem)
        candidate = self.output_dir / f"{base_name}.png"
        index = 1
        while candidate.exists():
            candidate = self.output_dir / f"{base_name}-{index}.png"
            index += 1
        return candidate


# ===================== 主流程 =====================

async def main_async() -> int:
    if not MD_PATHS_FILE.exists():
        print(f"Missing path list: {MD_PATHS_FILE}")
        print("Create md_paths.txt with one Markdown path per line.")
        return 1

    if not OUTPUT_DIR_FILE.exists():
        print(f"Missing output config: {OUTPUT_DIR_FILE}")
        print("Create output_dir.txt with one output directory path.")
        return 1

    source_paths: list[Path] = []
    seen_sources: set[str] = set()
    for raw_path in read_list_file(MD_PATHS_FILE):
        source_path = clean_user_path(raw_path)
        source_key = str(source_path)
        if source_key in seen_sources:
            continue
        seen_sources.add(source_key)
        source_paths.append(source_path)

    if not source_paths:
        print(f"{MD_PATHS_FILE} contains no valid Markdown paths.")
        return 1

    output_dir_lines = read_list_file(OUTPUT_DIR_FILE)
    if not output_dir_lines:
        print(f"{OUTPUT_DIR_FILE} is empty.")
        print("Add one output directory path to output_dir.txt.")
        return 1
    output_dir = clean_user_path(output_dir_lines[0])

    processed_paths = load_processed_paths()
    pending_paths: list[Path] = []
    skipped_count = 0
    missing_count = 0

    for source_path in source_paths:
        source_key = str(source_path)
        if source_key in processed_paths:
            print(f"[自动跳过] 已转换过：{source_path}")
            skipped_count += 1
            continue
        if not source_path.exists() or not source_path.is_file():
            print(f"[跳过] 未找到 Markdown 文件：{source_path}")
            missing_count += 1
            continue
        if source_path.suffix.lower() != ".md":
            print(f"[跳过] 不是 .md 文件：{source_path}")
            missing_count += 1
            continue
        pending_paths.append(source_path)

    if not pending_paths:
        print("\n没有待转换的文件，程序退出")
        print(f"已跳过：{skipped_count} | 缺失/无效：{missing_count}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n总计文件：{len(source_paths)} | 待转换：{len(pending_paths)}")
    print(f"画质：{SCALE_FACTOR}x | 输出：PNG")
    print("-" * 60)

    converted_count = 0
    failed_count = 0

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        for source_path in pending_paths:
            try:
                converter = MarkdownToPng(source_path, output_dir, browser)
                markdown_text = converter.load_markdown()
                html_content = converter.convert(markdown_text)
                out_path = await converter.save(html_content)
                append_processed_path(source_path)
                processed_paths.add(str(source_path))
                converted_count += 1
                file_size = out_path.stat().st_size
                size_mb = file_size / (1024 * 1024)
                print(
                    f"  ✅ {source_path.name} -> {out_path.name} "
                    f"({size_mb:.1f} MB)"
                )
            except Exception as exc:
                failed_count += 1
                print(f"  ❌ 处理失败：{source_path} | {str(exc)[:200]}")

        await browser.close()

    print("\n" + "=" * 60)
    print("全部任务执行完毕")
    print(f"已转换：{converted_count}")
    print(f"失败：{failed_count}")
    print(f"已跳过：{skipped_count}")
    print(f"缺失/无效：{missing_count}")
    print(f"输出目录：{output_dir}")
    print(f"已处理记录：{PROCESSED_FILE}")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
