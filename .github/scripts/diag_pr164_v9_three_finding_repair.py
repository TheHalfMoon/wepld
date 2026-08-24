#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from pathlib import Path

SCRIPT = Path('.github/scripts/wepld_pictorial_agile_source_admission_v9_integrity.py')
EVIDENCE = Path('docs/acquisition/WEPLD_PICTORIAL_LOCK_METADATA_OVERLAY_V9_EVIDENCE_2026-08-24.md')
REJECTED_HEAD = '9d7cec43dca2a41a149f7749aa5f6cfb1ad25714'


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

    review_section = r'''

## Independent exact-head review repair — F1/F2/F3

The independent review of rejected v9 head
`9d7cec43dca2a41a149f7749aa5f6cfb1ad25714` identified three findings.
This evidence revision records the bounded repair design only; it does not grant
merge, dependency, donor, product-runtime, provider/model, or completion authority.

### F1 — current no-snapshot canonical progression

After v9 is canonical, the first source-admission candidate must converge the exact
trusted v9 policy base with the exact repaired source reference
`04cc279133d536e2b4b68e01c019d7b595f0ed42`. The candidate is accepted only when:

- every changed path relative to the trusted policy base is a v7-classified
  Pictorial/Agile source/provenance/legal path;
- the complete source surface (Git mode + blob identity) is byte-identical to the
  exact repaired reference source surface;
- the repaired vendor, Pictorial, Agile, package.json, and bun.lock identities
  remain the content-addressed values recorded above; and
- the candidate commit is an exact two-parent convergence of the repaired reference
  and the trusted v9 policy base.

The raw `04cc279...` tree by itself is not an admission candidate after v9 becomes
canonical because it does not contain the canonical v9 policy/evidence bytes. A
fresh convergence candidate is therefore required and remains separately governed.

### F2 — pre-merge remote and post-merge local activation topology

Remote PR qualification and post-merge local activation intentionally use different
view types. v9 now verifies the same source-surface identity in both cases instead
of requiring a LocalRepositoryView to satisfy RemoteRepositoryView type checks.

For pre-merge qualification, the remote candidate must have exactly the repaired
reference and trusted v9 policy base as its two parents. For post-merge activation,
the pushed local checkout must be the merge of the trusted v9 policy base and that
qualified convergence candidate. The convergence candidate itself must still have
exactly the repaired reference and trusted v9 policy base as parents. This preserves
repair lineage across both stages without weakening the data-only PR gate.

### F3 — evidence retention

Whenever the v9 policy wrapper is present, this evidence file is mandatory and its
Git blob must equal the policy-bound evidence identity. Deletion, rename, or byte
mutation fails closed. The v9 self-tests include explicit deletion and mutation
negative oracles.

```text
REJECTED_V9_HEAD=9d7cec43dca2a41a149f7749aa5f6cfb1ad25714
REVIEW_RESULT=FAIL_REPAIRED_BY_SUCCESSOR_CANDIDATE
F1_CURRENT_NO_SNAPSHOT_PROGRESSION=REPAIRED_IN_CANDIDATE
F2_LOCAL_REMOTE_ACTIVATION_TOPOLOGY=REPAIRED_IN_CANDIDATE
F3_EVIDENCE_RETENTION=REPAIRED_IN_CANDIDATE
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
    if '## Independent exact-head review repair — F1/F2/F3' in evidence:
        raise SystemExit('review repair evidence section already present')
    evidence = evidence.rstrip() + review_section + '\n'
    evidence_bytes = evidence.encode('utf-8')
    evidence_blob = git_blob_sha1(evidence_bytes)

    script = replace_once(
        script,
        'EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "8a6529353a93f6d7bdf49e34f03028afcbc29fde"',
        f'EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "{evidence_blob}"',
        'evidence blob constant',
    )

    anchor = 'def _validate_overlay_shape(\n'
    helpers = r'''def _local_commit_sha(view: base.LocalRepositoryView) -> str:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(view.root), "rev-parse", "HEAD"],
            stderr=subprocess.STDOUT,
            text=True,
        ).strip().lower()
    except subprocess.CalledProcessError as exc:
        base.fail(f"unable to resolve local v9 commit identity: {exc}")
    if len(raw) != 40 or any(ch not in "0123456789abcdef" for ch in raw):
        base.fail(f"malformed local v9 commit identity: {raw!r}")
    return raw


