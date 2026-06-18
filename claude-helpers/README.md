# claude-helpers

A small collection of zsh + Python helpers for managing Claude Code sessions and the git worktrees they're tied to.

There are two layers:

- [**`claude-sessions`**](claude-sessions/) — a Python CLI that lists, opens, or deletes Claude Code session transcripts. The data layer; callable directly or via the `cls*` aliases.
- [**`clg*` worktree helpers**](#worktree-helpers-clg) — zsh functions that create / switch / delete git worktrees and hand the session lifecycle off to `claude-sessions`.

## Setup

Source the entry-point file from your `.zshrc`:

```sh
source /path/to/claude-helpers/claude-helpers
```

This:
- Prepends `<claude-helpers>/claude-sessions/` to `PATH`, so `claude-sessions` is callable from anywhere
- Defines the `clg*` worktree functions and the `cls*` / `cl` / `cln` aliases
- Resolves all paths relative to the entry-point's own location, so the directory can live anywhere on disk

## `claude-sessions` (the Python tool)

A subcommand-style CLI over Claude's session data at `~/.claude/projects/` (transcripts) and `~/.claude/sessions/` (live PID metadata). See the [full docs](claude-sessions/).

| Alias  | Command                  | Description |
|--------|--------------------------|-------------|
| `clsl` | `claude-sessions list`   | Lists sessions for the current cwd. Pass `-a` for every project, or `-c <path>` for a specific directory (mutually exclusive). |
| `clso` | `claude-sessions open`   | Arrow-key picker over the cwd's existing sessions plus a "start new" entry; auto-launches `<repo>/<branch>/s1` if no sessions exist yet. Pass `-n` to always start a new session, or `-r` to `claude --continue` the most recent (mutually exclusive). |
| `clsd` | `claude-sessions delete` | `-i <session-id>` to drop one transcript, `-c <cwd>` to drop the whole folder, `-f` to skip the confirmation. |

`clsl` color-codes the rows: grey = dead PID, red = live process with no transcript yet, orange = transcript with no recorded cwd (decoded from folder name), green = live `claude` process. Markers: `*` custom title, `↻` resumed session.

## Worktree helpers (`clg*`)

zsh functions that wrap `git worktree`, with the convention that worktrees live at `../<repo>-worktrees/<branch>`. Each command delegates session management to `claude-sessions`.

| Alias  | Command               | Description |
|--------|-----------------------|-------------|
| `clgn` | [new-gwt-claude](new-gwt-claude/)         | From a clean `main`, create a `<branch>` worktree at `../<repo>-worktrees/<branch>`, `cd` in, and run `claude-sessions open`. If run from inside a non-main worktree, hops to main first. |
| `clgs` | [switch-gwt-claude](switch-gwt-claude/)   | Arrow-key picker over all worktrees of the repo; `cd`s into the chosen one and runs `claude-sessions open`. |
| `clgd` | [delete-gwt-claude](delete-gwt-claude/)   | If you're inside a non-main worktree, deletes the current one. Otherwise picks from non-main worktrees. Force-removes the worktree, then `claude-sessions delete -c <path> -f` to drop the matching session folder. |
| `clgb` | [back-gwt-claude](back-gwt-claude/)       | `cd` to the base (main) worktree. No-op if you're already there. |

All four require the worktrees parent directory `../<repo>-worktrees/` to already exist (one-time `mkdir`).

## Layout

```
claude-helpers/
├── claude-helpers                  # entry point — source this
├── claude-sessions/                # Python CLI (claude-sessions + claude_store)
├── new-gwt-claude/
├── switch-gwt-claude/
├── delete-gwt-claude/
└── back-gwt-claude/
```

Each subdirectory has a README with full usage, controls, and prerequisites.

## Prerequisites

- zsh
- Python 3 (for `claude-sessions`)
- Claude Code CLI on `PATH` as `claude`
- Git
