#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import sys
import traceback

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / '.github' / 'scripts'))

import wepld_pictorial_agile_source_admission_v9_integrity as v9

# Bind every known alias that can reach the frozen v7 snapshot verifier so the
# diagnostic prints the call stack and then delegates unchanged.
v8 = v9.prior
v7 = v8.prior
original_v7 = v7._verify_snapshot
original_v8_alias = v8.PRIOR_VERIFY_SNAPSHOT
original_v9_alias = v9.PRIOR_VERIFY_SNAPSHOT


def traced(view, *, transition):
    print('TRACE_V7_VERIFY_SNAPSHOT_CALL', file=sys.stderr)
    print(f'transition={transition}', file=sys.stderr)
    print(f'view_type={type(view).__name__}', file=sys.stderr)
    try:
        print(f'vendor_tree={view.tree_identity("vendor")}', file=sys.stderr)
    except Exception as exc:
        print(f'vendor_tree_error={exc}', file=sys.stderr)
    traceback.print_stack(file=sys.stderr)
    return original_v7(view, transition=transition)

v7._verify_snapshot = traced
v8.PRIOR_VERIFY_SNAPSHOT = traced
v9.PRIOR_VERIFY_SNAPSHOT = traced

# Also update the alias v8 captured from v7 if a downstream path calls it.
assert original_v8_alias is original_v7
assert original_v9_alias is original_v7

raise SystemExit(v9.main([
    'verify-remote',
    '--repository', 'TheHalfMoon/wepld',
    '--sha', 'e8a70633fc7f60b1e8dd3e607e334e11d878bb0c',
    '--policy-root', str(ROOT),
    '--pr-base-sha', 'f91d765d21f497502e21414f49d42869218066b5',
]))
