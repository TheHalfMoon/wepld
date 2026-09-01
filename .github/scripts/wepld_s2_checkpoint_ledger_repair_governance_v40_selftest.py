#!/usr/bin/env python3
"""Self-tests for the v40 checkpoint+ledger corrected canonical-documentation targets."""

from typing import Any

import wepld_integrity as base
import wepld_s2_checkpoint_ledger_repair_governance_v40_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v40 self-test overlay exceeds read bound: {path}")
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
    base.fail(f"v40 self-test expected a fail-closed rejection: {label}")


def _check_authority_markers() -> None:
    if p.AUTH != "S2_CANONICAL_DOCUMENTATION_CHECKPOINT_AND_LEDGER_TARGET_CORRECTION":
        base.fail("v40 authority marker drift")
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
            base.fail(f"v40 must not grant {label}")
    if p.S2_IMPLEMENTATION_AUTHORITY != p.p.S2_IMPLEMENTATION_AUTHORITY:
        base.fail("v40 documentation correction must not widen S2 implementation authority")
    if p.DEPENDENCY_ADMISSION != p.p.DEPENDENCY_ADMISSION:
        base.fail("v40 documentation correction must not change dependency admission")
    if p.SOURCE_ADMISSION != p.p.SOURCE_ADMISSION:
        base.fail("v40 documentation correction must not change source admission")
    if p.GIT_ROUTE_DECISION != p.p.GIT_ROUTE_DECISION:
        base.fail("v40 must preserve the canonical S2-AUTH-013 route decision")
    if p.NEXT_AUTHORITY_GATE != "S2-AUTH-014":
        base.fail("v40 next authority gate drift")


def _check_correction_is_exactly_two_targets() -> None:
    if p.V39_FINAL_CHECKPOINT_BLOB != "dc749635fc6b7094bc414da18c982941bbed91a6":
        base.fail("v40 superseded v39 checkpoint identity drift")
    if p.V39_FINAL_LEDGER_BLOB != "cbd6f7bca4f8f33435320be2d153e59b4588f073":
        base.fail("v40 superseded v39 ledger identity drift")
    if p.FINAL_CHECKPOINT_BLOB != "c76985050e796ae7553d88c856c4f4e90e6bbbb6":
        base.fail("v40 corrected checkpoint identity drift")
    if p.FINAL_LEDGER_BLOB != "688f776b9097ab5ede9f7810218b2985753e0355":
        base.fail("v40 corrected ledger identity drift")
    if p.FINAL_CHECKPOINT_BLOB == p.V39_FINAL_CHECKPOINT_BLOB:
        base.fail("v40 accepts the superseded v39 FINAL checkpoint identity")
    if p.FINAL_LEDGER_BLOB == p.V39_FINAL_LEDGER_BLOB:
        base.fail("v40 accepts the superseded v39 FINAL ledger identity")

    # Everything except the two FINAL identities is inherited, not restated.
    if p.PRE_CHECKPOINT_BLOB != p.p.PRE_CHECKPOINT_BLOB:
        base.fail("v40 must inherit the PRE checkpoint unchanged")
    if p.PRE_LEDGER_BLOB != p.p.PRE_LEDGER_BLOB:
        base.fail("v40 must inherit the PRE ledger unchanged")
    if p.CHECKPOINT != p.p.CHECKPOINT or p.LEDGER != p.p.LEDGER:
        base.fail("v40 must inherit the documentation paths unchanged")
    if p.DOCS != p.p.DOCS or len(p.DOCS) != 2:
        base.fail("v40 must inherit the exact two-path transition shape")

    if p.PRE_CHECKPOINT_BLOB == p.FINAL_CHECKPOINT_BLOB:
        base.fail("v40 corrected checkpoint target equals its own PRE state")
    if p.PRE_LEDGER_BLOB == p.FINAL_LEDGER_BLOB:
        base.fail("v40 corrected ledger target equals its own PRE state")
    if p.FINAL_CHECKPOINT_BLOB == p.FINAL_LEDGER_BLOB:
        base.fail("v40 transition targets collapsed onto one identity")


