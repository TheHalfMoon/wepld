# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows; PowerShell scripts now supported without WSL)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [CodeBuddy CLI](https://www.codebuddy.cn/docs/cli/installation), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Pi Coding Agent](https://pi.dev), or [Oh My Pi](https://www.npmjs.com/package/@oh-my-pi/pi-coding-agent)
- [uv](https://docs.astral.sh/uv/) for package management (recommended) or [pipx](https://pipx.pypa.io/) for persistent installation
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) _(optional — required only when the git extension is enabled)_

## Installation

> [!IMPORTANT]
> Agile is distributed through two official channels, both published and maintained by the Agile maintainers: the [github/agile](https://github.com/TheHalfMoon/wepld) GitHub repository (source installs) and the [`wepld-agile`](https://pypi.org/project/wepld-agile/) package on [PyPI](https://pypi.org/project/wepld-agile/). Either route is supported for normal installs — use the commands shown below. After installing, run `agile version` as a local version/runtime sanity check. It confirms that the `agile` command is available and reports its version, but it does not prove whether the executable came from PyPI or GitHub. For offline or air-gapped environments, locally built wheels created from this repository are also valid.

Agile supports two install routes:

1. **Install from source (GitHub)** — the recommended route, pinned to a release tag.
2. **Install from PyPI** — install the published `wepld-agile` package with your usual Python tooling.

### Install from Source — Persistent Installation (Recommended)

Install once and use everywhere. Replace `vX.Y.Z` with a release tag from [Releases](https://github.com/TheHalfMoon/wepld/releases) — keep the leading `v` (for example, `v0.12.11`, not `0.12.11`):

> [!NOTE]
> The command below requires **[uv](https://docs.astral.sh/uv/)**. If you see `command not found: uv`, [install uv first](./install/uv.md).

```bash
uv tool install wepld-agile --from git+https://github.com/TheHalfMoon/wepld.git@vX.Y.Z
```

Then initialize a project:

```bash
agile init <PROJECT_NAME> --integration copilot
```

### Install from PyPI

Agile is also published to PyPI as [`wepld-agile`](https://pypi.org/project/wepld-agile/), so you can install it with your preferred Python package manager without referencing the Git URL:

```bash
# Using uv (recommended)
uv tool install wepld-agile

# Or using pipx
pipx install wepld-agile

# Or using pip
pip install wepld-agile
```

To install a specific release, pin the version — for example `uv tool install wepld-agile==0.12.11`. See the [PyPI installation guide](install/pypi.md) for details, including how to upgrade and how to [install from a custom or private package index](install/pypi.md#install-from-a-custom-or-private-package-index).

### One-time Usage

Run directly without installing — see the [One-time usage (uvx)](install/one-time.md) guide.

### Alternative Package Managers

- **PyPI** — see the [PyPI installation guide](install/pypi.md)
- **pipx** — see the [pipx installation guide](install/pipx.md)
- **Enterprise / Air-Gapped** — see the [air-gapped installation guide](install/air-gapped.md)

### Specify Integration

Interactive terminals prompt you to choose a coding agent integration during initialization. Non-interactive sessions, such as CI or piped runs, default to GitHub Copilot unless you pass `--integration`.

You can proactively specify your coding agent integration during initialization:

```bash
agile init <project_name> --integration claude
agile init <project_name> --integration gemini
agile init <project_name> --integration copilot
agile init <project_name> --integration codebuddy
agile init <project_name> --integration pi
agile init <project_name> --integration omp
```

### Specify Script Type (Shell, PowerShell, or Python)

Automation scripts are available as Bash (`.sh`), PowerShell (`.ps1`), and Python (`.py`) variants.

Auto behavior:

- Windows default: `ps`
- Other OS default: `sh`
- Interactive mode: you'll be prompted unless you pass `--script`

Force a specific script type:

```bash
agile init <project_name> --script sh
agile init <project_name> --script ps
agile init <project_name> --script py
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
agile init <project_name> --integration claude --ignore-agent-tools
```

## Verification

After installation, run the following command as a local version/runtime check:

```bash
agile version
```

This confirms that the `agile` command is available and reporting the expected version. It does not prove whether that executable came from PyPI or GitHub.

**Stay current:** Run `specify self check` periodically to learn whether a newer release is available — it is read-only and never modifies your installation. When you are ready to upgrade, follow the [Upgrade Guide](./upgrade.md).

After initialization, you should see the following commands available in your coding agent:

- `/agile.agile` - Create specifications
- `/agile.plan` - Generate implementation plans
- `/agile.tasks` - Break down into actionable tasks
- `/agile.implement` - Execute implementation tasks
- `/agile.analyze` - Validate cross-artifact consistency
- `/agile.clarify` - Identify and resolve ambiguities
- `/agile.checklist` - Generate quality checklists
- `/agile.constitution` - Create or update project principles
- `/agile.converge` - Assess codebase against artifacts and append remaining tasks
- `/agile.taskstoissues` - Convert tasks to issues

Scripts are installed into a variant subdirectory matching the chosen script type:

- `.agile/scripts/bash/` — contains `.sh` scripts (default on Linux/macOS)
- `.agile/scripts/powershell/` — contains `.ps1` scripts (default on Windows)
- `.agile/scripts/python/` — contains `.py` scripts (chosen with `--script py`; also installs the platform shell fallback)

## Troubleshooting

### Enterprise / Air-Gapped Installation

If your environment blocks access to PyPI or GitHub, see the [Enterprise / Air-Gapped Installation](install/air-gapped.md) guide for step-by-step instructions on creating portable wheel bundles.

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, see the [Air-Gapped Installation guide](install/air-gapped.md#git-credential-manager-on-linux) for Git Credential Manager setup instructions.
