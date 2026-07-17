#!/usr/bin/env bash
# pm-html-presentation :: inline.sh — 把一份 deck 打包成「单文件 / 内联 / 零外部依赖」HTML
#
# 做的事：
#   1. 内联 <link> 样式：base.css / fonts.css / animations.css
#   2. 内联主题：当前 theme-link + data-themes 里所有候选主题，
#      各成一个 <style data-pm-theme="X" [disabled]>，
#      并改写 inlined runtime.js 的 applyTheme，让 T 键换肤在单文件版照样可用
#   3. 内联 <script src>：runtime.js / fx-runtime.js
#   4. 剥离外部字体：@import url(http...) 与 <link href="https://fonts.googleapis...">
#   产物 = 一个自包含 .html，无 ../assets 相对路径依赖、无外网请求
#
# 说明（第二批已完成）：
#   chart.js / highlight.js / lucide / motion 等 CDN <script> 已全部干掉：
#   - charts.js 自研 SVG 图表、code-hl.js 轻量高亮 在此内联；
#   - guizang 模板的 lucide/motion 外链已删、字体外链已删（系统字体栈）。
#   本脚本产出的单文件版：零 ../assets、零外网请求。
#
# Usage:
#   inline.sh <deck.html> [out.html]
#   out 省略时生成 <原名>-single.html
#
set -euo pipefail

PY="${PM_HTML_INLINE_PY:-python3}"
IN="${1:-}"
OUT="${2:-}"

[ -z "$IN" ] && { echo "usage: inline.sh <deck.html> [out.html]" >&2; exit 1; }
[ -f "$IN" ] || { echo "error: $IN not found" >&2; exit 1; }

DIR="$(cd "$(dirname "$IN")" && pwd)"
[ -z "$OUT" ] && OUT="${DIR}/$(basename "${IN%.*}")-single.html"

"$PY" - "$DIR" "$IN" "$OUT" <<'PYEOF'
import sys, re, os

base_dir, inp, outp = sys.argv[1], sys.argv[2], sys.argv[3]
html = open(inp, encoding='utf-8').read()

def read_rel(href):
    p = os.path.normpath(os.path.join(base_dir, href))
    if os.path.exists(p):
        return open(p, encoding='utf-8').read()
    return None

def strip_http_imports(css):
    # 去掉 @import url(http...) （Google Fonts 等外部字体）
    return re.sub(r"@import\s+url\(\s*['\"]?https?://[^'\")]+?\s*\)\s*;?", "", css, flags=re.I)

# 1) 内联样式 link：base.css / fonts.css / animations.css
for token in ("base.css", "fonts.css", "animations.css"):
    m = re.search(r'<link[^>]*href=["\']([^"\']*' + re.escape(token) + r'[^"\']*)["\'][^>]*>', html, re.I)
    if m:
        css = read_rel(m.group(1))
        if css is not None:
            css = strip_http_imports(css)
            html = html.replace(m.group(0), '<style data-pm-asset="%s">\n%s\n</style>' % (token, css))

# 2) 主题：当前 theme-link + data-themes 全部候选 -> 独立 <style data-pm-theme>
m = re.search(r'<link[^>]*id=["\']theme-link["\'][^>]*href=["\']([^"\']+)["\']', html, re.I)
active = None
if m:
    href = m.group(1)
    mm = re.search(r'/themes/([^/]+)\.css$', href)
    if mm:
        active = mm.group(1)

dt = re.search(r'data-themes=["\']([^"\']+)["\']', html)
names = []
if dt:
    names = [x.strip() for x in dt.group(1).split(',') if x.strip()]
if active and active not in names:
    names.insert(0, active)
seen = set(); ordered = []
for n in names:
    if n not in seen:
        seen.add(n); ordered.append(n)
names = ordered

theme_dir = (os.path.dirname(os.path.normpath(os.path.join(base_dir, m.group(1))))
             if m else os.path.normpath(os.path.join(base_dir, '..', 'assets', 'themes')))

blocks = []
for i, name in enumerate(names):
    p = os.path.normpath(os.path.join(theme_dir, name + '.css'))
    if os.path.exists(p):
        css = strip_http_imports(open(p, encoding='utf-8').read())
        dis = '' if i == 0 else ' disabled'
        bid = ' id="theme-link"' if i == 0 else ''
        blocks.append('<style%s data-pm-theme="%s"%s>\n%s\n</style>' % (bid, name, dis, css))
    else:
        blocks.append('<!-- theme %s not found, skipped -->' % name)
theme_block = '\n'.join(blocks)

if m and blocks:
    html = html.replace(m.group(0), theme_block)
elif blocks:
    html = re.sub(r'(<head[^>]*>)', r'\1\n' + theme_block, html, count=1)

# 3) 内联脚本：runtime.js / fx-runtime.js / charts.js / code-hl.js
#    （charts.js=自研 SVG 图表替代 Chart.js；code-hl.js=轻量高亮替代 highlight.js；
#      guizang 模板的 lucide 外链已删除、googleapis 字体外链已删除，无需再内联图标库）
for jsname in ("runtime.js", "fx-runtime.js", "charts.js", "code-hl.js"):
    m2 = re.search(r'<script[^>]*src=["\']([^"\']*' + re.escape(jsname) + r'[^"\']*)["\'][^>]*>\s*</script>', html, re.I)
    if m2:
        js = read_rel(m2.group(1))
        if js is not None:
            # 改写 inlined runtime.js 的 applyTheme：单文件版按 <style data-pm-theme> 切换 disabled
            if jsname == "runtime.js":
                js = re.sub(
                    r"    function applyTheme\(name\) \{.*?\n    \}",
                    "    function applyTheme(name) {\n"
                    "      document.querySelectorAll('style[data-pm-theme]').forEach(function(s){\n"
                    "        s.disabled = (s.getAttribute('data-pm-theme') !== name);\n"
                    "      });\n"
                    "      root.setAttribute('data-theme', name);\n"
                    "      const ind = document.querySelector('.theme-indicator');\n"
                    "      if (ind) ind.textContent = name;\n"
                    "    }",
                    js, count=1, flags=re.S)
            html = html.replace(m2.group(0), '<script>\n%s\n</script>' % js)

# 4) 剥离内联外部字体 <link>（guizang 模板自带） + 残留 @import http
html = re.sub(r'<link[^>]*href=["\']https://fonts\.googleapis\.com[^>]*>\s*', '', html, flags=re.I)
html = strip_http_imports(html)

# 5) 剥离惰性属性 data-theme-base=".../assets/..."（单文件版换肤走 <style data-pm-theme>，不再读它）
html = re.sub(r'\s*data-theme-base=["\'][^"\']*["\']', '', html)

open(outp, 'w', encoding='utf-8').write(html)

# 排除 SVG 命名空间 http://www.w3.org/2000/svg（非网络请求，不算外部依赖）
ext = len(re.findall(r'https?://(?!www\.w3\.org)', html))
print("OK -> %s" % outp)
print("  themes inlined : %d (%s)" % (len(names), ", ".join(names) if names else "none"))
print("  external http refs left : %d  (已排除 SVG 命名空间 w3.org；charts.js/code-hl.js 已内联为零依赖；lucide 外链已删除无需内联)" % ext)
PYEOF

echo "open: $OUT"
