#!/usr/bin/env python3
"""Authorize one exact S1-013 evidence/ledger closeout; keep S1-014 closed."""

from __future__ import annotations
import argparse, hashlib, sys
from pathlib import Path
from typing import Any
import wepld_integrity as base

P=".github/scripts/wepld_s1_admission_steady_state_routing_v10_integrity.py"
V9=".github/scripts/wepld_s1_admission_steady_state_routing_v9_integrity.py"
V9_BLOB="69d187415b68bc4d4ab1a64244370749bc71113f"
FW=".github/workflows/foundation-integrity.yml"
AW=".github/workflows/s1-admission-integrity.yml"
CW=".github/workflows/s1-contracts.yml"
PW=".github/workflows/s1-performance.yml"
PP=".github/scripts/wepld_s1_performance_probe.py"
TASKS="specs/001-desktop-rust-trusted-core-handshake/tasks.md"
EVID="specs/001-desktop-rust-trusted-core-handshake/s1-013-performance-evidence.md"
OLD_WF={FW:"c49e76220a3d514ae8abca79034f65c444a8363c072c9d76e032f7483cd6c2d9",AW:"3e4453bb8f53f1baeefb5953bf62501a8311627fc3cffc4fe6ce6f219ce7af7d"}
WF={FW:"97d6f3bc5c6f668ebaa795f144e979c25b443fa3cc4d06d894e6d4a3a2f52f94",AW:"faa5c2c528378397117b6acaa5a8ed3ec23a51005b7d442e86d4cd9aa02e0273",CW:"008441e0e17542679c7bdc23e64ad6e2ce57664ed5c65e4842b7d8fbd77500d7"}
PW_SHA="7dd7f670740b651e30700a0fe10b4f1dcd8d51a46b257789e54a02c74df98784"
PW_BLOB="b16d57b42e617808d4b5d2547c1677e9ef7c3535"
PP_SHA="e3eb6572b7cd4e35f07abaadb460907919acc091e27db94e4ebbd8ee0b83d6af"
PP_BLOB="1b33c84c266ecab89af1b6e63f9677875fd5ecf5"
PRE_TASKS="d331b7f167fe67ae9061ed553cf0949fab12aae0"
CLOSE_TASKS="f8d9d09dc2e02861246614f374173a0a2bfff9c2"
EVID_SHA="cbbf6361a8e4bbc10a7d7426e361dd5b48ef6ee34d159763d1ce8aa23e62da46"
EVID_BLOB="bd79c1e64b397fda3677fb549e9a7feb0c5a8c3d"
BOOT=frozenset({P,FW,AW}); CLOSE=frozenset({TASKS,EVID})
AUTH="S1_013_EVIDENCE_LEDGER_CLOSEOUT_ONLY"; S1_014="NOT_AUTHORIZED"
MERGE="96fa229610f31598326493b75b40a3353b46bbbf"
RUNS=("32955349075","32955348827","32955348872")
_INST=False; _PRINT=None

def blob(data): return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()  # noqa: S324
def sha(data): return hashlib.sha256(data).hexdigest()
def ps(v): return {e.path for e in v.entries()}
def mode(v,p):
    for e in v.entries():
        if e.path==p:return e.mode
    base.fail(f"missing path: {p}")
def exact_art(v,p,s,b,label):
    d=v.read_bytes(p,base.MAX_POLICY_FILE_BYTES)
    if sha(d)!=s or blob(d)!=b: base.fail(f"{label} identity drifted")
def req_v9(v):
    if V9 not in ps(v):base.fail("v9 predecessor missing")
    if blob(v.read_bytes(V9,base.MAX_POLICY_FILE_BYTES))!=V9_BLOB:base.fail("v9 predecessor drifted")

root=base.LocalRepositoryView(Path(__file__).resolve().parents[2])
if blob(root.read_bytes(V9,base.MAX_POLICY_FILE_BYTES))!=V9_BLOB:base.fail("local v9 predecessor drifted")
import wepld_s1_admission_steady_state_routing_v9_integrity as v9  # noqa:E402

V9_DELTA=v9._require_exact_delta_v9; V9_BASE=v9._compare_base_controlled_v9
V9_ALLOWED=v9._validate_allowed_paths_v9; V9_FILES=v9._verify_policy_files_v9
V9_EXT=v9._verify_extension_paths_v9; V9_D=v9._verify_desktop_extension_paths_v9
V9_E=v9._verify_execution_extension_paths_v9; V9_PRINT=v9._print_success
CAND=v9._EXPECTED_CANDIDATE_LOCAL; RUNTIME=v9._EXPECTED_RUNTIME_MAIN

def topo():
    x=v9._topology()
    if not isinstance(x,tuple) or len(x)!=5:base.fail("v10 topology drifted")
    return x
def extset(c):
    x=getattr(c,"EXTENSION_CONTROLLED_PATHS",None)
    if not isinstance(x,(set,frozenset)):base.fail("v10 extension topology drifted")
    return frozenset(x)
