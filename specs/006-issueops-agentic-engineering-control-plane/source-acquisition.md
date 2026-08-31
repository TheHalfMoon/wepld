# Source Acquisition — IssueOps / Workflow Skills / Delegation

```text
STATUS = RESEARCH_INPUT_ONLY
CANONICAL_REGISTRY_COUNT = 402
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
IMPLEMENTATION_AUTHORITY = NONE
```

The canonical source registry does not currently admit the two newly studied donor repositories below. This document records them as future source-acquisition candidates only. A separately governed registry revision is required before any admission/import.

## Candidate A — mattpocock/skills

```text
REPOSITORY = mattpocock/skills
PINNED_REVISION = 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76
LICENSE_OBSERVED = MIT
ROLE_CANDIDATE = BEHAVIOR_ORACLE + WORKFLOW_DESIGN_QUARRY + TEST/NEGATIVE_ORACLE_CANDIDATE
SOURCE_ADMISSION = NONE
```

### Studied skill inventory

Stable engineering:

1. `ask-matt`
2. `code-review`
3. `codebase-design`
4. `diagnosing-bugs`
5. `domain-modeling`
6. `grill-with-docs`
7. `implement`
8. `improve-codebase-architecture`
9. `prototype`
10. `research`
11. `resolving-merge-conflicts`
12. `setup-matt-pocock-skills`
13. `tdd`
14. `to-spec`
15. `to-tickets`
16. `triage`
17. `wayfinder`
18. `wizard`

Stable productivity:

19. `grill-me`
20. `grilling`
21. `handoff`
22. `teach`
23. `to-questionnaire`
24. `wait-what`
25. `writing-for-agents`

In-progress:

26. `claude-handoff`
27. `implement-spec`
28. `loop-me`
29. `retro`
30. `setup-ts-deep-modules`
31. `writing-beats`
32. `writing-fragments`
33. `writing-shape`

Miscellaneous:

34. `git-guardrails-claude-code`
35. `migrate-to-shoehorn`
36. `scaffold-exercises`
37. `setup-pre-commit`

### WePLD adaptation plan

| Donor behavior | WePLD-native destination |
|---|---|
| ask-matt | `/askme` workflow router |
| wait-what | `/btw` context-aware re-explanation |
| triage | `/triage` + `/issues` Case triage |
| grilling / grill-me / grill-with-docs | `/grill` + internal decision-tree primitive |
| codebase-design / domain-modeling / improve-codebase-architecture | `/architect` + internal architecture/domain primitives |
| to-spec | `/spec` |
| to-tickets | `/tickets` tracer-bullet/dependency planner |
| implement / tdd | `/build` + internal TDD primitive |
| diagnosing-bugs | `/debug` feedback-loop-first diagnosis |
| code-review | `/review` with standards/spec axes |
| prototype | `/prototype` |
| research | `/research` |
| wayfinder | `/wayfinder` |
| handoff / claude-handoff | provider-neutral `/handoff`; never Claude-owned architecture |
| teach / scaffold-exercises | `/teach` + learning assets |
| to-questionnaire | `/questionnaire` |
| wizard | `/wizard` |
| loop-me | `/workflow` recurring/checkpointed workflow |
| retro | `/retro` |
| implement-spec | Edara/Mission Runtime task-graph orchestration, not a second build command |
| writing-for-agents | internal bounded-context packaging primitive |
| writing-beats/fragments/shape | future writing capability; not three mandatory commands |
| setup-ts-deep-modules | language-neutral `/architect` boundary qualification |
| resolving-merge-conflicts | intent-preserving reconciliation primitive subject to WePLD Git policy |
| git-guardrails-claude-code | Nawat effect policy/guardrails, provider-neutral |
| setup-pre-commit | optional repository qualification pattern, not mandatory dependency |
| migrate-to-shoehorn | generic migration workflow pattern only |
| setup-matt-pocock-skills | inspiration for WePLD workflow setup/triage conventions; no donor branding |

