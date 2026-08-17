#!/usr/bin/env python3
"""Bounded S1-010 Tauri shell admission extension over canonical S1-009 policy.

The privileged pull_request_target path executes this policy only from the trusted
PR base and inspects candidate Git objects as data. S1-010 product Rust/UI bytes
execute only in the separate token-minimal pull_request contracts workflow.

This file authorizes one future stage only. It does not implement S1-010.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity.py"
PRIOR_RUNNER_PATH = ".github/scripts/wepld_s1_desktop_integrity.py"
EXPECTED_PRIOR_RUNNER_GIT_BLOB_SHA1 = "36a342d5b7a2b405807fa73a6cc5089e4bdc0fe3"


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _bind_prior_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_desktop_integrity.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-009 policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-009 policy runner drifted: "
            f"expected={EXPECTED_PRIOR_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_runner_before_import()
import wepld_s1_desktop_integrity as desktop_runner  # noqa: E402
import wepld_s1_desktop_integrity_impl as prior  # noqa: E402

SHELL_STAGE = "S1_TAURI_SHELL_CANDIDATE"

S1_010_MARKER_PATHS = frozenset(
    {
        "apps/desktop/src-tauri/build.rs",
        "apps/desktop/src-tauri/tauri.conf.json",
        "apps/desktop/ui/index.html",
        "apps/desktop/ui/app.js",
        "apps/desktop/ui/style.css",
    }
)
S1_010_ALLOWED_PATHS = S1_010_MARKER_PATHS | {
    "apps/desktop/src-tauri/src/main.rs",
}
S1_010_FROZEN_DESKTOP_PATHS = prior.S1_009_ALLOWED_PATHS

MAX_S1_010_RUST_BYTES = 192_000
MAX_S1_010_CONFIG_BYTES = 64_000
MAX_S1_010_HTML_BYTES = 128_000
MAX_S1_010_JS_BYTES = 128_000
MAX_S1_010_CSS_BYTES = 128_000

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "3b1a0605fe317b6043b361cd5b5f4ba35dcf53ad300461c16b0f07ee48d618e6",
    ".github/workflows/s1-admission-integrity.yml": "25ddf87a78ce6d43464246af62c3323b926fe4aec3dcb28b502e0b26e0b7031b",
    ".github/workflows/s1-contracts.yml": "a39b99773304cc2941814a9acf532d04457342774401c6ba58db1ba0e304d2dc",
}

EXPECTED_BUILD_RS = """#![forbid(unsafe_code)]