def changed(c,b):
    x=v9._changed_paths(c,b)
    if not isinstance(x,(set,frozenset)):base.fail("v10 changed-path topology drifted")
    return frozenset(x)
def bootbase(v):return P not in ps(v)

def closeout(c,b,pre=PRE_TASKS,tasks=CLOSE_TASKS,es=EVID_SHA,eb=EVID_BLOB):
    if blob(b.read_bytes(TASKS,base.MAX_POLICY_FILE_BYTES))!=pre:base.fail("S1-013 closeout trusted ledger drifted")
    if EVID in ps(b) or EVID not in ps(c):base.fail("S1-013 closeout evidence state invalid")
    if mode(c,TASKS)!="100644" or mode(c,EVID)!="100644":base.fail("S1-013 closeout Markdown mode invalid")
    for v in (b,c):
        exact_art(v,PW,PW_SHA,PW_BLOB,"performance workflow")
        exact_art(v,PP,PP_SHA,PP_BLOB,"performance probe")
    if blob(c.read_bytes(TASKS,base.MAX_POLICY_FILE_BYTES))!=tasks:base.fail("S1-013 reconciled ledger identity drifted")
    exact_art(c,EVID,es,eb,"S1-013 performance evidence")

def delta(c,b):
    x=changed(c,b)
    if bootbase(b):
        if x==BOOT:req_v9(c);req_v9(b);return
        if x&BOOT:base.fail("v10 bootstrap delta must be exactly policy plus two workflows")
    if x==CLOSE:closeout(c,b);return
    if x&CLOSE:base.fail("S1-013 closeout delta must be exactly tasks plus evidence")
    V9_DELTA(c,b)

def basectrl(c,b):
    if not bootbase(b):V9_BASE(c,b);return
    for p in sorted(base.BASE_CONTROLLED_PATHS):
        cb=c.read_bytes(p,base.MAX_POLICY_FILE_BYTES);bb=b.read_bytes(p,base.MAX_POLICY_FILE_BYTES)
        if p in (FW,AW):
            if sha(cb)!=WF[p] or sha(bb)!=OLD_WF[p]:base.fail(f"v10 bootstrap workflow drifted: {p}")
        elif cb!=bb:base.fail(f"base-controlled path changed: {p}")

def ext(c,b,safe):
    safe=frozenset(safe)
    if P in safe:
        if P not in ps(c):base.fail("v10 wrapper missing")
        if bootbase(b):
            if P in ps(b):base.fail("v10 wrapper unexpectedly in bootstrap base")
        elif P not in ps(b) or c.read_bytes(P,base.MAX_POLICY_FILE_BYTES)!=b.read_bytes(P,base.MAX_POLICY_FILE_BYTES):base.fail("v10 steady-state wrapper drifted")
    rest=frozenset(safe-{P})
    if rest:V9_EXT(c,b,rest)
def dext(c,b):ext(c,b,extset(topo()[3]))
def eext(c,b):ext(c,b,extset(topo()[4]))
def allowed(paths,stage):V9_ALLOWED(set(paths)-{P},stage)

def files(v):
    req_v9(v);V9_FILES(v)
    if P not in ps(v):base.fail("v10 wrapper missing")
    if EVID in ps(v):
        if mode(v,TASKS)!="100644" or mode(v,EVID)!="100644":base.fail("S1-013 canonical closeout Markdown mode invalid")
        if blob(v.read_bytes(TASKS,base.MAX_POLICY_FILE_BYTES))!=CLOSE_TASKS:base.fail("S1-013 canonical ledger drifted")
        exact_art(v,EVID,EVID_SHA,EVID_BLOB,"S1-013 canonical evidence")
    elif blob(v.read_bytes(TASKS,base.MAX_POLICY_FILE_BYTES))!=PRE_TASKS:base.fail("S1-013 ledger changed before closeout")

def printer(stage,mode_):
    if _PRINT is not V9_PRINT:base.fail("v10 predecessor printer drifted")
    _PRINT(stage,mode_)
    print(f"s1_admission_steady_state_route_v10=V9_PRESERVED_PLUS_S1_013_CLOSEOUT")
    print(f"s1_admission_authority_expansion_v10={AUTH}")
    print(f"s1_013_measurement_merge_v10={MERGE}")
    print(f"s1_013_foundation_run_v10={RUNS[0]}")
    print(f"s1_013_contracts_run_v10={RUNS[1]}")
    print(f"s1_013_performance_run_v10={RUNS[2]}")
    print("effective_source_admission_v10=NONE")
    print("effective_dependency_admission_v10=NONE")
    print("effective_donor_execution_v10=NONE")
    print("new_product_runtime_authority_v10=NONE")
    print("network_listener_authority_v10=NONE")
    print("effective_model_provider_execution_v10=NONE")
    print("effective_model_weight_access_v10=NONE")
    print("effective_model_inference_v10=NONE")
    print("s1_013_evidence_closeout_v10=EXACT_CONTENT_ADDRESSED_TRANSITION_AFTER_V10_CANONICAL_ACTIVATION")
    print(f"s1_014_plus_v10={S1_014}")

