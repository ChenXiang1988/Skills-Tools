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

## HTML Prototype

Bad:

```text
The prototype imports Ant Design from a CDN and uses production-looking API calls.
```

Why it is wrong: the prototype is not offline and blurs conceptual component mapping with production implementation.

Required action: use local assets, record component mapping assumptions, and keep production API claims out of the prototype.

## Prototype Review

Bad:

```text
The prototype looks good. Some details can be optimized later.
```

Why it is wrong: findings are not mapped to rules, fields, acceptance criteria, or open questions.

Required action: turn each finding into a specific issue with evidence, impact, recommendation, and decision.
