<!-- Modified by WePLD on 2026-08-23: deterministic Pictorial rebrand/path integration from the pinned upstream source. -->
# Pictorial

Design guidance for AI coding agents. 1 skill, 23 commands, live browser iteration, and 59 deterministic detector rules for AI-generated frontend design.

> **Quick start:** From your project root, run `npx pictorial install`, then run `/pictorial init` inside your AI coding tool. Full docs: [github.com/TheHalfMoon/wepld](https://github.com/TheHalfMoon/wepld).

## Why Pictorial?

Anthropic's [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) was the first widely-used design skill for Claude. Pictorial started from there.

Every model trained on the same SaaS templates. Skip the guidance and you get the same handful of tells on every project: Inter for everything, purple-to-blue gradients, cards nested in cards, gray text on colored backgrounds, the rounded-square icon tile above every heading.

Pictorial adds:
- **One setup flow.** `/pictorial init` writes `PRODUCT.md` and offers `DESIGN.md`, so later commands know the audience, brand/product lane, voice, anti-references, colors, type, and components.
- **23 commands.** A shared design vocabulary with your AI: `polish`, `audit`, `critique`, `distill`, `animate`, `bolder`, `quieter`, and more.
- **59 deterministic detector rules** plus LLM-only critique checks. The CLI and browser extension run the deterministic rules with no LLM and no API key.

## What's Included

### The Skill: pictorial

The skill installs as one command:

```bash
/pictorial <command> <target>
```

Start every new project with:

```bash
/pictorial init
```

`init` asks whether the surface is brand (marketing, landing, portfolio) or product (app UI, dashboard, tool), then writes design context that every later command reads.

### 23 Commands

All commands are accessed through `/pictorial`:

| Command | What it does |
|---------|--------------|
| `/pictorial craft` | Full shape-then-build flow with visual iteration |
| `/pictorial init` | One-time setup: gather design context, write PRODUCT.md and DESIGN.md, configure live mode, recommend next steps |
| `/pictorial document` | Generate root DESIGN.md from existing project code |
| `/pictorial extract` | Pull reusable components and tokens into the design system |
| `/pictorial shape` | Plan UX/UI before writing code |
| `/pictorial critique` | UX design review: hierarchy, clarity, emotional resonance |
| `/pictorial audit` | Run technical quality checks (a11y, performance, responsive) |
| `/pictorial polish` | Final pass, design system alignment, and shipping readiness |
| `/pictorial bolder` | Amplify boring designs |
| `/pictorial quieter` | Tone down overly bold designs |
| `/pictorial distill` | Strip to essence |
| `/pictorial harden` | Error handling, i18n, text overflow, edge cases |
| `/pictorial onboard` | First-run flows, empty states, activation paths |
| `/pictorial animate` | Add purposeful motion |
| `/pictorial colorize` | Introduce strategic color |
| `/pictorial typeset` | Fix font choices, hierarchy, sizing |
| `/pictorial layout` | Fix layout, spacing, visual rhythm |
| `/pictorial delight` | Add moments of joy |
| `/pictorial overdrive` | Add technically extraordinary effects |
| `/pictorial clarify` | Improve unclear UX copy |
| `/pictorial adapt` | Adapt for different devices |
| `/pictorial optimize` | Performance improvements |
| `/pictorial live` | Visual variant mode: iterate on elements in the browser |

Use `/pictorial pin <command>` to create standalone shortcuts (e.g., `pin audit` creates `/audit`).

#### Usage Examples

```
/pictorial audit blog           # Audit blog hub + post pages
/pictorial critique landing     # UX design review
/pictorial polish settings      # Final pass before shipping
/pictorial harden checkout      # Add error handling + edge cases
```

Or use `/pictorial` directly with a description:
```
/pictorial redo this hero section
```

### Anti-Patterns

The skill includes explicit guidance on what to avoid:

- Don't use overused fonts (Arial, Inter, system defaults)
- Don't use gray text on colored backgrounds
- Don't use pure black/gray (always tint)
- Don't wrap everything in cards or nest cards inside cards
- Don't use bounce/elastic easing (feels dated)

## See It In Action

Visit [the Neo Mirai case study](https://github.com/TheHalfMoon/wepld/cases/neo-mirai) to see a before/after case study of a real project transformed with Pictorial commands.

## Installation

### Option 1: CLI installer (Recommended)

From the root of your project, run:

```bash
npx pictorial install
```

This shows the harness folders it detected (for example `~/.claude`, `~/.codex`, `~/.grok`, or project-local `.cursor`), lets you keep the detected set or customize providers, then asks whether to install into the current project or globally. Use `--providers=claude,codex,cursor,grok` and `--scope=project|global` to skip those choices in scripts. On Claude Code, Cursor, Codex, GitHub Copilot, and Grok Build, it also installs the provider-native hook manifest for the current project. Works with Cursor, Claude Code, Gemini CLI, Codex CLI, Grok Build, and every other supported tool. Reload your harness afterward.

To refresh an existing install, run:

```bash
npx pictorial update
```

Codex users should open `/hooks` after install or update and approve the project hook when prompted. Codex tracks trust by hook definition, so updates that change `.codex/hooks.json` can require approval again. Grok Build users need project folder trust (`/hooks-trust` or launch with `--trust`) before `.grok/hooks/` scripts run.

### Option 2: Git Submodule

For teams that want to keep Pictorial vendored and updated through Git, add this repo as a submodule and link the compiled provider build into your harness folders:

```bash
git submodule add https://github.com/TheHalfMoon/wepld .pictorial
npx pictorial link --source=.pictorial --providers=claude,cursor
git add .gitmodules .pictorial .claude .cursor
git commit -m "Add Pictorial skills"
```

Use the providers your project needs, for example `claude`, `cursor`, `gemini`, `codex`, `github`, `grok`, `opencode`, `pi`, `qoder`, `trae`, `trae-cn`, `rovo-dev`, or `vibe`. The command links individual skill folders from `.pictorial/dist/universal/` and leaves existing real skill directories untouched unless you pass `--force`.

To update later:

```bash
git submodule update --remote .pictorial
npx pictorial link --source=.pictorial --providers=claude,cursor
```

### Option 3: Plugin install

**Claude Code:**
```bash
/plugin marketplace add pbakaus/pictorial
```

> Claude Code only. After adding the marketplace, open `/plugin` and install Pictorial from the list.

**Grok Build:**
```bash
grok plugin install pbakaus/pictorial#plugin --trust
```

> Grok Build only. The `#plugin` suffix installs the slim plugin package (skills, agents, and hooks) instead of the full monorepo. Then run `/pictorial init` in a Grok session. Project-scoped installs via `npx pictorial install --providers=grok` also work and write `.grok/skills/` plus `.grok/hooks/pictorial.json`.

### Option 4: Download from Website

Visit [github.com/TheHalfMoon/wepld](https://github.com/TheHalfMoon/wepld), download the ZIP for your tool, and extract to your project.

### Option 5: Copy from Repository

**Cursor:**
```bash
cp -r dist/cursor/.cursor your-project/
```

> **Note:** Cursor skills require setup:
> 1. Switch to Nightly channel in Cursor Settings → Beta
> 2. Enable Agent Skills in Cursor Settings → Rules
>
> [Learn more about Cursor skills](https://cursor.com/docs/context/skills)

**Claude Code:**
```bash
# Project-specific
cp -r dist/claude-code/.claude your-project/

# Or global (applies to all projects)
cp -r dist/claude-code/.claude/* ~/.claude/
```

**OpenCode:**
```bash
cp -r dist/opencode/.opencode your-project/
```

**Pi:**
```bash
cp -r dist/pi/.pi your-project/
```

**Gemini CLI:**
```bash
cp -r dist/gemini/.gemini your-project/
```

> **Note:** Gemini CLI skills require setup:
> 1. Install preview version: `npm i -g @google/gemini-cli@preview`
> 2. Run `/settings` and enable "Skills"
> 3. Run `/skills list` to verify installation
>
> [Learn more about Gemini CLI skills](https://geminicli.com/docs/cli/skills/)

**Codex CLI:**
```bash
# Project-local
cp -r dist/agents/.agents your-project/
mkdir -p your-project/.codex
cp dist/codex/.codex/hooks.json your-project/.codex/hooks.json

# Or install the skill user-wide. Copy .codex/hooks.json into each project
# where you want the design hook to run.
mkdir -p ~/.agents/skills
cp -r dist/agents/.agents/skills/* ~/.agents/skills/
```

> The asset-producer subagent ships nested inside the skill's own `agents/` folder, which Codex auto-discovers. No separate `.codex/agents/` copy is needed. The hook is project-local because Codex discovers hooks from `.codex/hooks.json` next to trusted project config.

**GitHub Copilot:**
```bash
cp -r dist/github/.github your-project/
```

**Trae:**
```bash
# Trae China (domestic version)
cp -r dist/trae/.trae-cn/skills/* ~/.trae-cn/skills/

# Trae International
cp -r dist/trae/.trae/skills/* ~/.trae/skills/
```

> **Note:** Trae has two versions with different config directories:
> - **Trae China**: `~/.trae-cn/skills/`
> - **Trae International**: `~/.trae/skills/`
>
> After copying, restart Trae IDE to activate the skills.

**Rovo Dev:**
```bash
# Project-specific
cp -r dist/rovo-dev/.rovodev your-project/

# Or global (applies to all projects)
cp -r dist/rovo-dev/.rovodev/skills/* ~/.rovodev/skills/
```

**Qoder:**
```bash
# Project-specific
cp -r dist/qoder/.qoder your-project/

# Or global (applies to all projects)
cp -r dist/qoder/.qoder/skills/* ~/.qoder/skills/
```

**Mistral Vibe:**
```bash
# Project-specific
cp -r dist/vibe/.vibe your-project/

# Or global (applies to all projects)
cp -r dist/vibe/.vibe/skills/* ~/.vibe/skills/
```

**Grok Build:**
```bash
# Project-specific
cp -r dist/grok/.grok your-project/

# Or global (applies to all projects)
cp -r dist/grok/.grok/skills/* ~/.grok/skills/
```

> Prefer `npx pictorial install --providers=grok` or `grok plugin install pbakaus/pictorial#plugin --trust` so the design hook installs too. Project hooks need `/hooks-trust` (or `--trust`) once per folder.

**Google Antigravity:**
```bash
# Project-specific
cp -r dist/antigravity/.agent your-project/

# Or global (applies to all projects)
mkdir -p ~/.gemini/config/skills
cp -r dist/antigravity/.agent/skills/* ~/.gemini/config/skills/
```

## Usage

Once installed, every command runs through the single `/pictorial` skill:

```
/pictorial audit        # Find issues
/pictorial polish       # Final cleanup
/pictorial distill      # Remove complexity
/pictorial critique     # Full design review
```

Type `/pictorial` alone to see the full command list.

Most commands accept an optional argument to focus on a specific area:

```
/pictorial audit the header
/pictorial polish the checkout form
```

If you reach for one command often, pin it with `/pictorial pin audit` to get `/audit` as a standalone shortcut.

**Note:** Codex uses skills here, not `/prompts:` commands. Open `/skills` or type `$pictorial`. Repo-local installs live in `.agents/skills/`; user-wide installs live in `~/.agents/skills/`. GitHub Copilot uses `.github/skills/`. Restart the tool if a newly installed skill does not appear.

## Keeping `.pictorial` out of git

As you run commands, Pictorial writes working files under `.pictorial/`: critique and polish screenshots, live-mode session and preview state, runtime caches, and per-developer config. Most of it is ephemeral and should not be committed, while a few files are shared project artifacts that belong in the repo. Add this block to your project's `.gitignore`:

```gitignore
# pictorial-ignore-start
# Ephemeral output, runtime state, and per-dev overrides.
# Unanchored: .pictorial may sit at the repo root or under a nested
# workspace (apps/web/.pictorial/...); anchored patterns would miss it.
# Shared artifacts stay tracked: config.json, live/config.json,
# design.json, critique/*.md.
.pictorial/config.local.json
.pictorial/hook.cache.json
.pictorial/hook.pending.json
.pictorial/*.png
.pictorial/live/server.json
.pictorial/live/sessions/
.pictorial/live/previews/
.pictorial/live/annotations/
.pictorial/live/cache/
.pictorial/live/manual-edit-apply-transaction.json
.pictorial/live/manual-edit-events.jsonl
.pictorial/live/manual-edit-evidence/
.pictorial/live/pending-manual-edits.json
.pictorial/live/deferred-svelte-component-accepts.json
.pictorial/live/*.png
# pictorial-ignore-end
```

The block is wrapped in `# pictorial-ignore-start` / `# pictorial-ignore-end` markers so you can recognize and refresh it later. Patterns are unanchored on purpose: in a monorepo the active project (and its `.pictorial/` directory) often lives under a nested workspace path like `apps/web/`, and a root-anchored pattern would miss it.

**Keep these tracked** (they are shared project artifacts, do not add them to `.gitignore`):

- `.pictorial/config.json` (unified shared config)
- `.pictorial/live/config.json` (live-mode framework wiring)
- `.pictorial/design.json` (shared design spec)
- `.pictorial/critique/*.md` (review reports)

If an ephemeral file (a screenshot, `config.local.json`) was committed before you added the block, `.gitignore` will not untrack it automatically. Run `git rm --cached <path>` to stop tracking it without deleting your local copy.

## Design hook

On Claude Code, GitHub Copilot, Codex, Cursor, and Grok Build, `npx pictorial install` and `npx pictorial update` install a provider-native hook manifest along with the skill payload. The hook runs the Pictorial design detector on direct UI file edits and surfaces findings back into the agent flow. Claude Code, GitHub Copilot, Codex, and Grok Build surface findings after the edit (and run a deeper pass on Stop where supported). Cursor blocks bad proposed writes before they land.

Installed hook surfaces:

- Claude Code: `.claude/settings.local.json` (gitignored, machine-local) runs `${CLAUDE_PROJECT_DIR}/.claude/skills/pictorial/scripts/hook.mjs`. A hook moved into the shared `settings.json` is honored in place.
- GitHub Copilot: `.github/hooks/pictorial.json` (committed, shared by the Copilot CLI and the cloud agent) runs `.github/skills/pictorial/scripts/hook.mjs`. The Copilot CLI activates it once the file is on the repository's default branch and the folder is trusted.
- Cursor: `.cursor/hooks.json` runs `.cursor/skills/pictorial/scripts/hook-before-edit.mjs`.
- Codex: `.codex/hooks.json` runs `.agents/skills/pictorial/scripts/hook.mjs`.

The installer preserves unrelated hook entries and settings. If a hook manifest is malformed, install/update aborts by default; rerun with `--force` to back up the malformed file as `.bak` and replace it.

On an interactive `install`/`update`, Pictorial explains the hook and offers to install it (default yes). Your choice is remembered per-developer in the gitignored `.pictorial/config.local.json`, so you are not asked again; `--no-hooks` skips it for that run without recording anything. Hook lifecycle settings live under the `hook` key of `.pictorial/config.json`; detector ignores live under `detector`, shared by `/pictorial hooks` and `npx pictorial detect`.

For debugging, set `hook.auditLog` in `.pictorial/config.json` to a path (or the legacy `PICTORIAL_HOOK_LOG` env var) to write one NDJSON line per hook invocation. Leave it unset for normal use.

## Build path: comp-first or code-first

When a new surface gets designed, Pictorial either generates a full-fidelity comp first and builds to match it, or builds straight in code with the ambition written into the direction contract and checked at the finish. Comp-first composes bolder and takes longer; code-first is leaner and faster. `/pictorial init` asks once and records the answer as `buildPath` in `.pictorial/config.json`:

```json
{ "buildPath": "comp" }
```

The values are `comp` and `code`, and nothing else is read. Set it in the gitignored `.pictorial/config.local.json` to override the team's committed value on one machine, which is what you want when your harness has no image generation. In a monorepo, commit it once at the repo root and any workspace that wants something else sets its own. The choice appears at all only where image generation is available, since without it there is nothing to comp.

You do not have to re-run `init` to set it on a project that predates the setting, and you do not have to edit the file by hand either. Whatever is recorded is a default rather than a lock: every decision page carries a footer toggle, and flipping it binds that session only. Flip it on a project that has recorded nothing and Pictorial asks once, after the round, whether to keep it, then writes your answer. That is the whole migration path for an existing project: use the toggle when the default is wrong, and answer the question that follows.

Codex requires one platform step that Pictorial cannot safely skip: open `/hooks` after install or update and approve the project hook. There is no Codex marketplace/plugin install flow for this hook.

Full hook docs: [github.com/TheHalfMoon/wepld/docs/hooks](https://github.com/TheHalfMoon/wepld/docs/hooks).

Manual copy commands are fallback/debug instructions. The normal path is:

```bash
npx pictorial install
npx pictorial update
```

## CLI

Pictorial includes a standalone CLI for detecting anti-patterns without an AI harness:

```bash
npx pictorial detect src/                   # scan a directory
npx pictorial detect index.html             # scan an HTML file
npx pictorial detect https://example.com    # scan a URL (Puppeteer)
npx pictorial detect --json .               # CI-friendly JSON output
npx pictorial detect --no-config src/       # raw scan, ignoring project config/context
npx pictorial ignores list                  # show detector ignores
npx pictorial ignores add-file "src/legacy/**"
npx pictorial ignores add-value overused-font Inter --reason "Brand font"
```

The detector catches 59 deterministic issues across AI slop (side-tab borders, purple gradients, bounce easing, dark glows) and general design quality (line length, cramped padding, small touch targets, skipped headings, and more).

By default, `detect` respects the same `.pictorial/config.json` and `.pictorial/config.local.json` detector config as the design hook: `detector.ignoreRules`, `detector.ignoreFiles`, `detector.ignoreValues`, and `detector.designSystem.enabled`. Hook lifecycle settings such as `hook.enabled` only affect automatic hook execution.

For a waiver that should travel with one file instead of the repo config, add an inline comment in the file: `<!-- pictorial-disable overused-font: exported brand doc -->`. The marker works in any comment syntax, scopes to the whole file (or one line with `pictorial-disable-line` / `pictorial-disable-next-line`), and is bypassed by `--no-inline-ignores` or `--no-config`.

Full detector docs: [github.com/TheHalfMoon/wepld/docs/detector](https://github.com/TheHalfMoon/wepld/docs/detector).

## Supported Tools

- [Cursor](https://cursor.com)
- [Claude Code](https://claude.ai/code)
- [GitHub Copilot](https://github.com/features/copilot)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Codex CLI](https://github.com/openai/codex)
- [Grok Build](https://x.ai/cli)
- [OpenCode](https://opencode.ai)
- [Pi](https://pi.dev)
- [Kiro](https://kiro.dev)
- [Trae](https://trae.ai)
- [Rovo Dev](https://www.atlassian.com/software/rovo)
- [Qoder](https://qoder.com)
- [Mistral Vibe](https://docs.mistral.ai/vibe/code/overview)
- [Google Antigravity](https://antigravity.google)

## Community & Ecosystem

Join the community and ecosystem conversations:

- GitHub Discussions: file bugs, request features, and help newcomers.
- [Pictorial on npm](https://www.npmjs.com/package/pictorial): grab the CLI, follow releases, and star the package.
- Follow @pbakaus on Twitter for release notes, sample lint reports, and video highlights of new rules.

## Contributing

See [DEVELOP.md](docs/DEVELOP.md) for contributor guidelines and build instructions.

## License

Apache 2.0. See [LICENSE](LICENSE).

---

Created by [Paul Bakaus](https://www.paulbakaus.com)
