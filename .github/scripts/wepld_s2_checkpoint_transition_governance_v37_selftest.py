#!/usr/bin/env python3
"""Self-tests for the v37 canonical-documentation transition successor."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_transition_governance_v37_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v37 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _expect_failure(label: str, action: Any) -> None:
    try:
        action()
    except base.PolicyError:
        return
    base.fail(f"v37 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_CANONICAL_DOCUMENTATION_TRANSITION_ONLY":
        base.fail("v37 authority marker drift")
    for value, label in (
        (p.GIT_PROCESS_ADMISSION, "Git process admission"),
        (p.EXTERNAL_PROCESS_AUTHORITY, "external process authority"),
        (p.GIT_EXECUTION_AUTHORITY, "Git execution authority"),
        (p.NETWORK_AUTHORITY, "network authority"),
        (p.SOURCE_ADMISSION, "source admission"),
        (p.MODEL_PROVIDER_EXECUTION, "model/provider execution"),
        (p.DOCTOR_CLI_AUTHORITY, "Doctor/CLI authority"),
        (p.S3_PLUS_AUTHORITY, "S3+ authority"),
    ):
        if value != "NONE":
            base.fail(f"v37 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v37 documentation transition must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v37 documentation transition must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v37 documentation transition must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v37 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v37 next authority gate drift")


def _check_transition_targets_are_exact() -> None:
    if p.CHECKPOINT != "docs/canonical/CURRENT_STATE.md":
        base.fail("v37 checkpoint path drift")
    if p.LEDGER != "docs/learning/BUILD_LEARNING_LEDGER.md":
        base.fail("v37 ledger path drift")
    if p.DOCS != frozenset({p.CHECKPOINT, p.LEDGER}):
        base.fail("v37 transition must be exactly the two canonical documentation paths")

    if p.PRE_CHECKPOINT_BLOB != "28c50353718f4b836daf67df2a52f6d9471e847b":
        base.fail("v37 PRE checkpoint identity drift")
    if p.PRE_LEDGER_BLOB != "f06e42dbd2a5e658cc1dc7c9ea7d768ceae458fb":
        base.fail("v37 PRE ledger identity drift")

    # The PRE side must be exactly what the spent v34/v35 route left canonical. If a
    # successor ever silently re-pointed the starting bytes, the transition would no
    # longer begin from the state the repository actually holds.
    if p.PRE_CHECKPOINT_BLOB != p.p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v37 PRE checkpoint is not the canonical v35 FINAL checkpoint")
    if p.PRE_LEDGER_BLOB != p.p.p.FINAL_LEDGER_BLOB:
        base.fail("v37 PRE ledger is not the canonical v35 FINAL ledger")

    if p.FINAL_CHECKPOINT_BLOB == p.PRE_CHECKPOINT_BLOB:
        base.fail("v37 checkpoint transition target equals its own PRE state")
    if p.FINAL_LEDGER_BLOB == p.PRE_LEDGER_BLOB:
        base.fail("v37 ledger transition target equals its own PRE state")
    if p.FINAL_CHECKPOINT_BLOB == p.FINAL_LEDGER_BLOB:
        base.fail("v37 transition targets collapsed onto one identity")


def _check_predecessor_is_exact() -> None:
    p.req_v36(p.root)
    if p.V36_P_BLOB != "8980b61efac9e8e2a246d603b9e8ff6d07512b51":
        base.fail("v37 frozen v36 integrity identity drift")
    if p.V36_T_BLOB != "cd807991928c2d3a413d0ab52cee36224d9737d9":
        base.fail("v37 frozen v36 self-test identity drift")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v37 workflow projection does not reverse to v36: {path}")
        if p._V37_ENTRYPOINT in data:
            base.fail(f"v37 workflow projection left a v37 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V37_ENTRYPOINT,
        b"wepld_unknown_checkpoint_entrypoint.py",
        1,
    )
    view = OverlayView(p.raw_root, {p.FW: drifted})
    _expect_failure(
        "workflow entrypoint count drift",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_workflow_projection_rejects_extra_content() -> None:
    # A workflow that still carries the right number of v37 entrypoints but has any
    # other byte changed must not reverse to the canonical v36 predecessor hash.
    padded = p.raw_root.read_bytes(p.AW, base.MAX_POLICY_FILE_BYTES) + b"\n# smuggled\n"
    view = OverlayView(p.raw_root, {p.AW: padded})
    _expect_failure(
        "workflow carries content beyond the entrypoint migration",
        lambda: p._workflow_predecessor_projection(view),
    )


def _check_docs_transition_is_one_shot() -> None:
    # The candidate must hold FINAL and the base must hold PRE. A candidate that still
    # holds PRE, or a base that already holds FINAL, must both fail closed. This is the
    # property that makes the route self-consuming and non-repeatable.
    real = p.raw_root

    class _Doc:
        def __init__(self, checkpoint: bytes, ledger: bytes) -> None:
            self._m = {p.CHECKPOINT: checkpoint, p.LEDGER: ledger}

        def read_bytes(self, path: str, max_bytes: int) -> bytes:
            if path in self._m:
                return self._m[path]
            return real.read_bytes(path, max_bytes)

        def __getattr__(self, name: str) -> Any:
            return getattr(real, name)

    pre_checkpoint = real.read_bytes(p.CHECKPOINT, base.MAX_POLICY_FILE_BYTES)
    pre_ledger = real.read_bytes(p.LEDGER, base.MAX_POLICY_FILE_BYTES)

    _expect_failure(
        "candidate still holding PRE bytes",
        lambda: p.docs_transition(_Doc(pre_checkpoint, pre_ledger), real),
    )


def _check_local_state_supersession_is_strict() -> None:
    """The re-anchored local-state assertion must keep both inherited properties.

    v37 replaced the v34 and v35 local-documentation-state checks with its own. A
    replacement that merely returned would satisfy every predecessor self-test while
    enforcing nothing, so the replacement is exercised directly: a state on neither
    pinned side must fail, and a half-applied state must fail even though each file is
    individually on a recognised side.
    """
    for module, name, label in p._SUPERSEDED_LOCAL_STATE_CHECKS:
        if getattr(module, name) is not p._check_local_state_is_one_of_the_v37_pinned_states:
            base.fail(f"v37 local documentation state supersession missing: {label}")

    real = p.raw_root
    checkpoint = real.read_bytes(p.CHECKPOINT, base.MAX_POLICY_FILE_BYTES)
    foreign = OverlayView(real, {p.CHECKPOINT: checkpoint + b"\nforeign\n"})
    _expect_failure(
        "documentation state on neither pinned side",
        lambda: p._check_local_state_is_one_of_the_v37_pinned_states(foreign),
    )

    # A half-applied tree cannot be built from bytes this repository holds, because only
    # one side of the transition exists at a time. Moving the ledger's own pins for the
    # duration of one call produces the same condition the check must reject: the
    # checkpoint resolves to one side and the ledger to the other.
    original_pre = p.PRE_LEDGER_BLOB
    original_final = p.FINAL_LEDGER_BLOB
    actual_ledger = p.V25.blob(real.read_bytes(p.LEDGER, base.MAX_POLICY_FILE_BYTES))
    actual_checkpoint = p.V25.blob(checkpoint)
    opposite = "FINAL" if actual_checkpoint == p.PRE_CHECKPOINT_BLOB else "PRE"
    try:
        if opposite == "FINAL":
            p.PRE_LEDGER_BLOB = "0" * 40
            p.FINAL_LEDGER_BLOB = actual_ledger
        else:
            p.PRE_LEDGER_BLOB = actual_ledger
            p.FINAL_LEDGER_BLOB = "0" * 40
        _expect_failure(
            "half-applied documentation state",
            lambda: p._check_local_state_is_one_of_the_v37_pinned_states(),
        )
    finally:
        p.PRE_LEDGER_BLOB = original_pre
        p.FINAL_LEDGER_BLOB = original_final

    if p.PRE_LEDGER_BLOB != original_pre or p.FINAL_LEDGER_BLOB != original_final:
        base.fail("v37 self-test left the ledger pins moved")


def _check_bootstrap_scope_is_closed() -> None:
    expected = frozenset({p.P, p.T, p.FW, p.AW})
    if p.BOOT != expected:
        base.fail(f"v37 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v37 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v37 bootstrap must not carry the documentation transition")


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_transition_targets_are_exact()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_docs_transition_is_one_shot()
    _check_local_state_supersession_is_strict()
    _check_bootstrap_scope_is_closed()

    print("wepld v37 S2 canonical-documentation transition self-tests: PASS")
