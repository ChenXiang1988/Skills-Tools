# Diagram Patterns

## Flowchart

Use for steps and decisions.

```mermaid
flowchart TD
  A[Start] --> B{Decision}
  B -->|Yes| C[Action]
  B -->|No| D[Fallback]
```

## Swimlane-Style Flow

Mermaid does not have a native swimlane primitive. Use subgraphs for lanes.

```mermaid
flowchart LR
  subgraph User
    U1[Submit request]
  end
  subgraph System
    S1[Validate]
  end
  U1 --> S1
```

## State Diagram

Use for lifecycle transitions.

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Submitted
  Submitted --> Approved
  Submitted --> Rejected
```

## Sequence Diagram

Use for time-ordered interactions.

```mermaid
sequenceDiagram
  participant User
  participant App
  User->>App: Submit
  App-->>User: Result
```
