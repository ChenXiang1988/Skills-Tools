---
name: pm-prd
description: Create right-sized product requirements documents. Use when you need to write, review, resize, or refactor PRDs using L1/L2/L3 depth, requirement-analysis inputs, metrics definitions, scenario catalogs, use cases, artifact plans, field dictionaries, acceptance criteria, and standalone diagram references.
---

# PM PRD

## Capability Boundary

Create or review right-sized PRDs. Use the smallest PRD level that can safely support design, engineering, testing, and review.

Do not perform requirement analysis, invent metrics, create HTML prototypes, generate review artifacts, or embed full diagrams in the PRD body.

## Required Inputs

- `requirement_analysis.md`
- `metrics-definition.md`
- `scenario-catalog.md`
- `use-cases.md`
- `end-to-end-flow.md`
- `artifact-plan.md`
- Applicable context sources confirmed by `context_confirmation.md`

Stop when the requirement analysis bundle is missing, when metrics are undefined without a non-applicability reason, or when scenarios are too vague to produce testable acceptance criteria.

## PRD Sizing

Read `references/prd-sizing.md` before selecting a template:

- L1: light PRD for small, low-risk changes.
- L2: standard PRD for normal product iterations.
- L3: deep PRD for cross-system, high-risk, stateful, data-heavy, compliance-heavy, or launch-critical work.

## Outputs

- `prd.md`
- `field-dictionary.md` when fields, data sources, permissions, or write-back behavior matter.
- `acceptance-criteria.md` when acceptance criteria need testable structure.
- Standalone Mermaid diagram files when flow branches or state transitions are complex.

## Failure Cases

- Wrong use: forcing every request into L3.
- Wrong use: writing a PRD before requirement analysis, metrics, scenarios, and use cases exist.
- Bad output: fields are buried in prose instead of a field dictionary.
- Bad output: metrics are not referenced or success is defined as "feature launched."
- Bad output: acceptance criteria cannot be converted into test scenarios.
- Bad output: assumptions, open questions, or source conflicts are written as facts.
- Blocking gap: scope changed from requirement analysis without a recorded decision.

## Handoff Rules

- Use `pm-requirement-analysis` when the analysis bundle is incomplete.
- Use `pm-metrics-definition` when success metrics, guardrails, baselines, or thresholds are missing.
- Use `pm-mermaid-diagram` for standalone flow, swimlane, state, or sequence diagrams.
- Use `pm-html-prototype` after PRD sections and fields are stable enough to support UI screens.
- Use `humanizer` only after the PRD is factually stable.

## Resources

- PRD sizing: `references/prd-sizing.md`
- PRD quality checklist: `references/prd-quality-checklist.md`
- Diagram guidance: `references/diagram-guidelines.md`
- Templates: `templates/`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
