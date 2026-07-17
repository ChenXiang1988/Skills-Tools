---
name: pm-html-prototype
description: Generate offline HTML product prototypes with local assets, device frames, design-token usage, font constraints, component-library mapping, and self-checks. Use when Codex needs to create inspectable HTML prototypes from PRDs, scenario catalogs, design guidelines, or product requirements.
---

# PM HTML Prototype

## Capability Boundary

Create inspectable offline HTML prototypes for product review and requirement validation.

Do not produce production React, Ant Design, backend, API, or deployable application code. Do not create prototype review artifacts.

## Required Inputs

- Requirement analysis.
- Metrics definition when UI behavior is tied to measurable outcomes.
- Scenario catalog.
- Use cases and end-to-end flow when available.
- Artifact plan.
- PRD or draft requirement details.
- Design guidelines, component-library rules, frontend framework rules, and font constraints from the knowledge base when available.
- Design-system source. Prefer a project workspace `design-system/` directory when present; otherwise use the bundled generic `design-system/` shipped with pm-flow-kit.

Stop when the target user action, client surface, page/module, field list, or core system response is missing.

Stop when the artifact plan requires offline review but the available design or component approach depends on CDN, remote fonts, remote icons, or production APIs.

## Output Contract

Create or update files under the project prototype directory, usually `prototypes/` or the path configured by `.pm-flow/project_config.json`.

The scaffold includes:

- A snapshot of the selected design system under `prototypes/assets/design-system/`.
- Local CSS and JavaScript.
- Desktop and mobile shells.
- Device-frame support.
- DingTalk JinBuTi font asset.
- Prototype validator.

## Design System Source Order

Use the first available source:

1. `PM_FLOW_DESIGN_SYSTEM` environment variable.
2. `<project-root>/design-system`.
3. `<project-root>/.pm-flow/design-system`.
4. The bundled generic `design-system/` in pm-flow-kit.

The selected source must include `tokens.css`. Generated HTML must reference
`assets/design-system/tokens.css` before prototype layout CSS. The bundled
generic design system is a neutral fallback; project or knowledge-base design
guidelines override it.

## Failure Cases

- Bad input: no scenario names a page, module, client surface, or user action.
- Wrong use: using this skill to implement production app code.
- Bad output: prototype depends on CDN resources or external fonts.
- Bad output: Tailwind, icon libraries, component libraries, or fonts are referenced from remote URLs when offline output is required.
- Bad output: fields cannot be traced to PRD, field dictionary, use case, or scenario.
- Bad output: loading, empty, error, permission, timeout, duplicate-action, or concurrent-state screens are omitted when scenarios or acceptance criteria require them.
- Bad output: component-library API behavior is claimed without source verification.
- Bad output: design guidelines exist but are ignored.
- Bad output: prototype does not snapshot or reference the selected design system.

## Handoff Rules

- Use `pm-requirement-analysis` when scenario or use case coverage is incomplete.
- Use `pm-prd` when fields, rules, or acceptance criteria are not stable.
- Use `pm-prototype-review` only if the artifact plan requires a separate review artifact.
- Use `pm-context-contract` when design, component, frontend, or font constraints must be confirmed.

## Resources

- Scaffold assets: `assets/scaffold/`
- Bundled generic design system: `../../design-system/`
- Component mapping notes: `references/ant-design-adapter.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
