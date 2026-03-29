# Beads Rust Workflow Patterns

## Project Setup

```bash
# Initialize beads in a project
br init

# Add agent workflow instructions to AGENTS.md
br agents --add --force

# Generate shell completions
br completions zsh -o ~/.zfunc
```

## Solo Developer Workflow

```bash
# Morning: check what's ready
br ready
br stats

# Pick a task and claim it
br update bd-abc123 --claim

# Work on it... then close
br close bd-abc123 --reason "Implemented auth flow" --suggest-next

# End of session: export for git
br sync --flush-only
git add .beads/ && git commit -m "Update issue state"
```

## Agent Session Workflow

```bash
# Session start: import latest state
br sync --import-only

# Find actionable work
br ready --json

# Claim a task (atomic assign + in_progress)
br update bd-abc123 --claim --json

# Add progress notes
br comments add bd-abc123 "Started refactoring auth module"

# Complete the task
br close bd-abc123 --reason "Refactored auth module, all tests passing" --suggest-next --json

# Session end: export state
br sync --flush-only
```

## Planning and Decomposition

```bash
# Create an epic
br create "User Authentication System" -t epic -p 1

# Create child tasks
br create "Design auth schema" -t task -p 1 --parent bd-EPIC
br create "Implement JWT tokens" -t task -p 1 --parent bd-EPIC
br create "Add login endpoint" -t task -p 1 --parent bd-EPIC
br create "Add registration endpoint" -t task -p 2 --parent bd-EPIC

# Set up dependencies (login depends on JWT, JWT depends on schema)
br dep add bd-LOGIN bd-JWT
br dep add bd-JWT bd-SCHEMA

# Verify the plan
br dep tree bd-EPIC
br ready  # Should show only bd-SCHEMA (the unblocked root)
```

## Triage and Prioritization

```bash
# See everything open
br list -s open --long

# Check high-priority items
br list -p 0 -p 1

# Find stale issues
br stale --days 14

# Find overdue issues
br list --overdue

# Defer non-urgent work
br defer bd-123 bd-456 --until "+14d"

# Bulk label for sprint
br label add bd-123 bd-456 bd-789 -l "sprint-42"
```

## Dependency Management

```bash
# Add a blocking dependency
br dep add bd-FEATURE bd-PREREQ -t blocks

# Add a related (non-blocking) link
br dep add bd-FEATURE bd-RELATED -t related

# View what blocks an issue
br dep list bd-FEATURE --direction down

# View what an issue blocks
br dep list bd-PREREQ --direction up

# Visualize the full graph
br graph --all

# Check for circular dependencies
br dep cycles
```

## Multi-Agent Coordination

```bash
# Agent A claims work
br update bd-task1 --claim --actor "agent-a" --json

# Agent B checks what's available (excludes agent-a's claimed work)
br ready --unassigned --json

# Agent B claims different work
br update bd-task2 --claim --actor "agent-b" --json

# After both finish, sync for merge
br sync --flush-only
```

## Git Collaboration

```bash
# Before pushing: export DB state
br sync --flush-only
git add .beads/
git commit -m "Update issue state"
git push

# After pulling: import collaborator changes
git pull
br sync --import-only

# After merge conflicts in .beads/issues.jsonl
br sync --merge

# Check sync health
br sync --status
```

## Reporting

```bash
# Project overview
br stats

# Breakdown by type/priority/assignee
br stats --by-type --by-priority --by-assignee

# Count open issues by label
br count --by-label

# Generate changelog since last release
br changelog --since-tag v1.2.0

# Find orphaned issues (referenced in commits but still open)
br orphans
```

## Saved Queries

```bash
# Save a frequently-used filter
br query save "my-bugs" -d "My open bugs" --assignee me -t bug -s open

# Run it later
br query run "my-bugs"

# List saved queries
br query list
```

## Maintenance

```bash
# Run diagnostics
br doctor

# Repair if needed
br doctor --repair

# Check for missing template sections
br lint

# Prune old history backups
br history prune --keep 50

# Upgrade br itself
br upgrade --check
br upgrade
```

## Claude Code Hook Integration

Add to `.claude/settings.json` for automatic session management:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "br sync --import-only --quiet 2>/dev/null || true"
      }
    ],
    "PreCompact": [
      {
        "command": "br sync --flush-only --quiet 2>/dev/null || true"
      }
    ]
  }
}
```

This ensures:
- **SessionStart**: imports any JSONL changes from git (collaborator updates)
- **PreCompact**: exports DB state before context compaction (preserves work)
