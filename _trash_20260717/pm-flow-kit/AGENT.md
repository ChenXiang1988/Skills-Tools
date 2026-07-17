# pm-flow-kit Agent Protocol

This document is for agents using `pm-flow-kit`.

## Local Update Boundary

- Treat local skill/kit modification and publishing to a connector or the marketplace as two separate actions.
- When the human asks to modify, optimize, fix, or test `pm-flow-kit`, default to local files only.
- Do not publish or upload changes to a connector or marketplace, and do not bump the distributed version, unless the human explicitly asks to publish.
- Phrases that count as explicit publish approval include: "发布到连接器", "发布到市场", "上传", "重新发布", or equivalent wording.
- After local validation, report the local result and wait for the human's explicit instruction before publishing.

## Responsibility Boundary

- The agent reads the project knowledge base and decides which sources apply to the current task.
- The agent records cited sources, excluded sources, assumptions, and conflicts in the artifacts.
- `pm-flow-kit` provides workflow control, templates, gates, and package-internal specialist skills.
- `pm-flow-kit` does not store company or project knowledge directly.
- Knowledge bases should contain facts, constraints, standards, and references. Do not copy this protocol into a knowledge base.

## Startup Sequence

1. Use `skills/pm-flow/SKILL.md` as the entry skill.
2. Read `skills/pm-flow/USAGE.md`.
3. If no workspace binding exists, ask the human for the workspace root.
4. Confirm the workspace with `controller.py workspace bind --root <project-root> --confirm --by <name>`.
5. If a valid workspace binding already exists, do not ask again.
6. If no knowledge-base binding exists, ask the human for the knowledge-base root, confirmed source files, or explicit no-knowledge-base decision.
7. Confirm the knowledge-base boundary with `controller.py knowledge bind --root <project-root> --knowledge-root <knowledge-root> --confirm --by <name>`, or `controller.py knowledge bind --root <project-root> --none --reason <reason> --confirm --by <name>`.
8. If a valid knowledge-base binding already exists, do not ask again.
9. Run `controller.py status --root <project-root>`.
10. Complete context intake confirmation.
11. Complete the first-circle analysis bundle with `pm-requirement-analysis` and `pm-metrics-definition`.
12. Work only on `current_stage`.
13. If `.pm-flow/project_config.json` exists, use its artifact paths.

## Workspace Rules

- The human provides the workspace location; the human does not need to reshape existing folders for the plugin.
- The plugin may create `.pm-flow/`, `.pm-flow/work/`, and mapped artifacts. It must not rearrange existing human-owned information.
- If the human asks to change the workspace, run `controller.py workspace rebind --root <new-root> --confirm --by <name>`.
- If the current `--root` differs from the confirmed binding, stop work and clarify the workspace structure before continuing.

## Knowledge-Base Rules

- The human confirms the knowledge-base boundary; the agent reads selected sources inside that boundary.
- The plugin records the binding in `.pm-flow/project_config.json`; it does not store company knowledge inside the plugin.
- If the human asks to change the knowledge-base path, run `controller.py knowledge rebind --root <project-root> --knowledge-root <new-root> --confirm --by <name>`.
- If no external knowledge base is used, run `controller.py knowledge bind --root <project-root> --none --reason <reason> --confirm --by <name>`.
- If the knowledge-base root, manifest, or confirmed source list is missing, moved, or inconsistent, stop work and clarify the knowledge-base boundary before continuing.

## Internal Routing

- Global preflight: use `pm-context-contract`, `pm-requirement-analysis`, and `pm-metrics-definition`.
- Research: use `pm-research` to produce research-stage opportunity, user, market, competitor, benchmark, metric-context, source-risk, assumption, and open-question artifacts.
- Boundary: use `pm-boundary` to produce scope, non-scope, stakeholders, roles, permissions, surfaces, system ownership, constraints, dependencies, assumptions, risks, and decisions.
- Prototype: use `pm-html-prototype` when HTML prototype output is needed.
- Prototype review: use `pm-prototype-review` only when a separate review artifact is needed.
- PRD: use `pm-prd` for PRD sizing, field dictionary, and acceptance criteria.
- Review: use `pm-review` for the general review stage and readiness conclusion.
- Diagram: use `pm-mermaid-diagram` for standalone Mermaid files.
- Polish: use `humanizer` only after facts, scope, and acceptance criteria are stable.

## Advancement Rule

Every stage advances in this order:

```text
confirm -> mark -> close --checked -> validate
```

Before closing a stage, review every semantic check in `contract_config.json`. If a check does not apply, record the reason in the stage artifact or decision log.

## Forbidden

- Do not start product work without a confirmed workspace root.
- Do not ask for workspace location again when the binding is valid.
- Do not continue after a workspace mismatch without human-approved rebind.
- Do not start product work without a confirmed knowledge-base boundary or explicit no-knowledge-base decision.
- Do not ask for the knowledge-base path again when the binding is valid.
- Do not continue after a knowledge-base mismatch without human-approved rebind.
- Do not restructure existing human-owned folders during plugin setup.
- Do not write a PRD before checking `status`.
- Do not infer the current stage from chat history.
- Do not skip context confirmation.
- Do not skip requirement analysis, metrics definition, scenario catalog, use cases, end-to-end flow, or artifact planning.
- Do not advance without artifacts.
- Do not close without semantic checks.
- Do not read the whole knowledge base by default.
- Do not write assumptions as facts.
- Do not use package-external abilities by default.
- Do not use `humanizer` to change facts, scope, rules, or acceptance criteria.
