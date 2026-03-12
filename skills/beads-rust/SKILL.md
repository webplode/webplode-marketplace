---
name: beads-rust
description: Agent-first issue tracking with beads_rust (br CLI). Use when the user wants to manage tasks, track issues, plan work, query issue status, set up beads in a project, or coordinate agent workflows using the br issue tracker. Triggers on keywords like "beads", "br", "issue tracker", "track issue", "create issue", "ready issues", "blocked issues", or "beads rust".
---

# Beads Rust (br) -- Agent-First Issue Tracking

Manage local-first, git-friendly issue tracking using the `br` CLI (beads_rust). Beads externalizes task state into a persistent, git-versioned database so that progress, dependencies, and discovered issues survive across sessions and agents.

## Core Concepts

- **Bead**: an individual issue/task with ID, title, description, type, priority, status, dependencies, labels, and comments.
- **Storage**: SQLite (`.beads/beads.db`) for fast queries + JSONL (`.beads/issues.jsonl`) for git-friendly collaboration.
- **Non-invasive**: br never touches source code or runs git commands. It only writes to `.beads/`.
- **Agent-first**: every command supports `--json` output for programmatic use by AI agents.

## When to Use This Skill

- User asks to set up issue tracking in a project
- User wants to create, update, close, or query issues
- User needs to understand what work is ready, blocked, or stale
- User wants dependency-aware task planning
- User asks about beads, br, or issue tracking workflows
- Agent needs persistent task state across sessions

## Workflow Reference

See `references/cli-reference.md` for the complete command reference.
See `references/workflows.md` for common workflow patterns.

## Setup

Initialize beads in any project:

```bash
br init
br agents --add --force   # Add workflow instructions to AGENTS.md
```

## Essential Commands

### Issue Lifecycle

```bash
br create "Fix login timeout" -p 1 -t bug          # Create issue
br q "Quick task note"                               # Quick capture (ID only)
br show bd-abc123                                    # View details
br update bd-abc123 --claim                          # Claim (assign + in_progress)
br close bd-abc123 --reason "Fixed" --suggest-next   # Close + get next task
```

### Querying

```bash
br ready                        # Unblocked, open, not deferred
br ready --json                 # Structured output for agents
br blocked                      # What's waiting on dependencies
br stale --days 14              # Untouched for 14+ days
br list -s open -p 0 -p 1      # High-priority open issues
br search "authentication"     # Full-text search
br count --by-status            # Summary counts
br stats                        # Project overview
```

### Dependencies

```bash
br dep add bd-AUTH bd-SCHEMA    # AUTH depends on SCHEMA
br dep tree bd-AUTH             # Visualize dependency tree
br dep cycles                   # Detect circular dependencies
br graph --all                  # Full dependency graph
```

### Sync and Git Integration

```bash
br sync --flush-only            # Export DB to JSONL (for git commit)
br sync --import-only           # Import JSONL to DB (after git pull)
br sync --merge                 # 3-way merge (after merge conflicts)
br sync --status                # Check sync status
```

### Organization

```bash
br label add bd-123 -l "frontend"     # Add label
br label list-all                      # All labels with counts
br defer bd-123 --until "+7d"          # Defer for a week
br undefer bd-123                      # Make ready again
br comments add bd-123 "Progress note" # Add comment
```

## Agent Integration Rules

1. **Always use `--json`** when reading issue data programmatically.
2. **Claim before working**: `br update <id> --claim` sets assignee and status atomically.
3. **Close with reason**: `br close <id> --reason "description"` -- always explain what was done.
4. **Use `--suggest-next`** with close to get the next unblocked task.
5. **Sync before committing**: `br sync --flush-only` exports the DB state to JSONL for git.
6. **Sync after pulling**: `br sync --import-only` imports any JSONL changes from collaborators.
7. **Check ready first**: `br ready --json` shows only actionable work (open, unblocked, not deferred).
8. **Respect dependencies**: do not work on blocked issues; resolve blockers first.

## Priority Scale

| Value | Name | Meaning |
|-------|------|---------|
| 0 | P0 / Critical | Drop everything |
| 1 | P1 / High | Do next |
| 2 | P2 / Medium | Normal queue |
| 3 | P3 / Low | When time allows |
| 4 | P4 / Backlog | Someday/maybe |

## Issue Types

`task`, `bug`, `feature`, `epic`, `chore`, `spike`, `doc`

## Status Values

`open`, `in_progress`, `blocked`, `closed`, `deferred`, `draft`

## Output Modes

When presenting results to users:
- **Interactive**: use default text output with colors
- **Agent consumption**: use `--json` for structured data
- **Reports**: use `br stats`, `br count --by-*`, or `br changelog`
- **Dependency visualization**: use `br dep tree` or `br graph`

## Quality Checks

Before completing beads-related work:
- Verify the `.beads/` directory exists (run `br init` if not)
- Confirm sync status with `br sync --status`
- Check for dependency cycles with `br dep cycles`
- Run `br lint` to catch missing template sections
- Run `br doctor` if anything seems wrong
