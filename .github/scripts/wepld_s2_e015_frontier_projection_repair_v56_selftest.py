#!/usr/bin/env python3
"""Self-tests for the v56 S2-E015 canonical-frontier projection repair.

The repair must satisfy, in order:

  * the exact pre-reopen blob is accepted in the pre-transition state, and the
    full frozen predecessor self-test cascade passes under v56's projection
    (this is `run_predecessor_selftests`, run first);
  * the exact authorized post-reopen blob is accepted only for the one
    authorized transition, and no third blob ever is;
  * the historical projection touches exactly one path: `identity.rs`,
    `evidence_store.rs`, `lib.rs`, and the two documentation frontier paths keep
    their live, independent pins, so the projection can conceal nothing;
  * the projection is presented only after the live transition state is proven,
    so it can never hide an unauthorized underlying blob;
  * v55's `TEST_CHILD_PROCESS_AUTHORITY` static bound is still active, and the
    authorized post-reopen content passes it;
  * once the authorized post-reopen blob is canonical, any further change to the
    reopened path is rejected and needs a new successor;
  * v56 grants no new authority and widens nothing.
"""

from __future__ import annotations

import itertools
from typing import Any

import wepld_integrity as base
import wepld_s2_e015_frontier_projection_repair_v56_integrity as p

_OVERLAY_VIEW_COUNTER = itertools.count()

