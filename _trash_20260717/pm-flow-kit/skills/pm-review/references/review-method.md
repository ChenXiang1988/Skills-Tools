# Review Method

## Review Order

1. Confirm the review scope and artifact plan.
2. Check that required upstream artifacts are present and stable.
3. Compare PRD, prototype, diagrams, metrics, boundary, and decisions against each other.
4. Classify each issue by severity.
5. Record whether each finding is closed or intentionally unresolved.
6. State whether the work is ready or requires rework.

## Review Dimensions

- Problem and goal alignment.
- Scope and non-scope consistency.
- Role, permission, client surface, and system ownership clarity.
- Metrics quality and non-applicability reasons.
- Scenario, use case, and end-to-end flow coverage.
- Acceptance criteria testability.
- Source conflicts, assumptions, risks, and open questions.
- Prototype, diagram, and field traceability when applicable.

## Severity

- High: blocks downstream delivery or can create material business, compliance, data, permission, or user harm.
- Medium: likely causes rework, ambiguity, or quality regression.
- Low: local clarity, wording, or completeness issue that does not block the next stage.

## Readiness Rule

Use `Ready` only when high and medium findings are closed or explicitly accepted by the owner. Use `Rework required` when a blocking issue remains unresolved.
