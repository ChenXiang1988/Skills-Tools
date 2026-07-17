# PM Flow Usage

`pm-flow` is the workflow controller for `pm-flow-kit`. It turns product work into explicit state, required artifacts, decisions, and gates.

## Internal Skill Map

| Need | Use |
|---|---|
| Start, resume, and advance the workflow | `pm-flow` |
| Context and knowledge-base intake | `pm-context-contract` |
| Research-stage opportunity, user, market, competitor, benchmark, metrics context, source risk, assumptions, and open questions | `pm-research` |
| Requirement analysis, scenario catalog, use cases, end-to-end flow, artifact plan | `pm-requirement-analysis` |
| Metrics definition | `pm-metrics-definition` |
| Boundary-stage scope, non-scope, stakeholders, roles, permissions, surfaces, system ownership, constraints, dependencies, assumptions, risks, and decisions | `pm-boundary` |
| HTML prototype | `pm-html-prototype` |
| Optional prototype review artifact | `pm-prototype-review` |
| PRD sizing, templates, field dictionary, acceptance criteria | `pm-prd` |
| General independent review and readiness conclusion | `pm-review` |
| Mermaid diagrams | `pm-mermaid-diagram` |
| Final prose polishing | `humanizer` |

Load only the skill needed for the current action. Do not read the whole package at once.

## Workspace Binding

Before `pm-flow-kit` performs product work, the agent must know the workspace root.

Rules:

- If no workspace is bound, ask the human for the workspace location.
- Once the workspace is bound in `.pm-flow/project_config.json`, reuse it and do not ask again.
- If the human asks to change the workspace, rebind it explicitly.
- If the workspace directory was moved or the current `--root` no longer matches the binding, stop work and clarify the workspace structure.
- Do not rearrange the human's existing folders. The plugin may create `.pm-flow/` and `.pm-flow/work/`, plus mapped artifacts defined by `project_config.json`.

Commands:

```bash
python3 controller.py workspace status --root <workspace-root>
python3 controller.py workspace bind --root <workspace-root> --confirm --by <name>
python3 controller.py workspace rebind --root <new-workspace-root> --confirm --by <name>
```

`init` and `attach` also write the workspace binding. Use `workspace bind` before `init` when the human wants an explicit workspace confirmation step.

## Knowledge-Base Binding

Before `pm-flow-kit` performs product work, the agent must know the knowledge-base boundary.

Rules:

- If no knowledge base is bound, ask the human for the knowledge-base path or ask whether no external knowledge base is used.
- Once the knowledge base is bound in `.pm-flow/project_config.json`, reuse it and do not ask again.
- If the human asks to change the knowledge base, rebind it explicitly.
- If the knowledge-base root, manifest, or confirmed source list is missing, moved, or inconsistent, stop work and clarify the knowledge-base boundary.
- The agent reads the knowledge base. The plugin records the binding, gates, and artifacts; it does not store company knowledge inside the plugin.
- Do not read the whole knowledge base by default. Use the manifest, applicable source list, and current task to select sources.

Commands:

```bash
python3 controller.py knowledge status --root <project-root>
python3 controller.py knowledge bind --root <project-root> --knowledge-root <knowledge-root> --confirm --by <name>
python3 controller.py knowledge bind --root <project-root> --source <file> --confirm --by <name>
python3 controller.py knowledge bind --root <project-root> --none --reason "No external knowledge base is used for this task." --confirm --by <name>
python3 controller.py knowledge rebind --root <project-root> --knowledge-root <new-knowledge-root> --confirm --by <name>
```

`init` and `attach` automatically bind the knowledge base when `--context-root`, `--context-file`, or `--intake` is provided. If none is provided, the knowledge base remains unconfirmed and later product-work commands stop until `knowledge bind` is completed.

## Mandatory Preflight

The workflow must not start by writing a PRD, prototype, diagram, or review artifact. Complete these artifacts first:

```text
workspace binding
knowledge-base binding
context_confirmation.md
requirement_analysis.md
scenario-catalog.md
use-cases.md
end-to-end-flow.md
metrics-definition.md
artifact-plan.md
```

Order:

1. Generate and complete `context_confirmation.md`.
2. Confirm context intake.
3. Generate and complete requirement analysis, scenario, use case, flow, metrics, and artifact-plan artifacts.
4. Confirm requirement analysis.
5. Advance the current stage.

Commands:

```bash
python3 controller.py context confirm --root <project-root>
python3 controller.py context confirm --root <project-root> --confirm --by <name>
python3 controller.py analyze --root <project-root>
python3 controller.py analyze --root <project-root> --confirm --by <name>
```

The requirement analysis must cover:

- Problem and goal.
- Target users and scenarios.
- Scope and non-scope.
- Confirmed facts, assumptions, and open questions.
- Constraints, dependencies, and risks.
- Success criteria, metric lens, and acceptance lens.
- Requirement analysis level: A0, A1, A2, or A3.
- Recommended flow path and artifact plan.
- Scenario catalog at this minimum grain: role, client surface, trigger, user action, system response, fields, post-condition, exception, and acceptance lens.
- Use cases at this minimum grain: actor, goal, preconditions, trigger, main flow, alternate or exception flow, post-condition, fields, related metrics, and acceptance lens.
- End-to-end flow at this minimum grain: start/end, actors, systems, handoffs, branches, state changes, data touched, and exception paths.
- Metrics definition: primary metric, input metrics, guardrails, baseline/source/threshold, or non-applicability reason.
- Source error check with P3/P2/P1/P0 severity when needed.

