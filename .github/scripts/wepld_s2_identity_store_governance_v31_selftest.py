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


def run() -> None:
    # v31 bootstrap itself runs with canonical baseline dependency bytes but v31
    # workflow bytes. The predecessor must still self-test against exact v30.
    p.run_predecessor_selftests(p.root)

    # Regression for Foundation #834: the same predecessor chain must also pass
    # when the repository contains the exact governed S2-AUTH-012 dependency
    # state, by projecting only those admitted bytes back to canonical baseline.
    admitted = admitted_view()
    p.run_predecessor_selftests(admitted)

    p.install()
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
