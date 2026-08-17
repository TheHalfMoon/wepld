#!/usr/bin/env python3
"""Hardening wrapper for the bounded S1-010 Tauri shell admission policy.

This wrapper binds the exact prior shell-admission runner before import, then
adds the two post-egress review repairs without changing any S1-010 product
bytes: a frozen non-navigating HTML/CSP surface and cancellable observation
handler semantics.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v2.py"
PRIOR_SHELL_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity.py"
EXPECTED_PRIOR_SHELL_RUNNER_GIT_BLOB_SHA1 = "d870476b1468fcd297d2c6e30f89aa88f98db585"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "c697006749a3af19c5901e8872500b417ce095d5cd470b96dd1a4127ba361cf3",
    ".github/workflows/s1-admission-integrity.yml": "c37c291f927414bf6414a2352e681054e29ff55781d6c1fc5a49b4c8cd6b43d0",
    ".github/workflows/s1-contracts.yml": "3e49f693e5ee6a0f4fc8d01da6676bc37f7fb326045cc2429d6d431b672d9c19",
}

HARDENED_CSP = (
    "default-src 'self'; "
    "connect-src ipc: http://ipc.localhost; "
    "img-src 'self'; "
    "style-src 'self'; "
    "script-src 'self'; "
    "form-action 'none'; "
    "base-uri 'none'; "
    "object-src 'none'"
)

EXPECTED_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WePLD</title><link rel="stylesheet" href="./style.css"></head>
<body><main><h1>WePLD</h1><section role="status" aria-live="polite"><p id="core-readiness"></p><p id="core-health"></p><p id="core-version"></p><p id="core-capabilities"></p></section><button id="observation-start" type="button">Start observation</button><button id="observation-cancel" type="button">Cancel observation</button></main><script src="./app.js" defer></script></body></html>
"""

OBSERVATION_REQUEST_ID = "observationRequestId"
OBSERVE_JS_ASSIGNMENT = re.compile(
    r'\bobservationRequestId\s*=\s*await\s+invoke\s*\(\s*["\']core_observe_health["\']\s*\)'
)
CANCEL_JS_USE = re.compile(
    r'invoke\s*\(\s*["\']core_cancel_observation["\']\s*,\s*'
    r'\{\s*requestId\s*:\s*observationRequestId\s*\}\s*\)'
)
KNOWN_SEND_METHODS = frozenset(
    {
        "send_health",
        "send_version",
        "send_capabilities",
        "send_observe_health",
        "send_cancel",
    }
)
_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_shell_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_SHELL_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_SHELL_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_shell_runner_before_import()
import wepld_s1_shell_integrity as shell  # noqa: E402

_ORIGINAL_VERIFY_POLICY_FILES = shell.verify_policy_files
_ORIGINAL_VERIFY_FRONTEND = shell.verify_frontend
_ORIGINAL_VERIFY_SHELL_RUST = shell.verify_shell_rust


def _hardened_config() -> dict[str, object]:
    config = json.loads(json.dumps(shell.EXPECTED_TAURI_CONFIG))
    config["app"]["security"]["csp"] = HARDENED_CSP
    return config


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_SHELL_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_SHELL_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_SHELL_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    _ORIGINAL_VERIFY_POLICY_FILES(view)


