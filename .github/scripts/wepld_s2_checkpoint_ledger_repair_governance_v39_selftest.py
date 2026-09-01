#!/usr/bin/env python3
"""Self-tests for the v39 second corrected canonical-documentation ledger target."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v39_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v39 self-test overlay exceeds read bound: {path}")
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
    base.fail(f"v39 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_CANONICAL_DOCUMENTATION_LEDGER_TARGET_SECOND_CORRECTION_ONLY":
        base.fail("v39 authority marker drift")
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
            base.fail(f"v39 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v39 ledger correction must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v39 ledger correction must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v39 ledger correction must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v39 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v39 next authority gate drift")


def _check_correction_is_exactly_one_target() -> None:
    if p.V38_FINAL_LEDGER_BLOB != "ffd0d2f9264cae5d4ddf24985e5571a87f03fc04":
        base.fail("v39 superseded v38 ledger identity drift")
    if p.FINAL_LEDGER_BLOB != "cbd6f7bca4f8f33435320be2d153e59b4588f073":
        base.fail("v39 corrected ledger identity drift")
    if p.FINAL_LEDGER_BLOB == p.V38_FINAL_LEDGER_BLOB:
        base.fail("v39 accepts the superseded v38 FINAL ledger identity")

    # Everything except the ledger identity is inherited, not restated.
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v39 must inherit the PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v39 must inherit the PRE ledger unchanged")
    if p.FINAL_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v39 must inherit the FINAL checkpoint unchanged")
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v39 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v39 must inherit the exact two-path transition shape")

    if p.PRE_LEDGER_BLOB == p.FINAL_LEDGER_BLOB:
        base.fail("v39 corrected ledger target equals its own PRE state")
    if p.FINAL_LEDGER_BLOB == p.FINAL_CHECKPOINT_BLOB:
        base.fail("v39 transition targets collapsed onto one identity")


def _check_the_effective_consumer_moved_and_the_literal_did_not() -> None:
    """v39 must move v37's shared attribute and leave v38's self-literal alone.

    This is the distinction the whole successor turns on. v38 asserts its own FINAL ledger
    identity as a literal in its self-test, so overwriting v38's copy would break a check
    that is still correct about itself. Only the shared attribute in v37 may move.
    """
    if p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v39 did not bind the effective v37 consumer to the corrected target")
    if p.p.FINAL_LEDGER_BLOB != p.V38_FINAL_LEDGER_BLOB:
        base.fail("v39 must leave the v38 self-literal at its own value between calls")

    p._bind_corrected_ledger_target()
    if p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v39 ledger target rebind is not idempotent")

    original = p.p.p.FINAL_LEDGER_BLOB
    p.p.p.FINAL_LEDGER_BLOB = "0" * 40
    try:
        _expect_failure(
            "effective ledger target outside the exact old/corrected set",
            p._bind_corrected_ledger_target,
        )
    finally:
        p.p.p.FINAL_LEDGER_BLOB = original
    if p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v39 self-test left the effective ledger target moved")


def _check_reanchoring_is_installed_and_restores() -> None:
    """The re-anchored v38 checks must still run, and must not leak the corrected value.

    A wrapper that swallowed the inherited check would satisfy every predecessor self-test
    while enforcing nothing, so the wrappers are verified to be installed, to delegate to the
    originals, and to restore v38's literal even when the wrapped call raises.
    """
    for module, name in p._V38_REANCHORED:
        current = getattr(module, name)
        if current is p._V38_ORIGINALS[name]:
            base.fail(f"v39 re-anchoring of v38 {name} is missing")
        if not callable(current):
            base.fail(f"v39 re-anchoring of v38 {name} is not callable")

    observed = []

    def _probe() -> str:
        observed.append(p.p.FINAL_LEDGER_BLOB)
        return "PROBE"

    wrapped = p._with_corrected_identity(_probe)
    literal_before = p.p.FINAL_LEDGER_BLOB
    if wrapped() != "PROBE":
        base.fail("v39 re-anchoring wrapper does not delegate")
    if observed != [p.FINAL_LEDGER_BLOB]:
        base.fail(f"v39 wrapper did not present the corrected identity: {observed}")
    if p.p.FINAL_LEDGER_BLOB != literal_before:
        base.fail("v39 wrapper did not restore the v38 literal")

    def _raiser() -> None:
        base.fail("v39 self-test induced failure")

    _expect_failure("wrapped call that raises", p._with_corrected_identity(_raiser))
    if p.p.FINAL_LEDGER_BLOB != literal_before:
        base.fail("v39 wrapper did not restore the v38 literal after a failure")


def _check_predecessor_is_exact() -> None:
    p.req_v38(p.raw_root)


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v39 workflow projection does not reverse to v38: {path}")
        if p._V39_ENTRYPOINT in data:
            base.fail(f"v39 workflow projection left a v39 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V39_ENTRYPOINT,
        b"wepld_unknown_second_repair_entrypoint.py",
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
        base.fail(f"v39 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v39 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v39 bootstrap must not carry the documentation transition")


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_correction_is_exactly_one_target()
    _check_the_effective_consumer_moved_and_the_literal_did_not()
    _check_reanchoring_is_installed_and_restores()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()

    print("wepld v39 second corrected canonical-documentation ledger target self-tests: PASS")
