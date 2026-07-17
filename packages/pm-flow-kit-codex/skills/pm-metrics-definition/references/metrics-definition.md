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
- Treat exposure, page view, and click count as diagnostic input metrics unless the requirement proves they are the value moment.
- Mark missing baselines as unknown. Do not invent them.
- Tie every metric to a scenario, use case, field, event, or data source when possible.
- For compliance, safety, legal, or migration work, success may be "required completion with no regression"; still define guardrails.

## Diagnostic Checks

Use diagnostic checks when a metric will be used to evaluate feature impact:

- Data quality: pipeline delay, missing events, event definition changes, ETL failure, or dashboard freshness.
- Cohort and segment cuts: new vs. returning users, role, client surface, customer tier, region, channel, and version.
- Attribution: launch date, campaign overlap, seasonality, external events, or unrelated product changes.
- Guardrails: retention, complaint rate, support tickets, latency, cost, compliance risk, or conversion quality.

## Blocking Gaps

Block downstream PRD or prototype work when:

- no success condition can be stated;
- the metric depends on a data source that does not exist or is unknown and no assumption is acceptable;
- the user asks for KPI improvement but provides no target population or behavior;
- a metric would encourage harmful behavior without guardrails.
- feature impact is claimed from observed movement without any attribution or diagnostic check.
