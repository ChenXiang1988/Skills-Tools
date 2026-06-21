#!/usr/bin/env python3
"""
Batch convert Word .doc/.docx documents to Markdown.

Files:
  - doc_paths.txt
  - output_dir.txt
  - processed_doc_paths.txt
  - requirements.txt

Usage:
  python tools/doc_to_md/doc_to_md.py

Each non-empty line in doc_paths.txt can be either:
  - a document file path (.doc / .docx)
  - a directory path, which will be scanned recursively for .doc / .docx files

Lines starting with # are ignored.
PPT/PPTX files are intentionally skipped.
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
    from PIL import Image
except ImportError as exc:  # pragma: no cover - handled at runtime
    print(f"Missing dependency: {exc}")
    print("Install requirements with: python3 -m pip install -r requirements.txt")
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
DOC_PATHS_FILE = BASE_DIR / "doc_paths.txt"
OUTPUT_DIR_FILE = BASE_DIR / "output_dir.txt"
PROCESSED_FILE = BASE_DIR / "processed_doc_paths.txt"

SUPPORTED_EXTS = {".doc", ".docx"}
SKIPPED_EXTS = {".ppt", ".pptx"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".svg"}


@dataclass(frozen=True)
class SourceItem:
    source_path: Path
    input_root: Path | None


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
    name = re.sub(r"\s+", " ", name).strip().strip(".")
    return name or "document"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_text(value: str) -> str:
    value = html.unescape(value)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[\x00-\x1f\x7f]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def is_supported_document(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTS


def is_skipped_document(path: Path) -> bool:
    return path.suffix.lower() in SKIPPED_EXTS


def expand_input_path(entry_path: Path) -> tuple[list[SourceItem], int]:
    """Expand one entry from doc_paths.txt into source files."""
    if not entry_path.exists():
        print(f"[跳过] 未找到路径：{entry_path}")
        return [], 1

    if entry_path.is_file():
        if is_supported_document(entry_path):
            return [SourceItem(entry_path.resolve(), None)], 0
        if is_skipped_document(entry_path):
            print(f"[跳过] PPT 文件不处理：{entry_path}")
            return [], 1
        print(f"[跳过] 非 Word 文件：{entry_path}")
        return [], 1

    if entry_path.is_dir():
        items: list[SourceItem] = []
        skipped = 0
        for file_path in sorted(entry_path.rglob("*")):
            if not file_path.is_file():
                continue
            if is_supported_document(file_path):
                items.append(SourceItem(file_path.resolve(), entry_path.resolve()))
            elif is_skipped_document(file_path):
                print(f"[跳过] PPT 文件不处理：{file_path}")
                skipped += 1
        return items, skipped

    print(f"[跳过] 不支持的路径类型：{entry_path}")
    return [], 1


def collect_source_items() -> tuple[list[SourceItem], int]:
    items: list[SourceItem] = []
    skipped = 0
    seen_sources: set[str] = set()

    for raw_path in read_list_file(DOC_PATHS_FILE):
        entry_path = clean_user_path(raw_path)
        expanded_items, entry_skipped = expand_input_path(entry_path)
        skipped += entry_skipped

        for item in expanded_items:
            source_key = str(item.source_path.resolve())
            if source_key in seen_sources:
                print(f"[自动跳过] 重复输入：{item.source_path}")
                skipped += 1
                continue
            seen_sources.add(source_key)
            items.append(item)

    return items, skipped


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


def find_textutil() -> str | None:
    candidates = [
        shutil.which("textutil"),
        "/usr/bin/textutil",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def find_libreoffice() -> str | None:
    candidates = [
        shutil.which("soffice"),
        shutil.which("libreoffice"),
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def run_converter(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )


def convert_source_to_html(source_path: Path, temp_dir: Path) -> Path:
    html_path = temp_dir / f"{source_path.stem}.html"
    errors: list[str] = []

    textutil = find_textutil()
    if textutil:
        try:
            result = run_converter(
                [
                    textutil,
                    "-convert",
                    "html",
                    "-output",
                    str(html_path),
                    str(source_path),
                ]
            )
            if html_path.exists():
                return html_path
            if result.stdout.strip():
                errors.append(result.stdout.strip())
            if result.stderr.strip():
                errors.append(result.stderr.strip())
        except subprocess.CalledProcessError as exc:
            error_text = (exc.stderr or exc.stdout or str(exc)).strip()
            errors.append(f"textutil: {error_text}")

    libreoffice = find_libreoffice()
    if libreoffice:
        try:
            run_converter(
                [
                    libreoffice,
                    "--headless",
                    "--convert-to",
                    "html",
                    "--outdir",
                    str(temp_dir),
                    str(source_path),
                ]
            )
            html_candidates = sorted(temp_dir.glob("*.html")) + sorted(temp_dir.glob("*.htm"))
            if html_candidates:
                return html_candidates[0]
            errors.append("LibreOffice conversion finished but no HTML file was produced.")
        except subprocess.CalledProcessError as exc:
            error_text = (exc.stderr or exc.stdout or str(exc)).strip()
            errors.append(f"LibreOffice: {error_text}")

    if errors:
        raise RuntimeError(" | ".join(errors))
    raise RuntimeError("No HTML converter found. Install macOS textutil or LibreOffice.")


def extract_metadata(soup: BeautifulSoup) -> dict[str, str]:
    meta: dict[str, str] = {}

    head = soup.head
    if head:
        title_tag = head.find("title")
        if title_tag and title_tag.get_text(strip=True):
            meta["title"] = normalize_text(title_tag.get_text(" ", strip=True))

        for tag in head.find_all("meta"):
            key = tag.get("name") or tag.get("property")
            content = tag.get("content", "")
            if key and content:
                meta[key.strip().lower()] = normalize_text(content)

    return meta


def resolve_local_asset(html_dir: Path, raw_src: str) -> Path | None:
    raw_src = raw_src.strip()
    if not raw_src:
        return None
    if raw_src.startswith("data:") or raw_src.startswith("http://") or raw_src.startswith("https://"):
        return None

    parsed = urlparse(raw_src)
    candidate_text = unquote(parsed.path if parsed.scheme == "file" else raw_src)
    candidate_text = candidate_text.split("?")[0].split("#")[0]
    if not candidate_text:
        return None

    candidate_path = Path(candidate_text).expanduser()
    if candidate_path.is_absolute():
        return candidate_path if candidate_path.exists() else None

    direct = html_dir / candidate_path
    if direct.exists():
        return direct

    basename = candidate_path.name
    for path in html_dir.rglob(basename):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            return path

    stem = candidate_path.stem
    if stem:
        for path in html_dir.rglob(f"{stem}.*"):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
                return path

    return None


def copy_image_asset(source: Path, image_dir: Path, index: int) -> str:
    image_dir.mkdir(parents=True, exist_ok=True)
    ext = source.suffix.lower()
    if ext == ".jpeg":
        ext = ".jpg"

    if ext in {".png", ".jpg", ".gif", ".webp", ".bmp", ".svg"}:
        dest_name = f"image_{index:03d}{ext}"
        dest_path = image_dir / dest_name
        shutil.copy2(source, dest_path)
        return dest_name

    dest_name = f"image_{index:03d}.png"
    dest_path = image_dir / dest_name
    try:
        with Image.open(source) as img:
            img.save(dest_path, format="PNG")
    except Exception:
        shutil.copy2(source, dest_path)
    return dest_name


def rewrite_html_and_collect_images(html_path: Path, output_dir: Path) -> tuple[str, dict[str, str]]:
    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html_text, "lxml")
    metadata = extract_metadata(soup)

    if soup.head:
        soup.head.decompose()

    body = soup.body or soup
    images_dir = output_dir / "images"
    image_index = 0

    for img in body.find_all("img"):
        src = img.get("src", "").strip()
        if not src:
            alt = normalize_text(img.get("alt", ""))
            if alt:
                img.replace_with(alt)
            else:
                img.decompose()
            continue

        resolved = resolve_local_asset(html_path.parent, src)
        if resolved and resolved.exists():
            image_index += 1
            new_name = copy_image_asset(resolved, images_dir, image_index)
            img["src"] = f"images/{new_name}"
            continue

        if src.startswith("http://") or src.startswith("https://") or src.startswith("data:"):
            continue

        alt = normalize_text(img.get("alt", "")) or src
        print(f"  [图片未找到] {alt}")
        img.replace_with(f"[图片未找到: {alt}]")

    for tag in body.find_all(["script", "style"]):
        tag.decompose()

    body_html = body.decode_contents()
    markdown_text = md(
        body_html,
        heading_style="ATX",
        table_infer_header=True,
        keep_inline_images_in=["td"],
        strip=["script", "style"],
    )
    markdown_text = normalize_markdown(markdown_text)
    return markdown_text, metadata


def build_frontmatter(source_path: Path, metadata: dict[str, str]) -> str:
    author = metadata.get("author") or metadata.get("lastauthor") or ""

    lines = [
        "---",
        f"title: {yaml_quote(source_path.stem)}",
        f"source_path: {yaml_quote(str(source_path.resolve()))}",
        f"source_type: {yaml_quote(source_path.suffix.lower().lstrip('.'))}",
        f"converted_at: {yaml_quote(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}",
    ]
    if author:
        lines.append(f"author: {yaml_quote(author)}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def make_unique_dir(base_dir: Path) -> Path:
    candidate = base_dir
    index = 1
    while candidate.exists():
        candidate = base_dir.parent / f"{base_dir.name}-{index}"
        index += 1
    return candidate


def build_output_dir(source_path: Path, input_root: Path | None, output_root: Path) -> Path:
    if input_root is not None:
        try:
            relative = source_path.relative_to(input_root).with_suffix("")
            parts = [sanitize_filename(part) for part in relative.parts]
            base_dir = output_root.joinpath(*parts)
        except ValueError:
            base_dir = output_root / sanitize_filename(source_path.stem)
    else:
        base_dir = output_root / sanitize_filename(source_path.stem)

    return make_unique_dir(base_dir)


def save_markdown(output_dir: Path, markdown_text: str, frontmatter: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "document.md"
    md_path.write_text(frontmatter + markdown_text, encoding="utf-8")
    return md_path


def convert_one(source_path: Path, input_root: Path | None, output_root: Path) -> Path:
    with tempfile.TemporaryDirectory(prefix="doc_to_md_") as tmp:
        temp_dir = Path(tmp)
        html_path = convert_source_to_html(source_path, temp_dir)
        output_dir = build_output_dir(source_path, input_root, output_root)
        markdown_text, metadata = rewrite_html_and_collect_images(html_path, output_dir)
        frontmatter = build_frontmatter(source_path, metadata)
        md_path = save_markdown(output_dir, markdown_text, frontmatter)
        return md_path


def main() -> int:
    if not DOC_PATHS_FILE.exists():
        print(f"Missing path list: {DOC_PATHS_FILE}")
        print("Create doc_paths.txt with one Word file path or directory per line.")
        return 1

    if not OUTPUT_DIR_FILE.exists():
        print(f"Missing output config: {OUTPUT_DIR_FILE}")
        print("Create output_dir.txt with one output directory path.")
        return 1

    output_dir_lines = read_list_file(OUTPUT_DIR_FILE)
    if not output_dir_lines:
        print(f"{OUTPUT_DIR_FILE} is empty.")
        print("Add one output directory path to output_dir.txt.")
        return 1
    output_root = clean_user_path(output_dir_lines[0])

    source_items, skipped_count = collect_source_items()
    if not source_items:
        print(f"{DOC_PATHS_FILE} contains no valid .doc/.docx paths.")
        return 1

    processed_paths = load_processed_paths()
    pending_items: list[SourceItem] = []
    already_processed_count = 0
    missing_count = 0

    for item in source_items:
        source_key = str(item.source_path.resolve())
        if source_key in processed_paths:
            print(f"[自动跳过] 已转换过：{item.source_path}")
            already_processed_count += 1
            continue
        if not item.source_path.exists() or not item.source_path.is_file():
            print(f"[跳过] 未找到 Word 文件：{item.source_path}")
            missing_count += 1
            continue
        pending_items.append(item)

    if not pending_items:
        print("\n没有待转换的文件，程序退出")
        print(f"已跳过：{already_processed_count} | 无效/不支持：{skipped_count} | 缺失：{missing_count}")
        return 0

    output_root.mkdir(parents=True, exist_ok=True)
    print(f"\n总计文件：{len(source_items)} | 待转换：{len(pending_items)}")
    print("-" * 60)

    converted_count = 0
    failed_count = 0

    for item in pending_items:
        try:
            md_path = convert_one(item.source_path, item.input_root, output_root)
            append_processed_path(item.source_path)
            processed_paths.add(str(item.source_path.resolve()))
            converted_count += 1
            print(f"  ✅ {item.source_path} -> {md_path}")
        except Exception as exc:
            failed_count += 1
            print(f"  ❌ 处理失败：{item.source_path} | {str(exc)[:160]}")

    print("\n" + "=" * 60)
    print("全部任务执行完毕")
    print(f"已转换：{converted_count}")
    print(f"失败：{failed_count}")
    print(f"已跳过：{already_processed_count}")
    print(f"无效/不支持：{skipped_count}")
    print(f"缺失：{missing_count}")
    print(f"输出目录：{output_root}")
    print(f"已处理记录：{PROCESSED_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