def _check_binding_is_exact_and_idempotent() -> None:
    """The rebind must accept exactly two values per identity and reject any third."""
    if p.p.p.p.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v40 did not bind v37 to the corrected checkpoint target")
    if p.p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v40 did not bind v37 to the corrected ledger target")

    # Already-corrected is a valid resting state, so a second bind is a no-op.
    p._bind_corrected_targets()
    if p.p.p.p.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v40 checkpoint target rebind is not idempotent")
    if p.p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v40 ledger target rebind is not idempotent")

    saved_checkpoint = p.p.p.p.FINAL_CHECKPOINT_BLOB
    saved_ledger = p.p.p.p.FINAL_LEDGER_BLOB

    # Checkpoint alone outside the exact old/corrected set must fail closed, and must
    # not silently rebind the ledger identity along the way.
    p.p.p.p.FINAL_CHECKPOINT_BLOB = "0" * 40
    try:
        _expect_failure(
            "checkpoint target outside the exact old/corrected set",
            p._bind_corrected_targets,
        )
        if p.p.p.p.FINAL_LEDGER_BLOB != saved_ledger:
            base.fail("v40 checkpoint-only rejection must not disturb the ledger target")
    finally:
        p.p.p.p.FINAL_CHECKPOINT_BLOB = saved_checkpoint

    # Ledger alone outside the exact old/corrected set must fail closed too.
    p.p.p.p.FINAL_LEDGER_BLOB = "1" * 40
    try:
        _expect_failure(
            "ledger target outside the exact old/corrected set",
            p._bind_corrected_targets,
        )
        if p.p.p.p.FINAL_CHECKPOINT_BLOB != saved_checkpoint:
            base.fail("v40 ledger-only rejection must not disturb the checkpoint target")
    finally:
        p.p.p.p.FINAL_LEDGER_BLOB = saved_ledger

    # A mixed predecessor state - checkpoint already corrected, ledger still at an
    # ancient (pre-v38) identity that is neither v39's resting value nor v40's
    # corrected value - must also fail closed.
    p.p.p.p.FINAL_LEDGER_BLOB = "f9b2872639a20c46db4adcde4bf2a4372f4c117e"
    try:
        _expect_failure(
            "mixed predecessor identity (checkpoint corrected, ledger ancient)",
            p._bind_corrected_targets,
        )
    finally:
        p.p.p.p.FINAL_LEDGER_BLOB = saved_ledger

    if p.p.p.p.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v40 self-test left the checkpoint target moved")
    if p.p.p.p.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v40 self-test left the ledger target moved")


def _check_resting_view_wrapper_presents_delegates_and_restores() -> None:
    """The v39-resting-view wrapper must present, delegate, and always restore.

    A wrapper that swallowed the real bindings, or that failed to restore them after
    an exception, would let every nested predecessor self-test run against the wrong
    (or an inconsistently moved) pair without anyone noticing.
    """
    observed: list[tuple[str, str]] = []

    def _probe() -> str:
        observed.append((p.p.p.p.FINAL_CHECKPOINT_BLOB, p.p.p.p.FINAL_LEDGER_BLOB))
        return "PROBE"

    real_checkpoint = p.p.p.p.FINAL_CHECKPOINT_BLOB
    real_ledger = p.p.p.p.FINAL_LEDGER_BLOB
    if real_checkpoint != p.FINAL_CHECKPOINT_BLOB or real_ledger != p.FINAL_LEDGER_BLOB:
        base.fail("v40 self-test started with the binding already moved")

    wrapped = p._with_v39_resting_view(_probe)
    if wrapped() != "PROBE":
        base.fail("v40 resting-view wrapper does not delegate its return value")
    if observed != [(p.V39_FINAL_CHECKPOINT_BLOB, p.V39_FINAL_LEDGER_BLOB)]:
        base.fail(f"v40 wrapper did not present v39's resting pair: {observed}")
    if p.p.p.p.FINAL_CHECKPOINT_BLOB != real_checkpoint or p.p.p.p.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v40 wrapper did not restore the corrected pair after a normal return")

    def _raiser() -> None:
        base.fail("v40 self-test induced failure")

    _expect_failure("wrapped call that raises", p._with_v39_resting_view(_raiser))
    if p.p.p.p.FINAL_CHECKPOINT_BLOB != real_checkpoint or p.p.p.p.FINAL_LEDGER_BLOB != real_ledger:
        base.fail("v40 wrapper did not restore the corrected pair after a raised failure")