def _view_commit_sha(view: base.RepositoryView) -> str:
    if isinstance(view, base.RemoteRepositoryView):
        raw = view.commit_sha.lower()
    elif isinstance(view, base.LocalRepositoryView):
        raw = _local_commit_sha(view)
    else:
        base.fail("v9 admission lineage requires local or remote repository view")
    if len(raw) != 40 or any(ch not in "0123456789abcdef" for ch in raw):
        base.fail(f"malformed v9 repository-view commit identity: {raw!r}")
    return raw


def _shared_trusted_client(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> object:
    clients = [view.client for view in (candidate, policy_base) if isinstance(view, base.RemoteRepositoryView)]
    if not clients:
        base.fail("v9 repaired-source admission requires one trusted remote view")
    first = clients[0]
    if any(client is not first for client in clients[1:]):
        base.fail("v9 repaired-source admission remote views do not share trusted client")
    return first


def _source_surface_map(view: base.RepositoryView) -> dict[str, tuple[str, str]]:
    return {path: identity for path, identity in _blob_map(view).items() if PRIOR_IS_SOURCE_PATH(path)}


def _require_source_surface_equal(actual: dict[str, tuple[str, str]], expected: dict[str, tuple[str, str]], label: str) -> None:
    if actual == expected:
        return
    all_paths = sorted(set(actual) | set(expected))
    drift = [path for path in all_paths if actual.get(path) != expected.get(path)]
    preview = ", ".join(drift[:12])
    suffix = "" if len(drift) <= 12 else f" (+{len(drift) - 12} more)"
    base.fail(f"{label} source surface drifted: {preview}{suffix}")


def _commit_payload(client: object, sha: str, label: str) -> dict[str, Any]:
    payload = client.json(f"https://api.github.com/repos/{base.REPOSITORY}/git/commits/{sha}")
    if not isinstance(payload, dict) or payload.get("sha") != sha:
        base.fail(f"{label} commit API identity drifted")
    return payload


def _parent_shas(payload: dict[str, Any], label: str) -> tuple[str, ...]:
    parents = payload.get("parents")
    if not isinstance(parents, list):
        base.fail(f"{label} parent topology is malformed")
    shas: list[str] = []
    for parent in parents:
        if not isinstance(parent, dict) or not isinstance(parent.get("sha"), str):
            base.fail(f"{label} parent topology is malformed")
        shas.append(parent["sha"].lower())
    return tuple(shas)


def _require_exact_parent_set(payload: dict[str, Any], expected: frozenset[str], label: str) -> None:
    actual = _parent_shas(payload, label)
    if len(actual) != len(expected) or frozenset(actual) != expected:
        base.fail(f"{label} parent lineage drifted: expected={sorted(expected)} actual={list(actual)}")


def _require_initial_admission_path_shape(changed: frozenset[str]) -> None:
    if not changed:
        base.fail("v9 initial repaired-source admission has empty delta")
    unexpected = sorted(path for path in changed if not PRIOR_IS_SOURCE_PATH(path))
    if unexpected:
        base.fail("v9 initial repaired-source admission changed non-source paths: " + ", ".join(unexpected))
    if LOCK_PATH not in changed:
        base.fail("v9 initial repaired-source admission is missing repaired bun.lock")


def _require_initial_repaired_admission(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> None:
    changed = _changed_paths_exact(candidate, policy_base)
    _require_initial_admission_path_shape(changed)

    client = _shared_trusted_client(candidate, policy_base)
    reference = base.RemoteRepositoryView(base.REPOSITORY, REPAIR_CANDIDATE_HEAD, client)
    predecessor = base.RemoteRepositoryView(base.REPOSITORY, PREDECESSOR_SOURCE_HEAD, client)
    _require_remote_lineage(reference, predecessor)

    _require_source_surface_equal(_source_surface_map(candidate), _source_surface_map(reference), "v9 initial repaired-source candidate")
    if candidate.tree_identity("vendor") != REPAIRED_VENDOR_TREE:
        base.fail("v9 initial repaired-source vendor tree drifted")
    if candidate.tree_identity("vendor/pictorial") != REPAIRED_PICTORIAL_TREE:
        base.fail("v9 initial repaired-source Pictorial tree drifted")
    if candidate.tree_identity("vendor/agile") != AGILE_TREE:
        base.fail("v9 initial repaired-source Agile tree drifted")
    if _blob_identity(candidate, PACKAGE_JSON_PATH) != PACKAGE_JSON_BLOB:
        base.fail("v9 initial repaired-source package.json drifted")
    lock_bytes = candidate.read_bytes(LOCK_PATH, base.MAX_LOCKFILE_BYTES)
    if _git_blob_sha1(lock_bytes) != REPAIRED_LOCK_BLOB:
        base.fail("v9 initial repaired-source lock Git blob drifted")
    if _sha256(lock_bytes) != REPAIRED_LOCK_SHA256:
        base.fail("v9 initial repaired-source lock SHA-256 drifted")

    policy_sha = _view_commit_sha(policy_base)
    candidate_sha = _view_commit_sha(candidate)
    if isinstance(candidate, base.RemoteRepositoryView):
        payload = _commit_payload(client, candidate_sha, "v9 pre-merge admission candidate")
        _require_exact_parent_set(payload, frozenset({REPAIR_CANDIDATE_HEAD, policy_sha}), "v9 pre-merge admission candidate")
        return

    pushed = _commit_payload(client, candidate_sha, "v9 post-merge pushed head")
    pushed_parents = _parent_shas(pushed, "v9 post-merge pushed head")
    if len(pushed_parents) != 2 or policy_sha not in pushed_parents:
        base.fail("v9 post-merge pushed head must merge trusted policy base with qualified admission candidate")
    admission_sha = next(sha for sha in pushed_parents if sha != policy_sha)
    admission_payload = _commit_payload(client, admission_sha, "v9 qualified admission candidate")
    _require_exact_parent_set(admission_payload, frozenset({REPAIR_CANDIDATE_HEAD, policy_sha}), "v9 qualified admission candidate")
    admission_view = base.RemoteRepositoryView(base.REPOSITORY, admission_sha, client)
    _require_source_surface_equal(_source_surface_map(admission_view), _source_surface_map(reference), "v9 qualified admission candidate")


'''
    if anchor not in script:
        raise SystemExit('helper insertion anchor missing')
    script = script.replace(anchor, helpers + anchor, 1)

    pattern = re.compile(r'def _require_exact_delta_v9\(.*?\n\ndef _compare_base_controlled_v9\(', re.S)
    replacement = r'''def _require_exact_delta_v9(
    candidate: base.RepositoryView,
    policy_base: base.RepositoryView,
) -> None:
    changed = _changed_paths_exact(candidate, policy_base)

    if _is_bootstrap_base(policy_base):
        if changed == BOOTSTRAP_DELTA_PATHS:
            _require_prior_policy_base(policy_base)
            if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
                base.fail("Pictorial/Agile v9 policy bootstrap cannot mutate source")
            return
        if changed & BOOTSTRAP_DELTA_PATHS:
            base.fail(
                "Pictorial/Agile source-admission-v9 bootstrap delta must be exactly "
                "the v9 policy, two workflows, and bound evidence record"
            )
        if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
            base.fail("Pictorial/Agile source cannot transition before v9 is canonical")
        _delegate_exact_delta(candidate, policy_base)
        return

    base_has_snapshot = PRIOR_SNAPSHOT_PRESENT(policy_base)
    candidate_has_snapshot = PRIOR_SNAPSHOT_PRESENT(candidate)
    if not base_has_snapshot and candidate_has_snapshot:
        _require_initial_repaired_admission(candidate, policy_base)
        return

    if changed == frozenset({LOCK_PATH}):
        _require_bound_overlay(
            candidate,
            policy_base,
            require_remote_lineage=(isinstance(candidate, base.RemoteRepositoryView) and isinstance(policy_base, base.RemoteRepositoryView)),
        )
        return

    if any(PRIOR_IS_SOURCE_PATH(path) for path in changed):
        base.fail(
            "Pictorial/Agile source remains frozen after v8 except the exact "
            "v9 repaired-source admission or one bound bun.lock overlay"
        )
    _delegate_exact_delta(candidate, policy_base)


def _compare_base_controlled_v9('''
    script, count = pattern.subn(replacement, script, count=1)
    if count != 1:
        raise SystemExit(f'exact-delta replacement count={count}')

    script = replace_once(
        script,
        '    elif candidate_has_snapshot:\n        base.fail("v9 cannot introduce a new Pictorial/Agile source snapshot")',
        '    elif candidate_has_snapshot:\n        _require_initial_repaired_admission(candidate, policy_base)',
        'F1 compare-base snapshot tail',
    )

    evidence_anchor = 'def _verify_policy_files_v9(view: base.RepositoryView) -> None:\n'
    evidence_helper = r'''def _require_evidence_record(view: base.RepositoryView) -> None:
    paths = _paths(view)
    if POLICY_SCRIPT not in paths:
        return
    if EVIDENCE_PATH not in paths:
        base.fail("Pictorial/Agile source-admission-v9 evidence record is missing")
    evidence = view.read_bytes(EVIDENCE_PATH, base.MAX_POLICY_FILE_BYTES)
    if _git_blob_sha1(evidence) != EXPECTED_EVIDENCE_GIT_BLOB_SHA1:
        base.fail("Pictorial/Agile source-admission-v9 evidence record drifted")


'''
    if evidence_anchor not in script:
        raise SystemExit('evidence helper anchor missing')
    script = script.replace(evidence_anchor, evidence_helper + evidence_anchor, 1)

    script = replace_once(
        script,
        '    if EVIDENCE_PATH in _paths(view):\n        evidence = view.read_bytes(EVIDENCE_PATH, base.MAX_POLICY_FILE_BYTES)\n        if _git_blob_sha1(evidence) != EXPECTED_EVIDENCE_GIT_BLOB_SHA1:\n            base.fail("Pictorial/Agile source-admission-v9 evidence record drifted")',
        '    _require_evidence_record(view)',
        'F3 evidence retention',
    )

    selftest_anchor = 'def _selftest_authority() -> None:\n'
    selftests = r'''def _selftest_review_repairs() -> None:
    _require_initial_admission_path_shape(frozenset({LOCK_PATH}))
    base.expect_failure_matching(
        "v9 initial admission non-source rejection",
        "changed non-source paths",
        _require_initial_admission_path_shape,
        frozenset({LOCK_PATH, FOUNDATION_WORKFLOW}),
    )
    base.expect_failure_matching(
        "v9 initial admission missing-lock rejection",
        "missing repaired bun.lock",
        _require_initial_admission_path_shape,
        frozenset({next(iter(prior.prior.SOURCE_ARTIFACT_BLOBS))}),
    )

    policy_parent = "a" * 40
    _require_exact_parent_set(
        {"parents": [{"sha": REPAIR_CANDIDATE_HEAD}, {"sha": policy_parent}]},
        frozenset({REPAIR_CANDIDATE_HEAD, policy_parent}),
        "v9 parent-shape positive",
    )
    base.expect_failure_matching(
        "v9 wrong-parent rejection",
        "parent lineage drifted",
        _require_exact_parent_set,
        {"parents": [{"sha": REPAIR_CANDIDATE_HEAD}, {"sha": "b" * 40}]},
        frozenset({REPAIR_CANDIDATE_HEAD, policy_parent}),
        "v9 parent-shape negative",
    )

    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])
    evidence = local.read_bytes(EVIDENCE_PATH, base.MAX_POLICY_FILE_BYTES)
    _require_evidence_record(_memory_view({POLICY_SCRIPT: b"policy", EVIDENCE_PATH: evidence}))
    base.expect_failure_matching(
        "v9 evidence deletion rejection",
        "evidence record is missing",
        _require_evidence_record,
        _memory_view({POLICY_SCRIPT: b"policy"}),
    )
    base.expect_failure_matching(
        "v9 evidence mutation rejection",
        "evidence record drifted",
        _require_evidence_record,
        _memory_view({POLICY_SCRIPT: b"policy", EVIDENCE_PATH: evidence + b"x"}),
    )


'''
    if selftest_anchor not in script:
        raise SystemExit('review selftest anchor missing')
    script = script.replace(selftest_anchor, selftests + selftest_anchor, 1)
    script = replace_once(
        script,
        '    _selftest_overlay_contract()\n    _selftest_authority()',
        '    _selftest_overlay_contract()\n    _selftest_review_repairs()\n    _selftest_authority()',
        'review selftest call',
    )

    SCRIPT.write_text(script, encoding='utf-8', newline='\n')
    EVIDENCE.write_text(evidence, encoding='utf-8', newline='\n')
    Path('diag-v9-repair-summary.txt').write_text(
        '\n'.join([
            f'evidence_blob={evidence_blob}',
            f'script_sha256={hashlib.sha256(script.encode()).hexdigest()}',
            f'evidence_sha256={hashlib.sha256(evidence_bytes).hexdigest()}',
            'changed_files=2',
            'authority_expansion=NONE',
        ]) + '\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    main()
