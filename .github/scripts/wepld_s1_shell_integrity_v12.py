#!/usr/bin/env python3
"""Typed S1-010 status-projection repair over canonical v11 admission.

This wrapper binds the exact reviewed v11 policy before import, then repairs one
validated functional gap: the S1-010 shell must project actual typed Core
readiness, health, version/build identity, and capabilities rather than policy
fixture placeholders.

The repair introduces no dependency, package-manager, plugin, process,
filesystem, network, sidecar, branding, or S1-011+ authority. `wepld-contracts`
is already a direct Desktop dependency. Direct contract use is permitted only
through one exact frozen `main.rs` template; all inherited S1-010 restrictions
remain in force, including enqueue-only observation/cancellation handlers.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v12.py"
PRIOR_V11_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v11.py"
EXPECTED_PRIOR_V11_RUNNER_GIT_BLOB_SHA1 = "ed997967ab0553be95192e3b67c643c14c25e2b2"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "407876d6d1c08b316f10027be5b631956be1918cac85512550eb2491d448515b",
    ".github/workflows/s1-admission-integrity.yml": "f297d827123b4ecf63ee140f91afdb0a53b699876282606aeaa4831dfda5bc60",
    ".github/workflows/s1-contracts.yml": "ac443e5aa2cd257ef458dda8aaaec3f5d48a5e3a869bc7aad050e41601cb1dab",
}

EXPECTED_STATUS_MAIN = r"""#![forbid(unsafe_code)]
use std::sync::Mutex;
use wepld_contracts::Capability;
use wepld_contracts::HealthStatus;
use wepld_contracts::ResponseEnvelope;
use wepld_desktop::CoreClient;
use wepld_desktop::InboundEnvelope;

struct AppState {
    core: Mutex<Option<CoreClient>>,
}

#[tauri::command]
fn core_ready(state: tauri::State<'_, AppState>) -> bool {
    let mut guard = match state.core.lock() {
        Ok(guard) => guard,
        Err(_) => return false,
    };
    let client = match guard.as_mut() {
        Some(client) => client,
        None => return false,
    };
    let request_id = match client.send_health() {
        Ok(request_id) => request_id,
        Err(_) => return false,
    };
    match client.receive() {
        Ok(InboundEnvelope::Response(ResponseEnvelope::Health(fields))) => {
            fields.request_id == request_id && client.is_ready()
        }
        _ => false,
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
    match client.receive().map_err(|error| format!("{error:?}"))? {
        InboundEnvelope::Response(ResponseEnvelope::Health(fields))
            if fields.request_id == request_id =>
        {
            Ok(String::from(match fields.payload.status {
                HealthStatus::Healthy => "healthy",
                HealthStatus::Degraded => "degraded",
            }))
        }
        _ => Err(String::from("unexpected health response")),
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
    match client.receive().map_err(|error| format!("{error:?}"))? {
        InboundEnvelope::Response(ResponseEnvelope::Version(fields))
            if fields.request_id == request_id =>
        {
            Ok(format!(
                "{} ({})",
                fields.payload.core_version, fields.payload.build_id
            ))
        }
        _ => Err(String::from("unexpected version response")),
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
    match client.receive().map_err(|error| format!("{error:?}"))? {
        InboundEnvelope::Response(ResponseEnvelope::Capabilities(fields))
            if fields.request_id == request_id =>
        {
            Ok(fields
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
                .collect())
        }
        _ => Err(String::from("unexpected capabilities response")),
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
    client
        .send_observe_health()
        .map_err(|error| format!("{error:?}"))
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
    client
        .send_cancel(request_id)
        .map_err(|error| format!("{error:?}"))
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

_INSTALLED = False
_PRIOR_VERIFY_SHELL_RUST = None


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v11_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v11.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v11 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V11_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v11 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V11_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v11_runner_before_import()
import wepld_s1_shell_integrity_v11 as v11  # noqa: E402

shell = v11.shell


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V11_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V11_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v11 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V11_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v11._verify_policy_files(view)


def _verify_shell_rust(view: base.RepositoryView) -> None:
    if _PRIOR_VERIFY_SHELL_RUST is None:
        base.fail("S1-010 v12 prior Rust verifier was not installed")
    _PRIOR_VERIFY_SHELL_RUST(view)

    raw, _ = shell.prior.prior._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )
    if raw != EXPECTED_STATUS_MAIN:
        base.fail(
            "S1-010 Tauri main must equal the frozen typed status-projection template"
        )


def _install_v12_policy() -> None:
    global _INSTALLED, _PRIOR_VERIFY_SHELL_RUST
    if _INSTALLED:
        return

    v11._install_v11_policy()

    v10 = v11.v10
    v9 = v10.v9
    v8 = v9.v8
    v7 = v8.v7
    v6 = v7.v6
    v5 = v6.v5
    v4 = v5.v4
    v3 = v4.v3
    v2 = v3.v2

    for module in (
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

    shell.SHELL_RUST_PROHIBITED_IDENTIFIERS = frozenset(
        set(shell.SHELL_RUST_PROHIBITED_IDENTIFIERS) - {"wepld_contracts"}
    )

    _PRIOR_VERIFY_SHELL_RUST = shell.verify_shell_rust
    shell.verify_policy_files = _verify_policy_files
    shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def selftest() -> None:
    v11.selftest()
    _install_v12_policy()

    v10 = v11.v10
    safe = v10.v9.v8.v7.v6.v5.v4.v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_STATUS_MAIN.encode("ascii")
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)

    old_stub = v10.v9.v8.v7.v6.v5.v4.v3._safe_v3_fixture()
    base.expect_failure_matching(
        "S1-010 placeholder status handlers",
        "frozen typed status-projection template",
        _verify_shell_rust,
        base.MemoryView(old_stub),
    )

    wrong_correlation = dict(safe)
    wrong_correlation["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_STATUS_MAIN.replace(
        "fields.request_id == request_id && client.is_ready()",
        "client.is_ready()",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 readiness response correlation omission",
        "frozen typed status-projection template",
        _verify_shell_rust,
        base.MemoryView(wrong_correlation),
    )

    broadened_contract_surface = dict(safe)
    broadened_contract_surface["apps/desktop/src-tauri/src/main.rs"] = (
        EXPECTED_STATUS_MAIN.replace(
            "use wepld_contracts::ResponseEnvelope;\n",
            "use wepld_contracts::ProtocolEnvelope;\n"
            "use wepld_contracts::ResponseEnvelope;\n",
            1,
        ).encode("ascii")
    )
    base.expect_failure_matching(
        "S1-010 arbitrary contracts surface expansion",
        "frozen typed status-projection template",
        _verify_shell_rust,
        base.MemoryView(broadened_contract_surface),
    )

    observe_receive = dict(safe)
    observe_receive["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_STATUS_MAIN.replace(
        "    client\n"
        "        .send_observe_health()\n"
        "        .map_err(|error| format!(\"{error:?}\"))\n",
        "    let request_id = client\n"
        "        .send_observe_health()\n"
        "        .map_err(|error| format!(\"{error:?}\"))?;\n"
        "    let _ = client.receive();\n"
        "    Ok(request_id)\n",
        1,
    ).encode("ascii")
    base.expect_failure_matching(
        "S1-010 observation receive remains prohibited",
        "core_observe_health may not call or alias receive",
        _verify_shell_rust,
        base.MemoryView(observe_receive),
    )

    print("wepld S1 Tauri shell typed status-projection policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v12_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
