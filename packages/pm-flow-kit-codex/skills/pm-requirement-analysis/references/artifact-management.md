# Artifact Management Standard

Use the workspace standard first. If the workspace does not cover an artifact type, use this default structure.

```text
product/
  00-context/
    context_confirmation.md
  01-analysis/
    requirement_analysis.md
    scenario-catalog.md
    use-cases.md
    end-to-end-flow.md
    metrics-definition.md
    artifact-plan.md
  02-research/
    research.md
  03-boundary/
    boundary.md
  04-diagrams/
    diagram-index.md
    *.mmd
  05-prd/
    prd.md
    field-dictionary.md
    acceptance-criteria.md
  06-prototype/
    prototypes/
  07-review/
    review.md
    prototype-review.html
  08-delivery/
    test-scenarios.md
    delivery-checklist.md
```

## Rules

- `context_confirmation.md` records context intake.
- `requirement_analysis.md` records the analysis conclusion.
- `scenario-catalog.md` is the shared input for PRD, prototype, diagram, and test work.
- `use-cases.md` is the actor-goal flow contract for PRD, prototype, review, and testing work.
- `end-to-end-flow.md` is the actor/system handoff, state, branch, and exception contract.
- `metrics-definition.md` is the success, input, guardrail, baseline, source, and threshold contract.
- `artifact-plan.md` records whether each artifact is needed, where it lives, owner, and status.
- Mermaid diagrams live outside the PRD, normally under `product/04-diagrams/`.
- Field dictionaries live outside the PRD, normally under `product/05-prd/field-dictionary.md`.
- HTML prototypes live under `product/06-prototype/prototypes/` or the workspace-defined path.
- Prototype review artifacts are generated only when review materials are needed.
- Delivery checks are generated only for code-shipping, AI app launch, or implementation audit scenarios.
- Export artifacts are generated only when the user asks for export or the workspace standard requires an exportable package.
- Technical stack selection is recorded only when it is a confirmed constraint, feasibility risk, integration dependency, or delivery-risk input. Otherwise defer it.
- A requested PRD, diagram, or prototype does not imply that all other artifacts are needed.