IDPATH = "crates/core/tests/identity_store_v1.rs"
IDENTITY_SRC = "crates/core/src/identity.rs"
STORE_SRC = "crates/core/src/evidence_store.rs"
CORE_EXPORT = "crates/core/src/lib.rs"


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
                base.fail(f"v56 self-test overlay exceeds read bound: {path}")
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
            base.fail(f"v56 self-test rejection came from wrong cause: {label}: {exc}")
        return
    base.fail(f"v56 self-test expected fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_E015_CANONICAL_FRONTIER_PROJECTION_REPAIR_ONLY":
        base.fail("v56 authority marker drift")
    if p.V56_POLICY_REPAIR != "NOT_NEW_RUNTIME_AUTHORITY":
        base.fail("v56 must declare it grants no new runtime authority")
    if p.HISTORICAL_PROJECTION != "HISTORICAL_VIEW_ONLY":
        base.fail("v56 historical-projection marker drift")
    if p.POLICY_PROJECTION_REPAIR != "NOT_PRODUCT_CHANGE_NOT_EVIDENCE":
        base.fail("v56 projection-repair marker drift")
    if p.NEXT_AUTHORITY_GATE != "S2-ACCEPTANCE":
        base.fail("v56 next authority gate drift")

    for name in p._INHERITED_AUTHORITY_NAMES:
        if getattr(p, name) != getattr(p.q, name):
            base.fail(f"v56 changed inherited authority: {name}")
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
            base.fail(f"v56 must not grant {name}")
    if p.TEST_CHILD_PROCESS_AUTHORITY != "RE_EXEC_CURRENT_TEST_BINARY_ONLY":
        base.fail("v56 TEST_CHILD_PROCESS_AUTHORITY drift")
    if p.q.EXACT_FROZEN_BLOB != p.PRE_REOPEN_BLOB:
        base.fail("v56 PRE_REOPEN_BLOB must equal the inherited v55 EXACT_FROZEN_BLOB")


def _check_embedded_transition_bytes() -> None:
    if p.V25.blob(p._PRE_REOPEN_BYTES) != p.PRE_REOPEN_BLOB:
        base.fail("v56 embedded pre-reopen bytes do not hash to PRE_REOPEN_BLOB")
    if p.PRE_REOPEN_BLOB != "fc1fd55c47e5bb6879b8c5bb03cd0500bedcff0f":
        base.fail("v56 PRE_REOPEN_BLOB is not the exact v36 frontier pin")
    if p.V25.blob(p._POST_REOPEN_BYTES) != p.AUTHORIZED_POST_REOPEN_BLOB:
        base.fail("v56 embedded post-reopen bytes do not hash to AUTHORIZED_POST_REOPEN_BLOB")
    if p.AUTHORIZED_POST_REOPEN_BLOB == p.PRE_REOPEN_BLOB:
        base.fail("v56 authorized post-reopen blob must differ from the pre-reopen blob")
    if p._PRE_REOPEN_BYTES[:100] != p._POST_REOPEN_BYTES[:100]:
        base.fail("v56 authorized transition is not the same file family")
    marker = b"process_crash_releases_the_os_owned_catalog_lock"
    if marker in p._PRE_REOPEN_BYTES:
        base.fail("v56 pre-reopen bytes already contain the S2-E015 fixture")
    if marker not in p._POST_REOPEN_BYTES:
        base.fail("v56 authorized transition does not add the S2-E015 fixture")
    if not p._POST_REOPEN_BYTES.startswith(p._PRE_REOPEN_BYTES[:24]):
        base.fail("v56 authorized transition changed the file header")


def _check_live_transition_side() -> None:
    if p._live_transition_side(p.raw_root) != "PRE":
        base.fail("v56 real tree must currently be the pre-transition side")

    post_view = OverlayView(p.raw_root, {IDPATH: p._POST_REOPEN_BYTES})
    if p._live_transition_side(post_view) != "POST":
        base.fail("v56 must accept the exact authorized post-reopen blob as POST")

    third = OverlayView(p.raw_root, {IDPATH: b"// v56 self-test: an arbitrary third state\n"})
    _expect_failure(
        "v56 rejects a third blob for the reopened path",
        lambda: p._live_transition_side(third),
        "neither pinned transition side",
    )

    gone = OverlayView(p.raw_root, {}, omitted=frozenset({IDPATH}))
    _expect_failure(
        "v56 rejects a tree missing the reopened frontier path",
        lambda: p._live_transition_side(gone),
        "requires the reopened frontier path",
    )


def _check_projection_is_one_path_and_gated() -> None:
    """The transition gate and the historical projection are exercised as one
    unit through `_gated_selftest_read_bytes_wrapper` - exactly the call
    `run_predecessor_selftests` makes - so a regression that skips or hardcodes
    the gate cannot pass here. The projection touches exactly the one reopened
    path, restores exactly the bytes v36 pins, is built only when the gate
    proves the authorized POST state, and fails closed on any third blob before
    a wrapper exists. The frozen predecessor cascade run at the top of `run()`
    is the end-to-end proof for the real PRE tree.
    """
    original = base.LocalRepositoryView.read_bytes
    limit = base.MAX_POLICY_FILE_BYTES

    real_id = p.raw_root.read_bytes(IDPATH, limit)
    real_identity_src = p.raw_root.read_bytes(IDENTITY_SRC, limit)
    real_store_src = p.raw_root.read_bytes(STORE_SRC, limit)
    real_export = p.raw_root.read_bytes(CORE_EXPORT, limit)
    real_fw = p.raw_root.read_bytes(p.FW, limit)

    import wepld_s2_git_route_governance_v36_integrity as v36

    if v36.REQUIRED_CANONICAL_FRONTIER_BLOBS[IDPATH] != p.PRE_REOPEN_BLOB:
        base.fail("v56 PRE_REOPEN_BLOB is not the live v36 frontier pin for the reopened path")

    # Gate + wrapper together, authorized POST tree: the gate resolves POST and
    # the wrapper it returns projects exactly the one reopened path back to the
    # bytes v36 pins. A regression that stubs the gate to always-POST is caught
    # separately by _check_live_transition_side; a regression that bypasses the
    # gate in run_predecessor_selftests is caught here (this is the same
    # _gated_selftest_read_bytes_wrapper call that function makes).
    post_tree = OverlayView(p.raw_root, {IDPATH: p._POST_REOPEN_BYTES})
    gated_post = p._gated_selftest_read_bytes_wrapper(post_tree, original)
    projected = gated_post(p.raw_root, IDPATH, limit)
    if p.V25.blob(projected) != v36.REQUIRED_CANONICAL_FRONTIER_BLOBS[IDPATH]:
        base.fail("v56 POST projection did not restore exactly the v36-pinned pre-reopen bytes")

    # Gate + wrapper together, third-blob tree: fails closed at the gate, before
    # any wrapper is produced.
    third_tree = OverlayView(p.raw_root, {IDPATH: b"// v56 self-test: a third state\n"})
    _expect_failure(
        "v56 gate rejects a third blob before a wrapper is built",
        lambda: p._gated_selftest_read_bytes_wrapper(third_tree, original),
        "neither pinned transition side",
    )

    # Gate + wrapper together, PRE tree (the real state): no projection at all.
    gated_pre = p._gated_selftest_read_bytes_wrapper(p.raw_root, original)
    if gated_pre(p.raw_root, IDPATH, limit) != real_id:
        base.fail("v56 must not project the reopened path outside the authorized POST state")

    # Nothing else moves under the POST gate+wrapper: every other path reads
    # straight through, so v56 conceals no other change from any predecessor.
    if gated_post(p.raw_root, IDENTITY_SRC, limit) != real_identity_src:
        base.fail("v56 projection altered crates/core/src/identity.rs")
    if gated_post(p.raw_root, STORE_SRC, limit) != real_store_src:
        base.fail("v56 projection altered crates/core/src/evidence_store.rs")
    if gated_post(p.raw_root, CORE_EXPORT, limit) != real_export:
        base.fail("v56 projection altered crates/core/src/lib.rs")

    # The v56->v55 workflow reversal is applied under the same gate+wrapper.
    if gated_post(p.raw_root, p.FW, limit) == real_fw:
        base.fail("v56 gate+wrapper did not apply the workflow reversal")
    if p._V56_ENTRYPOINT in gated_post(p.raw_root, p.FW, limit):
        base.fail("v56 gate+wrapper left the v56 workflow entrypoint")

    # Read-bound guard: an absurdly small limit on the projected path fails
    # closed rather than returning truncated bytes.
    _expect_failure(
        "v56 projection respects the read bound",
        lambda: gated_post(p.raw_root, IDPATH, 16),
        "exceeds read bound",
    )


def _check_workflow_projection_reverses() -> None:
    projected = p._project_for_v55(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.Q_WF[path]:
            base.fail(f"v56 workflow projection does not reverse to exact v55: {path}")
        if p._V56_ENTRYPOINT in data:
            base.fail(f"v56 workflow projection left the v56 entrypoint: {path}")

    raw_fw = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES)
    drifted = raw_fw.replace(p._V56_ENTRYPOINT, b"wepld_unknown_entrypoint.py", 1)
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "v56 rejects a drifted workflow entrypoint count",
        lambda: p._workflow_replacements(view),
        "entrypoint count drifted",
    )


