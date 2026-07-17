---
name: pm-metrics-definition
description: Define product success metrics before PRD, prototype, or review output. Use when Codex needs to convert product goals into business metrics, user behavior metrics, guardrail metrics, baselines, metric definitions, data sources, decision thresholds, non-applicability reasons, and measurement risks for requirement analysis and PRD work.
---

# PM Metrics Definition

## Capability Boundary

Define the metric contract for a product requirement. The goal is to clarify why the requirement matters, what outcome it should change, how success will be measured, and which guardrails must not regress.

Do not perform full analytics, SQL analysis, A/B test evaluation, dashboard design, or growth strategy. Do not invent baselines or data sources.

## Required Inputs

- Requirement analysis or a clear product problem.
- Target users, roles, and client surfaces.
- Business goal or user outcome.
- Known data sources or analytics constraints, if available.

Stop and ask for clarification when the requirement has no business goal, no observable user behavior, or no way to distinguish success from completion.

Stop when the proposed metric is only exposure, launch, page view, task completion, or output creation and no value-creating behavior or business outcome is defined.

Continue with explicit assumptions only when the requirement is compliance, bug fix, internal cleanup, or purely explanatory and metrics are partially non-applicable.

## Output Contract

Create or update `metrics-definition.md` with:

- Business objective.
- User behavior objective.
- Primary success metric.
- Supporting input metrics.
- Guardrail metrics.
- Baseline or "unknown baseline" note.
- Metric formula and unit.
- Data source, owner, and collection point.
- Decision threshold.
- Measurement risks.
- Non-applicability reasons when a metric type is not needed.

## Failure Cases

- Bad input: "make it better" without a target outcome, user behavior, or decision threshold.
- Wrong use: treating task completion, feature launch, or document creation as the success metric.
- Wrong use: treating page exposure or click volume as activation without proving it represents the value moment.
- Bad output: vague metrics such as "user satisfaction improves" without formula, source, baseline, or threshold.
- Bad output: a primary metric with no guardrail metrics for quality, risk, latency, cost, or compliance impact.
- Bad output: invented analytics events, baselines, or dashboards not supported by source material.
- Bad output: claiming feature impact from a metric change without data-quality, cohort, channel, version, segment, seasonality, or attribution checks.

## Handoff Rules

- Use `pm-requirement-analysis` first when the product problem, target user, or scope is unclear.
- Use `pm-prd` after metrics are stable enough to constrain the PRD.
- Use `pm-mermaid-diagram` only when metrics depend on a flow or funnel that needs visualization.
- Use second-circle analytics skills only when raw data, experiment results, or SQL analysis is actually needed.

## Resources

- Template: `assets/templates/metrics-definition.md`
- Method reference: `references/metrics-definition.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
