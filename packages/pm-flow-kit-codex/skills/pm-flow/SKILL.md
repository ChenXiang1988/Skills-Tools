---
name: pm-flow
description: End-to-end product management workflow controller for workspace binding, knowledge-base path confirmation, staged context confirmation, research, boundary definition, requirement analysis, metrics definition, scenario and use-case coverage, end-to-end flow, prototype, PRD, and independent review delivery. Use when Codex needs to start, resume, or govern a product requirement with state tracking, required artifacts, gates, semantic checks, error handling, and cross-session progress.
---

# PM Flow

## Capability Boundary

`pm-flow` is the orchestration skill in `pm-flow-kit`. It owns workflow state, stage gates, artifact paths, and decisions.

It does not write the research artifact, boundary artifact, PRD, prototype, diagram, review artifact, metrics definition, requirement analysis, or final prose by itself.

It does not force a fixed all-in-one workflow. Artifact routing decides whether PRD, diagrams, HTML prototype, review artifact, delivery checks, export, or polishing are needed.

It must bind to one human-confirmed workspace root before product work starts. Once bound, reuse that workspace until the human explicitly changes it.

It must also bind to a human-confirmed knowledge-base boundary before product work starts. The boundary can be a knowledge-base root, a confirmed file list, or an explicit no-knowledge-base decision with a recorded reason.

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

0. Confirm the workspace root and write the binding to `.pm-flow/project_config.json`.
1. Confirm the knowledge-base path, source list, or explicit no-knowledge-base reason in `.pm-flow/project_config.json`.
2. Confirm context intake with `context_confirmation.md`.
3. Complete requirement analysis with `requirement_analysis.md`.
4. Complete scenario coverage with `scenario-catalog.md`.
5. Complete use case coverage with `use-cases.md`.
6. Complete end-to-end flow coverage with `end-to-end-flow.md`.
7. Complete metrics definition with `metrics-definition.md`.
8. Complete artifact planning with `artifact-plan.md`.

## Skill Routing Inside The Package

- Use `pm-context-contract` for context and knowledge-base intake.
- Use `pm-research` for research-stage opportunity, user, market, competitor, benchmark, metric-context, source-risk, assumption, and open-question artifacts.
- Use `pm-requirement-analysis` for requirement analysis, scenario catalog, use cases, end-to-end flow, and artifact plan.
- Use `pm-metrics-definition` for business, user behavior, input, guardrail, baseline, and threshold definitions.
- Use `pm-boundary` for scope, non-scope, stakeholders, roles, permissions, surfaces, system ownership, constraints, dependencies, assumptions, risks, and decisions.
- Use `pm-prd` for PRD sizing, PRD templates, field dictionary, and acceptance criteria.
- Use `pm-html-prototype` for offline HTML prototypes.
- Use `pm-prototype-review` only when a prototype-specific review artifact is needed.
- Use `pm-review` for general independent review-stage artifacts and readiness conclusion.
- Use `pm-mermaid-diagram` for standalone diagrams.
- Use `humanizer` only after the facts, scope, and acceptance criteria are stable.

Do not replace these package skills with outside PM skills unless the user explicitly asks for a separate tool.

## Failure Cases

- Wrong use: starting product work without asking the human for the workspace location when no workspace binding exists.
- Wrong use: asking for the workspace again when `.pm-flow/project_config.json` already has a valid binding.
- Wrong use: continuing after the workspace directory moved or changed without a human-approved rebind.
- Wrong use: starting product work without asking the human for the knowledge-base path or explicit no-knowledge-base decision when no knowledge-base binding exists.
- Wrong use: asking for the knowledge-base path again when `.pm-flow/project_config.json` already has a valid binding.
- Wrong use: continuing after the knowledge-base root, manifest, or confirmed source list is missing, moved, or inconsistent without a human-approved rebind.
- Wrong use: changing the user's existing information structure instead of writing plugin-owned files under `.pm-flow/` or mapped artifact paths.
- Wrong use: advancing a stage before the first-circle analysis bundle is complete.
- Wrong use: running market research, solution comparison, technical stack selection, PRD, diagrams, export, prototype, and review as a fixed bundle for every request.
- Wrong use: copying large external PM reference packs into the plugin instead of extracting reusable rules, templates, or failure cases.
- Bad output: defaulting every artifact to needed instead of using artifact-plan decisions.
- Bad output: producing PRD, prototype, or review output after P1/P0 source errors.
- Bad output: using a package skill name that does not exist in the current manifest.
- Blocking gap: context confirmation, requirement analysis, metrics, scenario, use cases, end-to-end flow, or artifact plan is missing or unconfirmed.

## Operating Rules For Agents

1. Read `USAGE.md` before operating the controller.
2. If no workspace binding exists, ask the human for the workspace root and run `controller.py workspace bind --root <workspace-root> --confirm --by <name>`.
3. If a valid workspace binding exists, do not ask for the workspace again.
4. If the human requests a workspace change, run `controller.py workspace rebind --root <new-workspace-root> --confirm --by <name>`.
5. If the controller reports a workspace mismatch, stop work and clarify the workspace structure before continuing.
6. If no knowledge-base binding exists, ask the human for the knowledge-base path, confirmed file list, or explicit no-knowledge-base decision.
7. If a valid knowledge-base binding exists, do not ask for the knowledge-base path again.
8. If the human requests a knowledge-base change, run `controller.py knowledge rebind --root <project-root> --knowledge-root <knowledge-root> --confirm --by <name>`.
9. If the controller reports a knowledge-base mismatch, missing manifest, or missing source, stop work and clarify the knowledge-base boundary before continuing.
10. Run `controller.py status --root <project-root>` before deciding the next action.
11. If context confirmation is not confirmed, complete it first.
12. If requirement analysis bundle is not confirmed, complete it second.
13. Work only on `current_stage`.
14. Follow `confirm -> mark -> close --checked -> validate`.
15. Record key decisions with `controller.py decide`.
16. Respect `.pm-flow/project_config.json` when the project defines custom artifact paths.
17. Treat assumptions as assumptions. Do not write them as facts.
18. If source material is wrong, classify the error severity and block P1/P0 issues before producing downstream artifacts.

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
python3 controller.py workspace status --root <project-root>
python3 controller.py workspace bind --root <project-root> --confirm --by <name>
python3 controller.py workspace rebind --root <new-project-root> --confirm --by <name>
python3 controller.py knowledge status --root <project-root>
python3 controller.py knowledge bind --root <project-root> --knowledge-root <knowledge-root> --confirm --by <name>
python3 controller.py knowledge bind --root <project-root> --none --reason "No external knowledge base is used for this task." --confirm --by <name>
python3 controller.py knowledge rebind --root <project-root> --knowledge-root <new-knowledge-root> --confirm --by <name>
python3 controller.py status --root <project-root>
python3 controller.py context confirm --root <project-root>
python3 controller.py analyze --root <project-root>
python3 controller.py confirm <stage> --root <project-root> --by <name>
python3 controller.py mark <stage> --root <project-root>
python3 controller.py close <stage> --root <project-root> --checked --by <name>
python3 controller.py validate --root <project-root>
```
