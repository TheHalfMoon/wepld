# Ponytail FULL — IssueOps Agentic Engineering Control Plane

```text
STATUS = COMPLETE_FOR_PLANNING_ONLY
IMPLEMENTATION_AUTHORITY = NONE
SOURCE_ADMISSION = NONE
```

## Core sufficiency questions

### Does WePLD need a new issue abstraction?

Yes, but only one provider-neutral `Case` abstraction. Provider-native issue/PR objects remain bindings. Do not create separate core models for GitHub, Linear, Jira, Sentry, or future providers.

### Does WePLD need a separate “agent team framework”?

No. Use the existing V2.3 architecture: Edara for topology, Mirefa for qualification, Nawat for effect-time authority, Mission Runtime for execution, and UWC for worker/protocol normalization.

### Does WePLD need one slash command per donor skill?

No. Expose durable user intents as commands and keep reusable engineering methods as internal capabilities.

### Does WePLD need one delegate command per provider?

No. `/delegate` + `/workers` is the stable product surface. Provider-specific adapters remain behind UWC/Mission Runtime.

### Does `/rag` require a vector database on day one?

No. Exact, lexical, metadata, and future Fehrest graph retrieval should come first. Vector/embedding machinery is optional and separately acquired only if it proves incremental value.

### Does drag/drop need terminal-specific core logic?

No. Normalize native drop events and path-paste/bracketed-paste observations into one `InputArtifact` contract. Terminal-specific parsing remains an adapter detail.

### Does IssueOps need its own authorization system?

No. Nawat remains the only effect-time authority. Issue provider permissions and autonomy profiles are inputs/ceilings, not grants.

### Does IssueOps need its own evidence database?

No. Build on the local evidence-store foundation and later Work/Fehrest timeline contracts rather than a parallel persistence silo.

### Does a merged PR mean a Case is complete?

No. Use Trusted Completion and preserve external merge/close state only as evidence/effects.

## Reuse targets before custom code

Prioritize acquisition of:

- provider API schemas/fixtures and retry/idempotency failure cases;
- terminal/path-paste handling behavior and tests;
- document/parser failure corpora;
- retrieval evaluation fixtures;
- worker CLI/protocol fixtures and containment failure modes;
- issue duplicate/root-cause benchmark data where rights permit;
- independent review/triage behavior oracles;
- queue/checkpoint/retry/recovery patterns.

## Explicit overdesign rejections

```text
ONE_CORE_MODEL_PER_ISSUE_PROVIDER = REJECT
ONE_COMMAND_PER_AGENT_PROVIDER = REJECT
DONOR_BRANDED_COMMAND_SURFACE = REJECT
MANDATORY_VECTOR_DB_FOR_RAG_MINIMUM = REJECT
AUTONOMY_PROFILE_AS_AUTHORIZATION = REJECT
DROP_TO_EXECUTE = REJECT
MERGE_EQUALS_COMPLETION = REJECT
CLOSE_ISSUE_EQUALS_COMPLETION = REJECT
FIXED_ALWAYS_ON_AGENT_TEAM = REJECT
UNBOUNDED_BACKGROUND_AGENT_EXECUTION = REJECT
SILENT_PROVIDER_FALLBACK = REJECT
SILENT_PAID_QUOTA_CONSUMPTION = REJECT
COPY_ALL_DONOR_SOURCE = REJECT
PULL_S3_PLUS_SCOPE_INTO_S2 = REJECT
```

## Minimum useful vertical sequence

1. inert artifact intake;
2. local Case import/representation;
3. read-only triage;
4. provenance-first local retrieval;
5. workflow routing;
6. one bounded qualified worker;
7. one read-only GitHub adapter;
8. prepare-only GitHub mutation path;
9. bounded implementation/review loop;
10. authorized landing and completion proof.

Any implementation plan that skips authority/evidence layers in order to reach “autonomous issue closing” faster fails Ponytail because it creates rework and unsafe parallel machinery.
