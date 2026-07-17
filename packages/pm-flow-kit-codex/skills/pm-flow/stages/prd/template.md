# {Requirement Name} - PRD Stage Entry

Copy this template to the project root as `prd.md`. `pm-flow` owns the stage gate. `pm-prd` owns PRD sizing, template selection, and PRD content.

## Context References

- Sources read for this stage:
- Applicable rules:
- Conflicts found:
- Stage assumptions:
- No-context reason, if applicable:

## PRD Level Decision

Use `pm-prd/references/prd-sizing.md` before writing the body.

- PRD level: L1 / L2 / L3
- Decision rationale:
  - Scope:
  - Affected roles and client surfaces:
  - State, permission, money, inventory, fulfillment, or data impact:
  - Cross-system or cross-team impact:
  - Risk and uncertainty:
- Template selected:

## Requirement Summary

- Background:
- Goal:
- Scope:
- Explicit non-scope:
- Success criteria:
- Metrics referenced:
- Scenario catalog referenced:
- Use cases referenced:
- End-to-end flow referenced:

## PRD Body

Paste the selected L1, L2, or L3 template body here. Do not mix templates. If complexity changes, update the PRD level decision first.

## Key Decisions

Record each key decision with `controller.py decide <stage> --text "..."`.

- Decision 1:
- Decision 2:

## Close Checklist

- [ ] pm-prd was used for PRD sizing and template selection.
- [ ] PRD level and rationale are explicit.
- [ ] The PRD satisfies the required sections for its level.
- [ ] Terminology and roles are aligned to project sources when they exist.
- [ ] Client surfaces and system ownership are explicit.
- [ ] Metrics definition, scenario catalog, use cases, and end-to-end flow are referenced or marked not applicable.
- [ ] Acceptance criteria and exception flows are included.
- [ ] Required diagrams, field dictionary, and acceptance criteria are produced as companion artifacts.
- [ ] Open questions are not written as facts.
- [ ] Key decisions are recorded in state.json.decisions.
