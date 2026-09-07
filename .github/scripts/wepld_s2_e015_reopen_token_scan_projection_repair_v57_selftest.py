#!/usr/bin/env python3
"""Self-tests for the v57 S2-E015 reopen token-scan projection repair.

v57 must:
  * run the full frozen v56 -> v55 -> ... self-test cascade with v56's two
    PRE-only real-tree assertions replaced by PRE-or-POST-agnostic equivalents
    (this is `run_predecessor_selftests`, run first);
  * accept the exact authorized S2-E015 fixture through the projected
    identity/store product verify - the reduced token scan plus a re-assertion
    of v55's child-process static bound;
  * still fully scan `identity.rs` and `evidence_store.rs` under that same
    projected verify;
  * still reject every forbidden token that is not one of the four authorized
    re-exec exceptions, in the reopened test file;
  * behave exactly like the inherited v28 hardened verifier for every other
    path and for the reopened path in any non-authorized state;
  * grant no new authority and widen nothing.
"""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_e015_reopen_token_scan_projection_repair_v57_integrity as p

_OVERLAY_VIEW_COUNTER = itertools.count()

IDPATH = p.IDENTITY_STORE_TEST
IDENTITY_SRC = "crates/core/src/identity.rs"
STORE_SRC = "crates/core/src/evidence_store.rs"


