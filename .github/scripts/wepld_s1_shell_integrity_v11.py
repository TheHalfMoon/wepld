#!/usr/bin/env python3
"""Deterministic Windows icon fixture repair for bounded S1-010 admission.

This wrapper binds the exact reviewed v10 policy before import and replaces the
lost external icon fixture with a self-reconstructible stdlib-only ICO recipe.
The icon is a neutral technical bootstrap resource, not product branding or UI
authority. No dependency, plugin, package-manager, process, filesystem, network,
sidecar, or frontend authority is introduced.

This file authorizes one repaired future S1-010 stage only. It does not
implement S1-010 product bytes.
"""

from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path

import wepld_integrity as base

POLICY_SCRIPT = ".github/scripts/wepld_s1_shell_integrity_v11.py"
PRIOR_V10_RUNNER_PATH = ".github/scripts/wepld_s1_shell_integrity_v10.py"
EXPECTED_PRIOR_V10_RUNNER_GIT_BLOB_SHA1 = "c562744f9119fc83360343ee1a8297d74a0ac307"

EXPECTED_WORKFLOW_SHA256 = {
    ".github/workflows/foundation-integrity.yml": "cecf5596e962bd8b70f810d919b992470ddb8fecc73584bc980414e41e5a8068",
    ".github/workflows/s1-admission-integrity.yml": "8dcb445191d30643e1ba1476422a3845ef058d36e0725b4558eb534ead8e7fb2",
    ".github/workflows/s1-contracts.yml": "ffbde8237a837ac8bfd6fbfb55985d081c78982fceb619f2da51184834877894",
}

ICON_PATH = "apps/desktop/src-tauri/icons/icon.ico"
EXPECTED_ICON_BYTES = 4286
EXPECTED_ICON_SHA256 = "8293595e42484de7f89ee953c0c4465731010ecb66bb8041097db97524ee47e8"
MAX_ICON_BYTES = 64_000

_INSTALLED = False


