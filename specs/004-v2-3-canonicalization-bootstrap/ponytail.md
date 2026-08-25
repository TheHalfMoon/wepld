# Ponytail FULL — Spec 004

## Question

What is the minimum sufficient mechanism for canonicalizing the already-qualified V2.3 planning candidate without weakening base-controlled governance?

## Decision

Use a two-event transition:

```text
EVENT_A = exact successor policy bootstrap
EVENT_B = exact V2.3 canonicalization
```

Rejected alternatives:

1. Directly edit `MASTER_PLAN_INDEX.md` under v4 — rejected because the trusted base correctly forbids it.
2. Make `MASTER_PLAN_INDEX.md` generally mutable — rejected as excessive authority expansion.
3. Reopen or rewrite V2.2 frozen artifacts — rejected because V2.2 remains immutable historical/canonical evidence.
4. Entangle source admission or active Pictorial/Agile PRs — rejected as unrelated and authority-expanding.
5. Make a broad “governance changes allowed” policy route — rejected because it destroys exact-transition safety.
6. Treat standing founder authorization as CI PASS — rejected; authority does not replace qualification.

## Minimum v5 responsibilities

- bind v4 predecessor bytes;
- bootstrap only itself plus the two workflows that select it;
- inherit v4 behavior for all other routes;
- recognize one exact V2.3 canonicalization delta after activation;
- derive allowed canonical bytes from the exact trusted-base V2.3 candidate;
- require exact index bytes tied to the derived canonical plan digest;
- include fail-closed negative tests for extra paths, candidate drift, arbitrary canonical-plan bytes, index drift, roadmap renumbering, source/dependency/runtime/model authority expansion, and reuse of the canonicalization route after it is consumed.

No new dependency, service, runtime, protocol, storage engine, source donor, or external package is required.
