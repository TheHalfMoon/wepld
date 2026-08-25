# Source Acquisition — Spec 004

## Decision

No new external source acquisition is required for the canonicalization bootstrap.

```text
EXTERNAL_SOURCE_ACQUISITION = NOT_REQUIRED
DONOR_SOURCE_IMPORT = NONE
DEPENDENCY_ACQUISITION = NONE
RUNTIME_ACQUISITION = NONE
MODEL_PROVIDER_ACQUISITION = NONE
```

## Reuse source

The work reuses only already-canonical WePLD-owned policy machinery and the already-merged V2.3 planning candidate:

- `.github/scripts/wepld_integrity.py` — trusted base-controlled core policy;
- `.github/scripts/wepld_s1_admission_steady_state_routing_v4_integrity.py` — exact predecessor for the successor wrapper;
- `.github/workflows/foundation-integrity.yml`;
- `.github/workflows/s1-admission-integrity.yml`;
- `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md` — qualified planning input, not authority until canonicalized;
- `docs/canonical/MASTER_PLAN_INDEX.md` — current base-controlled V2.2 authority index.

## Acquisition-style checks still required

Although no donor is acquired, the successor policy must treat its predecessor and canonicalization input as content-addressed inputs:
- exact predecessor policy Git blob identity;
- exact predecessor workflow SHA-256 identities;
- exact V2.3 candidate Git blob identity;
- exact trusted-base V2.2 index identity/content precondition;
- deterministic transformation into canonical V2.3 bytes;
- exact two-path canonicalization delta;
- fail-closed rejection if any identity drifts.

Future S4-G/S6-AH/S6-N/S7-S/S9-P path-level source acquisition remains capability-triggered and out of scope here.
