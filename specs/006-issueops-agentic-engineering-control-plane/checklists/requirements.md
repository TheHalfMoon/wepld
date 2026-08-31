# Requirements Checklist — Spec 006 Planning Candidate

```text
STATUS = READY_FOR_PLANNING_REVIEW
IMPLEMENTATION_AUTHORITY = NONE
```

## Scope integrity

- [x] Future planning only; current S2 scope unchanged.
- [x] P0 + S1..S10 numbering preserved.
- [x] No source/dependency/runtime/provider/network/Git/issue-write admission is claimed.
- [x] GitHub-first design does not make GitHub the core domain model.

## User intent coverage

- [x] Agentic automated issue operations are a primary product outcome.
- [x] GitHub Issues/PRs are first-class provider targets.
- [x] Additional issue/ticket/error providers have a stable adapter seam.
- [x] `/rag` supports arbitrary qualified user-selected sources.
- [x] CLI/Desktop drag/drop/path-paste intake is planned.
- [x] Matt skills study is fully represented and adapted to WePLD-native commands/primitives.
- [x] delegate-skills study is fully represented and adapted to provider-neutral delegation.

## Architecture integrity

- [x] Case/provider state separation is explicit.
- [x] Retrieval/truth separation is explicit.
- [x] Worker selection/qualification/authorization separation is explicit.
- [x] Autonomy ceiling/authorization separation is explicit.
- [x] Merge/closeout/Trusted Completion separation is explicit.
- [x] Drop/paste/execution separation is explicit.
- [x] No silent fallback or silent paid/quota execution is permitted.

## Delivery integrity

- [x] Capabilities are mapped to existing owning slices.
- [x] The plan uses incremental tracer bullets.
- [x] Read-only and prepare paths precede autonomous landing.
- [x] External writes require exact-target/idempotency semantics.
- [x] Required negative oracles are listed.
- [x] Future activation requires canonical build-method gates.

## Remaining review work

- [ ] Exact-head deterministic repository checks.
- [ ] Independent planning/correctness review.
- [ ] Reconciliation of all material findings.
- [ ] Final exact-head/race check before any authorized merge.
