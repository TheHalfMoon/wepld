# Provisional Tasks — S1 Desktop ↔ Rust Trusted Core Handshake

This file exists only to reconcile the current Spec Kit upstream ordering (`tasks` before `analyze`) with WePLD's canonical order (`analyze` before final `tasks`). It is NOT execution authority.

```text
STATUS = PROVISIONAL / NON-AUTHORITATIVE
BASE = 6eff72319cad99c878a80f0d5bce9f107d213679
IMPLEMENTATION = NOT_STARTED
```

## Candidate decomposition before analysis

- PT-001 — Complete S1 constitution/spec/clarifications/plan/checklist.
- PT-002 — Execute Ponytail FULL and record rejected unnecessary machinery.
- PT-003 — Re-pin Rust/Tauri/Serde/component candidates and establish Source Acquisition Check.
- PT-004 — Design a stage-aware successor to the P0-only `foundation-integrity` boundary.
- PT-005 — Resolve candidate dependency graph and produce lock/tree/SBOM/advisory evidence without adding product behavior.
- PT-006 — Finalize exact S1 component admission and dependency register.
- PT-007 — Implement WePLD protocol v1 contracts and bounded frame codec.
- PT-008 — Implement pure Core handshake/replay/cancellation state.
- PT-009 — Implement separate Core process over inherited stdin/stdout.
- PT-010 — Implement minimal Tauri Desktop host and static UI.
- PT-011 — Add cross-process negative/adversarial/recovery tests.
- PT-012 — Add Windows-first runtime qualification and secondary platform gates.
- PT-013 — Add performance/evidence capture.
- PT-014 — Run applicable security review and independent engineering review.
- PT-015 — Reconcile findings, rerun exact-head gates, and accept S1 under standing founder authority only when complete.
- PT-016 — Capture Build Learning evidence.

## Questions intentionally deferred to analysis

1. Should framing/state live in a separate `crates/ipc` crate or remain with contracts/core to avoid an abstraction-only crate?
2. Should dependency resolution and stage-aware CI migration be one change or two separately reviewed changes?
3. Which acceptance evidence must run on every PR versus only the final S1 acceptance head?
4. How can Windows sidecar lifecycle/orphan behavior be proven without prematurely importing S3 process-ownership scope?
5. Is any Tauri frontend command required beyond a narrow status/control projection, or can the desktop host drive the static UI with even less surface?
6. Which task boundaries are security-sensitive enough to require mandatory Codex Security diff scans before proceeding?

Final execution tasks are defined only after `analyze.md` resolves these questions.
