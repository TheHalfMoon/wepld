# Clarify — Spec 004

## Resolved questions

### Q1 — Is this permission to canonicalize V2.3 directly?
No. Current trusted policy classifies `docs/canonical/MASTER_PLAN_INDEX.md` as base-controlled. Spec 004 therefore uses a separate bootstrap-policy PR before the canonicalization PR.

### Q2 — Does standing founder authorization remove the bootstrap requirement?
No. Standing authorization permits governed execution but does not bypass trusted-base qualification. The repository explicitly requires a separately governed bootstrap/override event.

### Q3 — Must V2.3 renumber the roadmap?
No. Canonicalization preserves `P0 + S1..S10`; V2.3 enriches existing slices with bounded named gates.

### Q4 — Should the canonical plan reuse the candidate path as-is?
No. The current document explicitly declares `STATUS = CANDIDATE / NON-CANONICAL`. The canonicalization event should create a distinct canonical document derived deterministically from the exact merged candidate bytes and update the lightweight canonical index to point to it.

### Q5 — Should Spec 004 update `CURRENT_STATE.md`?
Not inside either acceptance-critical transition. Keep the bootstrap delta and canonicalization delta minimal. Durable continuation-memory refresh can be separately governed after canonical activation if needed.

### Q6 — Does this authorize future source-acquisition gates such as S4-G or S6-AH?
No. Canonicalizing roadmap intent does not execute future gates. Each owning slice still requires its own Spec Kit, Ponytail FULL, path-level Source Acquisition Check, deterministic gates, independent review, and applicable security review.

### Q7 — Can the bootstrap policy embed broad plan-mutation authority?
No. It must bind one predecessor and one exact semantic transition, fail closed for any other base-controlled mutation, and report that source/dependency/runtime/model authority remains `NONE`.
