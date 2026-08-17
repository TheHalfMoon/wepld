#!/usr/bin/env python3
"""Final hardening wrapper for the bounded S1-010 Tauri shell admission policy.

This wrapper binds the exact prior v2 shell-admission runner before import, then
freezes the future HTML and app.js bytes. The exact presentation both closes
comment/alias/indirect-invoke bypasses and requires the S1-010 UI to project
Core readiness, health, version, capabilities, and cancellable observation
state without adding network, filesystem, shell, or dynamic-HTML authority.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v3.py"
PRIOR_V2_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v2.py"
EXPECTED_PRIOR_V2_RUNNER_GIT_BLOB_SHA1 = "484907e0d216fe13550201b56cd214510291c31f"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "cbf8970348efbe2a797e10e3e8f75b8879a5ae19137a39f32e8530d7d32b904a",
    ".github/workflows/s1-admission-integrity.yml": "e8f4da72cc116c82c91acd19b3a83dd6e8cdeb98c9277a4bd935b00bf0a801e3",
    ".github/workflows/s1-contracts.yml": "a55826887801083d3aee0c24524094ea61154d883f1bf318111ae39aadec40e7",
}

EXPECTED_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WePLD</title><link rel="stylesheet" href="./style.css"></head>
<body><main><h1>WePLD</h1><section role="status" aria-live="polite"><p id="core-readiness"></p><p id="core-health"></p><p id="core-version"></p><p id="core-capabilities"></p><p id="observation-status">Observation idle</p></section><button id="observation-start" type="button">Start observation</button><button id="observation-cancel" type="button">Cancel observation</button></main><script src="./app.js" defer></script></body></html>
"""

EXPECTED_JS = """const { invoke } = window.__TAURI__.core;
const readinessStatus = document.getElementById("core-readiness");
const healthStatus = document.getElementById("core-health");
const versionStatus = document.getElementById("core-version");
const capabilitiesStatus = document.getElementById("core-capabilities");
const observationStatus = document.getElementById("observation-status");
let observationRequestId = null;

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
  try {
    observationRequestId = await invoke("core_observe_health");
    observationStatus.textContent = "Observation active";
  } catch (_error) {
    observationRequestId = null;
    observationStatus.textContent = "Observation unavailable";
  }
});

document.getElementById("observation-cancel").addEventListener("click", async () => {
  if (observationRequestId === null) return;
  try {
    await invoke("core_cancel_observation", { requestId: observationRequestId });
    observationRequestId = null;
    observationStatus.textContent = "Observation cancelled";
  } catch (_error) {
    observationStatus.textContent = "Cancellation failed";
  }
});

refresh();
"""

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_v2_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v2.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v2 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V2_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v2 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V2_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v2_runner_before_import()
import wepld_s1_shell_integrity_v2 as v2  # noqa: E402


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V2_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V2_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v2 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V2_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v2._verify_policy_files(view)


def _verify_frontend(view: base.RepositoryView) -> None:
    v2._verify_frontend(view)
    html = v2.shell._read_utf8(
        view,
        "apps/desktop/ui/index.html",
        v2.shell.MAX_S1_010_HTML_BYTES,
        "S1-010 HTML",
    )
    if html != EXPECTED_HTML:
        base.fail(
            "S1-010 HTML must equal the frozen status-projection presentation template"
        )
    js = v2.shell._read_utf8(
        view,
        "apps/desktop/ui/app.js",
        v2.shell.MAX_S1_010_JS_BYTES,
        "S1-010 JavaScript",
    )
    if js != EXPECTED_JS:
        base.fail(
            "S1-010 JavaScript must equal the frozen direct-invoke/status-projection/request-identity template"
        )


def _install_v3_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v2._install_v2_policy()

    v2.EXPECTED_HTML = EXPECTED_HTML
    v2.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v2.shell.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256
    v2.shell.prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    v2.shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v2.shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(v2.shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    v2.shell.verify_policy_files = _verify_policy_files
    v2.shell.verify_frontend = _verify_frontend
    _INSTALLED = True


def _safe_v3_fixture() -> dict[str, bytes]:
    safe = v2._safe_v2_fixture()
    safe["apps/desktop/ui/index.html"] = EXPECTED_HTML.encode()
    safe["apps/desktop/ui/app.js"] = EXPECTED_JS.encode()
    return safe


def selftest() -> None:
    # Preserve inherited expected rejection reasons first, then install the
    # exact-presentation hardening layer for the new tests and runtime verifier.
    v2.selftest()
    _install_v3_policy()

    safe = _safe_v3_fixture()
    fixture = base.MemoryView(safe)
    _verify_frontend(fixture)
    v2._verify_shell_rust(fixture)
    v2.shell.verify_shell_config(fixture)

    comment_indirect = dict(safe)
    comment_indirect["apps/desktop/ui/app.js"] = b"""const { invoke } = window.__TAURI__.core;
let observationRequestId = null;
// await invoke("core_ready");
// await invoke("core_health");
// await invoke("core_version");
// await invoke("core_capabilities");
// observationRequestId = await invoke("core_observe_health");
// invoke("core_cancel_observation", { requestId: observationRequestId });
await (invoke)("core_ready");
await (invoke)("core_health");
await (invoke)("core_version");
await (invoke)("core_capabilities");
await (invoke)("core_observe_health");
await (invoke)("core_cancel_observation", { requestId: 1 });
"""
    base.expect_failure_matching(
        "comment plus indirect invoke bypass",
        "frozen direct-invoke/status-projection/request-identity template",
        _verify_frontend,
        base.MemoryView(comment_indirect),
    )

    harmless_comment = dict(safe)
    harmless_comment["apps/desktop/ui/app.js"] = (
        EXPECTED_JS + "// no executable authority should be variable\n"
    ).encode()
    base.expect_failure_matching(
        "JavaScript comment mutation",
        "frozen direct-invoke/status-projection/request-identity template",
        _verify_frontend,
        base.MemoryView(harmless_comment),
    )

    alias_invoke = dict(safe)
    alias_invoke["apps/desktop/ui/app.js"] = EXPECTED_JS.replace(
        '    healthStatus.textContent = `Health: ${String(await invoke("core_health"))}`;',
        '    // await invoke("core_health");\n'
        '    const callCore = invoke;\n'
        '    healthStatus.textContent = `Health: ${String(await callCore("core_health"))}`;',
        1,
    ).encode()
    base.expect_failure_matching(
        "JavaScript invoke alias",
        "frozen direct-invoke/status-projection/request-identity template",
        _verify_frontend,
        base.MemoryView(alias_invoke),
    )

    discarded_projection = dict(safe)
    discarded_projection["apps/desktop/ui/app.js"] = EXPECTED_JS.replace(
        '    readinessStatus.textContent = `Ready: ${String(await invoke("core_ready"))}`;',
        '    await invoke("core_ready");',
        1,
    ).encode()
    base.expect_failure_matching(
        "discarded readiness projection",
        "frozen direct-invoke/status-projection/request-identity template",
        _verify_frontend,
        base.MemoryView(discarded_projection),
    )

    missing_observation_status = dict(safe)
    missing_observation_status["apps/desktop/ui/index.html"] = EXPECTED_HTML.replace(
        '<p id="observation-status">Observation idle</p>',
        "",
        1,
    ).encode()
    base.expect_failure_matching(
        "missing observation status projection",
        "frozen status-projection presentation template",
        _verify_frontend,
        base.MemoryView(missing_observation_status),
    )

    print("wepld S1 Tauri shell exact-presentation policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v3_policy()
    return v2.shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
