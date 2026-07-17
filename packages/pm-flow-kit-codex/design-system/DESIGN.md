# Generic Code-First Design Rules

This guide is for agents creating offline HTML prototypes.

## Principles

- Prioritize clarity, traceability, and reviewability over decoration.
- Use design tokens from `tokens.css`; avoid hard-coded colors, spacing, and
  radii when a token exists.
- Keep prototypes offline-openable. Do not depend on CDNs, remote fonts, remote
  icons, or production APIs.
- Treat this as a neutral fallback. If the project provides a design system,
  use the project design system instead.

## Token Rules

- Load `assets/design-system/tokens.css` before prototype CSS.
- Use semantic variables such as `--color-primary`, `--color-success`,
  `--color-warning`, `--color-error`, `--color-bg-container`, and
  `--color-text`.
- Use spacing variables such as `--space-2`, `--space-3`, `--space-4`,
  `--space-6`, and `--space-8`.
- Use `font-variant-numeric: tabular-nums` for tables, metrics, quantities, and
  KPI cards.

## Components

Use simple HTML/CSS components for prototypes:

- Buttons: one primary action per section.
- Forms: labels are explicit; required or invalid state is visible.
- Tables: numeric columns are right aligned; status is represented by tags.
- Cards: one main concept per card.
- Empty, loading, error, permission, timeout, duplicate-action, and concurrent
  states must be shown when scenarios or acceptance criteria require them.

## Do Not

- Do not force Ant Design unless the project asks for it.
- Do not introduce business-domain colors or status names into the generic kit.
- Do not use decorative gradients as substitutes for product state.
- Do not hide unresolved requirements behind polished visual treatment.
