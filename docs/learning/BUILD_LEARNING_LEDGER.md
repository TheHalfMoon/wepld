# WePLD Build Learning Ledger

This ledger starts with the fresh reconstitution. It is append-only by new records; corrections supersede earlier records rather than erasing history.

| Learning ID | Date | Tool/source | Pin/version | Context | Class | Observation | WePLD candidate impact | Status |
|---|---|---|---|---|---|---|---|---|
| `BL-0001` | 2026-08-14 | Continue | `continuedev/continue@5522c6f44ca0ac3528b37244818fbfa39b5af470` | Build protocol source review | POSITIVE_MECHANISM | Version-controlled rules/checks and explicit Chat/Plan/Agent modes provide useful separation of instructions and tool availability. | UWC/AGILLE/Assurance behavior oracle; source-controlled check pattern. | OBSERVED |
| `BL-0002` | 2026-08-14 | Continue | same | Build protocol source review | NEGATIVE_ORACLE | Tool policy can be configured Automatic; an agent-mode UI policy is not a WePLD authority grant. | Nawat test: tool automatic setting must never bypass exact effect grant. | OBSERVED |
| `BL-0003` | 2026-08-14 | Continue | same | Source acquisition | MAINTENANCE_EVIDENCE | Current README states the upstream repo is no longer actively maintained and calls 2.0.0 the final release. | Mine source/tests now, but avoid non-replaceable foundation dependency without explicit maintenance/exit decision. | OBSERVED |
