# claude-helpers

A small collection of zsh + Python helpers for managing git worktrees and Claude Code session transcripts.

## Setup

Source the entry-point file from your `.zshrc`:

```sh
source /path/to/claude-helpers/claude-helpers
```

This registers the worktree functions, wires up aliases for the standalone Python tools, and resolves all paths relative to the `claude-helpers` directory itself, so it works regardless of where you've placed it.

## Commands

| Alias | Command | Description |
|-------|---------|-------------|
| `clgn` | [new-gwt-claude](new-gwt-claude/) | Create a new git worktree from `main` and launch Claude Code in it. |
| `clgs` | [switch-gwt-claude](switch-gwt-claude/) | Interactively pick a worktree, `cd` into it, and resume (or start) a Claude session. |
| `clgd` | [delete-gwt-claude](delete-gwt-claude/) | Delete a worktree and its associated Claude session folder. |
| `clgb` | [back-gwt-claude](back-gwt-claude/) | `cd` to the base (main) worktree if currently inside a non-main worktree. |
| `clsl` | [claude-sessions list](claude-sessions/) | List all Claude Code sessions across projects, with PID / message count / preview. |
| `clso` | [claude-sessions open](claude-sessions/) | Resume an existing session for the cwd, or start a new one named `<repo>/<branch>/s…`. |
| `clsd` | [claude-sessions delete](claude-sessions/) | Delete Claude Code session transcripts by session ID or by working directory. |

### Worktree commands (`clg*`)

These wrap `git worktree` with the convention that worktrees live at `../<repo>-worktrees/<branch>` and each worktree gets its own named Claude session.

- `clgn <branch>` — must be on a clean `main`; creates the branch, the worktree, and runs `claude --name <branch>`.
- `clgs` — interactive picker (j/k/arrows, enter, q to quit). Prefers `claude --continue`; falls back to a fresh named session.
- `clgd` — if you're inside a non-main worktree, deletes the current one. Otherwise shows a picker of non-main worktrees. Force-removes the worktree and wipes the matching `~/.claude/projects/<encoded-cwd>/` folder.
- `clgb` — jump back to the base (main) worktree. No-op if you're already there.

### Session commands (`cls*`)

These operate on Claude Code's transcript store at `~/.claude/projects/`.

- `clsl` — by default, lists sessions for the current cwd. Pass `all` for every session across every project, or `-c <path>` to filter to a specific directory. Color-coded: green = active process, grey = dead PID, red = live process with no transcript yet. Markers: `*` custom title, `↻` resumed session.
- `clso` — arrow-key picker (`↑`/`↓` or `j`/`k`, enter, q/Esc to cancel) over the cwd's existing sessions, with a final "start new" entry; auto-launches `<repo>/<branch>/s1` if no sessions exist yet.
- `clsd -i <session-id>` — delete a single transcript `.jsonl`.
- `clsd -c <cwd>` — delete the entire encoded session folder for a working directory.
- Add `-f` to skip the confirmation prompt.

## Layout

```
claude-helpers/
├── claude-helpers                  # entry point — source this
├── new-gwt-claude/
├── switch-gwt-claude/
├── delete-gwt-claude/
├── back-gwt-claude/
└── claude-sessions/
```

Each subdirectory contains the script and (where applicable) a per-command `.md` with full usage, controls, and prerequisites.

## Prerequisites

- zsh
- Python 3 (for `clsl` and `clsd`)
- Claude Code CLI on `PATH` as `claude`
- Git