### Important incompatibilities/rejections

- Donor instructions that imply rebase/history rewriting MUST NOT override WePLD repository policy.
- Provider-specific background execution MUST become governed Mission Runtime work.
- Donor branding MUST NOT define user-facing WePLD product language.
- Skill prose is not authority and is not copied wholesale merely because the license permits reuse.

## Candidate B — amElnagdy/delegate-skills

```text
REPOSITORY = amElnagdy/delegate-skills
PINNED_REVISION = b781ee2e23089630e2fbee1cfd6174afe4edeb76
LICENSE_OBSERVED = MIT
ROLE_CANDIDATE = WORKER_ADAPTER_BEHAVIOR_ORACLE + DELEGATION_PROTOCOL_QUARRY + FAILURE_MODE_QUARRY
SOURCE_ADMISSION = NONE
```

### Studied skill inventory

1. `delegate-setup`
2. `agy`
3. `aider`
4. `claude`
5. `cline`
6. `codex`
7. `commandcode`
8. `copilot`
9. `cursor`
10. `grok`
11. `kimi`
12. `omp`
13. `opencode`
14. `pi`
15. `qoder`
16. `vibe`
17. `warp`
18. `zcode`

Shared behavior studied includes fleet schema, dispatch pattern, brief construction, CLI delegate protocol, queue/poll behavior, and review/land flow.

### WePLD adaptation plan

Do not expose one `/delegate-*` command per provider. Normalize all qualified providers behind:

```text
/delegate <task>
/delegate --to <worker> <task>
/workers
```

Required adapter facts:

- stable WePLD `worker_id`;
- opaque provider identity/session identifiers;
- capability descriptor;
- effect classes;
- enforceable vs advisory read-only/containment semantics;
- process/session lifecycle;
- structured event/result normalization;
- cancellation/recovery behavior;
- cost/quota/metering classification;
- provider/model identity;
- version/provenance;
- known unsafe/full-trust modes;
- qualification evidence and expiry.

### Security finding from cross-provider study

Provider flags are not semantically equivalent. Some workers offer enforceable sandbox modes; others expose advisory “read-only” behavior or full-trust/yolo modes. Therefore:

```text
PROVIDER_READONLY_FLAG != WEPLD_CONTAINMENT
PROVIDER_PERMISSION != NAWAT_GRANT
PROVIDER_SESSION_ID != TRUST
```

WePLD must qualify containment and effect behavior independently.

## Future acquisition sequence

1. Create a separately governed next source-registry revision candidate.
2. Add both repositories as pinned candidates with license/source hashes.
3. Mine only the paths needed by the owning slice.
4. Extract tests, fixtures, behavior contracts, negative oracles, and security/containment differences.
5. Compare against already-admitted sources to avoid duplicate machinery.
6. Decide reuse mode independently per capability:
   - reject;
   - behavior oracle only;
   - test/fixture acquisition;
   - documentation/process pattern;
   - bounded source reuse;
   - adapter candidate.
7. Run applicable license/security/dependency/portability/maintenance/exit qualification.
8. Admit only through the owning future slice; never through this planning candidate.

## Additional source classes to qualify later

IssueOps and RAG will require capability-triggered acquisition rather than broad discovery. Candidate categories include:

- GitHub API/App/webhook/reference implementations and fixtures;
- GitLab/Linear/Jira/Azure DevOps/Sentry API contracts when their adapter is actually activated;
- terminal bracketed-paste/path escaping behavior or reusable libraries;
- PDF/document/structured-data parsers and adversarial corpora;
- lexical/full-text retrieval engines;
- optional vector/embedding/index engines only if S4 evidence proves the need;
- code semantic-index/graph sources already contemplated by Fehrest;
- retry/idempotency/checkpoint libraries or patterns only when stdlib/admitted machinery is insufficient.

No category listing is source admission.
