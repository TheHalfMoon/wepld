#!/usr/bin/env python3
"""Self-tests for the v31 admitted-dependency self-test projection repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v31_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v31 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def read_text(
        self, path: str, limit: int = base.MAX_POLICY_FILE_BYTES
    ) -> str:
        data = self.read_bytes(path, limit)
        try:
            return data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            base.fail(f"tracked file is not UTF-8: {path}: {exc}")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def admitted_view() -> Any:
    manifest_path = p.V25.CORE_MANIFEST
    lock_path = p.V25.ROOT_CARGO_LOCK
    register_path = p.V26.DEPENDENCY_REGISTER

    if p._baseline_dependency_state_exact(p.root):
        baseline_lock = p.root.read_bytes(lock_path, p.V25.MAX_LOCK_BYTES)
        baseline_register = p.root.read_bytes(
            register_path, base.MAX_POLICY_FILE_BYTES
        )
        return OverlayView(
            p.root,
            {
                manifest_path: p.V25.ADMITTED_CORE_MANIFEST,
                lock_path: p.V25.expected_admitted_lock(baseline_lock),
                register_path: (
                    baseline_register + p.V29.CORRECTED_S2_DEPENDENCY_REGISTER_APPEND
                ),
            },
        )

    try:
        p._project_exact_admitted_dependency_state(p.root)
    except base.PolicyError:
        base.fail(
            "v31 self-test root dependency state is neither exact canonical baseline "
            "nor exact governed admitted form"
        )
    return p.root


def run() -> None:
    # Prove the canonical-baseline projection itself is well-formed without
    # executing the predecessor chain twice in one process. A second successful
    # predecessor invocation would retain predecessor hooks and contaminate later
    # negative self-tests.
    baseline = p.predecessor_selftest_view(p.root)
    for path, expected in p.P_WF.items():
        if p.V25.sha(baseline.read_bytes(path, base.MAX_POLICY_FILE_BYTES)) != expected:
            base.fail(f"v31 baseline predecessor workflow projection drifted: {path}")

    # Regression for Foundation #834: execute the frozen predecessor chain once
    # against the exact governed S2-AUTH-012 dependency state. On a canonical
    # baseline checkout this is an exact overlay; on an already-admitted checkout
    # the real root is used only after exact reverse-to-baseline validation.
    admitted = admitted_view()
    p.run_predecessor_selftests(admitted)

    p.install()

    # Regression for the real steady-state candidate-local path: inherited
    # base-control checks must see exact v30 workflow bytes while the admitted
    # dependency bytes remain real and governed by v30/v25.
    p.basectrl(admitted, p.root)
    p.files(admitted)

    wrong_lock = OverlayView(
        admitted,
        {
            p.V25.ROOT_CARGO_LOCK: (
                admitted.read_bytes(
                    p.V25.ROOT_CARGO_LOCK, p.V25.MAX_LOCK_BYTES
                )
                + b"\n"
            )
        },
    )
    base.expect_failure_matching(
        "v31 rejects malformed admitted dependency state before predecessor self-tests",
        "neither exact canonical baseline nor exact governed admitted form",
        p.run_predecessor_selftests,
        wrong_lock,
    )

    wrong_policy_file = OverlayView(
        admitted,
        {
            p.P: admitted.read_bytes(p.P, base.MAX_POLICY_FILE_BYTES) + b"\n",
        },
    )
    base.expect_failure_matching(
        "v31 rejects substituted policy bytes",
        "v31 policy file content drifted",
        p.files,
        wrong_policy_file,
    )

    wrong_selftest_file = OverlayView(
        admitted,
        {
            p.T: admitted.read_bytes(p.T, base.MAX_POLICY_FILE_BYTES) + b"\n",
        },
    )
    base.expect_failure_matching(
        "v31 rejects substituted self-test bytes",
        "v31 policy file content drifted",
        p.files,
        wrong_selftest_file,
    )

    if (
        p.AUTH
        != "S2_IDENTITY_STORE_ADMITTED_SELFTEST_PROJECTION_REPAIR_ONLY"
        or p.S2_IMPLEMENTATION_AUTHORITY
        != "STAGED_EXACT_DEPENDENCY_REGISTER_THEN_IDENTITY_STORE_PATHS_ONLY"
        or p.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
        or p.SOURCE_ADMISSION != "NONE"
    ):
        base.fail("v31 authority marker drift")

    print("wepld v31 S2 admitted-dependency self-test projection repair self-tests: PASS")
