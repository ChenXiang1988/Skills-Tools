---
name: pm-html-prototype
description: Generate offline HTML product prototypes with local assets, device
  frames, design-token usage, font constraints, component-library mapping, and
  self-checks. Use when you need to create inspectable HTML prototypes from
  PRDs, scenario catalogs, design guidelines, or product requirements.
disable: true
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
- Design guidelines, component-library rules, frontend framework rules, and font constraints from the knowledge base when available. The kit provides a **code-first design system at `design-system/`** (Ant Design based) — use it as the single token source for every prototype; it is the preferred source when the project is 云仓 (WMS/OMS/TMS/BMS) or Ant Design based, but `pm-html-prototype` stays usable for any project. See the "Design System" section.

Stop when the target user action, client surface, page/module, field list, or core system response is missing.

## Output Contract

Create or update files under the project prototype directory, usually `prototypes/` or the path configured by `.pm-flow/project_config.json`.

The scaffold includes:

- Local CSS and JavaScript.
- Desktop and mobile shells.
- Device-frame support.
- DingTalk JinBuTi font asset.
- Prototype validator.

## Design System (single source of truth)

The prototype consumes the kit's **code-first design system at `design-system/`** as its only token source — it does **not** bundle its own token set. `design-system/` is Ant Design based and a natural fit for 云仓 (WMS/OMS/TMS/BMS) and Ant Design projects, and `pm-html-prototype` stays usable for any project.

- **Web (Ant Design v5 base)**: `design-system/tokens.css` (light/dark CSS vars) + `design-system/components.html` (17 P0 components, copy-paste `.yc-*` snippets) + spec `design-system/DESIGN.md` (§9 component index).
- **PDA (antd-mobile base)**: `design-system/pda/tokens.css` + `design-system/pda/components.html` + `design-system/pda/DESIGN.md`.

**How scaffolding wires it**: `pm-flow scaffold` copies `design-system/` into each prototype as `prototypes/assets/design-system/` (a snapshot, so the prototype stays self-contained and offline-openable). The prototype's own `prototype-chrome.css` holds **layout/component styling only** and resolves every color, spacing, radius, and font from `design-system/tokens.css` via CSS variables. There is no second token source to mix — every prototype uses the same design system.

See `design-system/PROVENANCE.md` for internal-use scope and snapshot-sync notes.

## Failure Cases

- Bad input: no scenario names a page, module, client surface, or user action.
- Wrong use: using this skill to implement production app code.
- Bad output: prototype depends on CDN resources or external fonts.
- Bad output: fields cannot be traced to PRD, field dictionary, use case, or scenario.
- Bad output: component-library API behavior is claimed without source verification.
- Bad output: design guidelines exist but are ignored.

## Handoff Rules

- Use `pm-requirement-analysis` when scenario or use case coverage is incomplete.
- Use `pm-prd` when fields, rules, or acceptance criteria are not stable.
- Use `pm-prototype-review` only if the artifact plan requires a separate review artifact.
- Use `pm-context-contract` when design, component, frontend, or font constraints must be confirmed.

## Resources

- Scaffold assets: `assets/scaffold/`
- Design system (single token source): `../../design-system/` (Web + PDA; copied into each prototype as `prototypes/assets/design-system/` by `pm-flow scaffold`)
- Component mapping notes: `references/ant-design-adapter.md`
- Shared error taxonomy: `../../references/pm-shared/error-taxonomy.md`
- Bad-output examples: `../../references/pm-shared/bad-output-examples.md`