class OverlayView:
    def __init__(
        self,
        view: Any,
        replacements: dict[str, bytes] | None = None,
        *,
        omitted: frozenset[str] = frozenset(),
    ) -> None:
        self._view = view
        self._replacements = replacements or {}
        self._omitted = omitted
        self._instance_id = next(_OVERLAY_VIEW_COUNTER)

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._omitted:
            raise FileNotFoundError(path)
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v57 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        result = [e for e in self._view.entries() if e.path not in self._omitted]
        known = {e.path for e in result}
        for path in self._replacements:
            if path not in known and path not in self._omitted:
                result.append(base.TrackedEntry(mode="100644", path=path))
        return result

    def tree_identity(self, path: str) -> Any:
        return (self._instance_id, path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any, expected: str) -> None:
    try:
        action()
    except (base.PolicyError, FileNotFoundError) as exc:
        if expected not in str(exc):
            base.fail(f"v57 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v57 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_E015_REOPEN_TOKEN_SCAN_PROJECTION_REPAIR_ONLY":
        base.fail("v57 authority marker drift")
    if p.V57_POLICY_REPAIR != "NOT_NEW_RUNTIME_AUTHORITY":
        base.fail("v57 must declare it grants no new runtime authority")
    if p.TOKEN_SCAN_EXCEPTION != "NOT_TOKEN_SCAN_REMOVAL":
        base.fail("v57 token-scan-exception marker drift")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v57 next authority gate drift")
    for name in p._INHERITED_AUTHORITY_NAMES:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v57 changed inherited authority: {name}")
    for name in (
        "NETWORK_AUTHORITY",
        "MODEL_PROVIDER_EXECUTION",
        "S3_PLUS_AUTHORITY",
        "GENERAL_SHELL_AUTHORITY",
        "ARBITRARY_PROCESS_AUTHORITY",
        "PACKAGE_INSTALL_AUTHORITY",
        "PROJECT_NATIVE_COMMAND_EXECUTION",
        "GIT_MUTATION_AUTHORITY",
        "SAFE_DIRECTORY_MUTATION_AUTHORITY",
        "REMEDIATION_EXECUTION_AUTHORITY",
    ):
        if getattr(p, name) != "NONE":
            base.fail(f"v57 must not grant {name}")
    if p.TEST_CHILD_PROCESS_AUTHORITY != "RE_EXEC_CURRENT_TEST_BINARY_ONLY":
        base.fail("v57 TEST_CHILD_PROCESS_AUTHORITY drift")
    if p.AUTHORIZED_POST_REOPEN_BLOB != p.q.AUTHORIZED_POST_REOPEN_BLOB:
        base.fail("v57 authorized-post-reopen blob must equal the inherited v56 value")


def _check_exception_set_is_a_strict_subset() -> None:
    expected = frozenset({b"std::process", b"Command::", b"std::env", b"expect("})
    if p._AUTHORIZED_TEST_TOKEN_EXCEPTIONS != expected:
        base.fail(f"v57 authorized token exception set drifted: {p._AUTHORIZED_TEST_TOKEN_EXCEPTIONS}")
    forbidden = frozenset(p._v25support.FORBIDDEN_PRODUCT_TOKENS)
    if not p._AUTHORIZED_TEST_TOKEN_EXCEPTIONS <= forbidden:
        base.fail("v57 exceptions must be a subset of the inherited forbidden set")
    for must_stay in (b"unwrap(", b"panic!", b"std::net", b"unsafe {", b"reqwest", b"tokio"):
        if must_stay in p._AUTHORIZED_TEST_TOKEN_EXCEPTIONS:
            base.fail(f"v57 must never except {must_stay!r}")
        if must_stay not in forbidden:
            base.fail(f"v57 sanity: {must_stay!r} is expected in the inherited forbidden set")


def _check_authorized_fixture_passes_the_projected_verify() -> None:
    # The exact authorized fixture bytes (carried by v56) pass v57's projected
    # product verify end to end: reduced token scan + v55 child-process bound
    # re-assertion + full scan of identity.rs / evidence_store.rs.
    view = OverlayView(p.raw_root, {IDPATH: p.q._POST_REOPEN_BYTES})
    p._v57_hardened_product_verify(view)
    p._scan_authorized_reopen_test(view)


def _check_non_authorized_state_delegates_unchanged() -> None:
    if p._v57_hardened_product_verify is p._V28_HARDENED:
        base.fail("v57 product-verify must be a real wrapper, not the inherited hook")
    # Real tree (PRE on main, POST on the fixture branch) - must not raise.
    p._v57_hardened_product_verify(p.raw_root)
    # An explicit PRE view delegates to the inherited v28 hardened verifier,
    # which passes on the clean pre-reopen file.
    pre_view = OverlayView(p.raw_root, {IDPATH: p.q._PRE_REOPEN_BYTES})
    p._v57_hardened_product_verify(pre_view)
    p._V28_HARDENED(pre_view)


def _check_identity_and_store_still_fully_scanned() -> None:
    # Under the authorized-POST path, identity.rs / evidence_store.rs are still
    # scanned against the full forbidden-token set - v57's exception is scoped
    # to the one reopened test file only.
    for src_path in (IDENTITY_SRC, STORE_SRC):
        tainted = p.raw_root.read_bytes(src_path, base.MAX_POLICY_FILE_BYTES) + (
            b"\nfn _v57_selftest_taint() { let _ = std::process::id(); }\n"
        )
        view = OverlayView(
            p.raw_root, {IDPATH: p.q._POST_REOPEN_BYTES, src_path: tainted}
        )
        _expect_failure(
            f"v57 still fully scans {src_path} under the authorized-POST path",
            lambda view=view: p._v57_hardened_product_verify(view),
            "std::process",
        )


def _check_reduced_scan_still_rejects_non_excepted_tokens() -> None:
    # Bytes hashing to a chosen blob cannot be constructed, so move the pin for
    # the duration of one call, exactly as the v38/v40 self-tests do.
    saved = p.AUTHORIZED_POST_REOPEN_BLOB
    bad = (
        b"#![forbid(unsafe_code)]\n"
        b"// v57 self-test: authorized exceptions present, plus a forbidden one\n"
        b"fn _c() {\n"
        b"    let exe = std::env::current_exe().unwrap();\n"
        b"    let _ = std::process::Command::new(exe);\n"
        b"}\n"
    )
    bad_blob = p.V25.blob(bad)
    try:
        p.AUTHORIZED_POST_REOPEN_BLOB = bad_blob
        view = OverlayView(p.raw_root, {IDPATH: bad})
        _expect_failure(
            "v57 reduced scan still rejects unwrap( in the reopened test file",
            lambda: p._scan_authorized_reopen_test(view),
            "unwrap(",
        )
    finally:
        p.AUTHORIZED_POST_REOPEN_BLOB = saved
    if p.AUTHORIZED_POST_REOPEN_BLOB != saved:
        base.fail("v57 self-test left the authorized-post-reopen pin moved")


def _check_scan_reasserts_the_v55_child_process_bound() -> None:
    saved = p.AUTHORIZED_POST_REOPEN_BLOB
    # No forbidden non-exception token, but a string-literal executable - v55's
    # static bound must still reject it via v57's re-assertion.
    bad = (
        b"#![forbid(unsafe_code)]\n"
        b"fn _c() { let _ = std::process::Command::new(\"sh\").status(); }\n"
    )
    try:
        p.AUTHORIZED_POST_REOPEN_BLOB = p.V25.blob(bad)
        view = OverlayView(p.raw_root, {IDPATH: bad})
        _expect_failure(
            "v57 re-asserts the v55 child-process static bound on the fixture",
            lambda: p._scan_authorized_reopen_test(view),
            "string-literal executable",
        )
    finally:
        p.AUTHORIZED_POST_REOPEN_BLOB = saved


def _boot_base() -> OverlayView:
    return OverlayView(
        p.raw_root, p._workflow_replacements(p.raw_root), omitted=p.POLICY_FILES
    )


def _check_v57_delta_and_files_freeze() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v57 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v57 controlled-file set must equal policy-file set")

    p.delta(p.raw_root, _boot_base())
    p.files(p.raw_root)

    tampered = OverlayView(
        p.raw_root,
        {p.P: p.raw_root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# x\n"},
    )
    _expect_failure(
        "v57 policy files are frozen after activation",
        lambda: p.delta(tampered, p.raw_root),
        "frozen after activation",
    )
    smuggled = OverlayView(
        p.raw_root, {"docs/canonical/UNAUTHORIZED_V57_BOOTSTRAP.md": b"# smuggled\n"}
    )
    _expect_failure(
        "v57 bootstrap must be exactly the four bootstrap paths",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v57 policy files",
    )


def _check_workflow_projection_reverses() -> None:
    projected = p._project_for_v56(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v57 workflow projection does not reverse to exact v56: {path}")
        if p._V57_ENTRYPOINT in data:
            base.fail(f"v57 workflow projection left the v57 entrypoint: {path}")
    raw_fw = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES)
    drifted = raw_fw.replace(p._V57_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1)
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "v57 rejects a drifted workflow entrypoint count",
        lambda: p._workflow_replacements(view),
        "entrypoint count drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_exception_set_is_a_strict_subset()
    _check_authorized_fixture_passes_the_projected_verify()
    _check_non_authorized_state_delegates_unchanged()
    _check_identity_and_store_still_fully_scanned()
    _check_reduced_scan_still_rejects_non_excepted_tokens()
    _check_scan_reasserts_the_v55_child_process_bound()
    _check_workflow_projection_reverses()
    _check_v57_delta_and_files_freeze()
    p.install()
    p.overlay()
    print("wepld v57 S2-E015 reopen token-scan projection repair self-tests: PASS")


if __name__ == "__main__":
    run()
