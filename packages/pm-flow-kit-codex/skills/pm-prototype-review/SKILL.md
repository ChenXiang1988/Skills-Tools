---
name: pm-prototype-review
description: Create prototype review artifacts that connect UI elements to requirement rules. Use when requirement analysis says a separate review artifact is needed for comparing prototype screens, rules, fields, acceptance criteria, open questions, and review findings.
---

# PM Prototype Review

## Capability Boundary

Create a separate review artifact that maps prototype UI elements to rules, fields, acceptance criteria, open questions, and findings.

Do not create review artifacts by default. Do not create the underlying prototype. Do not silently change requirements.

## Required Inputs

- Requirement analysis.
- Metrics definition when review findings affect measurable outcomes.
- Scenario catalog.
- Use cases.
- Artifact plan.
- PRD or draft requirements.
- Existing prototype files.

Stop when `artifact-plan.md` does not say a review artifact is needed.

## Output Contract

- Review document or HTML review artifact.
- Findings list.
- Open questions.
- Decision and follow-up summary.

Each highlighted UI element should map to a rule, field, acceptance criterion, use case, metric, or open question.

## Failure Cases

- Wrong use: generating review artifacts because the workflow reached a review stage rather than because the artifact plan requires it.
- Bad input: prototype exists but no PRD, field dictionary, use case, or acceptance criteria exist to compare against.
- Bad output: "looks good" or "needs optimization" with no specific evidence.
- Bad output: findings are not mapped to a rule, field, acceptance criterion, use case, metric, or open question.
- Blocking gap: review reveals scope or data-rule conflict and no decision is recorded.

## Handoff Rules

- Use `pm-html-prototype` when the prototype itself must be created or fixed.
- Use `pm-prd` when requirement rules or acceptance criteria are incomplete.
- Use `pm-requirement-analysis` when the artifact plan does not justify a review artifact.

## Resources

- Review artifact guidance: `references/review-prototype.md`
- Review template assets: `assets/review/`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
