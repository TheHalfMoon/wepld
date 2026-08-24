#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
import subprocess
import sys
import traceback
from urllib.parse import urlparse

REPOSITORY = 'TheHalfMoon/wepld'
POLICY_HEAD = 'f91d765d21f497502e21414f49d42869218066b5'
CONVERGENCE = 'e8a70633fc7f60b1e8dd3e607e334e11d878bb0c'
POSTMERGE = 'c67eb570e9601f1dd21e1edd03a21926d29dc870'


def git(root: Path, *args: str, text: bool = False) -> bytes | str:
    return subprocess.check_output(
        ['git', '-C', str(root), *args],
        stderr=subprocess.STDOUT,
        text=text,
    )


class GitBackedClient:
    def __init__(self, root: Path):
        self.root = root

    def _commit(self, sha: str) -> dict:
        raw = git(self.root, 'cat-file', '-p', sha, text=True)
        assert isinstance(raw, str)
        tree = None
        parents: list[dict[str, str]] = []
        message_lines: list[str] = []
        in_message = False
        for line in raw.splitlines():
            if in_message:
                message_lines.append(line)
                continue
            if line == '':
                in_message = True
                continue
            if line.startswith('tree '):
                tree = line.split(' ', 1)[1]
            elif line.startswith('parent '):
                parents.append({'sha': line.split(' ', 1)[1]})
        if tree is None:
            raise RuntimeError(f'missing tree for commit {sha}')
        return {'sha': sha, 'tree': {'sha': tree}, 'parents': parents, 'message': '\n'.join(message_lines)}

    def _tree(self, sha: str) -> dict:
        raw = git(self.root, 'ls-tree', '-r', '-t', '-l', '-z', sha)
        assert isinstance(raw, bytes)
        rows: list[dict] = []
        for record in raw.split(b'\0'):
            if not record:
                continue
            meta, path_b = record.split(b'\t', 1)
            fields = meta.decode('ascii').split()
            mode, kind, object_sha = fields[:3]
            path = path_b.decode('utf-8')
            item: dict[str, object] = {'path': path, 'mode': mode, 'type': kind, 'sha': object_sha}
            if kind == 'blob':
                item['size'] = int(git(self.root, 'cat-file', '-s', object_sha, text=True).strip())
            rows.append(item)
        return {'sha': sha, 'truncated': False, 'tree': rows}

    def _blob(self, sha: str) -> dict:
        data = git(self.root, 'cat-file', 'blob', sha)
        assert isinstance(data, bytes)
        return {'sha': sha, 'encoding': 'base64', 'content': base64.b64encode(data).decode('ascii')}

    def _compare(self, spec: str) -> dict:
        base_sha, head_sha = spec.split('...', 1)
        if base_sha == head_sha:
            return {'status': 'identical'}
        result = subprocess.run(['git', '-C', str(self.root), 'merge-base', '--is-ancestor', base_sha, head_sha], check=False)
        if result.returncode == 0:
            return {'status': 'ahead'}
        reverse = subprocess.run(['git', '-C', str(self.root), 'merge-base', '--is-ancestor', head_sha, base_sha], check=False)
        if reverse.returncode == 0:
            return {'status': 'behind'}
        return {'status': 'diverged'}

    def json(self, url: str):
        parsed = urlparse(url)
        prefix = f'/repos/{REPOSITORY}'
        if not parsed.path.startswith(prefix):
            raise RuntimeError(f'unsupported repository URL: {url}')
        suffix = parsed.path[len(prefix):]
        if suffix.startswith('/git/commits/'):
            return self._commit(suffix.rsplit('/', 1)[1])
        if suffix.startswith('/git/trees/'):
            return self._tree(suffix.rsplit('/', 1)[1])
        if suffix.startswith('/git/blobs/'):
            return self._blob(suffix.rsplit('/', 1)[1])
        if suffix.startswith('/compare/'):
            return self._compare(suffix[len('/compare/'):])
        raise RuntimeError(f'unsupported GitHub API URL in deterministic E2E: {url}')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()

    for sha in (POLICY_HEAD, CONVERGENCE, POSTMERGE):
        git(root, 'cat-file', '-e', f'{sha}^{{commit}}')

    scripts = root / '.github' / 'scripts'
    sys.path.insert(0, str(scripts))
    import wepld_integrity as base

    fake = GitBackedClient(root)
    base.GitHubClient = lambda _token: fake  # type: ignore[assignment]

    import wepld_pictorial_agile_source_admission_v9_integrity as v9

    v8 = v9.prior
    v7 = v8.prior
    original_snapshot = v7._verify_snapshot

    def traced_snapshot(view, *, transition):
        print('TRACE_V7_VERIFY_SNAPSHOT_CALL', file=sys.stderr)
        print(f'transition={transition}', file=sys.stderr)
        print(f'view_type={type(view).__name__}', file=sys.stderr)
        print(f'vendor_tree={view.tree_identity("vendor")}', file=sys.stderr)
        traceback.print_stack(file=sys.stderr)
        return original_snapshot(view, transition=transition)

    # Patch every captured alias that may route to the frozen v7 verifier.
    v7._verify_snapshot = traced_snapshot
    if v8.PRIOR_VERIFY_SNAPSHOT is original_snapshot:
        v8.PRIOR_VERIFY_SNAPSHOT = traced_snapshot
    if v9.PRIOR_VERIFY_SNAPSHOT is original_snapshot:
        v9.PRIOR_VERIFY_SNAPSHOT = traced_snapshot

    os.environ['GITHUB_TOKEN'] = 'deterministic-git-backed-client-no-network'
    original = git(root, 'rev-parse', 'HEAD', text=True).strip()
    if original != POSTMERGE:
        raise SystemExit(f'local checkout drifted: expected={POSTMERGE} actual={original}')

    f1 = v9.main([
        'verify-remote', '--repository', REPOSITORY, '--sha', CONVERGENCE,
        '--policy-root', str(root), '--pr-base-sha', POLICY_HEAD,
    ])
    if f1 != 0:
        raise SystemExit(f'F1 deterministic Git-backed API E2E failed: status={f1}')
    print('f1_git_backed_api_e2e=PASS')

    os.environ['WEPLD_POLICY_BASE_SHA'] = POLICY_HEAD
    f2 = v9.main([
        'verify-local', '--root', str(root), '--remote-baseline', '--pr-base-sha', POSTMERGE,
    ])
    if f2 != 0:
        raise SystemExit(f'F2 deterministic Git-backed API E2E failed: status={f2}')
    print('f2_git_backed_api_e2e=PASS')
    print('network_api_calls=NONE')
    print('donor_code_execution=NONE')
    print('dependency_installation=NONE')
    print('model_provider_execution=NONE')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
