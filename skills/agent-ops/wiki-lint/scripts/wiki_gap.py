import os, re

# >>> ADJUST THIS to the wiki root <<<
WIKI = "/Users/martin/Documents/Martinjob/wiki-kb/wiki"
META = {"index.md", "log.md"}

# Candidate domain terms that could warrant a dedicated concept page.
CANDIDATES = [
    "波次", "效期", "FEFO", "安全库存", "周转", "呆滞", "滞销", "库龄",
    "批次", "序列号", "质检", "调拨", "移库", "ABC", "货位优化", "库位优化",
    "预占", "占用", "冻结", "在途", "集货", "分拣", "称重", "报关", "清关", "关税",
    "上架", "拣货", "复核", "补货", "暂存", "拦截",
]

# Terms that ALREADY have a dedicated page (slug keyword) -> exclude from "missing".
HAS_PAGE = {
    "拦截": "concept-interception-return-putaway",
    "补货": "concept-inventory-integrity",
    "暂存": "concept-billing-settlement",
}

pages = {}
for root, dirs, files in os.walk(WIKI):
    for f in files:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, f), WIKI)
            if os.path.basename(rel) in META:
                continue
            pages[rel] = open(os.path.join(root, f), encoding="utf-8").read()

results = []
for term in CANDIDATES:
    if term in HAS_PAGE:
        continue
    hits = []
    for rel, txt in pages.items():
        c = txt.count(term)
        if c:
            hits.append((rel, c))
    results.append((term, sum(c for _, c in hits), len(hits), hits))

results.sort(key=lambda x: (-x[2], -x[1]))

print("=== 缺失引用深扫 ===")
print(f"{'术语':<8}{'提及页数':<8}{'总次数':<8} 状态")
print("-" * 60)
for term, total, npages, hits in results:
    status = "⚠️ 多页提及但无独立页" if npages >= 3 else ("· 少量提及" if npages > 0 else "∅ 未提及")
    print(f"{term:<8}{npages:<8}{total:<8} {status}")
    if npages >= 3:
        for rel, c in sorted(hits, key=lambda x: -x[1])[:6]:
            print(f"        └ {rel} ({c})")
