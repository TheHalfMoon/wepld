#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

SCRIPT = Path('.github/scripts/wepld_pictorial_agile_source_admission_v9_integrity.py')
EVIDENCE = Path('docs/acquisition/WEPLD_PICTORIAL_LOCK_METADATA_OVERLAY_V9_EVIDENCE_2026-08-24.md')
BOUND_HEAD = 'f91d765d21f497502e21414f49d42869218066b5'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode('ascii') + data).hexdigest()


def main() -> None:
    script = SCRIPT.read_text(encoding='utf-8')
    evidence = EVIDENCE.read_text(encoding='utf-8')

    section = r'''

## F1 inherited repaired-snapshot verifier correction

Deterministic execution of the exact production `verify-remote` entrypoint against
the F2b convergence object exposed a remaining F1 mismatch at exact head
`f91d765d21f497502e21414f49d42869218066b5`.

The initial repaired-source admission correctly bound the candidate to the repaired
vendor identities, but a later steady-state base-control pass received a projected
`_PriorV18View` containing that same repaired snapshot and delegated it to the frozen
v7 snapshot verifier. v7 correctly accepts only the original snapshot trees, so it
rejected the already-bound repaired tree with:

`Pictorial/Agile frozen subtree drifted: vendor: expected=4c5259... actual=88b58d...`

This successor adds a v9 snapshot verifier with exactly two admissible generations:

- ORIGINAL: exact original vendor + Pictorial trees, delegated unchanged to the
  frozen v7 verifier;
- REPAIRED: exact repaired vendor + Pictorial trees, exact unchanged Agile tree,
  exact repaired package.json/bun.lock identities, and the same frozen v7 source-map,
  tools, legal, third-party legal, canonical-contract, and acquisition-artifact
  identities.

Mixed or third tree identities fail closed. No provenance/source-map record is
rewritten and no donor/dependency/runtime/provider authority is added.

```text
F1_REJECTED_HEAD=f91d765d21f497502e21414f49d42869218066b5
F1_FAILURE=INHERITED_V7_ORIGINAL_TREE_VERIFIER_ON_REPAIRED_PROJECTED_VIEW
F1_REPAIR=EXACT_TWO_GENERATION_V9_SNAPSHOT_VERIFIER
DEPENDENCY_ADMISSION=NONE
PACKAGE_EXECUTION=NONE
DONOR_EXECUTION=NONE
MODEL_PROVIDER_EXECUTION=NONE
PRODUCT_RUNTIME_ADMISSION=NONE
CANONICAL_POLICY_MERGE=NOT_AUTHORIZED
PR164_READY=NOT_AUTHORIZED
PR162_MERGE=NOT_AUTHORIZED
PR136_MERGE=NOT_AUTHORIZED
```
'''
    marker = '## F1 inherited repaired-snapshot verifier correction'
    if marker in evidence:
        raise SystemExit('F1 repaired-snapshot correction already present')
    evidence = evidence.rstrip() + section + '\n'
    evidence_bytes = evidence.encode('utf-8')
    evidence_blob = git_blob_sha1(evidence_bytes)

    script = replace_once(
        script,
        'EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "f065f04e0234d0a4dcbaf90be08b59f677331158"',
        f'EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "{evidence_blob}"',
        'evidence binding',
    )

    alias_anchor = 'PRIOR_IS_SOURCE_PATH = prior.PRIOR_IS_SOURCE_PATH\n'
    alias_addition = '''PRIOR_IS_SOURCE_PATH = prior.PRIOR_IS_SOURCE_PATH\nV7_VERIFY_ARTIFACT_BLOBS = prior.prior._verify_artifact_blobs\nV7_SOURCE_MAPS_TREE = "34fbb6a69a9e4dfa03ed20cc0f94d9814883ad58"\nV7_SOURCE_TOOLS_TREE = "444f9361eb3d204231f18e9148d073a01e04df3d"\nV7_SOURCE_LEGAL_TREE = "9b65277fa56081435196f21e1c6e5f8e9130a0a5"\nV7_SOURCE_LEGAL_THIRD_PARTY_TREE = "959d26daa7f8a872aee8710a25a4afb017a40c8c"\nV7_CONTRACT_PATH = "docs/acquisition/WEPLD_PICTORIAL_AGILE_FULL_DONOR_IMPORT_REBRAND_CONTRACT_2026-08-22.md"\nV7_CONTRACT_GIT_BLOB_SHA1 = "05e58e331fa6a119227127cb146e135f5b9789b7"\n'''
    script = replace_once(script, alias_anchor, alias_addition, 'v7 frozen verifier aliases')

    compare_anchor = 'def _compare_base_controlled_v9(\n'
    helper = r'''def _classify_v9_snapshot_trees(vendor_tree: str, pictorial_tree: str) -> str:
    if vendor_tree == ORIGINAL_VENDOR_TREE and pictorial_tree == ORIGINAL_PICTORIAL_TREE:
        return "ORIGINAL"
    if vendor_tree == REPAIRED_VENDOR_TREE and pictorial_tree == REPAIRED_PICTORIAL_TREE:
        return "REPAIRED"
    base.fail(
        "Pictorial/Agile v9 snapshot generation is mixed or unknown: "
        f"vendor={vendor_tree} pictorial={pictorial_tree}"
    )


def _require_v9_tree(view: base.RepositoryView, path: str, expected: str) -> None:
    actual = view.tree_identity(path)
    if actual != expected:
        base.fail(
            "Pictorial/Agile v9 repaired snapshot subtree drifted: "
            f"{path}: expected={expected} actual={actual}"
        )


def _verify_repaired_snapshot_v9(view: base.RepositoryView) -> None:
    _require_v9_tree(view, "vendor", REPAIRED_VENDOR_TREE)
    _require_v9_tree(view, "vendor/pictorial", REPAIRED_PICTORIAL_TREE)
    _require_v9_tree(view, "vendor/agile", AGILE_TREE)
    _require_v9_tree(view, "docs/acquisition/source-maps", V7_SOURCE_MAPS_TREE)
    _require_v9_tree(view, "docs/acquisition/tools", V7_SOURCE_TOOLS_TREE)
    _require_v9_tree(view, "legal", V7_SOURCE_LEGAL_TREE)
    _require_v9_tree(view, "legal/third-party", V7_SOURCE_LEGAL_THIRD_PARTY_TREE)

    if _blob_identity(view, PACKAGE_JSON_PATH) != PACKAGE_JSON_BLOB:
        base.fail("Pictorial/Agile v9 repaired snapshot package.json drifted")
    lock_bytes = view.read_bytes(LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    if _git_blob_sha1(lock_bytes) != REPAIRED_LOCK_BLOB:
        base.fail("Pictorial/Agile v9 repaired snapshot lock Git blob drifted")
    if _sha256(lock_bytes) != REPAIRED_LOCK_SHA256:
        base.fail("Pictorial/Agile v9 repaired snapshot lock SHA-256 drifted")

    contract = _git_blob_sha1(
        view.read_bytes(V7_CONTRACT_PATH, base.MAX_POLICY_FILE_BYTES)
    )
    if contract != V7_CONTRACT_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile v9 repaired snapshot canonical contract drifted")

    if prior.prior._verify_artifact_blobs is not V7_VERIFY_ARTIFACT_BLOBS:
        base.fail("Pictorial/Agile v9 frozen v7 artifact verifier drifted")
    V7_VERIFY_ARTIFACT_BLOBS(view)


def _verify_v9_snapshot(view: base.RepositoryView) -> None:
    generation = _classify_v9_snapshot_trees(
        view.tree_identity("vendor"),
        view.tree_identity("vendor/pictorial"),
    )
    if generation == "ORIGINAL":
        PRIOR_VERIFY_SNAPSHOT(view, transition=False)
        return
    if generation != "REPAIRED":
        base.fail(f"unexpected Pictorial/Agile v9 snapshot generation: {generation}")
    _verify_repaired_snapshot_v9(view)


'''
    if compare_anchor not in script:
        raise SystemExit('compare anchor missing')
    script = script.replace(compare_anchor, helper + compare_anchor, 1)

    script = replace_once(
        script,
        '        PRIOR_VERIFY_SNAPSHOT(policy_base, transition=False)\n',
        '        _verify_v9_snapshot(policy_base)\n',
        'steady policy-base snapshot verifier',
    )
    script = replace_once(
        script,
        '            PRIOR_VERIFY_SNAPSHOT(candidate, transition=False)\n',
        '            _verify_v9_snapshot(candidate)\n',
        'steady candidate snapshot verifier',
    )

    selftest_anchor = 'def _selftest_authority() -> None:\n'
    tests = r'''def _selftest_v9_snapshot_generation() -> None:
    if _classify_v9_snapshot_trees(ORIGINAL_VENDOR_TREE, ORIGINAL_PICTORIAL_TREE) != "ORIGINAL":
        base.fail("v9 original snapshot generation classifier drifted")
    if _classify_v9_snapshot_trees(REPAIRED_VENDOR_TREE, REPAIRED_PICTORIAL_TREE) != "REPAIRED":
        base.fail("v9 repaired snapshot generation classifier drifted")
    base.expect_failure_matching(
        "v9 mixed snapshot generation rejection",
        "mixed or unknown",
        _classify_v9_snapshot_trees,
        ORIGINAL_VENDOR_TREE,
        REPAIRED_PICTORIAL_TREE,
    )
    base.expect_failure_matching(
        "v9 unknown snapshot generation rejection",
        "mixed or unknown",
        _classify_v9_snapshot_trees,
        "0" * 40,
        "1" * 40,
    )


'''
    if selftest_anchor not in script:
        raise SystemExit('selftest anchor missing')
    script = script.replace(selftest_anchor, tests + selftest_anchor, 1)
    script = replace_once(
        script,
        '    _selftest_local_remote_client_bridge()\n    _selftest_authority()\n',
        '    _selftest_local_remote_client_bridge()\n    _selftest_v9_snapshot_generation()\n    _selftest_authority()\n',
        'v9 snapshot selftest invocation',
    )

    SCRIPT.write_text(script, encoding='utf-8')
    EVIDENCE.write_text(evidence, encoding='utf-8')
    Path('/tmp/pr164-v9-f1-repair.manifest').write_text(
        '\n'.join([
            f'bound_head={BOUND_HEAD}',
            f'script_sha256={hashlib.sha256(script.encode()).hexdigest()}',
            f'evidence_blob={evidence_blob}',
            f'evidence_sha256={hashlib.sha256(evidence_bytes).hexdigest()}',
            'changed_files=2',
            'authority_expansion=NONE',
        ]) + '\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    main()
