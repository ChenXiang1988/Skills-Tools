import os, re

# >>> ADJUST THIS to the wiki root <<<
WIKI = "/Users/martin/Documents/Martinjob/wiki-kb/wiki"
TODAY = "2026-07-06"

# file (rel to wiki/) -> (old 相关概念 line, new 相关概念 line, added orphan slugs)
WIRING = {
    # Example — replace with the actual orphan→source wiring map each run:
    # "concepts/concept-cross-docking.md": (
    #   "- 相关概念: [[concepts/concept-inbound-to-ready]], [[concepts/concept-order-to-deliver]]",
    #   "- 相关概念: [[concepts/concept-inbound-to-ready]], [[concepts/concept-order-to-deliver]], [[concepts/concept-cross-docking]]",
    #   ["concept-cross-docking"],
    # ),
}

def append_change_record(text, bullet):
    marker = "## 变更记录"
    i = text.find(marker)
    if i == -1:
        return text.rstrip() + "\n\n## 变更记录\n" + bullet + "\n"
    rest = text[i:]
    last_bullet = rest.rfind("\n- ")
    if last_bullet == -1:
        header_end = rest.find("\n")
        pos = i + header_end + 1
        return text[:pos] + "\n" + bullet + text[pos:]
    line_end = rest.find("\n", last_bullet + 1)
    if line_end == -1:
        line_end = len(rest)
    abs_pos = i + line_end
    return text[:abs_pos] + "\n" + bullet + text[abs_pos:]

ok, fail = [], []
for rel, (old, new, added) in WIRING.items():
    p = os.path.join(WIKI, rel)
    txt = open(p, encoding="utf-8").read()
    if old not in txt:
        fail.append((rel, "OLD_LINE_NOT_FOUND")); continue
    txt = txt.replace(old, new, 1)
    txt = re.sub(r"最后更新\*\*:\s*\d{4}-\d{2}-\d{2}", "最后更新**: " + TODAY, txt, count=1)
    links = ", ".join("[[concepts/%s]]" % a for a in added)
    bullet = "- %s: Lint 接线 — 关联补充入链 %s，来源本仓知识库体检" % (TODAY, links)
    txt = append_change_record(txt, bullet)
    open(p, "w", encoding="utf-8").write(txt)
    ok.append(rel)

print("OK (%d):" % len(ok))
for r in ok: print("  +", r)
print("FAIL (%d):" % len(fail))
for r, e in fail: print("  -", r, e)
