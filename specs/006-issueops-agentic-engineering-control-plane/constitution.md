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
EXTERNAL_CONTENT != INSTRUCTION_AUTHORITY
CONTENT_INSTRUCTION != USER_OR_POLICY_INTENT
RETRIEVED_TEXT != TOOL_INTENT
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
UNTRUSTED_CONTENT_CANNOT_EXPAND_EFFECTS = REQUIRED
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
11. Architecture boundaries are semantic trust/ownership boundaries, not mandatory deployment units; early tracer bullets may co-locate components in one process while preserving distinct inputs, outputs, failure states, and authority semantics.

## Untrusted-content / prompt-injection boundary

Issue bodies, comments, PR descriptions, code, logs, documents, retrieved passages, provider attachments, web content, repository text, worker output, and model output are **data by default**. Their presence in context does not promote embedded instructions into user intent, policy, authority, tool intent, or workflow control.

Future implementations that consume untrusted content MUST establish all of the following before any effect-capable agent route is qualified:

1. **Origin labeling** — every context fragment retains source identity, trust classification, and provenance sufficient to distinguish user/policy instructions from external data.
2. **Instruction/data separation** — untrusted source text is delivered through structured data/context envelopes, not concatenated as controlling system/policy instructions.
3. **Intent derivation** — effect proposals derive from an explicit `WorkflowIntent`, Assignment, or controlling policy. An instruction found only inside untrusted content cannot create or broaden an effect request.
4. **Least-context packaging** — workers receive the minimum sufficient evidence. Secrets, unrelated files, credentials, and unrelated collections are excluded unless independently required and authorized.
5. **Independent effect validation** — every material tool/process/network/provider/filesystem/Git effect is validated against exact target, effect class, current evidence, qualification, containment preconditions, and Nawat authority at effect time. Prompt sanitization alone is never a security boundary.
6. **No authority laundering** — quoted text, retrieved instructions, generated scripts, model recommendations, provider metadata, and review text cannot mint permissions, change autonomy ceilings, disable containment, select a paid route, or bypass review.
7. **Parser and active-content isolation** — parsers for archives/documents/repositories and any active-content expansion are separately qualified; unsupported, recursive, over-limit, malformed, or unsafe payloads fail closed.
8. **Egress control** — local attachment or collection membership never authorizes transmission to a remote model, embedding, retrieval, worker, or provider.
9. **Auditability** — context-package manifests record which untrusted sources were shown to which worker and which evidence contributed to any proposed effect.
10. **Adversarial qualification** — owning slices maintain negative-oracle corpora containing direct prompt injection, indirect RAG injection, tool-call coercion, fake policy text, fake reviewer commands, credential requests, encoded/obfuscated instructions, and cross-source instruction conflicts.

Minimum required negative oracles include:

```text
MALICIOUS_ISSUE_TEXT_CANNOT_CREATE_EFFECT
MALICIOUS_RAG_TEXT_CANNOT_EXPAND_EFFECT_SCOPE
FAKE_POLICY_IN_CONTENT_CANNOT_OVERRIDE_CANONICAL_POLICY
UNTRUSTED_TEXT_CANNOT_SELECT_PAID_OR_REMOTE_ROUTE
UNTRUSTED_TEXT_CANNOT_REQUEST_UNRELATED_SECRET_OR_FILE_ACCESS
MODEL_OR_WORKER_OUTPUT_CANNOT_SELF_AUTHORIZE_FOLLOW_ON_EFFECT
SANITIZATION_FAILURE_STILL_MEETS_EFFECT_TIME_DENIAL_BOUNDARY
```

The owning implementation may use sanitization, quoting, content filtering, model-side defenses, or prompt-injection classifiers as additional evidence. None of those mechanisms substitutes for structural authority and effect-time enforcement.