## Existing Project Mapping

If the project already defines its own directory structure, keep that structure unchanged and attach a `.pm-flow/project_config.json` mapping:

```json
{
  "workspace": {
    "root": "/absolute/path/to/workspace",
    "realpath": "/absolute/path/to/workspace",
    "confirmed_at": "2026-07-17T00:00:00+08:00",
    "confirmed_by": "human",
    "plugin_workdir": ".pm-flow/work",
    "preserve_existing_structure": true,
    "stop_on_mismatch": true
  },
  "knowledge_base": {
    "status": "confirmed",
    "mode": "root",
    "root": "/absolute/path/to/knowledge-base",
    "realpath": "/absolute/path/to/knowledge-base",
    "manifest": "/absolute/path/to/knowledge-base/CONTEXT_MANIFEST.md",
    "sources": [
      "/absolute/path/to/knowledge-base/CONTEXT_MANIFEST.md"
    ],
    "confirmed_at": "2026-07-17T00:00:00+08:00",
    "confirmed_by": "human",
    "no_knowledge_base_reason": null,
    "stop_on_mismatch": true
  },
  "artifacts": {
    "context_confirmation": "product/context-confirmation.md",
    "requirement_analysis": "product/requirement-analysis.md",
    "scenario_catalog": "product/scenario-catalog.md",
    "use_cases": "product/use-cases.md",
    "end_to_end_flow": "product/end-to-end-flow.md",
    "metrics_definition": "product/metrics-definition.md",
    "artifact_plan": "product/artifact-plan.md",
    "boundary": "product/scope.md",
    "prototype": "prototype/**/*.html",
    "prd": "requirements/prd.md",
    "review": "docs/review.md"
  }
}
```

## Stage Advancement

Use this sequence for each stage:

```bash
python3 controller.py status --root <project-root>
python3 controller.py confirm <stage> --root <project-root> --by <name>
python3 controller.py mark <stage> --root <project-root>
python3 controller.py close <stage> --root <project-root> --checked --by <name>
python3 controller.py validate --root <project-root>
```

`close --checked` means every semantic check in `contract_config.json` has been reviewed. If a check does not apply, record why in the stage artifact or decision log.

## Stage Guidance

- `research`: use `pm-research` to establish opportunity, user, market, competitor, benchmark, metric context, source risks, assumptions, and open questions.
- `boundary`: use `pm-boundary` to define scope, non-scope, stakeholders, roles, permissions, surfaces, system ownership, constraints, dependencies, assumptions, risks, and decisions.
- `prototype`: use `pm-html-prototype` only when the artifact plan says an HTML prototype is needed.
- `prd`: use `pm-prd`; create diagrams, field dictionary, and acceptance criteria as separate companion artifacts when needed.
- `review`: use `pm-review` to close open findings, risk issues, decisions, and downstream readiness.

## Diagrams

Use `pm-mermaid-diagram` when the requirement includes workflow branches, swimlanes, state transitions, sequence interactions, or architecture relationships. Store diagrams as standalone files, normally under `product/04-diagrams/`. The PRD should link to diagrams instead of embedding full chart bodies.

## Prototypes

Use `pm-html-prototype` for offline HTML prototypes. If the project knowledge base has design guidelines, component-library rules, frontend framework rules, or font constraints, apply them. If none exist, use the built-in baseline style and record the design assumptions.

Prototype scaffolding snapshots a design system into `prototypes/assets/design-system/`. Source order is: `PM_FLOW_DESIGN_SYSTEM`, project `design-system/`, project `.pm-flow/design-system/`, then the bundled generic `design-system/`. Project-specific design rules override the bundled fallback.

Use `pm-prototype-review` only when a review artifact is needed. The review artifact is not mandatory for every prototype.

## Review

Use `pm-review` for the general review stage. Use `pm-prototype-review` only for prototype-specific review artifacts requested by the artifact plan.

## PRD And Polishing

Use `pm-prd` to decide L1, L2, or L3 before writing the PRD.

Use `humanizer` only after content is factually stable. It may improve expression, but must not change scope, non-scope, roles, flow, states, permissions, fields, exceptions, acceptance criteria, key decisions, or open questions.

## Forbidden

- Starting work without a confirmed workspace root.
- Asking for workspace location again when `.pm-flow/project_config.json` already has a valid binding.
- Continuing after a workspace mismatch without human-approved rebind.
- Starting work without a confirmed knowledge-base path or explicit no-knowledge-base decision.
- Asking for the knowledge-base path again when `.pm-flow/project_config.json` already has a valid binding.
- Continuing after a knowledge-base root, manifest, or source mismatch without human-approved rebind.
- Restructuring existing human folders as part of plugin setup.
- Writing a PRD before checking `status`.
- Skipping context confirmation.
- Claiming knowledge-base usage without listing applicable and non-applicable sources.
- Skipping requirement analysis, metrics definition, use cases, end-to-end flow, or artifact planning.
- Producing PRD, prototype, diagram, or review output directly when the user asks for it.
- Continuing from P1/P0 source errors.
- Attacking people or groups when source material is wrong.
- Advancing without an artifact.
- Closing without semantic checks.
- Reading the entire knowledge base by default.
- Writing assumptions as facts.
- Closing a stage with unresolved conflicts.
- Bypassing the package artifact plan.
- Replacing `pm-prd` with another PRD generator by default.
- Adding code-shipping checks to ordinary product requirements by default.
