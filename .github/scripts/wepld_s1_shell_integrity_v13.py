#!/usr/bin/env python3
"""Review-reconciliation hardening for S1-010 typed status projection.

This wrapper binds the exact v12 repair, then incorporates fresh exact-head
review findings without widening S1 authority:

- readiness reports unavailable/error rather than fabricating `false` when the
  Core cannot be queried;
- observation start/cancel UI state is serialized so overlapping actions cannot
  orphan an active observation request ID.

All v1-v12 process/filesystem/network/plugin/Builder/macro/attribute/icon and
frozen-product restrictions remain in force.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v13.py"
PRIOR_V12_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v12.py"
EXPECTED_PRIOR_V12_RUNNER_GIT_BLOB_SHA1 = "fdd28437595f07dec35170acbd14ae31b0964229"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "12b6c5d897e55e05195eaf032bdb7b60f1ab3dfa870cbfbffcf7f303dfe77ecb",
    ".github/workflows/s1-admission-integrity.yml": "be03be0f62cfd8f7655997b27c485b32837b96fc63d0e607aca38f897b4c0f50",
    ".github/workflows/s1-contracts.yml": "eb18413585004610c60e8cfadfe5cc67d4f29f2029d06156dc4da6dfbc971beb",
}

EXPECTED_RECONCILED_MAIN = r"""#![forbid(unsafe_code)]
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
    match client.receive().map_err(|error| format!("{error:?}"))? {
        InboundEnvelope::Response(ResponseEnvelope::Health(fields))
            if fields.request_id == request_id =>
        {
            Ok(client.is_ready())
        }
        _ => Err(String::from("unexpected readiness response")),
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

EXPECTED_SERIALIZED_JS = r"""const { invoke } = window.__TAURI__.core;
const readinessStatus = document.getElementById("core-readiness");
const healthStatus = document.getElementById("core-health");
const versionStatus = document.getElementById("core-version");
const capabilitiesStatus = document.getElementById("core-capabilities");
const observationStatus = document.getElementById("observation-status");
let observationRequestId = null;
let observationBusy = false;

async function refresh() {
  try {
    readinessStatus.textContent = `Ready: ${String(await invoke("core_ready"))}`;
    healthStatus.textContent = `Health: ${String(await invoke("core_health"))}`;
    versionStatus.textContent = `Version: ${String(await invoke("core_version"))}`;
    const capabilities = await invoke("core_capabilities");
    capabilitiesStatus.textContent = `Capabilities: ${Array.isArray(capabilities) ? capabilities.join(", ") : String(capabilities)}`;
  } catch (_error) {
    readinessStatus.textContent = "Ready: unavailable";
    healthStatus.textContent = "Health: unavailable";
    versionStatus.textContent = "Version: unavailable";
    capabilitiesStatus.textContent = "Capabilities: unavailable";
  }
}

document.getElementById("observation-start").addEventListener("click", async () => {
  if (observationBusy || observationRequestId !== null) return;
  observationBusy = true;
  try {
    observationRequestId = await invoke("core_observe_health");
    observationStatus.textContent = "Observation active";
  } catch (_error) {
    observationRequestId = null;
    observationStatus.textContent = "Observation unavailable";
  } finally {
    observationBusy = false;
  }
});

document.getElementById("observation-cancel").addEventListener("click", async () => {
  if (observationBusy || observationRequestId === null) return;
  const requestId = observationRequestId;
  observationBusy = true;
  try {
    await invoke("core_cancel_observation", { requestId });
    if (observationRequestId === requestId) observationRequestId = null;
    observationStatus.textContent = "Observation cancelled";
  } catch (_error) {
    observationStatus.textContent = "Cancellation failed";
  } finally {
    observationBusy = false;
  }
});

refresh();
"""


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v12_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v12.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v12 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V12_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v12 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V12_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v12_runner_before_import()
import wepld_s1_shell_integrity_v12 as v12  # noqa: E402

v11 = v12.v11
v10 = v11.v10
v9 = v10.v9
v8 = v9.v8
v7 = v8.v7
v6 = v7.v6
v5 = v6.v5
v4 = v5.v4
v3 = v4.v3
v2 = v3.v2
shell = v12.shell

PRIOR_V12_STATUS_MAIN = v12.EXPECTED_STATUS_MAIN
PRIOR_V3_JS = v3.EXPECTED_JS
_INSTALLED = False


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V12_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V12_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v12 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V12_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v12._verify_policy_files(view)


def _install_v13_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v12._install_v12_policy()

    for module in (
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

    v12.EXPECTED_STATUS_MAIN = EXPECTED_RECONCILED_MAIN
    v2.CANCEL_JS_USE = re.compile(
        r'invoke\s*\(\s*["\']core_cancel_observation["\']\s*,\s*'
        r'\{\s*requestId\s*\}\s*\)'
    )
    v3.EXPECTED_JS = EXPECTED_SERIALIZED_JS

    shell.verify_policy_files = _verify_policy_files
    _INSTALLED = True


def selftest() -> None:
    v12.selftest()
    _install_v13_policy()

    safe = v3._safe_v3_fixture()
    safe["apps/desktop/src-tauri/src/main.rs"] = EXPECTED_RECONCILED_MAIN.encode("ascii")
    safe["apps/desktop/ui/app.js"] = EXPECTED_SERIALIZED_JS.encode("ascii")
    fixture = base.MemoryView(safe)

    v12._verify_shell_rust(fixture)
    v3._verify_frontend(fixture)

    old_v12_readiness = dict(safe)
    old_v12_readiness["apps/desktop/src-tauri/src/main.rs"] = PRIOR_V12_STATUS_MAIN.encode(
        "ascii"
    )
    base.expect_failure_matching(
        "S1-010 readiness may not fabricate false on unavailable Core",
        "frozen typed status-projection template",
        v12._verify_shell_rust,
        base.MemoryView(old_v12_readiness),
    )

    old_racy_frontend = dict(safe)
    old_racy_frontend["apps/desktop/ui/app.js"] = PRIOR_V3_JS.encode("ascii")
    base.expect_failure_matching(
        "S1-010 overlapping observation start/cancel race",
        "frozen direct-invoke/status-projection/request-identity template",
        v3._verify_frontend,
        base.MemoryView(old_racy_frontend),
    )

    missing_busy_guard = dict(safe)
    missing_busy_guard["apps/desktop/ui/app.js"] = EXPECTED_SERIALIZED_JS.replace(
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
    missing_target_guard["apps/desktop/ui/app.js"] = EXPECTED_SERIALIZED_JS.replace(
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

    print("wepld S1 Tauri shell review-reconciliation policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v13_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
