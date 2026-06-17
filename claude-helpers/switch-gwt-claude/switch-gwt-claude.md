# switch-gwt-claude

Interactively select a git worktree and launch or resume a Claude Code session in it.

## Usage

```sh
switch-gwt-claude
```

## Setup

Source the script in your `.zshrc` to use it as a shell function (required for `cd` to work in your current shell):

```sh
source /path/to/switch-gwt-claude
```

Or add the `bash_scripts` directory to your fpath/path and source it.

## What it does

1. Lists all git worktrees for the current repository.
2. Presents an interactive menu with arrow key / vim-style navigation.
3. On selection, `cd`s into the chosen worktree.
4. Resumes the most recent Claude session if one exists, otherwise starts a new session.

## Controls

| Key | Action |
|-----|--------|
| Up / `k` | Move selection up |
| Down / `j` | Move selection down |
| Enter | Select worktree |
| `q` / Escape | Cancel |

## Prerequisites

- Must be inside a git repository (any worktree of it)
- Claude Code CLI installed and available as `claude`
- zsh shell
