# Agentic Bug Fix

The **bug** extension adds a three-step bug triage process — assess, fix, and validate — that your coding agent runs alongside the core [Agentic SDD](agentic-sdd.md) process. Each bug lives in its own directory under `.agile/bugs/<slug>/`, with one Markdown report per stage.

> [!NOTE]
> Commands are written in `/agile.bug.*` form throughout this page. The exact invocation depends on your agent — some skills-based agents use `$agile-bug-*` (e.g. Codex, ZCode) or `/skill:agile-bug-*` (e.g. Kimi). Substitute the form your agent exposes.

The bug extension is a bundled, opt-in extension. Install it before using these commands:

```bash
agile extension add bug
```

The three commands share a single handle — the **slug**, the per-bug directory name under `.agile/bugs/`. Supply it with `slug=<name>`; if omitted, `/agile.bug.assess` asks for one (or generates a unique one in automated mode). Slugs are normalized to lowercase kebab-case. If an assessment already exists for a slug, an interactive run asks before overwriting it, while an automated run refuses and picks a new unique slug instead.

```text
/agile.bug.assess -> /agile.bug.fix -> /agile.bug.test
```

## `/agile.bug.assess`

Triages a bug report — pasted text (such as a stack trace) or a URL (such as a GitHub issue) — against the codebase: it judges whether the report is a real bug, locates the suspected code paths, and proposes a remediation. This command is **read-only**: it writes only `assessment.md` and never modifies source code.

```text
/agile.bug.assess "TypeError: cannot read properties of undefined (reading 'token') at /auth/callback"
```

```text
/agile.bug.assess https://github.com/example/repo/issues/1234 slug=callback-token
```

Output: `.agile/bugs/<slug>/assessment.md`.

## `/agile.bug.fix`

Applies the remediation described in the assessment and records exactly what changed. This is the **only** bug command that edits source code, and it stays within the files listed in the assessment unless new evidence requires expanding scope (logged under **Deviations from Assessment**).

```text
/agile.bug.fix slug=callback-token
```

Output: `.agile/bugs/<slug>/fix.md`.

## `/agile.bug.test`

Validates the fix by re-running the reproduction and any added tests, then records the verification result — one of `verified`, `partial`, or `failed`. Like `assess`, it is **read-only** with respect to source code. Verdicts are never over-claimed: if the assessment listed a reproduction that wasn't actually exercised, the overall result is downgraded to `partial` rather than reported as `verified`.

```text
/agile.bug.test slug=callback-token
```

Output: `.agile/bugs/<slug>/test.md`.
