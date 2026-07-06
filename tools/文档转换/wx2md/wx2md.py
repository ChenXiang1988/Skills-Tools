"""
wx2md.py - 微信文章批量转 Markdown（广告过滤+自定义输出目录版）
功能：
  1. 自动跳过已处理链接、断点续跑
  2. 自动屏蔽文末进群、关注、扫码、引流广告
  3. 微信图片防盗链下载
  4. 注释支持、非法文件名过滤
  5. 输出文件存放至配置文件指定的目录
用法：
  1. 同目录新建 links.txt，一行一条微信链接
  2. 执行：py wx2md.py
依赖：
  py -m pip install -r requirements.txt
  py -m playwright install chromium
"""
import asyncio
import base64
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.async_api import async_playwright

# ===================== 导入配置 =====================
from config import (
    LINKS_FILE,
    PROCESSED_FILE,
    OUTPUT_DIR,
    USER_AGENT,
    AD_KEYWORDS,
    USE_DATE_PREFIX,
    ARTICLE_FILENAME,
    IMAGE_DIR_NAME,
)

# ===================== 工具函数 =====================
def sanitize_filename(name: str) -> str:
    """清理文件名非法字符"""
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    name = name.strip().strip(".")
    return name[:100]

def ensure_dir(path: str):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)

def get_processed_links() -> set:
    """读取已处理链接"""
    processed = set()
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    processed.add(line)
    return processed

def add_processed_link(url: str):
    """记录已处理链接"""
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def remove_ad_content(soup: BeautifulSoup) -> None:
    """移除文末引流广告"""
    for p in soup.find_all(["p", "span", "div"]):
        text = p.get_text(strip=True)
        if AD_KEYWORDS.search(text):
            p.decompose()


def normalize_pub_date(raw: str) -> str:
    """
    将微信文章中的各种发布时间格式统一为标准格式 YYYY-MM-DD HH:MM:SS
    支持格式：
      - 2026年5月14日 08:58
      - 2026年5月14日 08:58:14
      - 2026-05-14 08:58
      - 2026/5/14 8:58
    秒数缺失时补 :00
    """
    if not raw:
        return ""
    raw = raw.strip()
    # 匹配中文格式：2026年5月14日 08:58 或 2026年5月14日 08:58:14
    m = re.match(
        r"(\d{4})年(\d{1,2})月(\d{1,2})日\s+(\d{1,2}):(\d{2})(?::(\d{2}))?",
        raw
    )
    if m:
        year, mon, day, hh, mm, ss = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)
        ss = ss if ss else "00"
        return f"{year}-{int(mon):02d}-{int(day):02d} {int(hh):02d}:{mm}:{ss}"
    # 匹配数字格式：2026-05-14 08:58 或 2026/5/14 8:58
    m2 = re.match(
        r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?",
        raw
    )
    if m2:
        year, mon, day, hh, mm, ss = m2.group(1), m2.group(2), m2.group(3), m2.group(4), m2.group(5), m2.group(6)
        ss = ss if ss else "00"
        return f"{year}-{int(mon):02d}-{int(day):02d} {int(hh):02d}:{mm}:{ss}"
    return raw

async def download_image(page, img_url: str, img_dir: str, img_name: str) -> str | None:
    """绕过微信防盗链下载图片"""
    try:
        js_code = f"""
        async () => {{
            const resp = await fetch("{img_url}", {{
                headers: {{ "Referer": "https://mp.weixin.qq.com/" }}
            }});
            const blob = await resp.blob();
            return new Promise((resolve) => {{
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            }});
        }}
        """
        data_url = await page.evaluate(js_code)
        if data_url and data_url.startswith("data:image"):
            header, b64 = data_url.split(",", 1)
            ext = "png"
            if "jpeg" in header or "jpg" in header:
                ext = "jpg"
            elif "gif" in header:
                ext = "gif"
            elif "webp" in header:
                ext = "webp"

            img_path = os.path.join(img_dir, f"{img_name}.{ext}")
            with open(img_path, "wb") as f:
                f.write(base64.b64decode(b64))
            return f"{img_name}.{ext}"
    except Exception as e:
        print(f"  [图片下载失败] {img_url}: {str(e)[:80]}")
    return None

