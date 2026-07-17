# Diagram Guidelines

Keep diagrams outside the PRD body. The PRD should link to standalone diagram files and summarize why each diagram exists.

## Default Location

```text
product/04-diagrams/
```

## Naming

| Need | Suggested file |
|---|---|
| Main workflow | `main-flow.mmd` |
| Swimlane process | `swimlane-flow.mmd` |
| State machine | `state-machine.mmd` |
| System sequence | `sequence.mmd` |
| Architecture relation | `architecture.mmd` |

## Rules

- Use Mermaid syntax.
- Add stable IDs for steps when they must map to scenarios or requirements.
- Do not duplicate a full diagram inside PRD prose.
- If a diagram is not needed, record the non-applicability reason in the PRD.
