# Metrics Definition Method

Use the smallest metric set that can support product decisions.

## Metric Types

- Primary success metric: the main outcome the requirement should improve.
- Input metrics: user behaviors or operational levers that plausibly drive the primary metric.
- Guardrail metrics: quality, risk, compliance, cost, latency, or support metrics that must not regress.
- Non-applicable metric: a metric type that is not relevant for the requirement, with a reason.

## Selection Rules

- Prefer observable behavior over opinions.
- Prefer ratios or rates over raw counts when population size changes.
- Mark missing baselines as unknown. Do not invent them.
- Tie every metric to a scenario, use case, field, event, or data source when possible.
- For compliance, safety, legal, or migration work, success may be "required completion with no regression"; still define guardrails.

## Blocking Gaps

Block downstream PRD or prototype work when:

- no success condition can be stated;
- the metric depends on a data source that does not exist or is unknown and no assumption is acceptable;
- the user asks for KPI improvement but provides no target population or behavior;
- a metric would encourage harmful behavior without guardrails.
