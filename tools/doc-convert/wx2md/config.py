"""
config.py - 微信文章转Markdown工具配置文件
可在此修改链接文件、输出目录、广告过滤关键词等配置
"""

import os
import re

# ===================== 文件路径配置 =====================
# 链接文件路径（相对于本文件目录）
LINKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "links.txt")

# 已处理链接记录文件
PROCESSED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "processed_links.txt")

# 输出目录（文章将保存到此目录）
# 默认：存放至 kb-wiki 的 raw/articles 目录
OUTPUT_DIR = "/Users/martin/Documents/Martinjob/Knowledge/kb-wiki/raw/articles"

# ===================== 浏览器配置 =====================
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ===================== 广告过滤配置 =====================
# 广告关键词正则（匹配：进群、加群、扫码、关注公众号、添加微信、交流群等引流文案）
AD_KEYWORDS = re.compile(
    r"(进群|加群|交流群|微信群|扫码关注|关注公众号|添加微信|添加好友|私信回复|后台回复|获取资料|领取福利|加好友|入群)",
    re.IGNORECASE
)

# ===================== 文章目录命名配置 =====================
# 是否使用日期前缀（格式：YYYY-MM-DD-标题）
USE_DATE_PREFIX = False

# 文章 Markdown 文件名（设为 "title" 则用文章标题命名，否则使用指定名称）
ARTICLE_FILENAME = "title"

# ===================== 图片配置 =====================
# 图片目录名
IMAGE_DIR_NAME = "images"
