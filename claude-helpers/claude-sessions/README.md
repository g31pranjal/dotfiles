# claude-sessions

List, open, or delete Claude Code session transcripts. Combines `clsl`, `clso`, and `clsd` under one subcommand-style CLI.

## Usage

```sh
claude-sessions list                     # sessions for current cwd
claude-sessions list all                 # every session, every project
claude-sessions list -c <cwd-path>       # sessions for a specific path
claude-sessions open                     # resume or start a session for the cwd
claude-sessions delete -i <session-id>
claude-sessions delete -c <cwd-path>
```

Aliased once `claude-helpers` is sourced:

| Alias  | Equivalent               |
| ------ | ------------------------ |
| `clsl` | `claude-sessions list`   |
| `clso` | `claude-sessions open`   |
| `clsd` | `claude-sessions delete` |

## Subcommands

### `list`

Walks `~/.claude/projects/` and prints one row per session, most recent first.

By default, only sessions whose cwd matches the **current directory** are shown. Pass `all` as a positional to show every session across every project, or `-c <path>` to filter to a specific directory (the path is normalized to absolute before matching).

```
TIME              SESSION                               PID    MSGS  CWD             TITLE / PREVIEW
----------------------------------------------------------------------------------------------------
2026-06-17 16:42  23b2bb41-f162-49d6-a1b8-9b0cdd5e2816  73214    18  ~/repos/foo     *  refactor auth
2026-06-17 12:01  9af0c2…                                          7  ~/repos/foo     ↻  pick up where we left off
```

**Columns:** `TIME` (last activity, local tz), `SESSION` (UUID), `PID` (live process for the session, blank otherwise; one extra row per additional registered PID), `MSGS` (user + assistant record count), `CWD` (with `~` collapsed), `TITLE / PREVIEW` (custom title or first non-synthetic prompt).

**Markers:** `*` custom title, `↻` resumed session.

**Colors** (TTY only): green = live `claude` process, grey = dead/recycled PID, red = live process with no transcript yet.

### `open`

Resume a session for the current directory, or start a new one. Names the session after the repo and current branch.

- **No existing sessions** for the cwd → launches `claude --name <repo>/<branch>/s1`.
- **One or more existing sessions** → opens an arrow-key picker:
  - Existing sessions appear first (most recent at the top).
  - The last entry is `start new: <repo>/<branch>/s<5-digit-random>`.
  - Navigate with `↑`/`↓` or `j`/`k`, `Enter` to select, `q` or `Esc` to cancel.
  - Picking an existing session runs `claude --resume <id>`; picking the new entry runs `claude --name <repo>/<branch>/s<random>`.

Where:
- `<repo>` = basename of the repo's main worktree.
- `<branch>` = `git branch --show-current`.

Errors out if not inside a git repository, if HEAD is detached, or if stdin/stdout isn't a TTY.

### `delete`

Delete transcripts in one of two modes (mutually exclusive, one required):

| Flag                 | Description                                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `-i`, `--id <UUID>`  | Delete the `.jsonl` for this session ID (searches across all `~/.claude/projects/*/`).                                                     |
| `-c`, `--cwd <PATH>` | Delete the entire `~/.claude/projects/<encoded-cwd>/` folder. The path is encoded with `/` and `_` both becoming `-` (Claude Code's scheme). |
| `-f`, `--force`      | Skip the `[y/N]` confirmation.                                                                                                             |

Exits `1` with an `Error:` message on stderr if the session ID has no match, the cwd has no encoded folder, or the folder contains no `.jsonl` files.

Only touches transcript files / folders — does **not** clean up `~/.claude/sessions/`, `~/.claude/session-env/`, `~/.claude/file-history/`, or `~/.claude/jobs/`.

## Examples

```sh
# List
clsl                         # current cwd only
clsl all                     # every session, every project
clsl -c ~/repos/foo          # specific directory

# Open
clso                         # picker (or auto-new if no sessions yet)

# Delete one session
clsd -i 23b2bb41-f162-49d6-a1b8-9b0cdd5e2816

# Delete every session for a directory
clsd -c .
clsd -c ~/repos/old-project

# Skip confirmation
clsd -f -c ~/repos/old-project
```

## Prerequisites

- Python 3
- A populated `~/.claude/projects/` from prior Claude Code use
- Git (for `open`)
- Claude Code CLI on `PATH` as `claude` (for `open`)
