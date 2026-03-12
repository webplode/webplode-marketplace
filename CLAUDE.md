# CLAUDE.md — Webplode Marketplace

## Beads (br) — Dependency-Aware Issue Tracking

Beads provides a lightweight, dependency-aware issue database and CLI (`br` - beads_rust) for selecting "ready work," setting priorities, and tracking status.

**Important:** `br` is non-invasive — it NEVER runs git commands automatically. You must manually commit changes after `br sync --flush-only`.

### Essential Commands

```bash
br ready              # Show issues ready to work (no blockers)
br list --status=open # All open issues
br show <id>          # Full issue details with dependencies
br create --title="..." --type=task --priority=2
br update <id> --claim  # Atomic: assign + set in_progress
br close <id> --reason "Completed" --suggest-next
br sync --flush-only  # Export to JSONL (NO git operations)
```

### Workflow Pattern

1. **Start**: Run `br ready` to find actionable work
2. **Claim**: Use `br update <id> --claim`
3. **Work**: Implement the task
4. **Complete**: Use `br close <id> --reason "..." --suggest-next`
5. **Sync**: Run `br sync --flush-only` then manually commit

### Key Concepts

- **Dependencies**: Issues can block other issues. `br ready` shows only unblocked work.
- **Priority**: P0=critical, P1=high, P2=medium, P3=low, P4=backlog (use numbers 0-4)
- **Types**: task, bug, feature, epic, chore, spike, doc
- **Status**: open, in_progress, blocked, closed, deferred, draft
- **Blocking**: `br dep add <issue> <depends-on>` to add dependencies
- **Agent output**: Always use `--json` for programmatic consumption

### Session Protocol

```bash
# Before ending any session:
git status              # Check what changed
git add <files>         # Stage code changes
br sync --flush-only    # Export beads to JSONL
git add .beads/         # Stage beads changes
git commit -m "..."     # Commit everything together
```

### Best Practices

- Check `br ready` at session start to find available work
- Update status as you work (claim → close)
- Create new issues with `br create` when you discover tasks
- Always `br sync --flush-only && git add .beads/` before ending session
- Use `br close <id> --suggest-next` to get the next unblocked task

---

## bv — Graph-Aware Triage Engine

bv is a graph-aware triage engine for beads projects. It computes PageRank, betweenness, critical path, cycles, HITS, eigenvector, and k-core metrics deterministically.

**Scope boundary:** bv handles *what to work on* (triage, priority, planning). For issue CRUD, use `br`. For agent coordination, use MCP Agent Mail.

**CRITICAL: Use ONLY `--robot-*` flags. Bare `bv` launches an interactive TUI that blocks your session.**

### The Entry Point: Start With Triage

```bash
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick + claim command
```

`--robot-triage` returns: `quick_ref`, `recommendations`, `quick_wins`, `blockers_to_clear`, `project_health`, `commands`.

### Command Reference

**Planning:**
| Command | Returns |
|---------|---------|
| `--robot-plan` | Parallel execution tracks with `unblocks` lists |
| `--robot-priority` | Priority misalignment detection with confidence |
| `--robot-capacity` | Capacity simulation and completion projection |
| `--robot-forecast <id\|all>` | ETA predictions with dependency-aware scheduling |

**Graph Analysis:**
| Command | Returns |
|---------|---------|
| `--robot-insights` | Full metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core |
| `--robot-graph` | Dependency graph as JSON/DOT/Mermaid |
| `--robot-blocker-chain <id>` | Full blocker chain for an issue |
| `--robot-impact-network [id]` | Impact network (empty=full, or specific ID) |

**Labels:**
| Command | Returns |
|---------|---------|
| `--robot-label-health` | Per-label health, velocity, staleness |
| `--robot-label-flow` | Cross-label dependency flow |
| `--robot-label-attention` | Attention-ranked labels |

**History:**
| Command | Returns |
|---------|---------|
| `--robot-history` | Bead-to-commit correlations |
| `--robot-diff --diff-since <ref>` | Changes since ref |
| `--robot-file-beads <path>` | Beads that touched a file |
| `--robot-file-hotspots` | Files touched by most beads |

**Alerts & Suggestions:**
| Command | Returns |
|---------|---------|
| `--robot-alerts` | Stale issues, blocking cascades, priority mismatches |
| `--robot-suggest` | Duplicates, missing deps, label suggestions, cycles |

### Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank
bv --robot-triage --robot-triage-by-track    # Group by parallel work streams
bv --robot-triage --robot-triage-by-label    # Group by domain
```

### jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.Cycles'                         # Circular deps (must fix!)
```

---

## UBS — Ultimate Bug Scanner

**Golden Rule:** `ubs <changed-files>` before every commit. Exit 0 = safe. Exit >0 = fix & re-run.

### Commands

```bash
ubs file.rs file2.rs                    # Specific files (fastest) — USE THIS
ubs $(git diff --name-only --cached)    # Staged files — before commit
ubs --only=rust,toml src/               # Language filter (3-5x faster)
ubs --ci --fail-on-warning .            # CI mode — strict
ubs .                                   # Whole project
```

### Output Formats

```bash
ubs .                        # Text (default)
ubs . --format=json          # Machine-readable JSON
ubs . --format=toon          # Token-Optimized (compact for agents)
ubs . --format=sarif         # SARIF (GitHub Code Scanning)
```

### Output Pattern

```
Warning Category (N errors)
    file.rs:42:5 — Issue description
    Suggested fix
Exit code: 1
```

Parse: `file:line:col` → location | suggested fix follows | Exit 0/1 → pass/fail

### Fix Workflow

1. Read finding → category + fix suggestion
2. Navigate `file:line:col` → view context
3. Verify real issue (not false positive)
4. Fix root cause (not symptom)
5. Re-run `ubs <file>` → exit 0
6. Commit

### Bug Severity

- **Critical (always fix):** Memory safety, use-after-free, data races, SQL injection
- **Important (production):** Unwrap panics, resource leaks, overflow checks
- **Contextual (judgment):** TODO/FIXME, println! debugging

### Reporting & Baselines

```bash
ubs . --html-report=report.html         # HTML report
ubs . --report-json=baseline.json       # Save baseline
ubs . --comparison=baseline.json        # Regression detection
```

### Maintenance

```bash
ubs doctor              # Audit environment
ubs doctor --fix        # Fix missing/corrupt modules
ubs --update            # Update ubs
```

---

## Integrated Workflow: br + bv + ubs

### Session Start

```bash
br sync --import-only        # Import any JSONL changes from git
bv --robot-triage            # Understand the landscape
br ready                     # See what's actionable
```

### Working on a Task

```bash
br update <id> --claim       # Claim the task
# ... implement changes ...
ubs $(git diff --name-only)  # Scan changed files
br close <id> --reason "..." --suggest-next  # Complete + get next
```

### Session End

```bash
ubs $(git diff --name-only --cached)  # Final quality check
br sync --flush-only                   # Export beads to JSONL
git add .beads/ <changed-files>        # Stage everything
git commit -m "..."                    # Commit
```

### Triage-Driven Development

```bash
bv --robot-triage | jq '.recommendations[0]'  # Get top pick
br update <id> --claim                          # Claim it
# ... work ...
ubs <changed-files>                             # Quality gate
br close <id> --reason "..." --suggest-next     # Complete
bv --robot-triage                               # Re-triage
```
