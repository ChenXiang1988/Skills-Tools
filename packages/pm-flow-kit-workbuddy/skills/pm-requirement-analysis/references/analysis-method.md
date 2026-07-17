# Requirement Analysis Method

This method is embedded in `pm-requirement-analysis` and does not depend on package-external PM skills.

## 1. Move From Solution To Problem

Users often request a feature directly. First answer:

- What problem is this trying to solve?
- Who is affected?
- What happens if nothing changes?
- What result is expected?
- Is the input a problem, opportunity, solution, or implementation instruction?

Do not treat the requested feature as the final solution without analysis.

## 2. Group Fragmented Inputs

When the input is a list of requests or feedback, group it before writing scenarios.

| Theme | Representative input | Affected users | Scope | Value | Risk | Suggested handling |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 3. Scenario Grain

The minimum scenario grain is:

```text
role + client surface + trigger + user action + system response + fields + post-condition + exception + acceptance lens
```

Each scenario must tell prototype and PRD work which page, action, data, and rule to cover.

## 4. Use Case Grain

The minimum use case grain is:

```text
actor + goal + preconditions + trigger + main flow + alternate flow + exception flow + post-condition + acceptance lens
```

Use cases explain what the actor is trying to accomplish. Scenarios explain where, when, and how the interaction happens.

## 5. End-To-End Flow Grain

The minimum end-to-end flow grain is:

```text
start event + end state + actors + systems + handoffs + decision branches + state changes + data touched + exception paths
```

Do not use broad phase names as a flow. A flow must show concrete handoffs and state changes.

## 6. Analysis Levels

| Level | Use When | Must Cover |
|---|---|---|
| A0 Quick check | Copy, small field, local explanation | Goal, scope, acceptance, metric non-applicability reason, artifact non-applicability reason |
| A1 Light clarification | One role, one page, simple rule | User, scenario, use case, boundary, metric lens, PRD level, acceptance |
| A2 Standard analysis | Normal iteration, multiple pages, roles, flow, or state change | Scenario catalog, use cases, end-to-end flow, metrics, exceptions, fields, assumptions, risks, artifact plan |
| A3 Deep analysis | New platform, core flow, cross-system work, money, inventory, fulfillment, permission, approval, compliance, or AI launch | End-to-end flow, state machine guidance, data definitions, metrics and guardrails, major risks, delivery or audit artifacts |
