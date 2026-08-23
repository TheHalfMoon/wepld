<div align="center">
    <img src="https://raw.githubusercontent.com/github/agile/main/media/logo_large.webp" alt="Agile Logo" width="200" height="200"/>
    <h1>🌱 Agile</h1>
    <h3><em>Define what to build before building it — with any AI coding agent.</em></h3>
</div>

<p align="center">
    <strong>An open source toolkit for building high-quality software with any AI coding agent — a ready-to-use spec-driven process (or bring your own), endlessly extensible, community-driven, and built for your whole organization.</strong>
</p>

<p align="center">
    <a href="https://github.com/TheHalfMoon/wepld/releases/latest"><img src="https://img.shields.io/github/v/release/github/agile" alt="Latest Release"/></a>
    <a href="https://github.com/TheHalfMoon/wepld/stargazers"><img src="https://img.shields.io/github/stars/github/agile?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/TheHalfMoon/wepld/blob/main/LICENSE"><img src="https://img.shields.io/github/license/github/agile" alt="License"/></a>
    <a href="https://github.github.io/agile/"><img src="https://img.shields.io/badge/docs-GitHub_Pages-blue" alt="Documentation"/></a>
</p>

<p align="center">
    <strong>English</strong> ·
    <a href="./README.zh-CN.md">简体中文</a>
</p>

