---
name: pm-mermaid-diagram
description: Generate standalone Mermaid diagrams for product management work. Use when Codex needs to turn requirement analysis, scenario catalogs, use cases, PRDs, or product flows into flowcharts, swimlane-style flows, state diagrams, sequence diagrams, architecture diagrams, mind maps, or standalone `.mmd` diagram files with artifact routing and bad-output checks.
---

# PM Mermaid Diagram

## Capability Boundary

Create product diagrams as standalone Mermaid files. Keep diagrams outside the PRD unless the user explicitly asks for inline Mermaid.

Do not use this skill to write PRDs, invent process steps, create production architecture, or replace scenario analysis.

## Required Inputs

- Requirement analysis, scenario catalog, use cases, PRD, or a clear text flow.
- Diagram purpose: user flow, swimlane, state transition, sequence, architecture, or concept map.
- Workspace diagram directory standard, if one exists.

Stop and ask for clarification when the actors, states, systems, or branch rules are too vague to draw without inventing meaning.

Stop when the request asks for one diagram to combine unrelated purposes such as product flow, data model, deployment, roadmap, and review decisions.

## Output Contract

- Suggested file path, normally under `product/04-diagrams/`.
- Mermaid code block.
- Short note explaining what the diagram covers.
- Source mapping back to scenario IDs, use case IDs, requirement IDs, or PRD sections when available.

## Diagram Selection

- Flowchart: process, decision branches, or user task flow.
- Swimlane-style flowchart: roles, teams, or systems crossing a process.
- State diagram: status lifecycle and transitions.
- Sequence diagram: interactions over time.
- Architecture diagram: system relationships.
- Mind map: concept breakdown.

Choose one primary purpose per diagram file. Split diagrams when a single output would mix user flow, state lifecycle, system interaction, data relationship, roadmap, or delivery plan.

## Failure Cases

- Bad input: "draw the process" without actors, trigger, steps, or system response.
- Wrong use: using a diagram to hide missing requirements, fields, permissions, or business rules.
- Bad output: a dense all-in-one diagram that cannot be traced to scenarios or use cases.
- Bad output: swimlanes named by vague departments when the actual actors are users, systems, or client surfaces.
- Bad output: diagram type is selected by habit instead of purpose.
- Bad output: product flow, state model, API sequence, architecture, and delivery roadmap are merged into one chart.
- Bad output: full Mermaid bodies embedded into the PRD when a standalone diagram file is required.

## Handoff Rules

- Use `pm-requirement-analysis` first when scenarios, actors, or branches are missing.
- Use `pm-prd` when the requested output is a requirement document, not a diagram.
- Use `pm-html-prototype` when the user needs inspectable UI screens.
- Use `pm-prototype-review` only when a separate review artifact is needed.

## Resources

- Diagram patterns: `references/diagram-patterns.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
