# Diagram Patterns

## Selection Discipline

Choose one purpose per diagram file:

- Process or user task flow -> flowchart.
- Role, team, system, or client-surface handoff -> swimlane-style flowchart with subgraphs.
- Status lifecycle -> state diagram.
- Time-ordered system or actor interaction -> sequence diagram.
- System relationship -> architecture diagram.
- Feature or concept breakdown -> mind map.

Split the output when the request mixes product flow, state lifecycle, API sequence, data model, roadmap, or delivery plan. Do not create a dense all-in-one diagram.

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

Use real actors, teams, systems, or client surfaces as lanes. Avoid vague lanes such as "Product", "Tech", or "Operation" unless the source material explicitly defines those as responsible actors.

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
