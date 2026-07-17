# Bad Output Examples

Use these examples as negative patterns. Do not copy the bad output into deliverables.

## Requirement Analysis

Bad:

```text
The user wants a dashboard. We will build a dashboard with charts and filters.
```

Why it is wrong: it treats the requested solution as the requirement and omits user, client surface, trigger, scope, constraints, and success condition.

Required action: convert the request into a product problem and mark missing inputs before downstream output.

## Metrics Definition

Bad:

```text
Success metric: feature launched successfully.
```

Why it is wrong: launch is delivery, not product success.

Required action: define the user behavior or business outcome the feature should change, plus guardrails.

Bad:

```text
Activation metric: number of users who saw the new page.
```

Why it is wrong: viewing a page is not necessarily activation unless the requirement proves that this view is the value moment.

Required action: identify the value-creating behavior, define the formula, segment, baseline, threshold, source, and guardrails before using the metric.

Bad:

```text
DAU increased after launch, so the feature worked.
```

Why it is wrong: correlation is treated as causation and there is no cohort, channel, version, segment, seasonality, or data-quality check.

Required action: mark this as an evaluation risk; define diagnostic cuts and attribution assumptions instead of claiming impact.

## Scenario Catalog

Bad:

```text
User completes approval flow.
```

Why it is wrong: missing role, client surface, trigger, user action, system response, fields, state change, exception, and acceptance lens.

Required action: expand to scenario-grain detail before PRD or prototype work.

## Use Case

Bad:

```text
Use case: manage suppliers.
```

Why it is wrong: the verb is too broad and has no actor goal, precondition, main flow, alternate flow, or post-condition.

Required action: split into specific use cases such as "Buyer creates supplier onboarding request" or "Approver rejects incomplete supplier profile."

## PRD

Bad:

```text
The page shows supplier name, status, and risk score. The system will be easy to use.
```

Why it is wrong: fields have no meaning, source, permission, validation, write-back behavior, or acceptance criteria.

Required action: add or link a field dictionary and testable acceptance criteria.

Bad:

```text
Problem: users need a search box to find suppliers.
```

Why it is wrong: it states a solution as the problem and hides the real user pain, current workaround, frequency, and success condition.

Required action: restate the problem before writing functional requirements, for example who cannot find what, in which surface, under what volume or constraint.

Bad:

```text
Acceptance criteria: the interface is beautiful, simple, and easy to use.
```

Why it is wrong: the criteria are subjective and cannot be converted into test scenarios.

Required action: replace subjective wording with observable behavior, limits, thresholds, supported states, and test steps.

Bad:

```text
Only happy-path flow is documented. Network failure, empty data, permission denial, duplicate submit, and timeout can be handled later.
```

Why it is wrong: exception flows are part of the requirement, not optional polish.

Required action: define exception triggers, system behavior, user recovery action, state changes, and acceptance lens before PRD approval.

Bad:

```text
The PRD includes a full Mermaid flowchart body inside the feature description because it is convenient.
```

Why it is wrong: diagrams become hard to route, review, version, and reuse when the workspace requires standalone diagram artifacts.

Required action: store diagrams as standalone files and link them from the PRD unless the workspace explicitly requires inline diagrams.

## Workflow Control

Bad:

```text
The user asked for a PRD, so run the complete flow: market research, solution comparison, technical stack selection, PRD, diagrams, export, and HTML prototype.
```

Why it is wrong: a fixed all-in-one workflow ignores requirement size, missing inputs, artifact plan, and user intent.

Required action: run requirement analysis first, choose the smallest needed artifact set, and mark unnecessary artifacts as not applicable.

Bad:

```text
Ask the user to choose React, Vue, backend language, database, and deployment before the product requirement is clear.
```

Why it is wrong: technical stack selection is being forced into product discovery and can bias the requirement before user problem, fields, and flow are stable.

Required action: defer technical stack questions unless they are a known workspace constraint or directly affect the product boundary.

## HTML Prototype

Bad:

```text
The prototype imports Ant Design from a CDN and uses production-looking API calls.
```

Why it is wrong: the prototype is not offline and blurs conceptual component mapping with production implementation.

Required action: use local assets, record component mapping assumptions, and keep production API claims out of the prototype.

Bad:

```text
The HTML prototype uses Tailwind CDN because it is faster, while the artifact plan requires offline review.
```

Why it is wrong: the output violates the offline constraint and may fail in restricted review environments.

Required action: use local CSS, local fonts, inline SVG or local icons, and record any unavailable design asset as a constraint.

Bad:

```text
The mobile prototype only shows the normal populated list.
```

Why it is wrong: reviewers cannot validate loading, empty, error, permission, timeout, or duplicate-action states.

Required action: include the state coverage required by scenarios and acceptance criteria, or record why a state is not applicable.

## Mermaid Diagram

Bad:

```text
Draw one large diagram containing research, product flow, data model, deployment, and roadmap.
```

Why it is wrong: a dense all-in-one diagram hides purpose and cannot be traced to scenarios, use cases, or artifact routing.

Required action: choose one diagram purpose and diagram type per file; split flow, state, sequence, architecture, and roadmap views when needed.

Bad:

```text
Swimlanes are Product, Tech, and Operation, but the actual flow depends on Buyer, Approver, Supplier, Web app, and ERP.
```

Why it is wrong: vague department lanes hide the true actors, client surfaces, and systems responsible for each step.

Required action: name lanes by real actors, systems, teams, or client surfaces from the scenario catalog.

## Prototype Review

Bad:

```text
The prototype looks good. Some details can be optimized later.
```

Why it is wrong: findings are not mapped to rules, fields, acceptance criteria, or open questions.

Required action: turn each finding into a specific issue with evidence, impact, recommendation, and decision.
