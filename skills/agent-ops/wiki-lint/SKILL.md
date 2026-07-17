---
name: wiki-lint
description: Lint / health-check a Karpathy-style LLM Wiki. Runs link-graph
  analysis (broken links, orphan pages, cross-reference density), contradiction
  & freshness scan, and a missing-reference term-frequency deep scan. Ships
  three reusable Python scripts (wiki_lint.py, wiki_wire.py, wiki_gap.py). Use
  after Ingest batches or on a schedule.
emoji: 🩺
disable: true
---

# Wiki Lint — 知识库健康巡检

Health-check a 3-layer LLM Wiki (`raw/` → `wiki/` → `SCHEMA.md`). Produces a report on:
1. **Broken links** — `[[wiki-link]]` pointing to a non-existent page.
2. **Orphan pages** — content pages with zero inbound links from other content pages.
3. **Cross-reference density** — average inbound links per page + hub pages.
4. **Contradictions / freshness** — `⚠️` markers (legit self-corrections vs real source conflicts) + `最后更新` distribution.
5. **Missing references** — domain terms mentioned across many pages but lacking a dedicated page.

## When to use
- After any Ingest batch (verify 0 broken / 0 orphan).
- On a recurring schedule (weekly) — pair with the screening workflow.
- Before publishing the wiki or onboarding a new contributor.

## Workflow
1. **Link-graph analysis** — run `scripts/wiki_lint.py`. It walks `wiki/`, extracts `[[links]]`, resolves them to existing `.md` files (handles `concepts/`, `entities/`, `topics/`, `wiki/` prefixes; strips `.md`; ignores `raw/` citations and code spans), and reports broken links, orphans, density, and `最后更新` spread.
   - **Critical correctness notes** (learned the hard way):
     - Wiki links omit the `.md` extension; page dict keys include it → normalize by appending `.md` to link targets.
     - `[[wiki/index.md]]` means the wiki root → strip the `wiki/` prefix.
     - Strip fenced ``` and inline ` code spans BEFORE extracting links, or backtick-quoted examples in `log.md` false-positive as broken links.
2. **Fix broken links** (defects) — edit the offending `[[link]]` (usually a missing `concepts/` folder prefix). Re-run to confirm 0.
3. **Wire orphans** (optional enhancement) — for each orphan page, add inbound `[[links]]` from 2–3 semantically-related source pages' `## 关联` section. Use `scripts/wiki_wire.py` (takes a file→(old_line,new_line,added) map) to bulk-apply, bump `最后更新`, and append a `## 变更记录` entry. Then re-run `wiki_lint.py` to confirm orphans → 0.
4. **Missing-reference deep scan** (optional) — run `scripts/wiki_gap.py` to count candidate domain terms across content pages. Distinguish **true gaps** (no page + raw/ source exists → recommend a new page) from **covered verbs** (e.g. 拣货/上架 already live inside a parent flow page — do NOT fragment).
5. **Record** — append a dated entry to `wiki/log.md` (broken-link fixes, wiring map, gap findings). Re-lock `wiki/` (`chmod -w` on files + dirs).

## Operating constraints (this wiki)
- `wiki/` is AI-exclusive write: unlock with `chmod +w wiki/**/*.md` (+ dirs) before edits, `chmod -w` after.
- Never modify `raw/` (read-only source).
- Every wiki page follows the template: 类型/创建时间/最后更新/来源/摘要/详情/关联/引用来源/变更记录.

## Scripts (in `scripts/`)
- `wiki_lint.py` — link-graph + broken/orphan/density/freshness report. Set `WIKI` constant to the wiki root.
- `wiki_wire.py` — bulk orphan wiring (inbound links + metadata). Edit the `WIRING` dict per run.
- `wiki_gap.py` — term-frequency missing-reference scan. Edit `CANDIDATES`/`HAS_PAGE` per run.

> All scripts are stdlib-only (Python 3.11+). Paths are hardcoded to the user's wiki root — adjust the `WIKI` constant before first run.
