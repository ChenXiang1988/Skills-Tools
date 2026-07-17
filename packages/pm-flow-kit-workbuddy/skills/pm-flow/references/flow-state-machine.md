# Flow State Machine

Each stage moves through:

```text
todo -> confirmed -> done -> closed
```

Rules:

- `confirm` means the stage output is ready to work on.
- `mark` checks required artifacts and marks the stage done.
- `close --checked` locks the stage after semantic checks.
- Previous stages must be closed before a later stage can be marked done.
- Global preflight blocks all stage advancement until context confirmation and requirement analysis are confirmed.
