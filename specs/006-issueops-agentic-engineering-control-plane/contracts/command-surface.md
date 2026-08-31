# Contract — Native Command Surface

```text
STATUS = FUTURE_PLANNING_CONTRACT
IMPLEMENTATION_AUTHORITY = NONE
```

## Command principle

Slash commands are user-intent surfaces. They normalize intent into WePLD capabilities and never bypass qualification, containment, Nawat authority, deterministic gates, review, or Trusted Completion.

## Planned stable commands

```text
/askme
/btw
/issues
/rag
/triage
/grill
/architect
/spec
/tickets
/build
/debug
/review
/prototype
/research
/wayfinder
/handoff
/teach
/questionnaire
/wizard
/retro
/workflow
/delegate
/workers
```

## Command semantics

### `/askme`

Routes the current user goal to the minimum sufficient qualified capability/workflow. It may recommend or invoke another command path according to current authority, but it must not silently select an unqualified paid/provider route.

### `/btw`

Re-explains current project/case/result/blocker state. Read-only by default and must not mutate workflow state merely by explaining it.

### `/issues`

Entry point for provider-neutral Case operations. Planned subcommands include inbox/list/sweep/show/attach/watch and later bounded execution intents.

### `/rag`

Creates/uses/manages named knowledge collections and performs provenance-first retrieval. Source access or refresh that requires filesystem/network effects remains separately governed.

### `/triage`

Produces evidence-backed classification, reproduction readiness, duplicate/root-cause candidates, blockers, and next frontier.

### `/grill`

Opens decision-boundary questions only after discoverable facts are gathered to the available qualified extent.

### `/architect`

Uses domain, boundary, seam, interface, dependency, and deep-module analysis. It does not authorize refactors.

### `/spec`

Produces/updates Spec Kit planning artifacts under the canonical build method.

### `/tickets`

Builds tracer-bullet tasks and a dependency frontier, including blockers and expand/contract steps where required.

### `/build`

Executes the authorized implementation workflow over a qualified spec/task target. TDD and deterministic checks are internal methods, not bypassable optional decorations when required.

### `/debug`

Creates a tight reproduction/feedback loop, records falsifiable hypotheses, diagnoses, repairs when authorized, and preserves regression evidence.

### `/review`

Runs or coordinates independent review with distinct standards/correctness and spec-conformance axes where applicable. Review never grants completion authority.

### `/prototype`

Runs a bounded throwaway experiment to answer one explicit engineering/product question. Prototype output is evidence, not automatically production code.

### `/research`

Produces source-backed research with provenance/citations and preserves uncertainty/conflict.

### `/wayfinder`

Builds a decision map/frontier for large foggy work without pretending unresolved decisions are implementation tasks.

### `/handoff`

Transfers durable context/session responsibility. It does not assign new bounded work unless explicitly combined with a delegation workflow.

### `/teach`

Maintains a durable learning flow and learning assets while preserving the distinction between instruction and engineering authority.

### `/questionnaire`

Produces structured questions/choices for external decision capture.

### `/wizard`

Guides human-only setup/migration steps where direct autonomous execution is unavailable or intentionally inappropriate.

### `/retro`

Captures evidence-backed workflow/environment improvements after work. Learning output remains candidate evidence.

### `/workflow`

Defines/checkpoints recurring or resumable workflows. Recurrence does not grant future effects beyond policy.

### `/delegate`

Assigns bounded work to a qualified worker through Edara/Mirefa/Nawat/Mission Runtime/UWC. Supports optional explicit `--to <worker>` requests without bypassing qualification or cost/containment policy.

### `/workers`

Shows worker catalog, capability, availability, containment evidence, cost/metering, qualification, and expiry where available.

## Optional aliases

User-friendly aliases such as `/fix <case-or-url>` may later normalize into `/issues` + `/build` workflow intent. An alias must not create a new authority path.

## Input composition

Commands may consume:

- current project/case/session context;
- explicit arguments;
- `InputArtifact` attachments;
- `@rag:<collection>` references;
- provider object URLs/references;
- explicit worker requests.

All composed inputs preserve source/provenance identity.

## Error semantics

Unknown, unsupported, stale, unqualified, unauthorized, or cost-blocked states must be explicit. Commands must not hide these conditions behind automatic fallback.
