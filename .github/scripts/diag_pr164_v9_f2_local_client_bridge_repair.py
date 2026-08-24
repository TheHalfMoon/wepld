#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

SCRIPT = Path('.github/scripts/wepld_pictorial_agile_source_admission_v9_integrity.py')
EVIDENCE = Path('docs/acquisition/WEPLD_PICTORIAL_LOCK_METADATA_OVERLAY_V9_EVIDENCE_2026-08-24.md')
BOUND_HEAD = '7d24c3047191822d687b5fb3cd52e228a6353651'


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

## F2 exact local+remote activation repair — successor correction

The first F1/F2 successor candidate repaired the intended topology but an actual
`verify-local --remote-baseline` diagnostic against exact head
`7d24c3047191822d687b5fb3cd52e228a6353651` exposed a remaining F2 defect:
a later callback can compare two LocalRepositoryView instances after the canonical
v5 runner has already established the trusted remote-baseline client. The prior
helper rejected that callback with `v9 repaired-source admission requires one
trusted remote view`.

This successor does not weaken lineage, source-surface, tree, package.json, lock,
or evidence checks. It creates one scoped GitHubClient only inside the existing
`verify-local --remote-baseline` entrypoint, makes that client available to nested
local/local callbacks, and clears it in `finally`. A Local+Local callback outside
that exact remote-baseline scope remains fail-closed.

```text
F2_REJECTED_HEAD=7d24c3047191822d687b5fb3cd52e228a6353651
F2_FAILURE=v9 repaired-source admission requires one trusted remote view
F2_REPAIR=SCOPED_REMOTE_BASELINE_CLIENT_BRIDGE
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
    marker = '## F2 exact local+remote activation repair — successor correction'
    if marker in evidence:
        raise SystemExit('F2 successor correction already present')
    evidence = evidence.rstrip() + section + '\n'
    evidence_bytes = evidence.encode('utf-8')
    evidence_blob = git_blob_sha1(evidence_bytes)

    script = replace_once(
        script,
        'EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "916f3b7e192a28f0d7f397087cdfacc858b26423"',
        f'EXPECTED_EVIDENCE_GIT_BLOB_SHA1 = "{evidence_blob}"',
        'evidence binding',
    )

    script = replace_once(
        script,
        '_INSTALLED = False\n_PRIOR_PRINT_SUCCESS: Any = None\n',
        '_INSTALLED = False\n_PRIOR_PRINT_SUCCESS: Any = None\n_LOCAL_REMOTE_CLIENT: Any = None\n',
        'scoped client global',
    )

    old_shared = '''def _shared_trusted_client(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> object:\n    clients = [view.client for view in (candidate, policy_base) if isinstance(view, base.RemoteRepositoryView)]\n    if not clients:\n        base.fail("v9 repaired-source admission requires one trusted remote view")\n    first = clients[0]\n    if any(client is not first for client in clients[1:]):\n        base.fail("v9 repaired-source admission remote views do not share trusted client")\n    return first\n'''
    new_shared = '''def _shared_trusted_client(candidate: base.RepositoryView, policy_base: base.RepositoryView) -> object:\n    clients = [view.client for view in (candidate, policy_base) if isinstance(view, base.RemoteRepositoryView)]\n    if clients:\n        first = clients[0]\n        if any(client is not first for client in clients[1:]):\n            base.fail("v9 repaired-source admission remote views do not share trusted client")\n        return first\n    if _LOCAL_REMOTE_CLIENT is None:\n        base.fail("v9 repaired-source admission requires trusted remote-baseline client scope")\n    return _LOCAL_REMOTE_CLIENT\n'''
    script = replace_once(script, old_shared, new_shared, 'shared trusted client bridge')

    selftest_anchor = 'def _selftest_authority() -> None:\n'
    bridge_test = '''def _selftest_local_remote_client_bridge() -> None:\n    global _LOCAL_REMOTE_CLIENT\n    if _LOCAL_REMOTE_CLIENT is not None:\n        base.fail("v9 scoped remote-baseline client leaked into selftest")\n    local = base.LocalRepositoryView(Path(__file__).resolve().parents[2])\n    sentinel = object()\n    _LOCAL_REMOTE_CLIENT = sentinel\n    try:\n        if _shared_trusted_client(local, local) is not sentinel:\n            base.fail("v9 scoped remote-baseline client bridge returned wrong identity")\n    finally:\n        _LOCAL_REMOTE_CLIENT = None\n    base.expect_failure_matching(\n        "v9 local/local outside remote-baseline scope rejection",\n        "requires trusted remote-baseline client scope",\n        _shared_trusted_client,\n        local,\n        local,\n    )\n\n\n'''
    if selftest_anchor not in script:
        raise SystemExit('selftest anchor missing')
    script = script.replace(selftest_anchor, bridge_test + selftest_anchor, 1)

    script = replace_once(
        script,
        '    _selftest_review_repairs()\n    _selftest_authority()\n',
        '    _selftest_review_repairs()\n    _selftest_local_remote_client_bridge()\n    _selftest_authority()\n',
        'bridge selftest invocation',
    )

    old_main = '''        if argv and argv[0] == "verify-local":\n            args = base.parse_args(argv)\n            if args.remote_baseline:\n                return prior._call_trusted_local_runner(args, shell, impl)\n'''
    new_main = '''        if argv and argv[0] == "verify-local":\n            args = base.parse_args(argv)\n            if args.remote_baseline:\n                global _LOCAL_REMOTE_CLIENT\n                if _LOCAL_REMOTE_CLIENT is not None:\n                    base.fail("v9 remote-baseline client scope is already active")\n                token = os.environ.get(args.github_token_env) or None\n                _LOCAL_REMOTE_CLIENT = base.GitHubClient(token)\n                try:\n                    return prior._call_trusted_local_runner(args, shell, impl)\n                finally:\n                    _LOCAL_REMOTE_CLIENT = None\n'''
    script = replace_once(script, old_main, new_main, 'verify-local scoped bridge')

    SCRIPT.write_text(script, encoding='utf-8')
    EVIDENCE.write_text(evidence, encoding='utf-8')

    Path('/tmp/pr164-v9-f2-repair.manifest').write_text(
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
