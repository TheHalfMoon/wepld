#!/usr/bin/env python3
"""Protocol-demultiplex hardening for S1-010 Tauri status/control projection.

This wrapper binds the exact reviewed v14 policy and repairs one canonical
protocol-correctness gap without modifying product bytes:

- every Tauri request/control command owns its immediate request/ack transaction
  under the existing serialized CoreClient mutex;
- each transaction waits for its exact response kind + request ID;
- typed observation Events may be skipped while awaiting that response;
- ObserveHealth and Cancel acknowledgements are consumed before the handler
  releases CoreClient state;
- cancellation rejects UnknownTarget while treating Cancelled/AlreadyTerminal
  as terminal success.

The observation lifetime never holds the mutex. `CoreClient::receive()` remains
bounded by the canonical S1-009 response timeout. No helper function, background
thread, dependency, process/filesystem/network/plugin/sidecar authority, UI
redesign, branding work, or S1-011+ scope is introduced.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v15.py"
PRIOR_V14_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v14.py"
EXPECTED_PRIOR_V14_RUNNER_GIT_BLOB_SHA1 = "0e360eddd766ca0dc167f01260c1a89cdfbc73c1"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "7d00afff944c3ea294204246b578b2b80d0303e5d2339532c437debee3ca2293",
    ".github/workflows/s1-admission-integrity.yml": "338e077df1ae16c7461de5c370822cea346099957e2b16cb5282f2342be52a5c",
    ".github/workflows/s1-contracts.yml": "cb31bdbfedce8c34b9f8a169577402e1c6aab1cd51a8a399f24e78c3ed804f14",
}

EXPECTED_DEMUX_MAIN = r"""#![forbid(unsafe_code)]
use std::sync::Mutex;
use wepld_contracts::CancellationOutcome;
use wepld_contracts::Capability;
use wepld_contracts::HealthStatus;
use wepld_contracts::ResponseEnvelope;
use wepld_desktop::CoreClient;
use wepld_desktop::InboundEnvelope;

struct AppState {
    core: Mutex<Option<CoreClient>>,
}

#[tauri::command]
fn core_ready(state: tauri::State<'_, AppState>) -> Result<bool, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_health()
        .map_err(|error| format!("{error:?}"))?;
    loop {
        match client.receive().map_err(|error| format!("{error:?}"))? {
            InboundEnvelope::Response(ResponseEnvelope::Health(fields))
                if fields.request_id == request_id =>
            {
                return Ok(client.is_ready());
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected readiness response"));
            }
        }
    }
}

#[tauri::command]
fn core_health(state: tauri::State<'_, AppState>) -> Result<String, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_health()
        .map_err(|error| format!("{error:?}"))?;
    loop {
        match client.receive().map_err(|error| format!("{error:?}"))? {
            InboundEnvelope::Response(ResponseEnvelope::Health(fields))
                if fields.request_id == request_id =>
            {
                return Ok(String::from(match fields.payload.status {
                    HealthStatus::Healthy => "healthy",
                    HealthStatus::Degraded => "degraded",
                }));
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected health response"));
            }
        }
    }
}

#[tauri::command]
fn core_version(state: tauri::State<'_, AppState>) -> Result<String, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_version()
        .map_err(|error| format!("{error:?}"))?;
    loop {
        match client.receive().map_err(|error| format!("{error:?}"))? {
            InboundEnvelope::Response(ResponseEnvelope::Version(fields))
                if fields.request_id == request_id =>
            {
                return Ok(format!(
                    "{} ({})",
                    fields.payload.core_version, fields.payload.build_id
                ));
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected version response"));
            }
        }
    }
}

#[tauri::command]
fn core_capabilities(state: tauri::State<'_, AppState>) -> Result<Vec<String>, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_capabilities()
        .map_err(|error| format!("{error:?}"))?;
    loop {
        match client.receive().map_err(|error| format!("{error:?}"))? {
            InboundEnvelope::Response(ResponseEnvelope::Capabilities(fields))
                if fields.request_id == request_id =>
            {
                return Ok(fields
                    .payload
                    .capabilities
                    .into_vec()
                    .into_iter()
                    .map(|capability| {
                        String::from(match capability {
                            Capability::Health => "health",
                            Capability::Version => "version",
                            Capability::Capabilities => "capabilities",
                            Capability::HealthObservation => "health_observation",
                            Capability::Cancellation => "cancellation",
                        })
                    })
                    .collect());
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected capabilities response"));
            }
        }
    }
}