def _check_child_process_static_bound_still_active() -> None:
    if not callable(p.q._verify_test_child_process_bounds):
        base.fail("v56 lost the inherited v55 child-process static bound")

    # The authorized post-reopen content passes v55's bound.
    ok_view = OverlayView(p.raw_root, {p.q.REOPEN_TEST: p._POST_REOPEN_BYTES})
    p.q._verify_test_child_process_bounds(ok_view)

    # A string-literal executable is still rejected by the inherited bound.
    bad = (
        p._PRE_REOPEN_BYTES
        + b'\nfn _b() { let _ = std::process::Command::new("sh").status(); }\n'
    )
    bad_view = OverlayView(p.raw_root, {p.q.REOPEN_TEST: bad})
    _expect_failure(
        "v56 keeps the v55 string-literal-executable rejection",
        lambda: p.q._verify_test_child_process_bounds(bad_view),
        "string-literal executable",
    )


def _check_reopen_single_use_after_post() -> None:
    post_base = OverlayView(p.raw_root, {IDPATH: p._POST_REOPEN_BYTES})
    further = OverlayView(
        p.raw_root, {IDPATH: p._POST_REOPEN_BYTES + b"\n// a later change\n"}
    )
    _expect_failure(
        "v56 rejects any further change once the authorized post-reopen blob is canonical",
        lambda: p.delta(further, post_base),
        "already consumed",
    )


def _boot_base() -> OverlayView:
    return OverlayView(
        p.raw_root, p._workflow_replacements(p.raw_root), omitted=p.POLICY_FILES
    )


def _check_v56_delta_and_files_freeze() -> None:
    if p.BOOT != frozenset({p.P, p.T, p.FW, p.AW}):
        base.fail("v56 bootstrap path set drift")
    if p.CONTROLLED_FILES != p.POLICY_FILES:
        base.fail("v56 controlled-file set must equal policy-file set")

    p.delta(p.raw_root, _boot_base())
    p.files(p.raw_root)

    tampered = OverlayView(
        p.raw_root,
        {p.P: p.raw_root.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# x\n"},
    )
    _expect_failure(
        "v56 policy files are frozen after activation",
        lambda: p.delta(tampered, p.raw_root),
        "frozen after activation",
    )

    smuggled = OverlayView(
        p.raw_root, {"docs/canonical/UNAUTHORIZED_V56_BOOTSTRAP.md": b"# smuggled\n"}
    )
    _expect_failure(
        "v56 bootstrap must be exactly the four bootstrap paths",
        lambda: p.delta(smuggled, _boot_base()),
        "bootstrap delta must be exactly two v56 policy files",
    )


def run() -> None:
    p.run_predecessor_selftests()
    _check_authority_markers()
    _check_embedded_transition_bytes()
    _check_live_transition_side()
    _check_projection_is_one_path_and_gated()
    _check_workflow_projection_reverses()
    _check_child_process_static_bound_still_active()
    _check_reopen_single_use_after_post()
    _check_v56_delta_and_files_freeze()
    p.install()
    p.overlay()
    print(
        "wepld v56 S2-E015 canonical-frontier projection repair self-tests: PASS"
    )


if __name__ == "__main__":
    run()
