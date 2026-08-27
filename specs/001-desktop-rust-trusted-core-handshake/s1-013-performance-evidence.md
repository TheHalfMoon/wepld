# S1-013 — Performance and Evidence Reconciliation

## Decision scope

This record reconciles the canonical S1-013 performance measurement and evidence packet.
It does not authorize S1-014, change S1 runtime behavior, admit source/dependencies, or
claim final S1 acceptance. While proposed on a non-canonical branch it is review data
only; it becomes canonical evidence only after the separately authorized closeout
transition is qualified and merged.

```text
TASK = S1-013
MEASUREMENT_PR = #179
MEASUREMENT_CANDIDATE_HEAD = c4fe5b1bbc4c27c68413e57019d3b47c9520997c
MEASUREMENT_MERGE = 96fa229610f31598326493b75b40a3353b46bbbf
MEASUREMENT_TREE = bac45bb1d103e5128bcc853d44430edd6b3b92ec
MEASUREMENT_STATE = MERGED_CANONICAL
S1_013_EVIDENCE_RECONCILIATION = THIS_RECORD
S1_014_PLUS = NOT_AUTHORIZED_BY_THIS_RECORD
S1_ACCEPTED = NO
```

## Canonical post-merge gates

All authoritative values below are bound to the exact canonical merge commit, not to
an earlier PR head or rejected measurement attempt.

```text
SUBJECT_SHA = 96fa229610f31598326493b75b40a3353b46bbbf
FOUNDATION = 32955349075 / #700 / push / SUCCESS
S1_CONTRACTS = 32955348827 / #162 / push / SUCCESS_3_OF_3
S1_PERFORMANCE = 32955348872 / #5 / push / SUCCESS
WINDOWS_CONTRACTS = SUCCESS
MACOS_SECONDARY = SUCCESS
UBUNTU_SECONDARY = SUCCESS
```

The Windows contracts job retained the previously required adversarial suite, exact
release-Core staging, pinned Tauri build-tool installation, NSIS build/install,
packaged launch/mismatch exercise, and cleanup. Linux/macOS remain secondary
compile/contract evidence and are not represented as Windows-equivalent runtime proof.

## Authoritative performance observations

Direct Core measurement:

```text
COLD_SCOPE = PROCESS_SPAWN_PLUS_FIRST_HEALTH_ROUNDTRIP
COLD_SAMPLES = 20
COLD_P50_MS = 4.4885
COLD_P95_MS = 9.6583

HEALTH_SAMPLES = 200
HEALTH_P50_MS = 0.3573
HEALTH_P95_MS = 0.4224
HEALTH_P99_MS = 0.4623

SMALL_REQUEST_THROUGHPUT_RPS = 2719.04637605499
CANCEL_SAMPLES = 40
CANCEL_P95_MS = 0.4073
CORE_PROCESS_TERMINATION_P95_MS = 0.9927
CORE_REPLACEMENT_HANDSHAKE_P95_MS = 4.9999
MALFORMED_REJECT_P95_MS = 4.4243
OVERSIZED_REJECT_P95_MS = 4.5799
```

Desktop-owned recovery measurement:

```text
SAMPLES = 10
P95_MS = 2259.4108
SUBJECT = CORECLIENT_CHILD_EXIT_DETECTION_EXPLICIT_RESTART_FRESH_LAUNCH_HEALTH_HANDSHAKE
SCOPE = END_TO_END_EXISTING_TEST_WITH_CARGO_AND_TEST_HARNESS_OVERHEAD
PURE_RUNTIME_CRASH_DETECTION_LATENCY_CLAIM = NO
```

The recovery value includes Cargo/test-harness overhead. It is retained as the measured
end-to-end qualification path and is not relabeled as a pure runtime primitive.

Diagnostic-drain observation:

```text
DIAGNOSTIC_PRESSURE_TEST = SUCCESS
DIAGNOSTIC_DRAIN_ELAPSED_MS = 2232.6816
RETAINED_DIAGNOSTIC_BOUND_BYTES = 65536
TRUNCATION_OBSERVED = PASS
PROTOCOL_PROGRESS_DURING_PRESSURE = PASS
PURE_DIAGNOSTIC_PRIMITIVE_LATENCY_CLAIM = NO
```

The diagnostic elapsed value is test-execution wall time; the safety-relevant result is
that pressure beyond retention capacity was drained while truncation remained observable
and protocol progress continued.

Packaged idle observation:

```text
WORKING_SET_SAMPLES = 12
SAMPLE_INTERVAL_MS = 250
SETTLE_SECONDS = 2
DESKTOP_WORKING_SET_MEAN_BYTES = 26316800
CORE_WORKING_SET_MEAN_BYTES = 4050944
DESKTOP_CPU_SECONDS_DELTA = 0
CORE_CPU_SECONDS_DELTA = 0
```

The zero CPU deltas are observations over this bounded idle sample window, not a claim
that either process can never consume CPU while idle on every machine.

## Exact subject identities

