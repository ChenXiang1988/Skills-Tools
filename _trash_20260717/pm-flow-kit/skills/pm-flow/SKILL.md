---
name: pm-flow
description: End-to-end product management workflow controller for staged
  context confirmation, requirement analysis, metrics definition, scenario and
  use-case coverage, end-to-end flow, prototype, PRD, and review delivery. Use
  when you need to start, resume, or govern a product requirement with state
  tracking, required artifacts, gates, semantic checks, error handling, and
  cross-session progress.
disable: true
---

# PM Flow

## Capability Boundary

`pm-flow` is the orchestration skill in `pm-flow-kit`. It owns workflow state, stage gates, artifact paths, and decisions.

It does not write the PRD, prototype, diagram, review artifact, metrics definition, requirement analysis, or final prose by itself.

## Required Position In The Plugin

Keep `pm-flow` when the plugin is used as a workflow system. Without it, the package becomes a loose toolkit and loses:

- A single state file for long-running work.
- Stage order and gate enforcement.
- Required artifact checks.
- Context confirmation, requirement analysis, metrics, scenario, use-case, flow, and artifact-plan preflight.
- Decision history.

If the package is intentionally converted into a simple PM toolkit, `pm-flow` can be removed. That is not the current design.

## Workflow

Supported paths:

| Type | Path |
|---|---|
| `new-platform` | `research -> boundary -> prototype -> prd -> review` |
| `iteration` | `boundary -> prototype -> prd -> review` |
| `iteration-lite` | `boundary -> prd -> review` |
| `micro` | `prd -> review` |

Global preflight is mandatory before any stage can advance:

1. Confirm context intake with `context_confirmation.md`.
2. Complete requirement analysis with `requirement_analysis.md`.
3. Complete scenario coverage with `scenario-catalog.md`.
4. Complete use case coverage with `use-cases.md`.
5. Complete end-to-end flow coverage with `end-to-end-flow.md`.
6. Complete metrics definition with `metrics-definition.md`.
7. Complete artifact planning with `artifact-plan.md`.

## Skill Routing Inside The Package

- Use `pm-context-contract` for context and knowledge-base intake.
- Use `pm-research` for the research stage: opportunity, user, market, competitor, benchmark, metric context, source-risk, assumption, and open-question artifacts.
- Use `pm-requirement-analysis` for requirement analysis, scenario catalog, use cases, end-to-end flow, and artifact plan.
- Use `pm-metrics-definition` for business, user behavior, input, guardrail, baseline, and threshold definitions.
- Use `pm-boundary` for the boundary stage: scope, non-scope, stakeholders, roles, permissions, client surfaces, system ownership, constraints, dependencies, assumptions, risks, and decisions.
- Use `pm-prd` for PRD sizing, PRD templates, field dictionary, and acceptance criteria.
- Use `pm-html-prototype` for offline HTML prototypes.
- Use `pm-prototype-review` only when a review artifact is needed.
- Use `pm-mermaid-diagram` for standalone diagrams.
- Use `pm-review` for the general review stage and readiness conclusion.
- Use `humanizer` only after the facts, scope, and acceptance criteria are stable.

Do not replace these package skills with outside PM skills unless the user explicitly asks for a separate tool.

## Failure Cases

- Wrong use: advancing a stage before the first-circle analysis bundle is complete.
- Bad output: defaulting every artifact to needed instead of using artifact-plan decisions.
- Bad output: producing PRD, prototype, or review output after P1/P0 source errors.
- Bad output: using a package skill name that does not exist in the current manifest.
- Blocking gap: context confirmation, requirement analysis, metrics, scenario, use cases, end-to-end flow, or artifact plan is missing or unconfirmed.

## Operating Rules For Agents

1. Read `USAGE.md` before operating the controller.
2. Run `controller.py status --root <project-root>` before deciding the next action.
3. If context confirmation is not confirmed, complete it first.
4. If requirement analysis bundle is not confirmed, complete it second.
5. Work only on `current_stage`.
6. Follow `confirm -> mark -> close --checked -> validate`.
7. Record key decisions with `controller.py decide`.
8. Respect `.pm-flow/project_config.json` when the project defines custom artifact paths.
9. Treat assumptions as assumptions. Do not write them as facts.
10. If source material is wrong, classify the error severity and block P1/P0 issues before producing downstream artifacts.

## Resources

- Usage guide: `USAGE.md`
- Contract gates: `contract_config.json`
- State machine: `references/flow-state-machine.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`

## Controller

Use the controller from this skill directory:

```bash
python3 controller.py init iteration --root <project-root> --project "Project" --requirement "Requirement"
python3 controller.py status --root <project-root>
python3 controller.py context confirm --root <project-root>
python3 controller.py analyze --root <project-root>
python3 controller.py confirm <stage> --root <project-root> --by <name>
python3 controller.py mark <stage> --root <project-root>
python3 controller.py close <stage> --root <project-root> --checked --by <name>
python3 controller.py validate --root <project-root>
```
