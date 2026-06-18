# new-gwt-claude

Create a git worktree and start Claude Code in the current tab.

## Usage

```sh
new-gwt-claude <branch_name>
```

## Setup

Source the script in your `.zshrc` to use it as a shell function (so your shell stays in the new worktree after Claude exits):

```sh
source /path/to/new-gwt-claude
```

It also works when executed directly — Claude runs in the worktree, but your shell returns to its original directory after Claude exits.

## What it does

1. **Validates** the environment:
   - Must be inside a git repository
   - If run from a non-main worktree, automatically `cd`s to the main worktree first
   - The main worktree must be on the `main` branch
   - The specified branch must not already exist
   - Working tree must be clean (no staged or unstaged changes)
   - The worktrees parent directory (`../<repo>-worktrees/`) must already exist

2. **Creates a git worktree** at `../<repo>-worktrees/<branch_name>` with a new branch of the given name.

3. **`cd`s into the worktree** and runs `claude` in the current tab.

## Prerequisites

- Git repository with a clean `main` branch checked out
- A pre-existing worktrees directory at `../<repo-name>-worktrees/`
- Claude Code CLI installed and available as `claude`
- zsh shell

## Example

```sh
# From ~/projects/my-app on main:
mkdir -p ../my-app-worktrees   # one-time setup
new-gwt-claude feature/add-login
# -> creates worktree at ../my-app-worktrees/feature/add-login
# -> cds into it and runs claude in the current tab
```

## Exit codes

| Code | Reason |
|------|--------|
| 1 | Missing argument, not in a git repo, not on main, branch exists, dirty tree, or worktrees directory missing |
