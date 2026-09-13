# Quick Start Guide

This guide will help you get started with Spec-Driven Development using Agile. Throughout, we illustrate each step with a running example: **Taskify**, a small team productivity platform.

> [!NOTE]
> Automation scripts are provided as Bash (`.sh`), PowerShell (`.ps1`), and Python (`.py`) variants. Interactive `agile init` prompts you to choose one; non-interactive runs (no TTY, or `--non-interactive`) default to a shell variant for your OS. Pass `--script sh|ps|py` to select explicitly.

Commands are shown here in `/agile.*` form, but the exact invocation depends on your agent. Some skills-based agents use `$agile-*` (e.g. Codex, ZCode) or `/skill:agile-*` (e.g. Kimi). Use whichever form your agent exposes — the steps are otherwise identical.

## Recommended Process

> [!TIP]
> **Context Awareness**: Agile tracks the active feature by the feature directory recorded in `.agile/feature.json` (overridable with the `AGILE_FEATURE_DIRECTORY` environment variable). Commands resolve the feature from that state, **not** from the checked-out Git branch — no Git required. The opt-in **git** extension adds numbered feature branches (e.g. `001-feature-name`) for organizing work in version control, but the active feature is still whichever directory that state points to; `git checkout` alone does not change it. To point commands at a different feature, update `.agile/feature.json` (or set `AGILE_FEATURE_DIRECTORY`).

After installing Agile, each command below is a step in the process. Two paths are common:

**Shorter path** — for smaller features:

1. `/agile.specify`
2. `/agile.plan`
3. `/agile.tasks`
4. `/agile.implement`
5. `/agile.converge`

**Full path** — for production features, adding `/agile.clarify`, `/agile.checklist`, and `/agile.analyze` as quality gates:

1. `/agile.constitution`
2. `/agile.specify`
3. `/agile.clarify`
4. `/agile.plan`
5. `/agile.checklist`
6. `/agile.tasks`
7. `/agile.analyze`
8. `/agile.implement`
9. `/agile.converge`

### Install Specify

**In your terminal**, install the CLI from PyPI (requires [uv](install/uv.md)), then initialize your project:

```bash
uv tool install wepld-agile
agile init taskify   # or: agile init .   to use the current directory
```

`init` lets you pick your coding agent interactively, or pass it explicitly with `--integration` (e.g. `--integration copilot`). For CI and AI agent harnesses, add `--non-interactive` so unspecified choices use documented defaults instead of hanging on an arrow-key picker.

> [!NOTE]
> Prefer `pipx`, one-time `uvx` runs, a pinned release, or an offline/air-gapped setup? See the [Installation Guide](installation.md) for all supported methods.
> Adding Agile to a repository that already contains code? Follow
> [Adopting Agile in an Existing Project](guides/existing-projects.md) before
> starting the workflow below.

### Step 1: `/agile.constitution` — set the ground rules

Establishes the project's guiding principles, which every later step is evaluated against. Run it once up front, passing your principles as arguments.

```text
/agile.constitution Taskify is a "Security-First" application. All user inputs must be validated. We use a microservices architecture. Code must be fully documented.
```

### Step 2: `/agile.specify` — describe what to build

Creates the feature specification from a natural-language description. Focus on the **what** and **why**, not the tech stack.

```text
/agile.specify Develop Taskify, a team productivity platform where predefined users create projects, assign tasks, comment, and move tasks across Kanban columns (To Do, In Progress, In Review, Done). Five users (one product manager, four engineers), three sample projects, no login for this first phase.
```

### Step 3: `/agile.clarify` — resolve ambiguities

Asks targeted questions about anything underspecified and folds your answers back into the spec, so you're not planning on top of ambiguity. Run it before planning, optionally with a focus area.

```text
/agile.clarify Focus on task card behavior — status changes, comment permissions, and user assignment.
```

### Step 4: `/agile.plan` — choose the tech stack

Generates the design artifacts from the spec. This is where implementation detail belongs — provide your tech stack and architecture.

```text
/agile.plan Use .NET Aspire with Postgres. The frontend is Blazor Server with drag-and-drop boards and real-time updates. Expose REST APIs for projects, tasks, and notifications.
```

### Step 5: `/agile.checklist` — validate the spec

Generates a custom quality checklist — "unit tests for your requirements" — to confirm the spec is complete, clear, and consistent before you break the work down. These custom checklists are reviewer-owned requirements-quality review artifacts: mark an item `[x]` only when the reviewer determines that requirement-quality criterion is satisfied. Checked custom items do not mean implementation work is complete.

```text
/agile.checklist
```

### Step 6: `/agile.tasks` — break the work down

Generates an actionable, dependency-ordered `tasks.md` from the design artifacts.

```text
/agile.tasks
```

### Step 7: `/agile.analyze` — check consistency

Reports conflicts, gaps, and ambiguities across `spec.md`, `plan.md`, and `tasks.md`. It's read-only — if it flags issues, fix them at the source and re-run before implementing.

```text
/agile.analyze
```

### Step 8: `/agile.implement` — build it

Executes the tasks in `tasks.md` in dependency order. Before implementation, it reads checklist checkbox state as a gate and asks before proceeding if any checklist items are unchecked; it does not change any checklist files or markers. The built-in `checklists/requirements.md` checklist is maintained by `/agile.specify` and `/agile.clarify`, while custom checklists remain reviewer-owned. Run it once to build everything, or scope it to one phase at a time for large features.

```text
/agile.implement
```

### Step 9: `/agile.converge` — verify completeness

Checks the codebase against the spec, plan, and tasks. If it finds gaps, it appends new tasks to `tasks.md`; run `/agile.implement` and converge again until it reports converged. Otherwise you're done — proceed to review or open a PR.

```text
/agile.converge
```

> [!TIP]
> For a full reference on each command — arguments, output, phased implementation, and how they interact — see [Agentic SDD](reference/agentic-sdd.md).

## Key Principles

- **Be explicit** about what you're building and why
- **Don't focus on tech stack** during specification phase
- **Iterate and refine** your specifications before implementation
- **Validate** requirements and plans before coding begins
- **Let the coding agent handle** the implementation details

## Next Steps

- See the [Agentic SDD](reference/agentic-sdd.md) reference for full detail on every command
- Read the [complete methodology](https://github.com/TheHalfMoon/wepld/blob/main/spec-driven.md) for in-depth guidance
- Compare the [core templates](https://github.com/TheHalfMoon/wepld/tree/main/templates) with
  [community walkthroughs](community/walkthroughs.md) to see how Spec-Driven Development is used in real projects
- Explore the [source code on GitHub](https://github.com/TheHalfMoon/wepld)