def overlay():
    sh,r,_,d,e=topo()
    pairs=((r.IMPL_REQUIRE_EXACT_DELTA,delta),(base.compare_base_controlled,basectrl),(d.verify_extension_controlled_paths,dext),(e.verify_extension_controlled_paths,eext),(sh.validate_allowed_paths,allowed),(sh.verify_policy_files,files),(sh.print_success,printer))
    if any(a is not b for a,b in pairs):base.fail("v10 overlay hook drifted")
    if P not in extset(d) or P not in extset(e):base.fail("v10 extension registration drifted")

def patch():v9.EXPECTED_WORKFLOW_SHA256=dict(WF)
def install():
    global _INST,_PRINT
    if _INST:overlay();return
    patch();v9._install_policy()
    sh,r,_,d,e=topo()
    pairs=((r.IMPL_REQUIRE_EXACT_DELTA,V9_DELTA),(base.compare_base_controlled,V9_BASE),(d.verify_extension_controlled_paths,V9_D),(e.verify_extension_controlled_paths,V9_E),(sh.validate_allowed_paths,V9_ALLOWED),(sh.verify_policy_files,V9_FILES),(sh.print_success,V9_PRINT))
    if any(a is not b for a,b in pairs):base.fail("v10 predecessor hook drifted")
    _PRINT=V9_PRINT
    d.EXTENSION_CONTROLLED_PATHS=frozenset(set(extset(d))|{P});e.EXTENSION_CONTROLLED_PATHS=frozenset(set(extset(e))|{P})
    r.IMPL_REQUIRE_EXACT_DELTA=delta;base.compare_base_controlled=basectrl
    d.verify_extension_controlled_paths=dext;e.verify_extension_controlled_paths=eext
    sh.validate_allowed_paths=allowed;sh.verify_policy_files=files;sh.print_success=printer
    _INST=True;overlay()

def mem(x):return base.MemoryView(x,trees={p:blob(d) for p,d in x.items()})
def selftest():
    patch();v9.selftest();install()
    for p in (FW,AW):
        if sha(root.read_bytes(p,base.MAX_POLICY_FILE_BYTES))!=WF[p]:base.fail(f"v10 workflow drifted: {p}")
    if AUTH!="S1_013_EVIDENCE_LEDGER_CLOSEOUT_ONLY" or S1_014!="NOT_AUTHORIZED":base.fail("v10 authority drifted")
    # Bootstrap is exact and mixed bootstrap fails.
    vb=root.read_bytes(V9,base.MAX_POLICY_FILE_BYTES);b={V9:vb,FW:b"o",AW:b"o"};c=dict(b);c.update({P:b"v10",FW:b"n",AW:b"n"})
    delta(mem(c),mem(b));m=dict(c);m["README.md"]=b"x"
    base.expect_failure_matching("v10 mixed bootstrap","bootstrap delta must be exactly",delta,mem(m),mem(b))
    # Exercise the future closeout with fixture identities.
    pt=b"prior";ct=b"close";ev=b"evidence";pw=b"pw";pp=b"pp";b={P:b"v10",TASKS:pt,PW:pw,PP:pp};c=dict(b);c[TASKS]=ct;c[EVID]=ev
    global PW_SHA,PW_BLOB,PP_SHA,PP_BLOB
    old=(PW_SHA,PW_BLOB,PP_SHA,PP_BLOB);PW_SHA,PW_BLOB,PP_SHA,PP_BLOB=sha(pw),blob(pw),sha(pp),blob(pp)
    try:
        closeout(mem(c),mem(b),blob(pt),blob(ct),sha(ev),blob(ev))
        w=dict(c);w[EVID]=b"wrong"
        base.expect_failure_matching("v10 wrong evidence","performance evidence identity drifted",closeout,mem(w),mem(b),pre=blob(pt),tasks=blob(ct),es=sha(ev),eb=blob(ev))
    finally:PW_SHA,PW_BLOB,PP_SHA,PP_BLOB=old
    print("wepld S1 steady-state routing v10 policy self-tests: PASS")

def main(argv):
    try:
        if argv and argv[0]=="selftest":selftest();return 0
        install()
        if argv and argv[0]=="verify-candidate-local":
            p=argparse.ArgumentParser(add_help=False);p.add_argument("--root",required=True);p.add_argument("--policy-base-root",required=True);p.add_argument("--policy-base-sha",required=True);a=p.parse_args(argv[1:])
            return CAND(a.root,a.policy_base_root,a.policy_base_sha)
        return RUNTIME(argv)
    except base.PolicyError as e:
        print(f"wepld integrity verification: FAIL: {e}",file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main(sys.argv[1:]))
