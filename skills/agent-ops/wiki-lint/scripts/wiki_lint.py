import os, re

# >>> ADJUST THIS to the wiki root for your knowledge base <<<
WIKI = "/Users/martin/Documents/Martinjob/wiki-kb/wiki"
META = {"index.md", "log.md"}
REL_PREFIXES = ("concepts/", "entities/", "topics/")

pages = {}
for root, dirs, files in os.walk(WIKI):
    for f in files:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), WIKI)
            pages[rel] = os.path.join(root, f)

link_re = re.compile(r"\[\[([^\]]+)\]\]")

def strip_code(s):
    s = re.sub(r"```.*?```", "", s, flags=re.DOTALL)
    s = re.sub(r"`[^`]*`", "", s)
    return s

def normalize(t):
    t = t.split("#")[0].strip()
    if not t or t.startswith("raw/") or t.startswith("http") or t.startswith("/"):
        return None
    if t.startswith("wiki/"):
        t = t[len("wiki/"):]
    if t in ("index.md", "log.md"):   # meta self-reference
        return t
    if t.startswith(REL_PREFIXES):
        return t if t.endswith(".md") else t + ".md"
    norm = os.path.normpath(os.path.join(os.path.dirname("X"), t))
    return norm if norm.endswith(".md") else norm + ".md"

outbound = {rel: set() for rel in pages}
broken = set()
inbound = {rel: set() for rel in pages}

for rel, full in pages.items():
    text = strip_code(open(full, encoding="utf-8").read())
    seen = set()
    for m in link_re.finditer(text):
        tgt = normalize(m.group(1))
        if tgt is None or tgt in seen:
            if tgt: seen.add(tgt)
            continue
        seen.add(tgt)
        if tgt in pages:
            outbound[rel].add(tgt)
            inbound[tgt].add(rel)
        else:
            broken.add((rel, tgt))

content = [r for r in pages if os.path.basename(r) not in META]
orphans = [r for r in content if not (inbound[r] - {"index.md", "log.md"})]
counts = [(r, len(inbound[r] - {"index.md", "log.md"})) for r in content]
counts.sort(key=lambda x: x[1])

print("=== WIKI LINT ===")
print(f"总页面数(含meta): {len(pages)} | 内容页: {len(content)}")
print(f"\n=== 断链/缺失页: {len(broken)} ===")
for src, tgt in sorted(broken):
    print(f"  - {src}  ->  [[{tgt}]]")
print(f"\n=== 孤立页面 (无内容页入链): {len(orphans)} ===")
for r in sorted(orphans):
    print(f"  - {r}")
print("\n=== 入链最少 (10) ===")
for r, c in counts[:10]:
    print(f"  {c:2d}  {r}")
print("\n=== 入链最多 (8) ===")
for r, c in counts[-8:][::-1]:
    print(f"  {c:2d}  {r}")
print("\n=== 最后更新 分布 ===")
dates = {}
for rel, full in pages.items():
    m = re.search(r"最后更新\*\*:\s*(\d{4}-\d{2}-\d{2})", open(full, encoding="utf-8").read())
    d = m.group(1) if m else "未知"
    dates.setdefault(d, []).append(rel)
for d in sorted(dates):
    print(f"  {d}: {len(dates[d])} 页")
print(f"\n平均内容页入链: {sum(c for _,c in counts)/len(counts):.2f}")
