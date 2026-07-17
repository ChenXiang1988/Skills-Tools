---
name: pm-review
description: Perform independent product artifact reviews for pm-flow-kit. Use
  when you need to review requirement analysis, metrics, boundary, PRDs,
  prototypes, diagrams, risks, decisions, or delivery readiness and produce
  review.md with findings, evidence, severity, resolution status, and final
  readiness.
disable: true
---

# PM Review

## Capability Boundary

Perform independent review across product artifacts. Use this skill for the `review` stage and for review work that is broader than prototype-only review.

Do not create the underlying PRD, prototype, diagram, metrics definition, or requirement analysis. Do not silently rewrite artifacts while reviewing them.

## Required Inputs

- Requirement analysis bundle.
- Metrics definition or a non-applicability reason.
- Boundary artifact when the flow includes boundary.
- PRD or downstream artifact being reviewed.
- Prototype, diagrams, or prototype review artifacts when the artifact plan says they are needed.
- Decision log, open questions, risks, and owner decisions.

Stop when required upstream artifacts are missing, when P1/P0 source errors are unresolved, or when a finding changes scope without an owner decision.

## Output Contract

Create or update `review.md` with:

- Context references and sources reviewed.
- Independent reviewer identity.
- Review dimensions and reviewed artifacts.
- Findings with severity, evidence, recommendation, owner, resolution, and status.
- Decision completeness check.
- Remaining open issues.
- Overall conclusion: `Ready` or `Rework required`.

Every finding must be specific enough for the owner to close or explicitly accept as unresolved.

## Failure Cases

- Wrong use: using this skill to generate the PRD or prototype being reviewed.
- Wrong use: closing review with generic wording such as "looks good" without evidence.
- Bad output: findings are not tied to source artifacts, acceptance criteria, rules, risks, or decisions.
- Bad output: unresolved high-risk findings are hidden in prose.
- Blocking gap: review discovers a scope, metric, permission, data, compliance, or source conflict without a recorded owner decision.

## Handoff Rules

- Use `pm-prd` when review reveals missing PRD sections, fields, rules, or acceptance criteria.
- Use `pm-boundary` when scope, non-scope, stakeholders, or assumptions are unclear.
- Use `pm-research` when opportunity, user, market, competitor, or benchmark evidence is missing.
- Use `pm-prototype-review` only when the artifact plan requires UI-to-rule review.
- Use `humanizer` only after findings and decisions are stable.

## Resources

- Review method: `references/review-method.md`
- Review template: `assets/templates/review.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
