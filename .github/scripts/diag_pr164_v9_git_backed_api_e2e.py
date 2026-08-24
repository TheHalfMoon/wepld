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
            if len(fields) < 3:
                raise RuntimeError(f'malformed ls-tree record: {meta!r}')
            mode, kind, object_sha = fields[:3]
            path = path_b.decode('utf-8')
            item: dict[str, object] = {'path': path, 'mode': mode, 'type': kind, 'sha': object_sha}
            if kind == 'blob':
                if len(fields) < 4 or not fields[3].isdigit():
                    raise RuntimeError(f'malformed blob size in ls-tree record: {meta!r}')
                item['size'] = int(fields[3])
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
        result = subprocess.run(
            ['git', '-C', str(self.root), 'merge-base', '--is-ancestor', base_sha, head_sha],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return {'status': 'ahead'}
        reverse = subprocess.run(
            ['git', '-C', str(self.root), 'merge-base', '--is-ancestor', head_sha, base_sha],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
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


def _trace_s1_011_delta(base) -> None:
    import wepld_s1_shell_integrity_v19 as v19

    original = v19._require_exact_delta

    def traced(candidate, policy_base):
        try:
            return original(candidate, policy_base)
        except base.PolicyError:
            candidate_entries = {entry.path: entry.mode for entry in candidate.entries()}
            base_entries = {entry.path: entry.mode for entry in policy_base.entries()}
            changed = set(candidate_entries) ^ set(base_entries)
            for relative in set(candidate_entries) & set(base_entries):
                if candidate_entries[relative] != base_entries[relative]:
                    changed.add(relative)
                    continue
                if candidate.tree_identity(relative) != policy_base.tree_identity(relative):
                    changed.add(relative)
            print('TRACE_S1_011_DELTA_FAILURE', file=sys.stderr)
            print(f'candidate_type={type(candidate).__name__}', file=sys.stderr)
            print(f'policy_base_type={type(policy_base).__name__}', file=sys.stderr)
            print(f'changed_count={len(changed)}', file=sys.stderr)
            print('changed_preview=' + ','.join(sorted(changed)[:20]), file=sys.stderr)
            print(
                'candidate_markers=' + str(v19._has_s1_011_markers(candidate, set(candidate_entries))),
                file=sys.stderr,
            )
            print(
                'policy_base_markers=' + str(v19._has_s1_011_markers(policy_base, set(base_entries))),
                file=sys.stderr,
            )
            traceback.print_stack(file=sys.stderr)
            raise

    v19._require_exact_delta = traced


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--policy-head', required=True)
    parser.add_argument('--convergence', required=True)
    parser.add_argument('--postmerge', required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()

    for sha in (args.policy_head, args.convergence, args.postmerge):
        git(root, 'cat-file', '-e', f'{sha}^{{commit}}')

    current = git(root, 'rev-parse', 'HEAD', text=True).strip()
    if current != args.postmerge:
        git(root, 'checkout', '--detach', args.postmerge)
        current = git(root, 'rev-parse', 'HEAD', text=True).strip()
    if current != args.postmerge:
        raise SystemExit(f'local checkout drifted: expected={args.postmerge} actual={current}')

    scripts = root / '.github' / 'scripts'
    sys.path.insert(0, str(scripts))
    import wepld_integrity as base

    fake = GitBackedClient(root)
    base.GitHubClient = lambda _token: fake  # type: ignore[assignment]
    import wepld_pictorial_agile_source_admission_v9_integrity as v9
    _trace_s1_011_delta(base)

    os.environ['GITHUB_TOKEN'] = 'deterministic-git-backed-client-no-network'

    f1 = v9.main([
        'verify-remote', '--repository', REPOSITORY, '--sha', args.convergence,
        '--policy-root', str(root), '--pr-base-sha', args.policy_head,
    ])
    if f1 != 0:
        raise SystemExit(f'F1 deterministic Git-backed API E2E failed: status={f1}')
    print('f1_git_backed_api_e2e=PASS')

    os.environ['WEPLD_POLICY_BASE_SHA'] = args.policy_head
    f2 = v9.main([
        'verify-local', '--root', str(root), '--remote-baseline', '--pr-base-sha', args.postmerge,
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
