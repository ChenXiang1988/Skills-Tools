---
name: pm-context-contract
description: Define and validate context contracts for product work. Use when
  you need to organize domain rules, knowledge-base entry points,
  CONTEXT_MANIFEST.md, intake.md, source constraints, rule strength, conflict
  handling, and scoped context reading before PM workflow output.
disable: true
---

# PM Context Contract

## Capability Boundary

Define the context contract for product work. Use it to decide what the agent may read, must cite, must ignore, and must not treat as authoritative.

Do not use this skill to write PRDs, prototypes, diagrams, or review artifacts. Do not read an entire knowledge base by default.

## Required Inputs

- Product requirement or intake.
- Knowledge-base root, manifest, index, or specific source files when available.
- Project, company, or workspace identity when multiple companies or projects exist.

If no knowledge base exists, record that explicitly and continue with assumptions. Stop when sources conflict on a MUST or FORBIDDEN rule and no owner decision is available.

## Output Contract

- `CONTEXT_MANIFEST.md` when a reusable knowledge-base entry point is needed.
- `intake.md` when a requirement input file is needed.
- `context_confirmation.md` when the current pm-flow run must confirm which context was used.

Each output must separate applicable sources, non-applicable sources, rule strength, conflicts, confidence, and citation conclusions.

## Failure Cases

- Bad input: only a broad folder is provided and no manifest, index, owner, or project scope exists.
- Wrong use: reading all files to "be safe" instead of selecting scoped sources.
- Bad output: conflicts are hidden, or outdated material is treated as current.
- Bad output: sources from another company or project are mixed into the current requirement.
- Blocking gap: a MUST/FORBIDDEN conflict affects PRD, prototype, metrics, or acceptance criteria.

## Handoff Rules

- Use `pm-requirement-analysis` after context is confirmed.
- Use `pm-html-prototype` when confirmed sources include design guidelines, component library, frontend framework, or font constraints.
- Use `pm-prd` when confirmed sources constrain fields, permissions, data sources, or acceptance criteria.

## Resources

- Use `references/context-contract.md` for the contract model.
- Use `assets/templates/context-manifest.md` for a knowledge-base manifest.
- Use `assets/templates/intake.md` for requirement intake.
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
