# Context Contract

A context contract tells an agent what it may read, what it must cite, what it must ignore, and how to handle conflicts.

## Manifest Fields

- Purpose: what the knowledge base is for.
- Scope: company, product line, project, domain, or design system.
- Required sources: files that must be read before work starts.
- Conditional sources: files to read only for specific stages or domains.
- Excluded sources: archived, obsolete, draft, or non-authoritative files.
- Rule strength: MUST, SHOULD, MAY, FORBIDDEN.
- Conflict policy: how to handle disagreement between sources.
- Owner: person or team responsible for updates.

## Intake Fields

- Project name.
- Requirement name.
- Requirement type.
- Background.
- Target users.
- Trigger scenario.
- Current process.
- Current problem.
- Expected result.
- Scope and non-scope.
- Client surfaces.
- Roles.
- Known constraints.
- Required sources.
- Terms.
- Known conflicts.
- Success criteria.
- Deliverable requirements.
- Assumptions and open questions.

## Conflict Handling

When sources conflict:

1. Prefer the newest authoritative source when ownership is clear.
2. Prefer MUST rules over SHOULD or MAY rules.
3. Prefer project-specific rules over generic rules only inside that project.
4. Record unresolved conflicts before advancing a stage.
5. Do not hide conflicts in generated PRDs or prototypes.