> [!NOTE]
> **One year of Agile — and 1.0.0**
>
> One year after the first commit, Agile has reached [1.0.0](https://github.com/TheHalfMoon/wepld/releases/tag/v1.0.0) — not because the work is finished or its shape is frozen, but because the project has grown into something coherent, useful, and shaped by far more people than those who started it.
>
> The lead maintainer's personal anniversary post, [*Agile Turns One — and Ships 1.0.0*](https://www.manorrock.com/blog/2026/08/21/agile_turns_one.html), defines what 1.0.0 actually means for the project: **it is now just a number**. As agents make adapting to change dramatically cheaper, the value moves from stability to adaptability.
>
> To everyone who has used Agile, challenged its assumptions, reported a problem, contributed code or documentation, created an extension or preset, shared an idea, or helped someone else get started: **thank you**. This milestone belongs to the community that carried the project through its first year and continues to shape where it goes next.

---

## Table of Contents

- [🤔 What is Spec-Driven Development?](#-what-is-spec-driven-development)
- [🐞 Bug Fixing with Agile](#-bug-fixing-with-agile)
- [💡 Assessing Ideas with Agile](#-assessing-ideas-with-agile)
- [⚡ Get Started](#-get-started)
- [📽️ Video Overview](#️-video-overview)
- [🌍 Community](#-community)
- [🤖 Supported AI Coding Agent Integrations](#-supported-ai-coding-agent-integrations)
- [🔧 Agile CLI Reference](#-wepld-agile-reference)
- [🧩 Making Agile Your Own: Extensions & Presets](#-making-agile-your-own-extensions--presets)
- [📦 Bundles: Role-Based Setups](#-bundles-role-based-setups)
- [📚 Core Philosophy](#-core-philosophy)
- [🌟 Development Phases](#-development-phases)
- [🎯 Experimental Goals](#-experimental-goals)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn More](#-learn-more)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

## 🤔 What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them.

### SDD Quickstart

Replace `vX.Y.Z` with the [latest release tag](https://github.com/TheHalfMoon/wepld/releases), keeping the leading `v`.

```bash
uv tool install wepld-agile --from git+https://github.com/TheHalfMoon/wepld.git@vX.Y.Z
agile init my-project --integration copilot
cd my-project
```

Launch your coding agent in the project directory, then:

0. **Establish** your project principles once (`/agile-constitution`). This is a one-time step per project.
1. **Specify** what you want to build (`/agile-specify`).
2. **Plan** how you will build it (`/agile-plan`).
3. **Break down** the plan into actionable tasks (`/agile-tasks`).
4. **Implement** the tasks (`/agile-implement`).
5. **Converge** the implementation against the spec, plan, and tasks (`/agile-converge`).

> [!NOTE]
> Repeat steps 4 and 5 until `/agile-converge` reports **Converged**.

## 🐞 Bug Fixing with Agile

Bug fixes are risky when an agent jumps straight from a report to a patch without validating the diagnosis or confirming that the fix resolves the original symptom. The bundled, opt-in bug extension provides a repeatable **assess → fix → test** workflow that keeps each fix scoped, evidence-based, and documented from root cause through verification.

### Bug Fix Quickstart

Replace `vX.Y.Z` with the [latest release tag](https://github.com/TheHalfMoon/wepld/releases), keeping the leading `v`.

```bash
uv tool install wepld-agile --from git+https://github.com/TheHalfMoon/wepld.git@vX.Y.Z
agile init my-project --integration copilot
cd my-project
agile extension add bug
```

Launch your coding agent in the project directory, then:

1. **Assess** the bug (`/agile-bug-assess "<bug report>" slug=login-crash`).
2. **Fix** the assessed cause (`/agile-bug-fix slug=login-crash`).
3. **Test** the fix (`/agile-bug-test slug=login-crash`).

## 💡 Assessing Ideas with Agile

Good ideas deserve evidence before commitment, whether or not they become software. The bundled, opt-in assess extension turns a raw idea into a documented **go / needs-clarification / kill** decision through an independent **intake → research → define → shape → decide** workflow.

### Idea Assessment Quickstart

Replace `vX.Y.Z` with the [latest release tag](https://github.com/TheHalfMoon/wepld/releases), keeping the leading `v`.

```bash
uv tool install wepld-agile --from git+https://github.com/TheHalfMoon/wepld.git@vX.Y.Z
agile init my-project --integration copilot
cd my-project
agile extension add assess
```

Launch your coding agent in the project directory, then:

1. **Intake** the idea (`/agile-assess-intake "<idea>" slug=offline-mode`).
2. **Research** supporting and opposing evidence (`/agile-assess-research slug=offline-mode`).
3. **Define** the problem, goals, and success metrics (`/agile-assess-define slug=offline-mode`).
4. **Shape** possible solutions and their trade-offs (`/agile-assess-shape slug=offline-mode`).
5. **Decide** whether to proceed, clarify, or stop (`/agile-assess-decide slug=offline-mode`).

> [!NOTE]
> Idea assessment is standalone. If you choose to build an idea with a **go** decision, you can hand it off to `/agile-specify`.

## ⚡ Get Started

### 1. Install Agile CLI

Requires **[uv](https://docs.astral.sh/uv/)** ([install uv](./docs/install/uv.md)). Replace `vX.Y.Z` with the latest release tag from [Releases](https://github.com/TheHalfMoon/wepld/releases) — keep the leading `v` (for example, `v0.12.11`, not `0.12.11`):

```bash
uv tool install wepld-agile --from git+https://github.com/TheHalfMoon/wepld.git@vX.Y.Z
```

Prefer installing from PyPI? The `wepld-agile` package is also published there:

```bash
uv tool install wepld-agile
```

See the [Installation Guide](./docs/installation.md) for alternative methods, verification, upgrade, and troubleshooting.

### 2. Initialize a project

```bash
agile init my-project --integration copilot
cd my-project
```

For CI or AI agent harnesses (no keyboard, or a PTY that cannot send arrow keys), pass `--non-interactive` so init never hangs on a picker. Combine with `--force` when initializing into a non-empty directory:

```bash
agile init my-project --non-interactive --ignore-agent-tools
agile init --here --force --non-interactive --integration claude
```

To check for updates or upgrade the installed CLI, use the self-management commands. See the [Upgrade Guide](./docs/upgrade.md) for detailed scenarios and customization options.

```bash
# Check whether a newer release is available (read-only — does not modify anything)
specify self check

# Preview what would run, without actually upgrading
specify self upgrade --dry-run

# Upgrade in place to the latest stable release (auto-detects uv tool vs pipx install)
specify self upgrade

# Or pin a specific release tag (replace vX.Y.Z[suffix] with your desired release tag)
specify self upgrade --tag vX.Y.Z[suffix]
```

Bare `specify self upgrade` executes immediately, matching the no-prompt behavior of commands like `pip install -U` and `npm update`. For `uv tool` installs, it runs `uv tool install wepld-agile --force --from <git ref>` under the hood so pinned release tags work, including dev, alpha/beta/rc, or build metadata suffixes. `uvx` (ephemeral) runs and source checkouts are detected and produce path-specific guidance instead of running an installer. Set `SPECIFY_UPGRADE_TIMEOUT_SECS` to cap how long the installer subprocess may run (default: no timeout — interrupt with `Ctrl+C` if needed).

### 3. Establish project principles

Launch your coding agent in the project directory. Most agents expose agile as `/agile.*` slash commands; Codex CLI and Command Code in skills mode use `$agile-*` instead; GitHub Copilot CLI uses `/agents` to select the agent or address it directly in a prompt.

Use the **`/agile.constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/agile.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

### 4. Create the spec

Use the **`/agile.agile`** command to describe what you want to build. Focus on the **what** and **why**, not the tech stack.

```bash
/agile.agile Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### 5. Create a technical implementation plan

Use the **`/agile.plan`** command to provide your tech stack and architecture choices.

```bash
/agile.plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### 6. Break down into tasks

Use **`/agile.tasks`** to create an actionable task list from your implementation plan.

```bash
/agile.tasks
```

### 7. Execute implementation

Use **`/agile.implement`** to execute all tasks and build your feature according to the plan.

```bash
/agile.implement
```

For detailed step-by-step instructions, see our [comprehensive guide](./spec-driven.md).

## 📽️ Video Overview

Want to see Agile in action? Watch our [video overview](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)!

[![Agile video header](https://raw.githubusercontent.com/github/agile/main/media/agile-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🌍 Community

Explore community-contributed resources on the [Agile docs site](https://github.github.io/agile/):

- [Extensions](https://github.github.io/agile/community/extensions.html) — commands, hooks, and capabilities
- [Presets](https://github.github.io/agile/community/presets.html) — template and terminology overrides
- [Bundles](https://github.github.io/agile/community/bundles.html) — role and team stacks composed from existing components
- [Walkthroughs](https://github.github.io/agile/community/walkthroughs.html) — end-to-end SDD scenarios
- [Friends](https://github.github.io/agile/community/friends.html) — projects that extend or build on Agile

> [!NOTE]
> Community contributions are independently created and maintained by their respective authors. Review source code before installation and use at your own discretion.

Want to contribute? See the [Extension Publishing Guide](extensions/EXTENSION-PUBLISHING-GUIDE.md), the [Presets Publishing Guide](presets/PUBLISHING.md), or the [Community Bundles guide](docs/community/bundles.md).

## 🤖 Supported AI Coding Agent Integrations

Agile works with 30+ AI coding agents — both CLI tools and IDE-based assistants. See the full list with notes and usage details in the [Supported AI Coding Agent Integrations](https://github.github.io/agile/reference/integrations.html) guide.

Run `specify integration list` to see all available integrations in your installed version.

## Available Slash Commands

After running `agile init`, your AI coding agent will have access to these slash commands for structured development. For integrations that support skills mode, passing `--integration <agent> --integration-options="--skills"` installs agent skills instead of slash-command prompt files.

### Core Commands

Essential commands for the Spec-Driven Development workflow:

| Command                  | Agent Skill            | Description                                                                |
| ------------------------ | ---------------------- | -------------------------------------------------------------------------- |
| `/agile.constitution`  | `agile-constitution` | Create or update project governing principles and development guidelines   |
| `/agile.agile`       | `agile-specify`      | Define what you want to build (requirements and user stories)              |
| `/agile.plan`          | `agile-plan`         | Create technical implementation plans with your chosen tech stack          |
| `/agile.tasks`         | `agile-tasks`        | Generate actionable task lists for implementation                          |
| `/agile.taskstoissues` | `agile-taskstoissues`| Convert generated task lists into GitHub issues for tracking and execution |
| `/agile.implement`     | `agile-implement`    | Execute all tasks to build the feature according to the plan               |
| `/agile.converge`      | `agile-converge`     | Assess the codebase against spec/plan/tasks and append remaining work as new tasks |

### Optional Commands

Additional commands for enhanced quality and validation:

| Command              | Agent Skill            | Description                                                                                                                          |
| -------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `/agile.clarify`   | `agile-clarify`      | Clarify underspecified areas (recommended before `/agile.plan`; formerly `/quizme`)                                                |
| `/agile.analyze`   | `agile-analyze`      | Cross-artifact consistency & coverage analysis (run after `/agile.tasks`, before `/agile.implement`)                             |
| `/agile.checklist` | `agile-checklist`    | Generate custom quality checklists that validate requirements completeness, clarity, and consistency (like "unit tests for English") |

## 🔧 Agile CLI Reference

For full command details, options, and examples, see the [CLI Reference](https://github.github.io/agile/reference/overview.html).

## 🧩 Making Agile Your Own: Extensions & Presets

Agile can be tailored to your needs through two complementary systems — **extensions** and **presets** — plus project-local overrides for one-off adjustments:

| Priority | Component Type                                    | Location                         |
| -------: | ------------------------------------------------- | -------------------------------- |
|      ⬆ 1 | Project-Local Overrides                           | `.agile/templates/overrides/`  |
|        2 | Presets — Customize core & extensions             | `.agile/presets/templates/`    |
|        3 | Extensions — Add new capabilities                 | `.agile/extensions/templates/` |
|      ⬇ 4 | Agile Core — Built-in SDD commands & templates | `.agile/templates/`            |

- **Templates** are resolved at **runtime** — Agile walks the stack top-down and uses the first match.
- Project-local overrides (`.agile/templates/overrides/`) let you make one-off adjustments for a single project without creating a full preset.
- **Extension/preset commands** are applied at **install time** — when you run `agile extension add` or `specify preset add`, command files are written into agent directories (e.g., `.claude/commands/`).
- If multiple presets or extensions provide the same command, the highest-priority version wins. On removal, the next-highest-priority version is restored automatically.
- If no overrides or customizations exist, Agile uses its core defaults.

### Extensions — Add New Capabilities

Use **extensions** when you need functionality that goes beyond Agile's core. Extensions introduce new commands and templates — for example, adding domain-specific workflows that are not covered by the built-in SDD commands, integrating with external tools, or adding entirely new development phases. They expand *what Agile can do*.

```bash
# Search available extensions
agile extension search

# Install an extension
agile extension add <extension-name>
```

For example, extensions could add Jira integration, post-implementation code review, V-Model test traceability, or project health diagnostics.

See the [Extensions reference](https://github.github.io/agile/reference/extensions.html) for the full command guide. Browse the [community extensions](https://github.github.io/agile/community/extensions.html) for what's available.

### Presets — Customize Existing Workflows

Use **presets** when you want to change *how* Agile works without adding new capabilities. Presets override the templates and commands that ship with the core *and* with installed extensions — for example, enforcing a compliance-oriented spec format, using domain-specific terminology, or applying organizational standards to plans and tasks. They customize the artifacts and instructions that Agile and its extensions produce.

```bash
# Search available presets
specify preset search

# Install a preset
specify preset add <preset-name>
```

For example, presets could restructure spec templates to require regulatory traceability, adapt the workflow to fit the methodology you use (e.g., Agile, Kanban, Waterfall, jobs-to-be-done, or domain-driven design), add mandatory security review gates to plans, enforce test-first task ordering, or localize the entire workflow to a different language. The [pirate-speak demo](https://github.com/mnriem/agile-pirate-speak-preset-demo) shows just how deep the customization can go. Multiple presets can be stacked with priority ordering.

See the [Presets reference](https://github.github.io/agile/reference/presets.html) for the full command guide, including resolution order and priority stacking.

## 📦 Bundles: Role-Based Setups

Extensions and presets are individual building blocks. A **bundle** packages a
curated set of them — extensions, presets, steps, and workflows — into a single,
versioned, role-oriented setup so a whole team persona (product manager, business
analyst, security researcher, developer, …) can be provisioned with one command.

A bundle is described by a hand-written `bundle.yml` manifest. It pins each
component to a version and, optionally, targets a specific integration; a bundle
with no `integration` is **agnostic** and inherits whatever integration the
project already uses.

```bash
# Discover bundles in the active catalog stack
agile bundle search [<query>]

# Inspect the exact component set a bundle will add (equals what install does)
agile bundle info <bundle-id>

# Install a bundle's full component set in one operation
agile bundle install <bundle-id>

# See what's installed, then update or remove non-destructively
agile bundle list
agile bundle update <bundle-id>     # or --all
agile bundle remove <bundle-id>     # removes only this bundle's components
```

Bundles resolve from a **priority-ordered catalog stack** (project > user >
built-in). Each source carries an install policy: `install-allowed` sources can
be installed from, while `discovery-only` sources are visible in `search`/`info`
but refuse installation. Manage the stack with `agile bundle catalog list|add|remove`.

Authors validate and package bundles locally. Distribution is hosting the built
artifact and adding a catalog source; community bundle submissions use the
[Bundle Submission](https://github.com/TheHalfMoon/wepld/issues/new?template=bundle_submission.yml)
issue template so required component catalogs and install evidence can be reviewed:

```bash
agile bundle validate --path ./my-bundle      # structural + reference checks
agile bundle build --path ./my-bundle         # produce a versioned .zip artifact
```

Four ready-to-read example bundle manifests live under
[`examples/bundles/`](examples/bundles/) (product manager, business analyst,
security researcher, developer). These are bundle packaging examples, not
filled generated feature specs; for end-to-end community examples, see the
[community walkthroughs](https://github.github.io/agile/community/walkthroughs.html).

Key guarantees: `info` shows exactly what `install` adds (transparency);
installs are idempotent and confined to the project root; `remove` never touches
components another installed bundle still needs; and all consume/author commands
work **offline** against local or pinned sources.

### When to Use Which

| Goal | Use |
| --- | --- |
| Add a brand-new command or workflow | Extension |
| Customize the format of specs, plans, or tasks | Preset |
| Integrate an external tool or service | Extension |
| Enforce organizational or regulatory standards | Preset |
| Ship reusable domain-specific templates | Either — presets for template overrides, extensions for templates bundled with new commands |
| Provision a complete role-based setup in one command | Bundle |

## 📚 Core Philosophy

Spec-Driven Development is a structured process that emphasizes:

- **Intent-driven development** where specifications define the "*what*" before the "*how*"
- **Rich specification creation** using guardrails and organizational principles
- **Multi-step refinement** rather than one-shot code generation from prompts
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

## 🌟 Development Phases

| Phase                                    | Focus                    | Key Activities                                                                                                                                                     |
| ---------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **0-to-1 Development** ("Greenfield")    | Generate from scratch    | <ul><li>Start with high-level requirements</li><li>Generate specifications</li><li>Plan implementation steps</li><li>Build production-ready applications</li></ul> |
| **Creative Exploration**                 | Parallel implementations | <ul><li>Explore diverse solutions</li><li>Support multiple technology stacks & architectures</li><li>Experiment with UX patterns</li></ul>                         |
| **Iterative Enhancement** ("Brownfield") | Brownfield modernization | <ul><li>Add features iteratively</li><li>Modernize legacy systems</li><li>Adapt processes</li></ul>                                                                |

For existing projects, keep Agile tooling updates separate from feature
artifact evolution: refresh managed project files when upgrading, and update
`specs/` artifacts when intended behavior changes. The
[Evolving Specs guide](./docs/guides/evolving-specs.md) describes the
recommended brownfield loop.

## 🎯 Experimental Goals

Our research and experimentation focus on:

### Technology independence

- Create applications using diverse technology stacks
- Validate the hypothesis that Spec-Driven Development is a process not tied to specific technologies, programming languages, or frameworks

### Enterprise constraints

- Demonstrate mission-critical application development
- Incorporate organizational constraints (cloud providers, tech stacks, engineering practices)
- Support enterprise design systems and compliance requirements

### User-centric development

- Build applications for different user cohorts and preferences
- Support various development approaches (from vibe-coding to AI-native development)

### Creative & iterative processes

- Validate the concept of parallel implementation exploration
- Provide robust iterative feature development workflows
- Extend processes to handle upgrades and modernization tasks

## 🔧 Prerequisites

- **Linux/macOS/Windows**
- [Supported](#-supported-ai-coding-agent-integrations) AI coding agent.
- [uv](https://docs.astral.sh/uv/) for package management (recommended) or [pipx](https://pipx.pypa.io/) for persistent installation
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

If you encounter issues with an agent, please open an issue so we can refine the integration.

## 📖 Learn More

- **[Complete Spec-Driven Development Methodology](./spec-driven.md)** - Deep dive into the full process
- **[Quick Start Guide](https://github.github.io/agile/quickstart.html)** - Step-by-step implementation walkthrough

---

## 💬 Support

For support, please open a [GitHub issue](https://github.com/TheHalfMoon/wepld/issues/new). We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

## 🙏 Acknowledgements

This project is heavily influenced by and based on the work and research of [John Lam](https://github.com/jflam).

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
