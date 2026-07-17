---
name: humanizer
description: Polish product writing without changing facts, scope, metrics,
  requirements, decisions, acceptance criteria, or source meaning. Use when you
  need to remove AI-like writing patterns from stable PRDs, requirement
  summaries, review notes, release notes, or product documents after product
  facts are already confirmed.
disable: true
---

# Humanizer

## Capability Boundary

Improve expression only. Make stable product text sound clearer, more natural, and less AI-generated.

Do not change facts, scope, non-scope, metrics, requirements, field definitions, rules, decisions, open questions, acceptance criteria, source citations, or risk severity.

## Required Inputs

- Stable source text.
- Target audience or tone, if known.
- Any facts, terms, or wording that must not change.

Stop when the text is still factually unstable, when open questions are unresolved, or when the user asks for "polish" but the content contains requirement gaps that need `pm-requirement-analysis` or `pm-prd`.

## Output Contract

Provide:

- Humanized text.
- Brief change note when helpful.
- Explicit note if any wording was not changed because it would risk changing meaning.

## Failure Cases

- Wrong use: polishing before the PRD, metrics, scope, or acceptance criteria are stable.
- Bad output: changing a requirement while trying to improve tone.
- Bad output: converting product documentation into marketing copy.
- Bad output: removing caveats, assumptions, open questions, or source uncertainty.
- Bad output: making the writing "more confident" when the source is uncertain.

## Handoff Rules

- Use `pm-requirement-analysis` when the text exposes missing problem, scope, scenario, use case, or flow information.
- Use `pm-metrics-definition` when success metrics or thresholds are vague.
- Use `pm-prd` when the document structure or requirement content needs correction.
- Use `pm-prototype-review` when the text is a review finding that must map to UI, rules, fields, or acceptance criteria.

## Resources

- AI-writing pattern reference: `references/ai-writing-patterns.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