# ===================== 单篇文章处理 =====================
async def process_article(context, url: str):
    """处理单篇微信文章"""
    print(f"\n>>> 开始处理: {url}")
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_selector("#js_content", timeout=15000)

        # 提取标题
        title_el = await page.query_selector("#activity_name, .rich_media_title")
        title = await title_el.inner_text() if title_el else "未命名"
        title = title.strip()

        # 提取公众号作者
        author_el = await page.query_selector("#js_name, .profile_nickname")
        author = await author_el.inner_text() if author_el else "未知公众号"
        author = author.strip()

        # 提取副标题区域完整元信息
        # 副标题结构通常为：作者名 发布时间 阅读数/听读数
        pub_date = ""
        read_count = ""

        # --- 发布时间：优先 #publish_time，再尝试 .rich_media_meta_text 中匹配日期格式 ---
        date_el = await page.query_selector("#publish_time")
        if date_el:
            pub_date = (await date_el.inner_text()).strip()
        if not pub_date:
            meta_texts = await page.evaluate("""() => {
                const els = document.querySelectorAll('#publish_time, .rich_media_meta_text');
                return Array.from(els).map(el => el.textContent.trim()).filter(t => t);
            }""")
            date_pattern = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}")
            for t in meta_texts:
                if date_pattern.search(t):
                    pub_date = t
                    break
            if not pub_date:
                loose_pattern = re.compile(r"\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}:\d{2}")
                for t in meta_texts:
                    if loose_pattern.search(t):
                        pub_date = t
                        break

        # --- 标准化发布时间格式为 YYYY-MM-DD HH:MM:SS ---
        if pub_date:
            pub_date = normalize_pub_date(pub_date)

        # --- 阅读/听读人数 ---
        count_info = await page.evaluate("""() => {
            const body = document.body.innerHTML;
            const match = body.match(/(\\d+(?:\\.\\d+)?万?\\+?)\\s*人/);
            return match ? match[0] : '';
        }""")
        read_count = count_info if count_info else ""

        print(f"  标题：{title}")
        print(f"  公众号：{author}")
        print(f"  发布时间：{pub_date}")
        if read_count:
            print(f"  阅读：{read_count}")

        # 提取正文HTML
        content_html = await page.evaluate(
            "() => { const node = document.getElementById('js_content'); return node ? node.innerHTML : ''; }"
        )
        if not content_html:
            print("  [警告] 未抓取到文章正文，跳过本篇")
            return

        # 构建文章目录
        safe_title = sanitize_filename(title)
        if USE_DATE_PREFIX:
            date_prefix = datetime.now().strftime("%Y-%m-%d")
            article_dir_name = f"{date_prefix}-{safe_title}"
        else:
            article_dir_name = safe_title
        article_dir = os.path.join(OUTPUT_DIR, article_dir_name)
        img_dir = os.path.join(article_dir, IMAGE_DIR_NAME)
        ensure_dir(img_dir)

        # 解析HTML
        soup = BeautifulSoup(content_html, "html.parser")

        # 移除引流广告
        remove_ad_content(soup)

        # 处理图片
        imgs = soup.find_all("img")
        for idx, img in enumerate(imgs, 1):
            src = img.get("data-src") or img.get("src")
            if not src:
                continue
            local_name = f"img_{idx:03d}"
            local_file = await download_image(page, src, img_dir, local_name)
            if local_file:
                img["src"] = f"{IMAGE_DIR_NAME}/{local_file}"
                if "data-src" in img.attrs:
                    del img.attrs["data-src"]

        # 清理冗余标签属性
        for tag in soup.find_all(True):
            for attr in ["class", "id", "style", "data-tools"]:
                if attr in tag.attrs:
                    del tag.attrs[attr]

        # HTML 转 Markdown
        clean_html = str(soup)
        markdown = md(clean_html, heading_style="ATX", strip=["script", "style"])

        # 头部元信息
        frontmatter = f"""---
title: {title}
author: {author}
pub_date: {pub_date}
source_url: {url}
capture_time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
        if read_count:
            frontmatter += f"\nread_count: {read_count}"
        frontmatter += "\n---\n\n"
        # 写入MD文件
        if ARTICLE_FILENAME == "title":
            md_filename = f"{safe_title}.md"
        else:
            md_filename = f"{ARTICLE_FILENAME}.md"
        md_path = os.path.join(article_dir, md_filename)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + markdown)

        print(f"  ✅ 处理完成（已过滤引流广告），文件已保存至：{md_path}")

    except Exception as e:
        print(f"  ❌ 处理失败：{str(e)[:120]}")
    finally:
        await page.close()

# ===================== 主逻辑 =====================
async def main():
    ensure_dir(OUTPUT_DIR)
    # 读取待处理链接
    if not os.path.exists(LINKS_FILE):
        print(f"错误：未找到 {LINKS_FILE}")
        print("请在当前目录创建 links.txt，每行填写一条微信文章链接")
        return

    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f]

    # 过滤空行、#注释行
    all_links = []
    for line in raw_lines:
        if line and not line.startswith("#"):
            all_links.append(line)

    if not all_links:
        print("links.txt 中无有效链接，程序退出")
        return

    # 读取已处理链接
    processed_links = get_processed_links()
    pending_links = []
    for link in all_links:
        if link in processed_links:
            print(f"[自动跳过] 已处理过：{link}")
        else:
            pending_links.append(link)

    if not pending_links:
        print("\n所有链接均已处理完毕，程序退出")
        return

    print(f"\n总计链接：{len(all_links)} | 待处理：{len(pending_links)}")
    print("-" * 60)

    # 启动浏览器批量处理
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1280, "height": 800},
            locale="zh-CN"
        )

        for url in pending_links:
            if "mp.weixin.qq.com" not in url:
                print(f"\n[跳过] 非微信文章链接：{url}")
                add_processed_link(url)
                continue

            await process_article(context, url)
            add_processed_link(url)

        await browser.close()

    print("\n" + "=" * 60)
    print("🎉 全部任务执行完毕！")
    print(f"已处理链接记录：{PROCESSED_FILE}")
    print(f"文章统一输出至目录：{OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
