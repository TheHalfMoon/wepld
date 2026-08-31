# Spec 006 Constitution — IssueOps Agentic Engineering Control Plane

```text
STATUS = FUTURE_PLANNING_CANDIDATE
CANONICAL_BASE = 573670eca575a5972e52b623b01b3143d036d281
CURRENT_ACTIVE_SLICE = S2
ROADMAP = P0 + S1..S10
ROADMAP_REMAP = NONE
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
NETWORK_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION_AUTHORITY = NONE
GIT_WRITE_AUTHORITY = NONE
ISSUE_PROVIDER_WRITE_AUTHORITY = NONE
```

## Purpose

This specification plans a future WePLD-native control plane for issue operations, arbitrary RAG, CLI/Desktop artifact intake, workflow skills, and governed multi-agent delegation. It does not activate any future slice or alter the active S2 authority chain.

## Inherited authority

All canonical repository governance at the exact trusted base remains controlling, especially:

- `AGENTS.md`
- `docs/canonical/ARCHITECTURE_INVARIANTS.md`
- `docs/canonical/BUILD_METHOD.md`
- `docs/canonical/SECURITY_REVIEW_POLICY.md`
- `docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md`
- `docs/canonical/MASTER_PLAN_INDEX.md`
- `docs/canonical/MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md`
- `docs/acquisition/SOURCE_REGISTRY_INDEX.md`

Candidate text never creates authority.

## Non-negotiable invariants

```text
CASE_STATE != PROVIDER_STATE
ISSUE_PROVIDER_PERMISSION != NAWAT_GRANT
AUTONOMY_LEVEL != UNBOUNDED_AUTHORITY
DROP_EVENT != EXECUTION_AUTHORITY
ATTACHMENT != TRUSTED_CONTENT
RAG_RESULT != TRUTH
RETRIEVAL_SCORE != TRUTH
CITATION != AUTHORITY
WORKER_SELECTION != AUTHORIZATION
REMOTE_AGENT_IDENTITY != TRUST
PROVIDER_SESSION_ID != WEPLD_SESSION_ID
MODEL_REVIEW != COMPLETION_DECISION
GREEN_CI != COMPLETION_DECISION
MERGE != TRUSTED_COMPLETION
CLOSE_ISSUE != TRUSTED_COMPLETION
NO_SILENT_PROVIDER_MODEL_WORKER_FALLBACK = REQUIRED
PAID_OR_METERED_EXECUTION_WITHOUT_EXPLICIT_AUTHORITY = DENIED
```

## Design principles

1. GitHub is the first-class issue provider, not the internal data model.
2. WePLD owns the durable `Case` model, evidence timeline, session identity, workflow state, authority boundaries, and completion semantics.
3. External issue systems, model providers, coding agents, RAG engines, and protocol SDKs remain adapters behind WePLD-owned contracts.
4. User-facing workflow names are WePLD-native. Donor branding is not the product surface.
5. Human attention is reserved for real decision boundaries, policy approvals, unresolved ambiguity, and residual risk—not routine agent mechanics.
6. Read, prepare, execute, land, and close effects are separately qualified and authorized.
7. Dropped or pasted content is inert input until an explicit governed action consumes it.
8. Retrieval must be provenance-first, freshness-aware, inspectable, and fail closed when required evidence is stale or missing.
9. Automation must be replayable, interruptible, idempotent where externally observable, and safe under duplicate delivery/retry.
10. Every material autonomous case must end with inspectable completion evidence, not merely a green provider status.
