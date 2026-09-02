#!/usr/bin/env python3
"""Self-tests for the v41 predecessor-selftest resting-view scope repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v41_integrity as p
import wepld_s1_admission_steady_state_routing_v18_integrity as _v18
import wepld_s1_admission_steady_state_routing_v20_integrity as _v20


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v41 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


class _FixedView:
    """A minimal fully-synthetic view over a fixed path->bytes mapping."""

    def __init__(self, values: dict[str, bytes]) -> None:
        self._values = values

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        data = self._values[path]
        if len(data) > max_bytes:
            base.fail(f"v41 self-test fixed view exceeds read bound: {path}")
        return data

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return [base.TrackedEntry(mode="100644", path=path) for path in self._values]


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except base.PolicyError:
        return
    base.fail(f"v41 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_PREDECESSOR_SELFTEST_RESTING_VIEW_SCOPE_REPAIR_ONLY":
        base.fail("v41 authority marker drift")
    for value, label in (
        (p.GIT_PROCESS_ADMISSION, "Git process admission"),
        (p.EXTERNAL_PROCESS_AUTHORITY, "external process authority"),
        (p.GIT_EXECUTION_AUTHORITY, "Git execution authority"),
        (p.NETWORK_AUTHORITY, "network authority"),
        (p.MODEL_PROVIDER_EXECUTION, "model/provider execution"),
        (p.DOCTOR_CLI_AUTHORITY, "Doctor/CLI authority"),
        (p.S3_PLUS_AUTHORITY, "S3+ authority"),
    ):
        if value != "NONE":
            base.fail(f"v41 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v41 scope repair must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v41 scope repair must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v41 scope repair must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v41 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v41 next authority gate drift")


def _check_no_target_moved() -> None:
    """v41 corrects a self-test scoping defect, not a documentation identity."""
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v41 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v41 must inherit the exact two-path transition shape")
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v41 must inherit the PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v41 must inherit the PRE ledger unchanged")
    if p.FINAL_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v41 must inherit v40's corrected checkpoint target unchanged")
    if p.FINAL_LEDGER_BLOB != p.p.FINAL_LEDGER_BLOB:
        base.fail("v41 must inherit v40's corrected ledger target unchanged")
    if p.p.p.p.p.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v41 must not move the live checkpoint binding")
    if p.p.p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v41 must not move the live ledger binding")


def _check_narrow_call_sites_still_reconcile() -> None:
    """Each of the six narrow call sites must still see v39's resting pair for its
    own dynamic extent, and restore the real (corrected) pair afterward - proving
    the repair narrows the window without breaking the reconciliation those six
    functions actually need.
    """
    v37 = p.p.p.p.p
    real_checkpoint = v37.FINAL_CHECKPOINT_BLOB
    real_ledger = v37.FINAL_LEDGER_BLOB
    if real_checkpoint != p.FINAL_CHECKPOINT_BLOB or real_ledger != p.FINAL_LEDGER_BLOB:
        base.fail("v41 self-test started with the binding already moved")

    observed: list[tuple[str, str]] = []

    def _probe() -> str:
        observed.append((v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB))
        return "PROBE"

    wrapped = p.p._with_v39_resting_view(_probe)
    if wrapped() != "PROBE":
        base.fail("v41 narrow resting-view wrapper does not delegate its return value")
    if observed != [(p.p.V39_FINAL_CHECKPOINT_BLOB, p.p.V39_FINAL_LEDGER_BLOB)]:
        base.fail(f"v41 narrow call site did not observe v39's resting pair: {observed}")
    if v37.FINAL_CHECKPOINT_BLOB != real_checkpoint or v37.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v41 narrow resting-view wrapper did not restore the real pair")

    def _raiser() -> None:
        base.fail("v41 self-test induced failure")

    _expect_failure("wrapped call that raises", p.p._with_v39_resting_view(_raiser))
    if v37.FINAL_CHECKPOINT_BLOB != real_checkpoint or v37.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v41 narrow resting-view wrapper did not restore the real pair after a raise")

    for module, name in p._NARROW_RESTING_VIEW_CALL_SITES:
        if getattr(module, name) not in p._ORIGINAL_NARROW_CALL_SITE_FUNCTIONS.values():
            base.fail(
                "v41 narrow resting-view call site left wrapped outside a call: "
                f"{module.__name__}.{name}"
            )


def _run_predecessor_selftests_and_check_live_tree_pin() -> None:
    """Run the (now-corrected) predecessor self-test cascade exactly once, and prove
    that v20's fresh-local-view S1-016 regression - the exact site root-caused
    against PR #263 - observes v37's real, current pin throughout, never v39's
    resting pair. This is the direct fix for
    "S1-016 Build Learning bytes drifted" on a candidate carrying v40's genuinely
    corrected bytes.
    """
    observed: list[tuple[str, str]] = []
    original_regression = _v20._fresh_local_view_projection_regression

    def _recording_regression() -> None:
        v37 = p.p.p.p.p
        observed.append((v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB))
        return original_regression()

    _v20._fresh_local_view_projection_regression = _recording_regression
    try:
        p.run_predecessor_selftests()
    finally:
        _v20._fresh_local_view_projection_regression = original_regression

    v37 = p.p.p.p.p
    if len(observed) != 1:
        base.fail(f"v41 expected v20's live-tree regression to run exactly once: {observed}")
    if observed[0] != (v37.FINAL_CHECKPOINT_BLOB, v37.FINAL_LEDGER_BLOB):
        base.fail(
            "v41 live-tree S1-016 classification did not observe the real, "
            f"current pin during the predecessor self-test cascade: {observed[0]}"
        )
    if observed[0] == (p.p.V39_FINAL_CHECKPOINT_BLOB, p.p.V39_FINAL_LEDGER_BLOB):
        base.fail("v41 live-tree S1-016 classification still observed v39's resting pair")


def _check_widening_chain_still_discriminates() -> None:
    """Positive and negative oracle for the actual defect: the S1-016 widening chain
    (v34._state -> v37._state -> raw v18.state) must accept a live tree whose Build
    Learning ledger content genuinely matches v37's current pin, and must still fail
    closed for content that matches nothing recognized - proving the repair does not
    silently defeat the acceptance check it was careful not to touch.
    """
    raw_root = p.raw_root
    root_state = _v18.state(raw_root)
    root_tasks = raw_root.read_bytes(_v18.TASKS, base.MAX_POLICY_FILE_BYTES)
    if root_state == "PRE_S1_016":
        pre_tasks = root_tasks
    elif root_state == "ACCEPTED_S1":
        pre_tasks = _v18.reverse_tasks(root_tasks)
    else:
        base.fail(f"v41 self-test could not establish a known S1-016 state: {root_state}")
    evidence = raw_root.read_bytes(_v18.S1_015_EVID, base.MAX_POLICY_FILE_BYTES)
    if _v18.blob(evidence) != _v18.S1_015_EVID_BLOB:
        base.fail("v41 self-test canonical S1-015 evidence drifted")
    accepted_tasks = _v18.expected_tasks(pre_tasks)
    acceptance_bytes = raw_root.read_bytes(_v18.ACCEPTANCE, base.MAX_POLICY_FILE_BYTES)
    if _v18.blob(acceptance_bytes) != _v18.FINAL_ACCEPTANCE_BLOB:
        base.fail("v41 self-test could not establish the exact accepted acceptance bytes")

    chosen_ledger_bytes = b"# v41 self-test synthetic FINAL Build Learning ledger\n"
    chosen_ledger_blob = p.V25.blob(chosen_ledger_bytes)
    wrong_ledger_bytes = b"# v41 self-test synthetic WRONG Build Learning ledger\n"
    wrong_ledger_blob = p.V25.blob(wrong_ledger_bytes)
    if chosen_ledger_blob == wrong_ledger_blob:
        base.fail("v41 self-test synthetic ledger identities collided")

    v37 = p.p.p.p.p
    saved_ledger = v37.FINAL_LEDGER_BLOB
    v37.FINAL_LEDGER_BLOB = chosen_ledger_blob
    try:
        accepted_view = _FixedView(
            {
                _v18.TASKS: accepted_tasks,
                _v18.ACCEPTANCE: acceptance_bytes,
                _v18.LEARNING: chosen_ledger_bytes,
                _v18.S1_015_EVID: evidence,
            }
        )
        result = _v18.state(accepted_view)
        if result != "ACCEPTED_S1":
            base.fail(f"v41 widening chain did not accept genuinely-correct content: {result}")

        wrong_view = _FixedView(
            {
                _v18.TASKS: accepted_tasks,
                _v18.ACCEPTANCE: acceptance_bytes,
                _v18.LEARNING: wrong_ledger_bytes,
                _v18.S1_015_EVID: evidence,
            }
        )
        _expect_failure(
            "widening chain accepting content that matches no recognized identity",
            lambda: _v18.state(wrong_view),
        )
    finally:
        v37.FINAL_LEDGER_BLOB = saved_ledger

    if v37.FINAL_LEDGER_BLOB != saved_ledger:
        base.fail("v41 self-test left the live ledger pin moved")


def _check_predecessor_is_exact() -> None:
    p.req_v40(p.raw_root)
    if p.V40_P_BLOB != "19c98eb05fbebfc41f7c793ee269a89b1db95880":
        base.fail("v41 frozen v40 integrity identity drift")
    if p.V40_T_BLOB != "9f6ca73a3e03a7704cf8608224750d37355a32d2":
        base.fail("v41 frozen v40 self-test identity drift")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v41 workflow projection does not reverse to v40: {path}")
        if p._V41_ENTRYPOINT in data:
            base.fail(f"v41 workflow projection left a v41 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V41_ENTRYPOINT,
        b"wepld_unknown_resting_view_scope_repair_entrypoint.py",
        1,
    )
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_workflow_projection_rejects_extra_content() -> None:
    padded = p.raw_root.read_bytes(p.AW, base.MAX_POLICY_FILE_BYTES) + b"\n# smuggled\n"
    view = OverlayView(p.raw_root, {p.AW: padded})
    _expect_failure(
        "workflow carries content beyond the entrypoint migration",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v41 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v41 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v41 bootstrap must not carry any documentation transition")


def _check_bootstrap_delta_rejects_third_path() -> None:
    """The bootstrap delta must be exactly the four boot files, never a fifth."""

    class _ExtraPathView:
        def __init__(self, extra: dict[str, bytes]) -> None:
            self._extra = extra

        def read_bytes(self, path: str, max_bytes: int) -> bytes:
            if path in self._extra:
                return self._extra[path]
            return p.raw_root.read_bytes(path, max_bytes)

        def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
            return self.read_bytes(path, limit).decode("utf-8", errors="strict")

        def entries(self) -> Any:
            base_paths = {entry.path for entry in p.raw_root.entries()}
            result = list(p.raw_root.entries())
            for name in self._extra:
                if name not in base_paths:
                    result.append(base.TrackedEntry(mode="100644", path=name))
            return result

        def __getattr__(self, name: str) -> Any:
            return getattr(p.raw_root, name)

    boot_files = {
        path: p.raw_root.read_bytes(path, base.MAX_POLICY_FILE_BYTES) for path in p.BOOT
    }
    smuggled_path = "docs/canonical/UNAUTHORIZED_THIRD_PATH.md"
    candidate = _ExtraPathView({**boot_files, smuggled_path: b"# smuggled\n"})

    class _BootBase:
        def read_bytes(self, path: str, max_bytes: int) -> bytes:
            return p.raw_root.read_bytes(path, max_bytes)

        def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
            return self.read_bytes(path, limit).decode("utf-8", errors="strict")

        def entries(self) -> Any:
            excluded = set(p.POLICY_FILES)
            return [entry for entry in p.raw_root.entries() if entry.path not in excluded]

        def __getattr__(self, name: str) -> Any:
            return getattr(p.raw_root, name)

    if not p.bootbase(_BootBase()):
        base.fail("v41 self-test bootstrap-base fixture is not recognized as a boot base")
    _expect_failure(
        "bootstrap delta carrying a fifth (unauthorized) path",
        lambda: p.delta(candidate, _BootBase()),
    )


def _check_predecessor_package_exactness_rejects_drift() -> None:
    """v41 requires exactly the frozen v40 package; any drift must fail closed."""
    drifted_view = OverlayView(p.raw_root, {p.p.P: p.raw_root.read_bytes(p.p.P, base.MAX_POLICY_FILE_BYTES) + b"\n# drift\n"})
    _expect_failure(
        "predecessor v40 integrity file drifted",
        lambda: p.req_v40(drifted_view),
    )


def run() -> None:
    _run_predecessor_selftests_and_check_live_tree_pin()
    p.install()

    _check_authority_markers()
    _check_no_target_moved()
    _check_narrow_call_sites_still_reconcile()
    _check_widening_chain_still_discriminates()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_third_path()
    _check_predecessor_package_exactness_rejects_drift()

    print(
        "wepld v41 predecessor-selftest resting-view scope repair "
        "self-tests: PASS"
    )
