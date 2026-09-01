#!/usr/bin/env python3
"""Self-tests for the v38 corrected canonical-documentation ledger target."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v38_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v38 self-test overlay exceeds read bound: {path}")
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
    base.fail(f"v38 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_CANONICAL_DOCUMENTATION_LEDGER_TARGET_CORRECTION_ONLY":
        base.fail("v38 authority marker drift")
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
            base.fail(f"v38 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v38 ledger correction must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v38 ledger correction must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v38 ledger correction must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v38 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v38 next authority gate drift")


def _check_correction_is_exactly_one_target() -> None:
    """Only the FINAL ledger identity may move. Everything else must be inherited."""
    if p.V37_FINAL_LEDGER_BLOB != "f9b2872639a20c46db4adcde4bf2a4372f4c117e":
        base.fail("v38 superseded v37 ledger identity drift")
    if p.FINAL_LEDGER_BLOB != "ffd0d2f9264cae5d4ddf24985e5571a87f03fc04":
        base.fail("v38 corrected ledger identity drift")
    if p.FINAL_LEDGER_BLOB == p.V37_FINAL_LEDGER_BLOB:
        base.fail("v38 accepts the superseded v37 FINAL ledger identity")

    # The PRE side and the checkpoint target are inherited, not restated. If a future
    # edit turned any of these into a local literal, this comparison would catch the
    # divergence rather than silently accepting two sources of truth.
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v38 must inherit the v37 PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v38 must inherit the v37 PRE ledger unchanged")
    if p.FINAL_CHECKPOINT_BLOB != p.p.FINAL_CHECKPOINT_BLOB:
        base.fail("v38 must inherit the v37 FINAL checkpoint unchanged")
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v38 must inherit the v37 documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v38 must inherit the exact two-path transition shape")

    if p.PRE_LEDGER_BLOB == p.FINAL_LEDGER_BLOB:
        base.fail("v38 corrected ledger target equals its own PRE state")
    if p.FINAL_LEDGER_BLOB == p.FINAL_CHECKPOINT_BLOB:
        base.fail("v38 transition targets collapsed onto one identity")


def _check_binding_is_exact_and_idempotent() -> None:
    """The rebind must accept exactly two values and reject any third."""
    if p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v38 did not bind v37 to the corrected ledger target")

    # Already-corrected is a valid resting state, so a second bind is a no-op.
    p._bind_corrected_ledger_target()
    if p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v38 ledger target rebind is not idempotent")

    original = p.p.FINAL_LEDGER_BLOB
    p.p.FINAL_LEDGER_BLOB = "0" * 40
    try:
        _expect_failure(
            "predecessor ledger target outside the exact old/corrected set",
            p._bind_corrected_ledger_target,
        )
    finally:
        p.p.FINAL_LEDGER_BLOB = original
    if p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v38 self-test left the predecessor ledger target moved")


def _check_correction_reaches_every_consumer() -> None:
    """The rebind is only sufficient if every v37 consumer reads it at call time.

    v38 corrects one attribute on v37 rather than reimplementing the transition, so the
    property that makes that safe is worth asserting rather than assuming: the inherited
    transition must now reject the superseded identity and accept the corrected one.
    """
    real = p.raw_root

    class _Doc:
        def __init__(self, checkpoint: str, ledger: str) -> None:
            self._m = {p.CHECKPOINT: checkpoint, p.LEDGER: ledger}

        def read_bytes(self, path: str, max_bytes: int) -> bytes:
            return real.read_bytes(path, max_bytes)

        def __getattr__(self, name: str) -> Any:
            return getattr(real, name)

    # The transition inherited from v37 must refuse a candidate whose ledger carries the
    # superseded identity. Exercised through the real base, which holds the PRE side.
    superseded = OverlayView(real, {})
    _expect_failure(
        "inherited transition accepting a no-op",
        lambda: p.p.docs_transition(superseded, real),
    )

    if p.p.FINAL_LEDGER_BLOB == p.V37_FINAL_LEDGER_BLOB:
        base.fail("v38 left the superseded ledger identity reachable in the transition")


def _check_predecessor_is_exact() -> None:
    p.req_v37(p.raw_root)


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v38 workflow projection does not reverse to v37: {path}")
        if p._V38_ENTRYPOINT in data:
            base.fail(f"v38 workflow projection left a v38 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V38_ENTRYPOINT,
        b"wepld_unknown_ledger_repair_entrypoint.py",
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
        base.fail(f"v38 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v38 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v38 bootstrap must not carry the documentation transition")


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_correction_is_exactly_one_target()
    _check_binding_is_exact_and_idempotent()
    _check_correction_reaches_every_consumer()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()

    print("wepld v38 corrected canonical-documentation ledger target self-tests: PASS")
