---
name: pm-boundary
description: Define boundary-stage product scope for pm-flow-kit. Use when you
  need to create boundary.md with scope, non-scope, stakeholders, roles,
  permissions, client surfaces, system ownership, constraints, dependencies,
  assumptions, risks, priorities, and decision handoff before prototype or PRD
  work.
disable: true
---

# PM Boundary

## Capability Boundary

Create the `boundary` stage artifact. Convert research and requirement analysis into a controlled scope boundary that downstream PRD, prototype, and review work can trust.

Do not write the PRD or prototype. Do not expand scope without a recorded decision.

## Required Inputs

- Requirement analysis and artifact plan.
- Research artifact when the flow includes research.
- Context confirmation and confirmed knowledge-base sources.
- Scenario catalog, use cases, end-to-end flow, and metrics definition.
- Known stakeholders, roles, permissions, systems, and constraints.

Stop when scope and non-scope cannot be separated, when a MUST/FORBIDDEN source conflict affects the boundary, or when a role/permission/system owner is missing for a write or decision flow.

## Output Contract

Create or update `boundary.md` with:

- Scope and non-scope.
- Stakeholders, roles, responsibilities, and permissions.
- Client surfaces and system ownership.
- Constraints, dependencies, and source rules.
- Assumptions, risks, priorities, and open questions.
- Decisions needed before PRD or prototype work.

## Failure Cases

- Bad input: only a solution request exists and the underlying problem or actor is unclear.
- Wrong use: using boundary to write final requirements or UI details.
- Bad output: non-scope is empty or vague.
- Bad output: assumptions are written as facts.
- Blocking gap: role, permission, data ownership, or system boundary is unresolved.

## Handoff Rules

- Use `pm-research` when opportunity, user, market, competitor, or benchmark context is insufficient.
- Use `pm-prd` after scope, roles, ownership, and acceptance lens are stable.
- Use `pm-html-prototype` only when the artifact plan says an inspectable prototype is needed.
- Use `pm-review` when the boundary itself needs independent review or creates downstream risk.

## Resources

- Boundary method: `references/boundary-method.md`
- Boundary template: `assets/templates/boundary.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
