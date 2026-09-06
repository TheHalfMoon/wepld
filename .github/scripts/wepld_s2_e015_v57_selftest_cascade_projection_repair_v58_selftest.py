#!/usr/bin/env python3
"""Self-tests for the v58 S2-E015 v57-selftest-cascade projection repair.

v58 must:
  * run the full frozen v57 -> v56 -> ... self-test cascade with the reopened
    path's *bytes* projected back to its pre-reopen form, so `files()` /
    `delta()` calls inside the frozen predecessor self-tests and their own
    post-cascade checks never let the inherited v28 token scan observe
    `std::process` in the tranche (this is v56's frontier-projection mechanism,
    widened in scope);
  * project only when the real tree holds the exact authorized post-reopen
    blob, and touch no path but the reopened one and the two workflows;
  * grant no new authority and widen nothing.
"""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_e015_v57_selftest_cascade_projection_repair_v58_integrity as p

_OVERLAY_VIEW_COUNTER = itertools.count()

IDPATH = p.IDENTITY_STORE_TEST


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
                base.fail(f"v58 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v58 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v58 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_E015_V57_SELFTEST_CASCADE_PROJECTION_REPAIR_ONLY":
        base.fail("v58 authority marker drift")
    if p.V58_POLICY_REPAIR != "NOT_NEW_RUNTIME_AUTHORITY":
        base.fail("v58 must declare it grants no new runtime authority")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v58 next authority gate drift")
    for name in p._INHERITED_AUTHORITY_NAMES:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v58 changed inherited authority: {name}")
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
            base.fail(f"v58 must not grant {name}")
    if p.TEST_CHILD_PROCESS_AUTHORITY != "RE_EXEC_CURRENT_TEST_BINARY_ONLY":
        base.fail("v58 TEST_CHILD_PROCESS_AUTHORITY drift")


def _check_pre_reopen_projection_mechanism() -> None:
    if p._V57_HARDENED_PRODUCT_VERIFY is p._V28_HARDENED:
        base.fail("v58 sanity: v57's projected verifier must differ from v28's raw hook")
    if p.V25.blob(p._PRE_REOPEN_BYTES) != p.PRE_REOPEN_BLOB:
        base.fail("v58 inherited pre-reopen bytes do not hash to PRE_REOPEN_BLOB")

    original = base.LocalRepositoryView.read_bytes
    wf = p._workflow_replacements(p.raw_root)
    wrapper = p._identity_store_pre_projected(original, wf)

    # Reading the reopened path through the wrapper always yields bytes hashing
    # to the pre-reopen blob - passthrough when the real tree is PRE, projected
    # when it is the authorized POST - so the inherited v28 clean-PRE scan and
    # v36 frontier pin both accept it.
    got = wrapper(p.raw_root, IDPATH, base.MAX_POLICY_FILE_BYTES)
    if p.V25.blob(got) != p.PRE_REOPEN_BLOB:
        base.fail("v58 pre-reopen projection did not yield the pre-reopen blob")

    # Workflow paths reversed; every other path passes straight through.
    for wfp in (p.FW, p.AW):
        if wrapper(p.raw_root, wfp, base.MAX_POLICY_FILE_BYTES) != wf[wfp]:
            base.fail(f"v58 wrapper did not apply the workflow reversal: {wfp}")
        if p._V58_ENTRYPOINT in wrapper(p.raw_root, wfp, base.MAX_POLICY_FILE_BYTES):
            base.fail(f"v58 wrapper left the v58 entrypoint: {wfp}")
    idsrc = "crates/core/src/identity.rs"
    if wrapper(p.raw_root, idsrc, base.MAX_POLICY_FILE_BYTES) != p.raw_root.read_bytes(
        idsrc, base.MAX_POLICY_FILE_BYTES
    ):
        base.fail("v58 wrapper must not alter any path but the reopened one and workflows")


def _check_projected_verify_behaviour() -> None:
    limit = base.MAX_POLICY_FILE_BYTES
    # The authorized fixture bytes (carried by v56, reachable via v57's q) pass.
    post_bytes = p.q.q._POST_REOPEN_BYTES
    ok_view = OverlayView(p.raw_root, {IDPATH: post_bytes})
    p._V57_HARDENED_PRODUCT_VERIFY(ok_view)

    # Non-authorized content in the reopened path still gets v28's full scan.
    tainted = post_bytes[:200] + b"\nfn _v58_taint() { let _ = std::process::id(); }\n"
    bad_view = OverlayView(p.raw_root, {IDPATH: tainted})
    _expect_failure(
        "v58 projected verify still fully scans a non-authorized reopened blob",
        lambda: p._V57_HARDENED_PRODUCT_VERIFY(bad_view),
        "unauthorized token",
    )

    # identity.rs is still fully scanned under the authorized-POST path.
    id_src = "crates/core/src/identity.rs"
    id_tainted = p.raw_root.read_bytes(id_src, limit) + (
        b"\nfn _v58_taint() { let _ = std::process::id(); }\n"
    )
    id_view = OverlayView(p.raw_root, {IDPATH: post_bytes, id_src: id_tainted})
    _expect_failure(
        "v58 projected verify still fully scans identity.rs",
        lambda: p._V57_HARDENED_PRODUCT_VERIFY(id_view),
        "std::process",
    )


def _boot_base() -> OverlayView:
    return OverlayView(
        p.raw_root, p._workflow_replacements(p.raw_root), omitted=p.POLICY_FILES
    )


def _check_v58_delta_and_files_freeze() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v58 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v58 controlled-file set must equal policy-file set")
    p.delta(p.raw_root, _boot_base())
    tampered = OverlayView(
        p.raw_root,
        {p.P: p.raw_root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# x\n"},
    )
    _expect_failure(
        "v58 policy files are frozen after activation",
        lambda: p.delta(tampered, p.raw_root),
        "frozen after activation",
    )
    smuggled = OverlayView(
        p.raw_root, {"docs/canonical/UNAUTHORIZED_V58_BOOTSTRAP.md": b"# smuggled\n"}
    )
    _expect_failure(
        "v58 bootstrap must be exactly the four bootstrap paths",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v58 policy files",
    )


def _check_workflow_projection_reverses() -> None:
    projected = p._project_for_v57(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v58 workflow projection does not reverse to exact v57: {path}")
        if p._V58_ENTRYPOINT in data:
            base.fail(f"v58 workflow projection left the v58 entrypoint: {path}")
    raw_fw = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES)
    drifted = raw_fw.replace(p._V58_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1)
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "v58 rejects a drifted workflow entrypoint count",
        lambda: p._workflow_replacements(view),
        "entrypoint count drifted",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_pre_reopen_projection_mechanism()
    _check_projected_verify_behaviour()
    _check_workflow_projection_reverses()
    _check_v58_delta_and_files_freeze()
    p.install()
    p.overlay()
    print("wepld v58 S2-E015 v57-selftest-cascade projection repair self-tests: PASS")


if __name__ == "__main__":
    run()
