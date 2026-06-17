# delete-gwt-claude

Interactively delete a git worktree.

## Usage

```sh
delete-gwt-claude
```

## Setup

Source the script in your `.zshrc` to use it as a shell function (required for `cd` to work in your current shell when deleting the current worktree):

```sh
source /path/to/delete-gwt-claude
```

## What it does

The behavior depends on where you run it from:

**Inside a non-main worktree:** Prompts to delete the current worktree. On confirmation, `cd`s back to the main worktree and removes the current one with `git worktree remove --force`.

**Inside the main worktree:** Lists all non-main worktrees in an interactive menu. On selection, prompts for confirmation and removes the chosen worktree with `git worktree remove --force`.

In both cases:
- The underlying branch is left intact — only the worktree directory is removed.
- The corresponding Claude Code session folder under `~/.claude/projects/<encoded-cwd>/` is also deleted, taking all transcripts for that worktree with it. The encoding maps `/` and `_` in the worktree path to `-` (the same scheme Claude Code uses).

## Controls

| Key | Action |
|-----|--------|
| Up / `k` | Move selection up |
| Down / `j` | Move selection down |
| Enter | Select worktree |
| `q` / Escape | Cancel |
| `y` | Confirm deletion (at the prompt) |
| anything else | Cancel deletion (at the prompt) |

## Prerequisites

- Must be inside a git repository (any worktree of it)
- zsh shell

## Notes

- Uses `--force`, so worktrees with uncommitted changes are removed without warning. Make sure work is committed or stashed first.
- The session folder deletion is also irreversible — all transcripts for the deleted worktree are gone. There's currently no flag to skip this.
- The main worktree is never offered as a deletion target.
