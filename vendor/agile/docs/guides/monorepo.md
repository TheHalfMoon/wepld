# Using Agile in a Monorepo

A Agile project is **directory-scoped**: the project is whichever directory
contains `.agile/`. A monorepo can hold several independent Agile projects
under one repository root, each with its own `.agile/`, `specs/`, constitution,
and feature numbering.

Root resolution already prefers the **nearest** `.agile/` over the Git
toplevel, so commands run from inside a member project resolve to that project,
not the repo root.

## Layout

```text
my-monorepo/
├── .git/                     # one Git repository at the root
├── apps/
│   ├── web/
│   │   └── .agile/         # Agile project "web"
│   │       └── memory/constitution.md
│   └── api/
│       └── .agile/         # Agile project "api"
│           └── memory/constitution.md
└── packages/
    └── ui/
        └── .agile/         # Agile project "ui"
```

Initialize each member project independently:

```bash
agile init apps/web --integration claude
agile init apps/api --integration claude
```

Each project keeps its own `specs/` directory and numbers features
independently (`apps/web/specs/001-…`, `apps/api/specs/001-…`).

## Working inside a member project

The default workflow is unchanged: change into the project directory and run the
slash commands. Root resolution finds the nearest `.agile/`.

```bash
cd apps/web
# then run /agile.specify, /agile.plan, … in your agent
```

## Targeting a member project from the repo root

For non-interactive or CI runs where you do not want to `cd`, set
**`AGILE_INIT_DIR`** to the member project root (the directory *containing*
`.agile/`). Relative paths resolve against the current directory.

```bash
# operate on apps/web from the monorepo root (no cd required)
export AGILE_INIT_DIR=apps/web
```

The path must exist and contain `.agile/`. If it does not, the command
**errors and does not fall back** to the current directory or the Git toplevel.
This is deliberate: a typo never writes specs into the wrong project. A
nonexistent path is reported as you typed it; a path that exists but is not a
Agile project is reported as its resolved absolute path:

```text
# AGILE_INIT_DIR=apps/wbe  (typo: no such directory)
ERROR: AGILE_INIT_DIR does not point to an existing directory: apps/wbe

# AGILE_INIT_DIR=apps  (exists, but has no .agile/ of its own)
ERROR: AGILE_INIT_DIR is not a Agile project (no .agile/ directory): /home/you/my-monorepo/apps
```

`AGILE_INIT_DIR` selects the **project**; `AGILE_FEATURE_DIRECTORY` selects
the **feature** within it. They compose: set both to pick a project and a
feature non-interactively. See the
[`AGILE_INIT_DIR` reference](../reference/core.md#environment-variables) for
the full contract and the two-axes model.

The `agile` CLI's project-scoped subcommands honor the same variable, so they
target a member project from the root without `cd` too:

```bash
export AGILE_INIT_DIR=apps/web
specify workflow list          # lists apps/web's workflows
agile integration status     # reports apps/web's integration
```

The validation rules are the same: the path must exist and contain `.agile/`,
with no fallback to the current directory.

## How `AGILE_INIT_DIR` reaches your agent

`AGILE_INIT_DIR` is read by the shell scripts that the slash commands invoke
(`get_repo_root` in Bash, `Get-RepoRoot` in PowerShell). It takes effect only
when it is present in the environment of the shell that runs those scripts.

- **Scripted / CI runs:** export it in the same shell that drives the commands;
  it is reliable there.
- **Interactive agents:** whether an exported variable reaches the shell tool an
  agent uses is agent-specific. Export `AGILE_INIT_DIR` *before* launching the
  agent, and verify once (e.g. run `/agile.specify` and confirm the new feature
  landed under the intended project's `specs/`).

## Git in a monorepo

> [!NOTE]
> Agile project files are scoped to the **resolved project root**, but Git
> operations still run in the containing Git work tree. In a monorepo with a
> single Git repository at the root and projects in subdirectories, feature
> branch creation creates or switches branches in the shared root repository.
> Spec directories still live under the selected member project, while the Git
> branch namespace is shared by the whole monorepo. Manage branches and commits
> at the repository root, or initialize Git per member project if you want
> isolated per-project branch namespaces.

## Constitutions

Each member project has its own `.agile/memory/constitution.md` and
`/agile.constitution` edits the local project's file. Agile does not provide
a built-in base/inheritance mechanism; if you want one constitution to reference
shared rules elsewhere in the monorepo, you need to maintain that wiring yourself.
Otherwise, duplicate or sync shared engineering rules per project.