fn main() {
    tauri_build::build();
}
"""

EXPECTED_TAURI_CONFIG = {
    "productName": "WePLD",
    "version": "0.0.0",
    "identifier": "com.wepld.desktop",
    "build": {"frontendDist": "../ui"},
    "app": {
        "withGlobalTauri": True,
        "windows": [
            {
                "label": "main",
                "title": "WePLD",
                "width": 960,
                "height": 640,
            }
        ],
        "security": {
            "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self'; style-src 'self'; script-src 'self'"
        },
    },
    "bundle": {"active": True, "externalBin": ["binaries/wepld-core"]},
}

SHELL_RUST_PROHIBITED_IDENTIFIERS = frozenset(
    {
        "fs",
        "net",
        "process",
        "env",
        "Command",
        "File",
        "OpenOptions",
        "TcpStream",
        "TcpListener",
        "UdpSocket",
        "UnixStream",
        "UnixListener",
        "NamedPipe",
        "tokio",
        "thread",
        "include",
        "include_bytes",
        "include_str",
        "extern",
        "path",
        "loop",
        "while",
        "for",
        "impl",
        "trait",
        "wepld_contracts",
        "restart",
        "launch_id",
        "drain_diagnostics",
        "diagnostics_truncated",
    }
)

REQUIRED_COMMANDS = frozenset(
    {
        "core_ready",
        "core_health",
        "core_version",
        "core_capabilities",
        "core_observe_health",
        "core_cancel_observation",
    }
)
ALLOWED_FUNCTIONS = REQUIRED_COMMANDS | {"main"}
ALLOWED_TAURI_QUALIFIED = frozenset(
    {"command", "State", "Builder", "generate_handler", "generate_context"}
)

TAURI_COMMAND_FN = re.compile(
    r"#\s*\[\s*tauri\s*::\s*command\s*\]\s*"
    r"(?:pub\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
)
RUST_FN = re.compile(r"\b(?:pub\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
TAURI_QUALIFIED = re.compile(r"\btauri\s*::\s*([A-Za-z_][A-Za-z0-9_]*)")
USE_TAURI = re.compile(r"\buse\s+tauri\b")
GENERATE_HANDLER = re.compile(
    r"tauri\s*::\s*generate_handler!\s*\[([^\]]*)\]",
    re.DOTALL,
)
FORBIDDEN_RUST_TEXT = re.compile(
    r"(?i)(?:tauri[_-]plugin[_-](?:shell|fs|http)|"
    r"plugin\s*\(|https?://|wss?://|powershell|cmd\.exe|/bin/(?:sh|bash|zsh))"
)
MODULE_DECL = re.compile(r"\bmod\s+[A-Za-z_][A-Za-z0-9_]*")

FORBIDDEN_FRONTEND_TEXT = re.compile(
    r"(?i)(?:https?://|wss?://|fetch\s*\(|XMLHttpRequest|WebSocket|EventSource|"
    r"navigator\.sendBeacon|eval\s*\(|new\s+Function\s*\(|"
    r"document\.cookie|localStorage|sessionStorage|"
    r"window\.location|document\.location|innerHTML\s*=|"
    r"import\s*\(|<iframe\b|<object\b|<embed\b)"
)
INVOKE_CALL = re.compile(r"\binvoke\s*\(\s*[\"']([a-z][a-z0-9_]*)[\"']")
ANY_INVOKE_CALL = re.compile(r"\binvoke\s*\(")
REMOTE_OR_ABSOLUTE_ASSET = re.compile(
    r"(?i)(?:src|href)\s*=\s*[\"'](?:[a-z][a-z0-9+.-]*:|//|/)"
)
CSS_EXTERNAL = re.compile(r"(?i)(?:@import\b|url\s*\()")

EXPECTED_HTML_TOKENS = (
    "<main",
    "<h1",
    'role="status"',
    'aria-live="polite"',
    'id="core-readiness"',
    'id="core-health"',
    'id="core-version"',
    'id="core-capabilities"',
    'id="observation-start"',
    'id="observation-cancel"',
    'href="./style.css"',
    'src="./app.js"',
)
EXPECTED_JS_BOOTSTRAP = "window.__TAURI__.core"

# The bootstrap advances only these controlled workflow bytes and installs this
# runner into the protected extension surface. Earlier product/source policy is
# still frozen by the inherited verifiers and trusted-base comparisons.
prior.EXTENSION_CONTROLLED_PATHS = frozenset(
    set(prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
)
prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
    set(prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
)
prior.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256


def _require_s1_009_inputs(paths: set[str], scope: str) -> None:
    missing = prior.S1_009_MARKER_PATHS - paths
    if missing:
        base.fail(
            f"{scope} candidate is missing canonical S1-009 Desktop inputs: "
            + ", ".join(sorted(missing))
        )
    prior._require_process_inputs(paths, scope)


def classify_stage(paths: set[str]) -> str:
    markers = paths & S1_010_MARKER_PATHS
    if markers:
        missing = S1_010_MARKER_PATHS - paths
        if missing:
            base.fail(
                "partial S1-010 Tauri shell candidate is prohibited; missing: "
                + ", ".join(sorted(missing))
            )
        _require_s1_009_inputs(paths, "S1-010 Tauri shell")
        return SHELL_STAGE
    return prior.classify_stage(paths)


def validate_allowed_paths(paths: set[str], stage: str) -> None:
    if stage != SHELL_STAGE:
        prior.validate_allowed_paths(paths, stage)
        return

    allowed = {path for path in paths if base.is_common_allowed(path)}
    allowed |= prior.EXTENSION_CONTROLLED_PATHS
    allowed |= base.STAGE_B_ALL_PATHS
    allowed |= prior.prior.S1_006_ALLOWED_PATHS
    allowed |= prior.prior.S1_007_ALLOWED_PATHS
    allowed |= prior.prior.S1_008_ALLOWED_PATHS
    allowed |= prior.S1_009_ALLOWED_PATHS
    allowed |= S1_010_ALLOWED_PATHS
    allowed |= {
        path
        for path in paths
        if path.startswith(base.FROZEN_GLIB_VENDOR_PREFIX + "/")
    }

    unexpected = sorted(paths - allowed)
    if unexpected:
        base.fail("tracked path outside S1-010 allowlist: " + ", ".join(unexpected))

    missing = sorted(base.REQUIRED_PATHS - paths)
    if missing:
        base.fail("required canonical path missing: " + ", ".join(missing))

    extra_root_src = sorted(
        path for path in paths if path.startswith("src/") and path != "src/.gitkeep"
    )
    if extra_root_src:
        base.fail(
            "root src/ remains a historical placeholder only: "
            + ", ".join(extra_root_src)
        )


def verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-009 policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    prior.verify_policy_files(view)


def _verify_shell_component_base(view: base.RepositoryView, paths: set[str]) -> None:
    expected_text = dict(base.STAGE_B_TEXT)
    expected_text["Cargo.toml"] = base.ROOT_CARGO_COMPONENT
    expected_text.pop("crates/contracts/src/lib.rs")
    expected_text.pop("crates/core/src/main.rs")
    expected_text.pop("apps/desktop/src-tauri/src/main.rs")

    for relative, expected in expected_text.items():
        base.read_text_exact(view, relative, expected)

    lock_bytes = view.read_bytes(base.STAGE_B_LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    base.require_frozen_component_lock_identity(lock_bytes)
    base.validate_lock_bytes(lock_bytes, allow_frozen_glib=True)
    base.verify_frozen_glib_vendor(view, paths, base.COMPONENT_STAGE)


def _read_utf8(view: base.RepositoryView, relative: str, limit: int, scope: str) -> str:
    data = view.read_bytes(relative, limit)
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        base.fail(f"{scope} is not UTF-8: {relative}: {exc}")
    if "\x00" in text:
        base.fail(f"{scope} contains NUL: {relative}")
    return text


def verify_shell_config(view: base.RepositoryView) -> None:
    relative = "apps/desktop/src-tauri/tauri.conf.json"
    text = _read_utf8(view, relative, MAX_S1_010_CONFIG_BYTES, "S1-010 Tauri config")
    try:
        config = json.loads(text)
    except json.JSONDecodeError as exc:
        base.fail(f"S1-010 Tauri config is invalid JSON: {exc}")
    if config != EXPECTED_TAURI_CONFIG:
        base.fail(
            "S1-010 Tauri config must equal the frozen minimal local-static/externalBin template"
        )


def verify_build_script(view: base.RepositoryView) -> None:
    relative = "apps/desktop/src-tauri/build.rs"
    text = _read_utf8(view, relative, MAX_S1_010_RUST_BYTES, "S1-010 build script")
    if text != EXPECTED_BUILD_RS:
        base.fail("S1-010 build.rs must be exactly the minimal tauri_build::build() hook")


def verify_shell_rust(view: base.RepositoryView) -> None:
    relative = "apps/desktop/src-tauri/src/main.rs"
    raw, code = prior.prior._read_rust(
        view, relative, MAX_S1_010_RUST_BYTES, "S1-010 Tauri main"
    )
    prior.prior._require_forbid(raw, relative, "S1-010")
    if desktop_runner.DESKTOP_PATH_ATTRIBUTE.search(code):
        base.fail("S1-010 Tauri main #[path]/cfg_attr path indirection is prohibited")

    identifiers = set(prior.prior.RUST_IDENTIFIER.findall(code))
    forbidden = sorted(identifiers & SHELL_RUST_PROHIBITED_IDENTIFIERS)
    if forbidden:
        base.fail(
            "S1-010 Tauri main prohibited effect identifier(s): "
            + ", ".join(forbidden)
        )
    if FORBIDDEN_RUST_TEXT.search(raw):
        base.fail("S1-010 Tauri main contains prohibited plugin/network/shell material")
    if MODULE_DECL.search(code):
        base.fail("S1-010 Tauri main may not introduce local modules")
    if USE_TAURI.search(code):
        base.fail("S1-010 Tauri main may not alias/import the Tauri crate")

    tauri_names = set(TAURI_QUALIFIED.findall(code))
    unexpected_tauri = sorted(tauri_names - ALLOWED_TAURI_QUALIFIED)
    if unexpected_tauri:
        base.fail(
            "S1-010 Tauri main may use only the frozen Tauri API primitives; unexpected: "
            + ", ".join(unexpected_tauri)
        )

    functions = RUST_FN.findall(code)
    if set(functions) != ALLOWED_FUNCTIONS or len(functions) != len(ALLOWED_FUNCTIONS):
        base.fail(
            "S1-010 Tauri main functions must be exactly main plus the six frozen commands"
        )

    if len(re.findall(r"\btauri\s*::\s*Builder\s*::\s*default\s*\(", code)) != 1:
        base.fail("S1-010 Tauri main must construct exactly one tauri::Builder::default()")
    if len(re.findall(r"\.\s*manage\s*\(", code)) != 1:
        base.fail("S1-010 Tauri main must install exactly one bounded app state")
    if len(re.findall(r"\.\s*invoke_handler\s*\(", code)) != 1:
        base.fail("S1-010 Tauri main must expose exactly one invoke handler")
    if len(
        re.findall(
            r"\.\s*run\s*\(\s*tauri\s*::\s*generate_context!\s*\(\s*\)\s*\)",
            code,
        )
    ) != 1:
        base.fail("S1-010 Tauri main must run only the generated local Tauri context")

    commands = TAURI_COMMAND_FN.findall(code)
    if set(commands) != REQUIRED_COMMANDS or len(commands) != len(REQUIRED_COMMANDS):
        base.fail(
            "S1-010 Tauri main command surface must be exactly: "
            + ", ".join(sorted(REQUIRED_COMMANDS))
        )
    handlers = GENERATE_HANDLER.findall(code)
    if len(handlers) != 1:
        base.fail("S1-010 Tauri main must define exactly one generate_handler list")
    handler_names = {
        match.group(0)
        for match in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*", handlers[0])
    }
    if handler_names != REQUIRED_COMMANDS:
        base.fail("S1-010 generate_handler must expose exactly the six S1 commands")

    if "wepld_desktop::CoreClient" not in code:
        base.fail("S1-010 Tauri main must project only through canonical CoreClient")
    if "std::sync::Mutex" not in code:
        base.fail("S1-010 Tauri main must serialize CoreClient access with std::sync::Mutex")
    if "CoreClient::start" not in code:
        base.fail("S1-010 Tauri main must initialize the canonical owned CoreClient")


def verify_frontend(view: base.RepositoryView) -> None:
    html = _read_utf8(
        view, "apps/desktop/ui/index.html", MAX_S1_010_HTML_BYTES, "S1-010 HTML"
    )
    js = _read_utf8(
        view, "apps/desktop/ui/app.js", MAX_S1_010_JS_BYTES, "S1-010 JavaScript"
    )
    css = _read_utf8(
        view, "apps/desktop/ui/style.css", MAX_S1_010_CSS_BYTES, "S1-010 CSS"
    )

    for relative, text in (
        ("apps/desktop/ui/index.html", html),
        ("apps/desktop/ui/app.js", js),
    ):
        if FORBIDDEN_FRONTEND_TEXT.search(text):
            base.fail(
                f"S1-010 static frontend contains prohibited dynamic/network material: {relative}"
            )

    if REMOTE_OR_ABSOLUTE_ASSET.search(html):
        base.fail("S1-010 HTML assets must be local relative files only")
    if CSS_EXTERNAL.search(css):
        base.fail("S1-010 CSS may not import or fetch external assets")
    if "<script" in html and 'src="./app.js"' not in html:
        base.fail("S1-010 HTML script surface must be the local ./app.js only")
    if html.count("<script") != 1 or html.count("</script>") != 1:
        base.fail("S1-010 HTML must contain exactly one external script element")
    if html.count("<link") != 1 or 'href="./style.css"' not in html:
        base.fail("S1-010 HTML must contain exactly one local stylesheet link")

    missing_tokens = [token for token in EXPECTED_HTML_TOKENS if token not in html]
    if missing_tokens:
        base.fail(
            "S1-010 HTML missing required static/accessibility token(s): "
            + ", ".join(missing_tokens)
        )

    if js.count(EXPECTED_JS_BOOTSTRAP) != 1 or js.count("__TAURI__") != 1:
        base.fail("S1-010 JavaScript may expose only window.__TAURI__.core")
    calls = INVOKE_CALL.findall(js)
    all_invoke_count = len(ANY_INVOKE_CALL.findall(js))
    if all_invoke_count != len(calls):
        base.fail("S1-010 JavaScript invoke calls must all use literal frozen command names")
    if set(calls) != REQUIRED_COMMANDS or len(calls) != len(REQUIRED_COMMANDS):
        base.fail(
            "S1-010 JavaScript invoke surface must call each frozen command exactly once: "
            + ", ".join(sorted(REQUIRED_COMMANDS))
        )


def verify_shell_sources(view: base.RepositoryView) -> None:
    verify_build_script(view)
    verify_shell_config(view)
    verify_shell_rust(view)
    verify_frontend(view)


def freeze_s1_009_desktop(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    for relative in sorted(S1_010_FROZEN_DESKTOP_PATHS):
        if candidate.read_bytes(relative, prior.MAX_S1_009_SOURCE_BYTES) != policy_base.read_bytes(
            relative, prior.MAX_S1_009_SOURCE_BYTES
        ):
            base.fail(f"S1-010 candidate changed frozen S1-009 Desktop lifecycle: {relative}")


def verify_view(
    view: base.RepositoryView,
    *,
    policy_base: base.RepositoryView | None = None,
) -> str:
    paths = base.validate_entries(view.entries())
    stage = classify_stage(paths)

    # The bootstrap tree has no S1-010 product marker. Preserve full S1-009
    # verification while recognizing only this new controlled policy script and
    # exact workflow-byte advance.
    if stage != SHELL_STAGE:
        return prior.verify_view(view, policy_base=policy_base)

    validate_allowed_paths(paths, stage)
    if view.read_bytes("src/.gitkeep", 1):
        base.fail("src/.gitkeep must be empty")

    base.verify_reviewer_configs(view)
    base.verify_dependency_register(view)
    base.verify_archive(view)
    verify_policy_files(view)

    _verify_shell_component_base(view, paths)
    prior.prior.verify_protocol_sources(view)
    prior.prior.verify_state_sources(view)
    prior.prior.verify_process_sources(view)
    prior.verify_desktop_sources(view)
    verify_shell_sources(view)

    if any(path.startswith(".github/repair-payload/") for path in paths):
        base.fail("repair payload leaked into active tree")
    if "docs/canonical/CODEX_SECURITY_REVIEW_POLICY.md" in paths:
        base.fail("duplicate canonical security-review policy detected")

    if policy_base is not None:
        base.verify_base_path_preservation(
            paths, base.validate_entries(policy_base.entries())
        )
        base.compare_base_controlled(view, policy_base)
        prior.verify_extension_controlled_paths(view, policy_base)
        prior.prior.freeze_s1_005_evidence(view, policy_base)
        prior.prior.freeze_s1_006_protocol(view, policy_base)
        prior.prior.freeze_s1_007_state(view, policy_base)
        prior.freeze_s1_008_process(view, policy_base)
        freeze_s1_009_desktop(view, policy_base)

    return stage


def _safe_shell_fixture() -> dict[str, bytes]:
    main = b"""#![forbid(unsafe_code)]
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
fn core_observe_health(_state: tauri::State<'_, AppState>) -> Result<u64, String> { Ok(0) }
#[tauri::command]
fn core_cancel_observation(_state: tauri::State<'_, AppState>, _request_id: u64) -> Result<String, String> { Ok(String::new()) }

fn main() {
    let state = AppState { core: Mutex::new(CoreClient::start().ok()) };
    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![core_ready, core_health, core_version, core_capabilities, core_observe_health, core_cancel_observation])
        .run(tauri::generate_context!())
        .expect("Tauri runtime failed");
}
"""
    html = b"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WePLD</title><link rel="stylesheet" href="./style.css"></head>
<body><main><h1>WePLD</h1><section role="status" aria-live="polite"><p id="core-readiness"></p><p id="core-health"></p><p id="core-version"></p><p id="core-capabilities"></p></section><button id="observation-start" type="button">Start observation</button><button id="observation-cancel" type="button">Cancel observation</button></main><script src="./app.js" defer></script></body></html>
"""
    js = b"""const { invoke } = window.__TAURI__.core;
async function refresh() { await invoke("core_ready"); await invoke("core_health"); await invoke("core_version"); await invoke("core_capabilities"); }
document.getElementById("observation-start").addEventListener("click", async () => { await invoke("core_observe_health"); });
document.getElementById("observation-cancel").addEventListener("click", async () => { await invoke("core_cancel_observation", { requestId: 1 }); });
refresh();
"""
    css = b"""html { font-family: system-ui, sans-serif; }
body { margin: 0; }
main { max-width: 48rem; margin: 0 auto; padding: 2rem; }
button:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
"""
    return {
        "apps/desktop/src-tauri/build.rs": EXPECTED_BUILD_RS.encode(),
        "apps/desktop/src-tauri/tauri.conf.json": (
            json.dumps(EXPECTED_TAURI_CONFIG, indent=2) + "\n"
        ).encode(),
        "apps/desktop/src-tauri/src/main.rs": main,
        "apps/desktop/ui/index.html": html,
        "apps/desktop/ui/app.js": js,
        "apps/desktop/ui/style.css": css,
    }


def selftest() -> None:
    # Run inherited tests before installing the stricter S1-010 path detector so
    # their expected rejection reasons remain stable.
    prior.selftest()
    desktop_runner.selftest_runner()

    base_paths = set(base.REQUIRED_PATHS) | {"README.md", "src/.gitkeep"}
    component_paths = (
        base_paths
        | set(base.STAGE_B_ALL_PATHS)
        | {base.FROZEN_GLIB_VENDOR_PREFIX + "/src/variant_iter.rs"}
        | set(prior.EXTENSION_CONTROLLED_PATHS)
    )
    protocol_paths = component_paths | set(prior.prior.S1_006_MARKER_PATHS)
    state_paths = protocol_paths | set(prior.prior.S1_007_MARKER_PATHS)
    process_paths = state_paths | set(prior.prior.S1_008_MARKER_PATHS)
    desktop_paths = process_paths | set(prior.S1_009_MARKER_PATHS)
    shell_paths = desktop_paths | set(S1_010_ALLOWED_PATHS)

    if classify_stage(desktop_paths) != prior.DESKTOP_STAGE:
        base.fail("S1-010 self-test: prior Desktop stage compatibility failed")
    validate_allowed_paths(desktop_paths, prior.DESKTOP_STAGE)
    if classify_stage(shell_paths) != SHELL_STAGE:
        base.fail("S1-010 self-test: shell-stage classification failed")
    validate_allowed_paths(shell_paths, SHELL_STAGE)

    base.expect_failure_matching(
        "partial S1-010 shell candidate",
        "partial S1-010 Tauri shell candidate is prohibited",
        classify_stage,
        desktop_paths | {"apps/desktop/src-tauri/tauri.conf.json"},
    )
    base.expect_failure_matching(
        "tracked sidecar binary",
        "tracked path outside S1-010 allowlist",
        validate_allowed_paths,
        shell_paths
        | {"apps/desktop/src-tauri/binaries/wepld-core-x86_64-pc-windows-msvc.exe"},
        SHELL_STAGE,
    )
    base.expect_failure_matching(
        "frontend package manager",
        "tracked path outside S1-010 allowlist",
        validate_allowed_paths,
        shell_paths | {"apps/desktop/package.json"},
        SHELL_STAGE,
    )
    base.expect_failure_matching(
        "capability expansion",
        "tracked path outside S1-010 allowlist",
        validate_allowed_paths,
        shell_paths | {"apps/desktop/src-tauri/capabilities/default.json"},
        SHELL_STAGE,
    )

    safe = _safe_shell_fixture()
    fixture = base.MemoryView(safe)
    verify_build_script(fixture)
    verify_shell_config(fixture)
    verify_shell_rust(fixture)
    verify_frontend(fixture)

    bad_build = dict(safe)
    bad_build["apps/desktop/src-tauri/build.rs"] = (
        b"#![forbid(unsafe_code)]\nfn main() { println!(\"cargo:rustc-env=ESCAPE=1\"); tauri_build::build(); }\n"
    )
    base.expect_failure_matching(
        "build-script effect expansion",
        "S1-010 build.rs must be exactly",
        verify_build_script,
        base.MemoryView(bad_build),
    )

    bad_config = dict(safe)
    config = dict(EXPECTED_TAURI_CONFIG)
    config["plugins"] = {"shell": {}}
    bad_config["apps/desktop/src-tauri/tauri.conf.json"] = (
        json.dumps(config, indent=2) + "\n"
    ).encode()
    base.expect_failure_matching(
        "shell plugin config",
        "frozen minimal local-static/externalBin template",
        verify_shell_config,
        base.MemoryView(bad_config),
    )

    remote_ui = dict(safe)
    remote_ui["apps/desktop/ui/app.js"] = (
        safe["apps/desktop/ui/app.js"] + b'fetch("https://example.invalid");\n'
    )
    base.expect_failure_matching(
        "frontend network escape",
        "prohibited dynamic/network material",
        verify_frontend,
        base.MemoryView(remote_ui),
    )

    dynamic_ui = dict(safe)
    dynamic_ui["apps/desktop/ui/app.js"] = (
        safe["apps/desktop/ui/app.js"]
        + b'document.body.innerHTML = "<p>escape</p>";\n'
    )
    base.expect_failure_matching(
        "frontend innerHTML escape",
        "prohibited dynamic/network material",
        verify_frontend,
        base.MemoryView(dynamic_ui),
    )

    dynamic_invoke = dict(safe)
    dynamic_invoke["apps/desktop/ui/app.js"] = (
        safe["apps/desktop/ui/app.js"]
        + b'const extraCommand = "core_health"; invoke(extraCommand);\n'
    )
    base.expect_failure_matching(
        "dynamic invoke escape",
        "invoke calls must all use literal frozen command names",
        verify_frontend,
        base.MemoryView(dynamic_invoke),
    )

    tauri_global_escape = dict(safe)
    tauri_global_escape["apps/desktop/ui/app.js"] = (
        safe["apps/desktop/ui/app.js"] + b"void window.__TAURI__.event;\n"
    )
    base.expect_failure_matching(
        "Tauri global escape",
        "may expose only window.__TAURI__.core",
        verify_frontend,
        base.MemoryView(tauri_global_escape),
    )

    process_escape = dict(safe)
    process_escape["apps/desktop/src-tauri/src/main.rs"] = (
        safe["apps/desktop/src-tauri/src/main.rs"]
        + b"fn escape() { let _ = std::process::Command::new(\"cmd.exe\"); }\n"
    )
    base.expect_failure_matching(
        "Tauri main nested process",
        "S1-010 Tauri main prohibited effect identifier",
        verify_shell_rust,
        base.MemoryView(process_escape),
    )

    tauri_api_escape = dict(safe)
    tauri_api_escape["apps/desktop/src-tauri/src/main.rs"] = (
        safe["apps/desktop/src-tauri/src/main.rs"]
        + b"fn escape(_app: tauri::AppHandle) {}\n"
    )
    base.expect_failure_matching(
        "extra Tauri API",
        "may use only the frozen Tauri API primitives",
        verify_shell_rust,
        base.MemoryView(tauri_api_escape),
    )

    helper_escape = dict(safe)
    helper_escape["apps/desktop/src-tauri/src/main.rs"] = (
        safe["apps/desktop/src-tauri/src/main.rs"] + b"fn helper() {}\n"
    )
    base.expect_failure_matching(
        "extra helper function",
        "functions must be exactly main plus the six frozen commands",
        verify_shell_rust,
        base.MemoryView(helper_escape),
    )

    extra_command = dict(safe)
    extra_command["apps/desktop/src-tauri/src/main.rs"] = (
        safe["apps/desktop/src-tauri/src/main.rs"]
        + b"#[tauri::command]\nfn arbitrary() {}\n"
    )
    base.expect_failure_matching(
        "extra Tauri command",
        "functions must be exactly main plus the six frozen commands",
        verify_shell_rust,
        base.MemoryView(extra_command),
    )

    print("wepld S1 Tauri shell integrity policy self-tests: PASS")


def print_success(stage: str, mode: str) -> None:
    if stage != SHELL_STAGE:
        prior.print_success(stage, mode)
        return

    print("wepld integrity verification: PASS")
    print(f"mode={mode}")
    print(f"stage={stage}")
    print(f"canonical_archive_sha256={base.EXPECTED_ARCHIVE_SHA256}")
    print(f"master_plan_sha256={base.EXPECTED_PLAN_SHA256}")
    print(f"source_registry_entries={base.EXPECTED_SOURCE_REGISTRY_ENTRIES}")
    print("source_admission=0")
    print("source_acquisition_check=PASS")
    print("runtime_dependency_admission=EXACT_S1_GRAPH")
    print("cubic_provider_effective_state=NOT_PROVEN_SAFE_BY_REPOSITORY_POLICY")
    print("product_implementation_authorized=S1_010_ONLY")


def main(argv: list[str]) -> int:
    args = base.parse_args(argv)
    try:
        if args.command == "selftest":
            selftest()
            return 0

        desktop_runner._install_desktop_path_attribute()
        token = os.environ.get(args.github_token_env) or None
        client = base.GitHubClient(token)

        if args.command == "verify-local":
            view = base.LocalRepositoryView(Path(args.root))
            stage = verify_view(view)
            if args.remote_baseline:
                desktop_runner.verify_remote_baseline(client, args.pr_base_sha)
            print_success(stage, "LOCAL_CHECKOUT")
            return 0

        policy_base = base.LocalRepositoryView(Path(args.policy_root))
        candidate = base.RemoteRepositoryView(args.repository, args.sha, client)
        stage = verify_view(candidate, policy_base=policy_base)
        desktop_runner.verify_remote_baseline(client, args.pr_base_sha)
        print_success(stage, "REMOTE_CANDIDATE_DATA_ONLY")
        return 0

    except base.PolicyError as exc:
        print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