class _DocView:
    """A view that reports chosen bytes for the two documentation paths."""

    def __init__(self, view: Any, checkpoint: bytes, ledger: bytes) -> None:
        self._view = view
        self._m = {p.CHECKPOINT: checkpoint, p.LEDGER: ledger}

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._m:
            data = self._m[path]
            if len(data) > max_bytes:
                base.fail(f"v40 self-test doc view exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES) -> str:
        return self.read_bytes(path, limit).decode("utf-8", errors="strict")

    def entries(self) -> Any:
        return self._view.entries()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def _check_every_consumer_resolves_both_identities_at_call_time() -> None:
    """Both v37 consumers must resolve each identity independently, at call time.

    v37's ``docs_transition`` and ``_check_local_state_is_one_of_the_v37_pinned_states``
    are inherited unchanged from v40's perspective; only the pins they read moved. A
    consumer that had captured either pin at import time would not notice v40's
    correction. Because the checkpoint identity has never moved before v40, this test
    specifically exercises a checkpoint-only mismatch as well as a ledger-only one -
    the case v38's own inherited proof (exercised through ``run_predecessor_selftests``
    above) never had reason to cover.
    """
    real = p.p.p.p.raw_root

    pre_checkpoint_bytes = b"# v40 self-test synthetic PRE checkpoint\n"
    final_checkpoint_bytes = b"# v40 self-test synthetic FINAL checkpoint\n"
    pre_ledger_bytes = b"# v40 self-test synthetic PRE ledger\n"
    final_ledger_bytes = b"# v40 self-test synthetic FINAL ledger\n"

    synthetic_pre_checkpoint = p.V25.blob(pre_checkpoint_bytes)
    synthetic_final_checkpoint = p.V25.blob(final_checkpoint_bytes)
    synthetic_pre_ledger = p.V25.blob(pre_ledger_bytes)
    synthetic_final_ledger = p.V25.blob(final_ledger_bytes)
    synthetic = (
        synthetic_pre_checkpoint,
        synthetic_final_checkpoint,
        synthetic_pre_ledger,
        synthetic_final_ledger,
    )
    if len(set(synthetic)) != len(synthetic):
        base.fail("v40 self-test synthetic identities collided")

    base_view = _DocView(real, pre_checkpoint_bytes, pre_ledger_bytes)
    final_view = _DocView(real, final_checkpoint_bytes, final_ledger_bytes)

    v37 = p.p.p.p
    saved = (
        v37.PRE_CHECKPOINT_BLOB,
        v37.PRE_LEDGER_BLOB,
        v37.FINAL_CHECKPOINT_BLOB,
        v37.FINAL_LEDGER_BLOB,
    )
    try:
        v37.PRE_CHECKPOINT_BLOB = synthetic_pre_checkpoint
        v37.PRE_LEDGER_BLOB = synthetic_pre_ledger
        v37.FINAL_CHECKPOINT_BLOB = synthetic_final_checkpoint
        v37.FINAL_LEDGER_BLOB = synthetic_final_ledger

        # Accept phase: both consumers must be satisfied by the synthetic FINAL state.
        v37.docs_transition(final_view, base_view)
        v37._check_local_state_is_one_of_the_v37_pinned_states(final_view)
        v37._req_canonical_frontier(final_view)

        # Reject phase 1: only the checkpoint moves away; ledger stays FINAL-correct.
        v37.FINAL_CHECKPOINT_BLOB = "2" * 40
        _expect_failure(
            "docs_transition resolving a stale checkpoint identity",
            lambda: v37.docs_transition(final_view, base_view),
        )
        _expect_failure(
            "local documentation state resolving a stale checkpoint identity",
            lambda: v37._check_local_state_is_one_of_the_v37_pinned_states(final_view),
        )
        _expect_failure(
            "canonical frontier resolving a stale checkpoint identity",
            lambda: v37._req_canonical_frontier(final_view),
        )
        v37.FINAL_CHECKPOINT_BLOB = synthetic_final_checkpoint

        # Reject phase 2: only the ledger moves away; checkpoint stays FINAL-correct.
        v37.FINAL_LEDGER_BLOB = "3" * 40
        _expect_failure(
            "docs_transition resolving a stale ledger identity",
            lambda: v37.docs_transition(final_view, base_view),
        )
        _expect_failure(
            "local documentation state resolving a stale ledger identity",
            lambda: v37._check_local_state_is_one_of_the_v37_pinned_states(final_view),
        )
        _expect_failure(
            "canonical frontier resolving a stale ledger identity",
            lambda: v37._req_canonical_frontier(final_view),
        )
    finally:
        (
            v37.PRE_CHECKPOINT_BLOB,
            v37.PRE_LEDGER_BLOB,
            v37.FINAL_CHECKPOINT_BLOB,
            v37.FINAL_LEDGER_BLOB,
        ) = saved

    if v37.FINAL_CHECKPOINT_BLOB != p.FINAL_CHECKPOINT_BLOB:
        base.fail("v40 self-test left the checkpoint target moved")
    if v37.FINAL_LEDGER_BLOB != p.FINAL_LEDGER_BLOB:
        base.fail("v40 self-test left the ledger target moved")
    if v37.PRE_LEDGER_BLOB != p.PRE_LEDGER_BLOB:
        base.fail("v40 self-test left the PRE ledger moved")
    if v37.PRE_CHECKPOINT_BLOB != p.PRE_CHECKPOINT_BLOB:
        base.fail("v40 self-test left the PRE checkpoint moved")


def _check_predecessor_is_exact() -> None:
    p.req_v39(p.raw_root)
    if p.V39_P_BLOB != "f789b29431c58669449b3119cfe5dc9ffe6f8741":
        base.fail("v40 frozen v39 integrity identity drift")
    if p.V39_T_BLOB != "a4c4b43744a57f4c98aa48bf130867c1902c5b88":
        base.fail("v40 frozen v39 self-test identity drift")


def _check_workflow_projection_reverses() -> None:
    projected = p._workflow_predecessor_projection(p.raw_root)
    for path in (p.FW, p.AW):
        data = projected.read_bytes(path, base.MAX_POLICY_FILE_BYTES)
        if p.V25.sha(data) != p.P_WF[path]:
            base.fail(f"v40 workflow projection does not reverse to v39: {path}")
        if p._V40_ENTRYPOINT in data:
            base.fail(f"v40 workflow projection left a v40 entrypoint: {path}")


def _check_workflow_projection_rejects_drift() -> None:
    drifted = p.raw_root.read_bytes(p.FW, base.MAX_POLICY_FILE_BYTES).replace(
        p._V40_ENTRYPOINT,
        b"wepld_unknown_checkpoint_and_ledger_repair_entrypoint.py",
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
        base.fail(f"v40 bootstrap path set drifted: {sorted(p.BOOT)}")
    if p.CONTROLLED_FILES != frozenset({p.P, p.T}):
        base.fail("v40 controlled file set must be exactly the two policy files")
    if p.BOOT & p.DOCS:
        base.fail("v40 bootstrap must not carry the documentation transition")


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
        base.fail("v40 self-test bootstrap-base fixture is not recognized as a boot base")
    _expect_failure(
        "bootstrap delta carrying a fifth (unauthorized) path",
        lambda: p.delta(candidate, _BootBase()),
    )


def _check_activation_label_annotation() -> None:
    """The cosmetic v39 label mismatch is documented, never silently propagated."""
    if "wepld_v39_activation_label_known_defect=" not in _printer_output():
        base.fail("v40 activation output must document the known v39 cosmetic mismatch")


def _printer_output() -> str:
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        p.printer("test", "test")
    return buf.getvalue()


def run() -> None:
    p.run_predecessor_selftests()
    p.install()

    _check_authority_markers()
    _check_correction_is_exactly_two_targets()
    _check_binding_is_exact_and_idempotent()
    _check_resting_view_wrapper_presents_delegates_and_restores()
    _check_every_consumer_resolves_both_identities_at_call_time()
    _check_predecessor_is_exact()
    _check_workflow_projection_reverses()
    _check_workflow_projection_rejects_drift()
    _check_workflow_projection_rejects_extra_content()
    _check_bootstrap_scope_is_closed()
    _check_bootstrap_delta_rejects_third_path()
    _check_activation_label_annotation()

    print(
        "wepld v40 checkpoint+ledger corrected canonical-documentation target "
        "self-tests: PASS"
    )