#[tauri::command]
fn core_observe_health(state: tauri::State<'_, AppState>) -> Result<u64, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let request_id = client
        .send_observe_health()
        .map_err(|error| format!("{error:?}"))?;
    loop {
        match client.receive().map_err(|error| format!("{error:?}"))? {
            InboundEnvelope::Response(ResponseEnvelope::ObserveHealth(fields))
                if fields.request_id == request_id =>
            {
                return Ok(request_id);
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected observation response"));
            }
        }
    }
}

#[tauri::command]
fn core_cancel_observation(
    state: tauri::State<'_, AppState>,
    request_id: u64,
) -> Result<u64, String> {
    let mut guard = state
        .core
        .lock()
        .map_err(|_| String::from("core state unavailable"))?;
    let client = guard
        .as_mut()
        .ok_or_else(|| String::from("core unavailable"))?;
    let cancel_id = client
        .send_cancel(request_id)
        .map_err(|error| format!("{error:?}"))?;
    loop {
        match client.receive().map_err(|error| format!("{error:?}"))? {
            InboundEnvelope::Response(ResponseEnvelope::Cancel(fields))
                if fields.request_id == cancel_id =>
            {
                match fields.payload.outcome {
                    CancellationOutcome::Cancelled | CancellationOutcome::AlreadyTerminal => {
                        return Ok(cancel_id);
                    }
                    CancellationOutcome::UnknownTarget => {
                        return Err(String::from("unknown observation target"));
                    }
                }
            }
            InboundEnvelope::Event(_) => continue,
            InboundEnvelope::ProtocolError(_) => {
                return Err(String::from("core protocol error"));
            }
            InboundEnvelope::Response(_) => {
                return Err(String::from("unexpected cancellation response"));
            }
        }
    }
}

