# back-gwt-claude

`cd` to the base (main) git worktree if you're currently inside a non-main worktree. No-op if you're already there.

Aliased as `clgb` once `claude-helpers` is sourced.

## Usage

```sh
back-gwt-claude
# or
clgb
```

## Setup

Source the script in your `.zshrc` so that `cd` takes effect in your current shell:

```sh
source /path/to/back-gwt-claude
```

It's sourced automatically when you source the top-level `claude-helpers` file.

## What it does

1. Confirms you're inside a git repository.
2. Resolves the main worktree path with `git worktree list --porcelain | head -1`.
3. If the current worktree's top level matches that path, returns silently.
4. Otherwise, `cd`s to the main worktree.

## Prerequisites

- Must be inside a git repository (any worktree of it)
- zsh shell (must be sourced as a function for `cd` to affect the parent shell)

## Exit codes

| Code | Reason |
|------|--------|
| 0 | Already at the base worktree, or `cd` to base succeeded |
| 1 | Not inside a git repository |
