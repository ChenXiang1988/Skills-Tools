# Analysis Routing

Use requirement analysis to decide which downstream artifacts are needed.

## Routing Questions

- Is a PRD needed?
- Is the PRD L1, L2, or L3?
- Are success, input, and guardrail metrics needed?
- Are use cases needed?
- Is end-to-end flow coverage needed?
- Are field definitions, data sources, permissions, or write-back behavior important enough to require `field-dictionary.md`?
- Are acceptance criteria complex enough to require `acceptance-criteria.md`?
- Is an HTML prototype needed?
- Is a separate prototype review artifact needed?
- Are Mermaid diagrams needed?
- Are test scenarios or delivery checks needed?
- Is final prose polishing needed?

## Default Routing

- PRD: use `pm-prd`.
- Metrics definition: use `pm-metrics-definition`.
- HTML prototype: use `pm-html-prototype`.
- Prototype review artifact: use `pm-prototype-review` only when needed.
- Diagrams: use `pm-mermaid-diagram`.
- Polishing: use `humanizer` after facts are stable.