fn main() {
    let state = AppState {
        core: Mutex::new(CoreClient::start().ok()),
    };
    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![
            core_ready,
            core_health,
            core_version,
            core_capabilities,
            core_observe_health,
            core_cancel_observation
        ])
        .run(tauri::generate_context!())
        .expect("Tauri runtime failed");
}
"""


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v14_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v14.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v14 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V14_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v14 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V14_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v14_runner_before_import()
import wepld_s1_shell_integrity_v14 as v14  # noqa: E402

v13 = v14.v13
v12 = v14.v12
v11 = v14.v11
v10 = v14.v10
v9 = v14.v9
v8 = v14.v8
v7 = v14.v7
v6 = v14.v6
v5 = v14.v5
v4 = v14.v4
v3 = v14.v3
v2 = v14.v2
shell = v14.shell

PRIOR_V14_MAIN = v13.EXPECTED_RECONCILED_MAIN
_INSTALLED = False


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V14_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V14_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v14 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V14_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v14._verify_policy_files(view)


def _verify_observation_handler_semantics(code: str) -> None:
    observe = v2._function_body(code, "core_observe_health")
    cancel = v2._function_body(code, "core_cancel_observation")

    observe_sends = v2._known_send_methods(observe)
    if observe_sends != {"send_observe_health"}:
        base.fail(
            "S1-010 core_observe_health may use only send_observe_health for its bounded transaction"
        )
    cancel_sends = v2._known_send_methods(cancel)
    if cancel_sends != {"send_cancel"}:
        base.fail(
            "S1-010 core_cancel_observation may use only send_cancel for its bounded transaction"
        )


def _install_v15_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v14._install_v14_policy()

    for module in (
        v14,
        v13,
        v12,
        v11,
        v10,
        v9,
        v8,
        v7,
        v6,
        v5,
        v4,
        v3,
        v2,
        shell,
        shell.prior,
    ):
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    # `loop` is admitted only because the complete future main.rs remains frozen
    # below. Every other inherited effect/surface restriction remains unchanged.
    shell.SHELL_RUST_PROHIBITED_IDENTIFIERS = frozenset(
        set(shell.SHELL_RUST_PROHIBITED_IDENTIFIERS) - {"loop"}
    )

    # Replace the older blanket "no receive in observe/cancel" rule with the
    # narrower send-surface invariant. Exact full-file equality below controls
    # every receive/event/correlation/outcome operation.
    v2._verify_observation_handler_semantics = _verify_observation_handler_semantics

    v13.EXPECTED_RECONCILED_MAIN = EXPECTED_DEMUX_MAIN
    v12.EXPECTED_STATUS_MAIN = EXPECTED_DEMUX_MAIN

    shell.verify_policy_files = _verify_policy_files
    _INSTALLED = True


def selftest() -> None:
    # Preserve every inherited v1-v12 oracle before installing the v13-v15
    # reconciled semantics. v13/v14 selftests intentionally encode superseded
    # product templates and are therefore not acceptance oracles for this layer.
    v12.selftest()
    _install_v15_policy()

    safe = v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_DEMUX_MAIN.encode("ascii")
    safe["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.encode("ascii")
    fixture = base.MemoryView(safe)

    v12._verify_shell_rust(fixture)
    v3._verify_frontend(fixture)
    shell.verify_shell_config(fixture)

    old_enqueue_only = dict(safe)
    old_enqueue_only["apps/desktop/src-tauri/src/main.rs"] = PRIOR_V14_MAIN.encode("ascii")
    base.expect_failure_matching(
        "S1-010 enqueue-only observation/cancel leaves acknowledgements unowned",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(old_enqueue_only),
    )

    no_event_demux = dict(safe)
    no_event_demux["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_DEMUX_MAIN.replace(
        "            InboundEnvelope::Event(_) => continue,\n",
        '            InboundEnvelope::Event(_) => {\n'
        '                return Err(String::from("unexpected readiness event"));\n'
        "            }\n",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 status transaction must demultiplex interleaved events",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(no_event_demux),
    )

    no_correlation = dict(safe)
    no_correlation["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_DEMUX_MAIN.replace(
        "                if fields.request_id == request_id =>\n",
        "                =>\n",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 status response request-id correlation",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(no_correlation),
    )

    unknown_cancel_success = dict(safe)
    unknown_cancel_success["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_DEMUX_MAIN.replace(
        '                    CancellationOutcome::UnknownTarget => {\n'
        '                        return Err(String::from("unknown observation target"));\n'
        "                    }\n",
        "                    CancellationOutcome::UnknownTarget => {\n"
        "                        return Ok(cancel_id);\n"
        "                    }\n",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 cancellation must reject unknown target",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(unknown_cancel_success),
    )

    old_racy_frontend = dict(safe)
    old_racy_frontend["apps/desktop/ui/app.js"] = v13.PRIOR_V3_JS.encode("ascii")
    base.expect_failure_matching(
        "S1-010 overlapping observation start/cancel race",
        "S1-010 JavaScript must cancel the exact stored observation request id",
        v3._verify_frontend,
        base.MemoryView(old_racy_frontend),
    )

    missing_busy_guard = dict(safe)
    missing_busy_guard["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.replace(
        "  if (observationBusy || observationRequestId !== null) return;\n",
        "",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 observation start serialization guard",
        "frozen direct-invoke/status-projection/request-identity template",
        v3._verify_frontend,
        base.MemoryView(missing_busy_guard),
    )

    missing_target_guard = dict(safe)
    missing_target_guard["apps/desktop/ui/app.js"] = v13.EXPECTED_SERIALIZED_JS.replace(
        "    if (observationRequestId === requestId) observationRequestId = null;\n",
        "    observationRequestId = null;\n",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 cancellation target identity guard",
        "frozen direct-invoke/status-projection/request-identity template",
        v3._verify_frontend,
        base.MemoryView(missing_target_guard),
    )

    print("wepld S1 Tauri shell protocol-demultiplex policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v15_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
