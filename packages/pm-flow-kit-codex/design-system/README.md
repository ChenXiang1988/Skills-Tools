# PM Flow Kit Design System

This is the generic bundled design system for offline HTML prototypes.

It is intentionally domain-neutral. Project-specific design systems can override
it by placing a `design-system/` directory at the project workspace root.

## Files

| File | Purpose |
|---|---|
| `tokens.css` | Generic Web tokens and CSS variables. |
| `DESIGN.md` | Usage rules for agents creating HTML prototypes. |
| `components.html` | Copyable HTML component snippets using `.pf-*` classes. |
| `pda/tokens.css` | Optional PDA/mobile token extension. |
| `pda/DESIGN.md` | PDA/mobile usage rules. |
| `pda/components.html` | PDA/mobile component snippets. |
| `PROVENANCE.md` | Source and override policy. |

## Use

`pm-flow scaffold` snapshots the selected design system into:

```text
prototypes/assets/design-system/
```

Selection order:

1. `PM_FLOW_DESIGN_SYSTEM` when set.
2. `<project-root>/design-system` when present.
3. `<project-root>/.pm-flow/design-system` when present.
4. This bundled `design-system/`.

The generated prototype should reference `assets/design-system/tokens.css`
before prototype layout CSS.