def _git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _expected_icon_fixture() -> bytes:
    """Return the exact neutral 32x32 32-bpp Windows ICO fixture.

    The recipe is intentionally stdlib-only and fully deterministic so the
    authorized resource can always be reconstructed from canonical policy.
    """
    width = 32
    height = 32

    rows: list[bytes] = []
    for bottom_up_y in range(height):
        y = height - 1 - bottom_up_y
        row = bytearray()
        for x in range(width):
            if 10 <= x < 22 and 10 <= y < 22:
                red = green = blue = 0xF2
            else:
                red = green = blue = 0x22
            alpha = 0xFF
            row.extend((blue, green, red, alpha))
        rows.append(bytes(row))

    xor_bitmap = b"".join(rows)
    and_row_bytes = ((width + 31) // 32) * 4
    and_mask = b"\x00" * (and_row_bytes * height)

    bitmap_info_header = struct.pack(
        "<IiiHHIIiiII",
        40,
        width,
        height * 2,
        1,
        32,
        0,
        len(xor_bitmap) + len(and_mask),
        0,
        0,
        0,
        0,
    )
    image = bitmap_info_header + xor_bitmap + and_mask

    icon_dir = struct.pack("<HHH", 0, 1, 1)
    image_offset = 6 + 16
    icon_dir_entry = struct.pack(
        "<BBBBHHII",
        width,
        height,
        0,
        0,
        1,
        32,
        len(image),
        image_offset,
    )
    return icon_dir + icon_dir_entry + image


def _bind_prior_v10_runner_before_import() -> None:
    path = Path(__file__).resolve().with_name("wepld_s1_shell_integrity_v10.py")
    try:
        data = path.read_bytes()
    except OSError as exc:
        base.fail(f"unable to read frozen S1-010 v10 shell policy runner: {exc}")
    actual = _git_blob_sha1(data)
    if actual != EXPECTED_PRIOR_V10_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v10 shell policy runner drifted: "
            f"expected={EXPECTED_PRIOR_V10_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )


_bind_prior_v10_runner_before_import()
import wepld_s1_shell_integrity_v10 as v10  # noqa: E402

shell = v10.shell


def _check_icon_identity(data: bytes) -> None:
    if len(data) != EXPECTED_ICON_BYTES:
        base.fail(
            "S1-010 deterministic Tauri icon size drifted: "
            f"expected={EXPECTED_ICON_BYTES} actual={len(data)}"
        )
    actual = hashlib.sha256(data).hexdigest()
    if actual != EXPECTED_ICON_SHA256:
        base.fail(
            "S1-010 Tauri icon must equal the deterministic Windows resource fixture: "
            f"expected_sha256={EXPECTED_ICON_SHA256} actual_sha256={actual}"
        )
    expected = _expected_icon_fixture()
    if data != expected:
        base.fail(
            "S1-010 Tauri icon bytes differ from the canonical deterministic recipe"
        )


def _verify_policy_files(view: base.RepositoryView) -> None:
    runner_bytes = view.read_bytes(PRIOR_V10_RUNNER_PATH, base.MAX_POLICY_FILE_BYTES)
    actual = _git_blob_sha1(runner_bytes)
    if actual != EXPECTED_PRIOR_V10_RUNNER_GIT_BLOB_SHA1:
        base.fail(
            "frozen S1-010 v10 shell policy runner drifted in repository view: "
            f"expected={EXPECTED_PRIOR_V10_RUNNER_GIT_BLOB_SHA1} actual={actual}"
        )
    v10._verify_policy_files(view)


def _verify_shell_icon(view: base.RepositoryView) -> None:
    data = view.read_bytes(ICON_PATH, MAX_ICON_BYTES)
    _check_icon_identity(data)


def _verify_shell_sources(view: base.RepositoryView) -> None:
    shell.verify_build_script(view)
    shell.verify_shell_config(view)
    shell.verify_shell_rust(view)
    shell.verify_frontend(view)
    _verify_shell_icon(view)


def _install_v11_policy() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    v10._install_v10_policy()

    v9 = v10.v9
    hash_modules = (
        v10,
        v9,
        v9.v8,
        v9.v8.v7,
        v9.v8.v7.v6,
        v9.v8.v7.v6.v5,
        v9.v8.v7.v6.v5.v4.v3,
        v9.v8.v7.v6.v5.v4.v3.v2,
        shell,
        shell.prior,
    )
    for module in hash_modules:
        module.EXPECTED_WORKFLOW_SHA256 = EXPECTED_WORKFLOW_SHA256

    shell.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )
    shell.prior.prior.EXTENSION_CONTROLLED_PATHS = frozenset(
        set(shell.prior.prior.EXTENSION_CONTROLLED_PATHS) | {POLICY_SCRIPT}
    )

    shell.verify_policy_files = _verify_policy_files
    shell.verify_shell_sources = _verify_shell_sources
    _INSTALLED = True


def selftest() -> None:
    v10.selftest()
    _install_v11_policy()

    generated = _expected_icon_fixture()
    if len(generated) != EXPECTED_ICON_BYTES:
        base.fail(
            "canonical deterministic icon recipe produced wrong size: "
            f"expected={EXPECTED_ICON_BYTES} actual={len(generated)}"
        )
    generated_sha256 = hashlib.sha256(generated).hexdigest()
    if generated_sha256 != EXPECTED_ICON_SHA256:
        base.fail(
            "canonical deterministic icon recipe produced wrong SHA-256: "
            f"expected={EXPECTED_ICON_SHA256} actual={generated_sha256}"
        )
    _check_icon_identity(generated)

    base.expect_failure_matching(
        "S1-010 deterministic icon size mutation",
        "icon size drifted",
        _check_icon_identity,
        generated[:-1],
    )
    mutated = bytearray(generated)
    mutated[-1] ^= 1
    base.expect_failure_matching(
        "S1-010 deterministic icon byte mutation",
        "must equal the deterministic Windows resource fixture",
        _check_icon_identity,
        bytes(mutated),
    )

    if len(EXPECTED_ICON_SHA256) != 64:
        base.fail("S1-010 deterministic icon SHA-256 must be 64 lowercase hexadecimal characters")
    if EXPECTED_ICON_SHA256.lower() != EXPECTED_ICON_SHA256:
        base.fail("S1-010 deterministic icon SHA-256 must be lowercase")

    print("wepld S1 Tauri shell deterministic Windows-icon policy self-tests: PASS")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "selftest":
        try:
            selftest()
            return 0
        except base.PolicyError as exc:
            print(f"wepld integrity verification: FAIL: {exc}", file=sys.stderr)
            return 1

    _install_v11_policy()
    return shell.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