```text
RUNNER_IMAGE = windows-2025-vs2026
RUNNER_IMAGE_VERSION = 20260818.207.1
WINDOWS_OS = Microsoft Windows NT 10.0.26100.0
RUNNER_ARCH = X64
RUSTC = 1.97.1 (8bab26f4f 2026-07-14)
CARGO = 1.97.1 (c980f4866 2026-06-30)
PYTHON = 3.12.10
TARGET = x86_64-pc-windows-msvc
TAURI_SOURCE_COMMIT = 7cd71369c00978a3783b6ae3e9972358abbe4ae6
TAURI_CLI = 2.11.4 / EXISTING_ADMITTED_CI_BUILD_TOOL_ONLY
PROTOCOL_VERSION = 1

CARGO_LOCK_SHA256 = a8f7ae6ae35b636a51e33e2d16cdc634f85d6f27595be9f69185b6f0d5a1dd8e
CORE_SHA256 = abbc4d82758a020932b99a7fccba9a78bac35dd01daa128576009017e91f46ec
PACKAGED_DESKTOP_SHA256 = 3ae5ae9b9c57c147b03533af9f801df972f95690a66f4d42a45cb05b549cf77d
PACKAGED_CORE_SHA256 = abbc4d82758a020932b99a7fccba9a78bac35dd01daa128576009017e91f46ec
```

Measurement implementation identities retained by canonical v9:

```text
PERFORMANCE_WORKFLOW = .github/workflows/s1-performance.yml
PERFORMANCE_WORKFLOW_GIT_BLOB_SHA1 = b16d57b42e617808d4b5d2547c1677e9ef7c3535
PERFORMANCE_WORKFLOW_SHA256 = 7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784

PERFORMANCE_PROBE = .github/scripts/wepld_s1_performance_probe.py
PERFORMANCE_PROBE_GIT_BLOB_SHA1 = 1b33c84c266ecab89af1b6e63f9677875fd5ecf5
PERFORMANCE_PROBE_SHA256 = e3eb6572b7cd4e35f07abaadb460907919acc091e27db94e4ebbd8ee0b83d6af
```

## Safety-budget reconciliation

The S1 plan defines its initial limits as safety upper bounds, not performance targets.
This measurement establishes latency, throughput, memory/CPU observations, and
diagnostic-pressure behavior, but it does not establish a safe smaller bound for payload,
wire-frame, in-flight request, health-watch, capability-item, protocol-error text, or
retained-diagnostic limits.

```text
BUDGET_TIGHTENING_DECISION = NO_SAFE_LOWER_BOUND_PROVEN_KEEP_EXISTING_SAFETY_LIMITS

LENGTH_PREFIX_BYTES = 4
MAX_PAYLOAD_BYTES = 65536
MAX_WIRE_FRAME_BYTES = 65540
MAX_IN_FLIGHT_REQUESTS = 32
MAX_HEALTH_WATCHES = 8
MAX_CAPABILITY_ITEMS = 64
MAX_PROTOCOL_ERROR_TEXT_BYTES = 1024
MAX_RETAINED_DIAGNOSTIC_BYTES = 65536
REPLAY_STATE = O(1)_HIGHEST_ACCEPTED_COMMAND_ID_PER_LAUNCH
```

No budget is claimed tightened. The task requirement is satisfied by making the
evidence-based decision: lower bounds are adopted only where evidence proves them; this
run does not prove such a lower bound.

## Raw-evidence retention limitation

The canonical performance workflow did not upload a GitHub Actions artifact for run
`32955348872`.

```text
RAW_ACTION_ARTIFACT = NONE_UPLOADED
AUTHORITATIVE_RETAINED_SURFACE = GITHUB_ACTIONS_RUN_LOGS_AND_JOB_SUMMARY
DURABLE_RAW_ZIP_RETENTION = NOT_PRESENT
LIMITATION_SILENTLY_WAIVED = NO
```

The values in this record were reconciled from the completed canonical-main run logs.
No nonexistent artifact is represented as durable retention.

## Rejected measurement history

The earlier run remains a negative oracle only:

```text
REJECTED_HEAD = 56f03eea9a8a2eeaa39c79821f9ae0b8e1d9c3f6
REJECTED_RUN = 32929228402
REJECTED_CLASS = EXACT_HEAD_MEASUREMENT_INVALIDATED_BY_THREE_MATERIAL_REVIEW_FINDINGS
REVIEW_FINDING_IDS = 3860338193,3860338199,3860338204
REJECTED_MEASUREMENT_AUTHORITY = NONE
```

Its numbers are not reused in this closeout.

## Authority boundary

```text
SOURCE_ADMISSION = NONE
DEPENDENCY_ADMISSION = NONE
DONOR_EXECUTION = NONE
NEW_PRODUCT_RUNTIME_AUTHORITY = NONE
NETWORK_LISTENER_AUTHORITY = NONE
MODEL_PROVIDER_EXECUTION = NONE
MODEL_WEIGHT_ACCESS = NONE
MODEL_INFERENCE = NONE
S1_014_PLUS = NOT_AUTHORIZED
S1_ACCEPTANCE = NOT_CLAIMED
```

S1-014 remains the next execution-authoritative task only after this S1-013 evidence
reconciliation and ledger transition are separately qualified, merged, and proven on
canonical `main`.
