# delete-claude-sessions

Delete Claude Code session transcripts — either a single session by ID, or every session for a given working directory.

## Usage

```sh
delete-claude-sessions -i <session-id>
delete-claude-sessions -c <cwd-path>
```

Aliased as `clsd` once `~/bash_scripts/claude-helpers` is sourced.

## Options

| Flag | Description |
|------|-------------|
| `-i`, `--id <UUID>` | Delete the transcript `.jsonl` for this session ID. Searches across all `~/.claude/projects/*/`. |
| `-c`, `--cwd <PATH>` | Delete the entire `~/.claude/projects/<encoded-cwd>/` folder for this directory. The path is encoded the same way Claude Code does (slashes and underscores both become dashes). |
| `-f`, `--force` | Skip the confirmation prompt. |
| `-h`, `--help` | Show usage. |

`-i` and `-c` are mutually exclusive; one is required.

## Behavior

- Prompts `[y/N]` before deleting unless `-f` is passed.
- Exits with code `1` and an `Error:` message on stderr if:
  - The session ID has no matching transcript.
  - The cwd has no encoded folder under `~/.claude/projects/`.
  - The encoded folder exists but contains no `.jsonl` files.
- Only touches transcript files / folders. Does **not** clean up related state in `~/.claude/sessions/`, `~/.claude/session-env/`, `~/.claude/file-history/`, or `~/.claude/jobs/`.

## Examples

```sh
# Delete one session
clsd -i 23b2bb41-f162-49d6-a1b8-9b0cdd5e2816

# Delete all sessions for a directory
clsd -c ~/repos/foo
clsd -c .

# Skip confirmation
clsd -f -c ~/repos/old-project
```

## Prerequisites

- Python 3
- A populated `~/.claude/projects/` from prior Claude Code use
