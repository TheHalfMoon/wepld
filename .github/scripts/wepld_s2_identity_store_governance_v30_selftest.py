#!/usr/bin/env python3
"""Self-tests for the v30 dependency policy-file projection repair."""

from typing import Any

import wepld_integrity as base
import wepld_s2_identity_store_governance_v30_integrity as p


class OverlayView:
    def __init__(self, view: Any, replacements: dict[str, bytes]) -> None:
        self._view = view
        self._replacements = replacements

    def read_bytes(self, path: str, max_bytes: int) -> bytes:
        if path in self._replacements:
            data = self._replacements[path]
            if len(data) > max_bytes:
                base.fail(f"v30 self-test overlay exceeds read bound: {path}")
            return data
        return self._view.read_bytes(path, max_bytes)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._view, name)


def admitted_view() -> Any:
    manifest_path = p.p.s.r.q.p.CORE_MANIFEST
    lock_path = p.p.s.r.q.p.ROOT_CARGO_LOCK
    register_path = p.p.s.r.q.DEPENDENCY_REGISTER

    baseline_lock = p.root.read_bytes(lock_path, p.p.s.r.q.p.MAX_LOCK_BYTES)
    baseline_register = p.root.read_bytes(register_path, base.MAX_POLICY_FILE_BYTES)
    return OverlayView(
        p.root,
        {
            manifest_path: p.p.s.r.q.p.ADMITTED_CORE_MANIFEST,
            lock_path: p.p.s.r.q.p.expected_admitted_lock(baseline_lock),
            register_path: (
                baseline_register + p.p.CORRECTED_S2_DEPENDENCY_REGISTER_APPEND
            ),
        },
    )


def run() -> None:
    p.prepare_p()
    p.p.selftest()

    view = admitted_view()
    if view.read_bytes(
        p.p.s.r.q.p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES
    ) != p.p.s.r.q.p.ADMITTED_CORE_MANIFEST:
        base.fail("v30 admitted self-test view Core manifest drifted")
    admitted_lock = view.read_bytes(
        p.p.s.r.q.p.ROOT_CARGO_LOCK, p.p.s.r.q.p.MAX_LOCK_BYTES
    )
    if admitted_lock.count(p.p.s.r.q.p.ADMITTED_CORE_LOCK_STANZA) != 1:
        base.fail("v30 admitted self-test view Core lock stanza drifted")
    admitted_register = view.read_bytes(
        p.p.s.r.q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES
    )
    if not admitted_register.endswith(p.p.CORRECTED_S2_DEPENDENCY_REGISTER_APPEND):
        base.fail("v30 admitted self-test view dependency register drifted")

    p.install()
    p.files(view)
    paths = base.validate_entries(view.entries())
    p.shell_component_base(view, paths)

    projected = p.project_admitted_dependency_state(view)
    if (
        p.p.s.r.q.p.blob(
            projected.read_bytes(
                p.p.s.r.q.p.CORE_MANIFEST, base.MAX_POLICY_FILE_BYTES
            )
        )
        != p.CORE_MANIFEST_BASE_BLOB
    ):
        base.fail("v30 projected Core manifest baseline identity drifted")
    if (
        p.p.s.r.q.p.blob(
            projected.read_bytes(
                p.p.s.r.q.p.ROOT_CARGO_LOCK, p.p.s.r.q.p.MAX_LOCK_BYTES
            )
        )
        != p.ROOT_LOCK_BASE_BLOB
    ):
        base.fail("v30 projected Cargo.lock baseline identity drifted")
    if (
        p.p.s.r.q.p.blob(
            projected.read_bytes(
                p.p.s.r.q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES
            )
        )
        != p.DEPENDENCY_REGISTER_BASE_BLOB
    ):
        base.fail("v30 projected dependency-register baseline identity drifted")

    wrong_manifest = OverlayView(
        view,
        {
            p.p.s.r.q.p.CORE_MANIFEST: (
                p.p.s.r.q.p.ADMITTED_CORE_MANIFEST + b"\n"
            )
        },
    )
    base.expect_failure_matching(
        "v30 rejects widened admitted manifest",
        "neither exact canonical baseline nor exact governed admitted form",
        p.files,
        wrong_manifest,
    )

    wrong_lock = OverlayView(
        view,
        {
            p.p.s.r.q.p.ROOT_CARGO_LOCK: (
                view.read_bytes(
                    p.p.s.r.q.p.ROOT_CARGO_LOCK, p.p.s.r.q.p.MAX_LOCK_BYTES
                )
                + b"\n"
            )
        },
    )
    base.expect_failure_matching(
        "v30 rejects whole-lock drift hidden by structural dependency state",
        "does not reverse to exact canonical v29 baseline",
        p.files,
        wrong_lock,
    )

    wrong_register = OverlayView(
        view,
        {
            p.p.s.r.q.DEPENDENCY_REGISTER: (
                view.read_bytes(
                    p.p.s.r.q.DEPENDENCY_REGISTER, base.MAX_POLICY_FILE_BYTES
                )
                + b"\n"
            )
        },
    )
    base.expect_failure_matching(
        "v30 rejects dependency-register suffix drift",
        "neither exact canonical baseline nor exact governed admitted form",
        p.files,
        wrong_register,
    )

    if (
        p.AUTH != "S2_IDENTITY_STORE_POLICY_FILE_PROJECTION_REPAIR_ONLY"
        or p.S2_IMPLEMENTATION_AUTHORITY
        != "STAGED_EXACT_DEPENDENCY_REGISTER_THEN_IDENTITY_STORE_PATHS_ONLY"
        or p.DEPENDENCY_ADMISSION
        != "STAGED_EXACT_GETRANDOM_0_4_3_SHA2_0_10_9_WITH_REGISTER_ONLY"
        or p.SOURCE_ADMISSION != "NONE"
    ):
        base.fail("v30 authority marker drift")

    print("wepld v30 S2 dependency policy-file projection repair self-tests: PASS")
