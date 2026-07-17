---
name: pm-requirement-analysis
description: Analyze product requirements before downstream output. Use when Codex needs to convert rough or direct user requests into requirement analysis, scenario catalog, use cases, end-to-end flow, artifact plan, assumptions, risks, source-error checks, and output routing before metrics, PRD, prototype, diagram, review, or polishing work.
---

# PM Requirement Analysis

## Capability Boundary

Turn rough requests into a controlled product analysis bundle. This skill defines the problem, scope, scenarios, use cases, end-to-end flow needs, analysis level, risks, and downstream artifact plan.

Do not write the final PRD, HTML prototype, prototype review artifact, final diagrams, metrics analysis, or polished prose.

Do not turn one requested artifact into a fixed full workflow. Decide each downstream artifact independently.

## Required Inputs

- Original request or intake.
- Context confirmation when company, project, domain, design, component, font, or frontend constraints exist.
- Known users, roles, client surfaces, business goal, or source materials when available.

Stop when the request has no identifiable user, problem, scope, or expected outcome. Continue with explicit assumptions only when the missing information is non-blocking for the selected analysis level.

## Output Contract

Always produce or update:

- `requirement_analysis.md`
- `scenario-catalog.md`
- `use-cases.md`
- `end-to-end-flow.md`
- `metrics-definition.md`
- `artifact-plan.md`

Each file may record a non-applicability reason, but it must not be omitted from the first-circle analysis bundle.

## Required Granularity

- Scenario grain: role + client surface + trigger + user action + system response + fields + post-condition + exception + acceptance lens.
- Use case grain: actor + goal + preconditions + main flow + alternate or exception flow + post-condition + acceptance lens.
- Flow grain: start/end, actors, systems, state changes, handoffs, decision branches, and exception paths.
- Metrics grain: business objective, user behavior objective, primary metric, input metrics, guardrails, baseline/source/threshold, or non-applicability reason.

## Failure Cases

- Bad input: "build this page" without problem, role, client surface, or expected outcome.
- Wrong use: skipping requirement analysis because the user directly asked for a PRD or prototype.
- Bad output: scenarios are broad phases rather than concrete user/system interactions.
- Bad output: use cases omit preconditions, exception flows, or post-conditions.
- Bad output: artifact plan marks every artifact as needed by default.
- Bad output: technical stack selection is forced before it is known to be a product constraint.
- Bad output: a solution request is accepted as the problem statement without restating the underlying user or business problem.
- Blocking gap: P1/P0 source error, missing owner decision, or unresolvable scope conflict.

## Handoff Rules

- Use `pm-context-contract` first when source scope or knowledge-base usage is unclear.
- Use `pm-metrics-definition` when metrics need deeper definition than the basic template.
- Use `pm-prd` only after the analysis bundle is stable.
- Use `pm-html-prototype` only when the artifact plan requires inspectable screens.
- Use `pm-prototype-review` only when the artifact plan requires a separate review artifact.
- Use `pm-mermaid-diagram` when flow, state, sequence, or swimlane diagrams are needed.
- Use `humanizer` only after facts, scope, metrics, and acceptance criteria are stable.

## Resources

- Method reference: `references/analysis-method.md`
- Artifact management: `references/artifact-management.md`
- Requirement analysis template: `assets/templates/requirement-analysis.md`
- Scenario catalog template: `assets/templates/scenario-catalog.md`
- Use cases template: `assets/templates/use-cases.md`
- End-to-end flow template: `assets/templates/end-to-end-flow.md`
- Artifact plan template: `assets/templates/artifact-plan.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