def _function_body(code: str, name: str) -> str:
    match = re.search(rf"\bfn\s+{re.escape(name)}\s*\(", code)
    if match is None:
        base.fail(f"S1-010 Tauri main missing expected function body: {name}")
    brace = code.find("{", match.end())
    if brace == -1:
        base.fail(f"S1-010 Tauri main missing function body brace: {name}")

    depth = 0
    for index in range(brace, len(code)):
        char = code[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return code[brace + 1 : index]
    base.fail(f"S1-010 Tauri main has unterminated function body: {name}")


def _known_send_methods(body: str) -> set[str]:
    identifiers = set(shell.prior.prior.RUST_IDENTIFIER.findall(body))
    return identifiers & KNOWN_SEND_METHODS


def _verify_observation_handler_semantics(code: str) -> None:
    observe = _function_body(code, "core_observe_health")
    cancel = _function_body(code, "core_cancel_observation")

    if re.search(r"\breceive\b", observe):
        base.fail(
            "S1-010 core_observe_health may not call or alias receive while holding shared CoreClient state"
        )
    if re.search(r"\breceive\b", cancel):
        base.fail(
            "S1-010 core_cancel_observation may not call or alias receive while holding shared CoreClient state"
        )

    observe_sends = _known_send_methods(observe)
    if observe_sends != {"send_observe_health"}:
        base.fail(
            "S1-010 core_observe_health may enqueue only send_observe_health before releasing CoreClient state"
        )
    cancel_sends = _known_send_methods(cancel)
    if cancel_sends != {"send_cancel"}:
        base.fail(
            "S1-010 core_cancel_observation may enqueue only send_cancel before releasing CoreClient state"
        )


def _verify_shell_rust(view: base.RepositoryView) -> None:
    _ORIGINAL_VERIFY_SHELL_RUST(view)
    _, code = shell.prior.prior._read_rust(
        view,
        "apps/desktop/src-tauri/src/main.rs",
        shell.MAX_S1_010_RUST_BYTES,
        "S1-010 Tauri main",
    )
    _verify_observation_handler_semantics(code)


def _verify_frontend(view: base.RepositoryView) -> None:
    _ORIGINAL_VERIFY_FRONTEND(view)
    html = shell._read_utf8(
        view,
        "apps/desktop/ui/index.html",
        shell.MAX_S1_010_HTML_BYTES,
        "S1-010 HTML",
    )
    if html != EXPECTED_HTML:
        base.fail(
            "S1-010 HTML must equal the frozen non-navigating static presentation template"
        )

    js = shell._read_utf8(
        view,
        "apps/desktop/ui/app.js",
        shell.MAX_S1_010_JS_BYTES,
        "S1-010 JavaScript",
    )
    if OBSERVATION_REQUEST_ID not in js:
        base.fail("S1-010 JavaScript must retain the observation request identity")
    if OBSERVE_JS_ASSIGNMENT.search(js) is None:
        base.fail(
            "S1-010 JavaScript must store the request id returned by core_observe_health"
        )
    if CANCEL_JS_USE.search(js) is None:
        base.fail(
            "S1-010 JavaScript must cancel the exact stored observation request id"
        )


def _install_v2_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    shell.EXPECTED_TAURI_CONFIG = _hardened_config()
    shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    shell.prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.verify_frontend = _verify_frontend
    shell.verify_shell_rust = _verify_shell_rust
    _INSTALLED = True


def _safe_v2_fixture() -> dict[str, bytes]:
    safe = shell._safe_shell_fixture()
    safe["apps/desktop/src-tauri/tauri.conf.json"] = (
        json.dumps(shell.EXPECTED_TAURI_CONFIG, indent=2) + "\n"
    ).encode()
    safe["apps/desktop/ui/index.html"] = EXPECTED_HTML.encode()
    safe["apps/desktop/ui/app.js"] = b"""const { invoke } = window.__TAURI__.core;
let observationRequestId = null;
async function refresh() { await invoke("core_ready"); await invoke("core_health"); await invoke("core_version"); await invoke("core_capabilities"); }
document.getElementById("observation-start").addEventListener("click", async () => { observationRequestId = await invoke("core_observe_health"); });
document.getElementById("observation-cancel").addEventListener("click", async () => { if (observationRequestId === null) return; await invoke("core_cancel_observation", { requestId: observationRequestId }); observationRequestId = null; });
refresh();
"""
    safe["apps/desktop/src-tauri/src/main.rs"] = b"""#![forbid(unsafe_code)]
use std::sync::Mutex;
use wepld_desktop::CoreClient;

struct AppState {
    core: Mutex<Option<CoreClient>>,
}

#[tauri::command]
fn core_ready(_state: tauri::State<'_, AppState>) -> bool { false }
#[tauri::command]
fn core_health(_state: tauri::State<'_, AppState>) -> Result<String, String> { Ok(String::new()) }
#[tauri::command]
fn core_version(_state: tauri::State<'_, AppState>) -> Result<String, String> { Ok(String::new()) }
#[tauri::command]
fn core_capabilities(_state: tauri::State<'_, AppState>) -> Result<Vec<String>, String> { Ok(Vec::new()) }
#[tauri::command]
fn core_observe_health(state: tauri::State<'_, AppState>) -> Result<u64, String> {
    let mut guard = state.core.lock().map_err(|_| String::from("core state unavailable"))?;
    let client = guard.as_mut().ok_or_else(|| String::from("core unavailable"))?;
    client.send_observe_health().map_err(|error| format!("{error:?}"))
}
#[tauri::command]
fn core_cancel_observation(state: tauri::State<'_, AppState>, request_id: u64) -> Result<u64, String> {
    let mut guard = state.core.lock().map_err(|_| String::from("core state unavailable"))?;
    let client = guard.as_mut().ok_or_else(|| String::from("core unavailable"))?;
    client.send_cancel(request_id).map_err(|error| format!("{error:?}"))
}

fn main() {
    let state = AppState { core: Mutex::new(CoreClient::start().ok()) };
    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![core_ready, core_health, core_version, core_capabilities, core_observe_health, core_cancel_observation])
        .run(tauri::generate_context!())
        .expect("Tauri runtime failed");
}
"""
    return safe


def selftest() -> None:
    # Preserve all inherited expected rejection reasons before installing the
    # stricter post-review hardening layer.
    shell.selftest()
    _install_v2_policy()

    safe = _safe_v2_fixture()
    fixture = base.MemoryView(safe)
    _verify_shell_rust(fixture)
    _verify_frontend(fixture)
    shell.verify_shell_config(fixture)

    form_escape = dict(safe)
    form_escape["apps/desktop/ui/index.html"] = EXPECTED_HTML.replace(
        "<main>", '<form action="//host.example"><main>'
    ).replace("</main>", "</main></form>").encode()
    base.expect_failure_matching(
        "HTML form egress",
        "frozen non-navigating static presentation template",
        _verify_frontend,
        base.MemoryView(form_escape),
    )

    meta_refresh = dict(safe)
    meta_refresh["apps/desktop/ui/index.html"] = EXPECTED_HTML.replace(
        "<head>", '<head><meta http-equiv="refresh" content="0;url=//host.example">'
    ).encode()
    base.expect_failure_matching(
        "HTML navigation mutation",
        "frozen non-navigating static presentation template",
        _verify_frontend,
        base.MemoryView(meta_refresh),
    )

    observe_receive = dict(safe)
    observe_receive["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"client.send_observe_health().map_err(|error| format!(\"{error:?}\"))",
        b"let request_id = client.send_observe_health().map_err(|error| format!(\"{error:?}\"))?; let _ = client.receive(); Ok(request_id)",
    )
    base.expect_failure_matching(
        "observation holds state across receive",
        "core_observe_health may not call or alias receive",
        _verify_shell_rust,
        base.MemoryView(observe_receive),
    )

    cancel_receive = dict(safe)
    cancel_receive["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(
        b"client.send_cancel(request_id).map_err(|error| format!(\"{error:?}\"))",
        b"let cancel_id = client.send_cancel(request_id).map_err(|error| format!(\"{error:?}\"))?; let _ = client.receive(); Ok(cancel_id)",
    )
    base.expect_failure_matching(
        "cancel holds state across receive",
        "core_cancel_observation may not call or alias receive",
        _verify_shell_rust,
        base.MemoryView(cancel_receive),
    )

    wrong_observe_send = dict(safe)
    wrong_observe_send["apps/desktop/src-tauri/src/main.rs"] = safe[
        "apps/desktop/src-tauri/src/main.rs"
    ].replace(b"send_observe_health()", b"send_health()")
    base.expect_failure_matching(
        "observation wrong send method",
        "core_observe_health may enqueue only send_observe_health",
        _verify_shell_rust,
        base.MemoryView(wrong_observe_send),
    )

    hardcoded_cancel = dict(safe)
    hardcoded_cancel["apps/desktop/ui/app.js"] = safe[
        "apps/desktop/ui/app.js"
    ].replace(b"requestId: observationRequestId", b"requestId: 1")
    base.expect_failure_matching(
        "hard-coded observation cancel identity",
        "cancel the exact stored observation request id",
        _verify_frontend,
        base.MemoryView(hardcoded_cancel),
    )

    print("wepld S1 Tauri shell hardening policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v2_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
