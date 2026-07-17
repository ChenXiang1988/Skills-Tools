---
name: pm-research
description: Produce research-stage product context for pm-flow-kit. Use when
  you need to complete opportunity, user, market, competitor, benchmark, metric
  context, source-risk, assumption, and open-question research before boundary,
  prototype, or PRD work.
disable: true
---

# PM Research

## Capability Boundary

Create the `research` stage artifact for product work. Focus on evidence, context, and uncertainty needed before scope and solution decisions.

Do not write the PRD, prototype, or final review. Do not treat unverified assumptions as facts.

## Required Inputs

- Requirement analysis and artifact plan.
- Context confirmation and knowledge-base sources when available.
- Known users, roles, client surfaces, business goals, or market/problem context.
- Metrics definition when available.

Continue with explicit non-applicability notes when market, competitor, or benchmark research does not apply to a small internal or compliance task.

Stop when the task needs external facts that are unavailable and would materially affect scope, risk, or acceptance criteria.

## Output Contract

Create or update `research.md` with:

- Opportunity and problem context.
- Target user and scenario evidence.
- Market, competitor, or benchmark context, or non-applicability reasons.
- Metric context and success lens.
- Project constraints from confirmed sources.
- Assumptions, risks, and open questions.
- Recommendation for boundary work.

## Failure Cases

- Wrong use: turning research into a PRD or solution design.
- Bad output: inventing market facts, competitors, benchmarks, or user evidence.
- Bad output: listing generic research categories without a decision impact.
- Bad output: failing to separate confirmed facts, assumptions, and open questions.
- Blocking gap: missing evidence changes the recommended flow path, scope, or risk level.

## Handoff Rules

- Use `pm-boundary` after research when scope, non-scope, roles, constraints, or risks must be locked.
- Use `pm-requirement-analysis` when problem, users, scenarios, or artifact routing are still unclear.
- Use `pm-metrics-definition` when success metrics or thresholds are weak.
- Use `pm-prd` only after research and boundary are stable enough for requirements.

## Resources

- Research method: `references/research-method.md`
- Research template: `assets/templates/research.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
