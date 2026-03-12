---
name: beads-viewer
description: Graph-aware triage and analysis engine for beads projects using bv CLI. Use when the user wants to triage issues, analyze dependency graphs, get priority recommendations, plan execution order, check project health, run sprint burndowns, forecast ETAs, or get AI-powered issue insights. Triggers on keywords like "bv", "beads viewer", "triage", "priority analysis", "dependency graph", "project health", "burndown", "forecast", "what should I work on".
---

# Beads Viewer (bv) -- Graph-Aware Triage Engine

bv is a graph-aware triage engine for beads projects. It computes PageRank, betweenness, critical path, cycles, HITS, eigenvector, and k-core metrics deterministically to help you decide *what to work on next*.

**Scope boundary:** bv handles *what to work on* (triage, priority, planning). For issue CRUD operations, use `br` (beads-rust skill). For agent-to-agent coordination, use MCP Agent Mail.

## Critical Rule

**ALWAYS use `--robot-*` flags for programmatic access. Bare `bv` launches an interactive TUI that blocks the session.**

## When to Use This Skill

- User asks "what should I work on next?"
- User wants project health analysis or triage recommendations
- User needs dependency graph visualization or analysis
- User wants sprint burndown or ETA forecasting
- User asks about blocked issues, bottlenecks, or critical paths
- User wants to understand priority misalignments
- User needs label health or cross-label flow analysis

## The Entry Point: Start With Triage

`bv --robot-triage` is the single mega-command. It returns:
- `quick_ref`: at-a-glance counts + top 3 picks
- `recommendations`: ranked actionable items with scores, reasons, unblock info
- `quick_wins`: low-effort high-impact items
- `blockers_to_clear`: items that unblock the most downstream work
- `project_health`: status/type/priority distributions, graph metrics
- `commands`: copy-paste shell commands for next steps

```bash
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick + claim command
```

## Command Reference

### Planning

| Command | Returns |
|---------|---------|
| `--robot-plan` | Parallel execution tracks with `unblocks` lists |
| `--robot-priority` | Priority misalignment detection with confidence |
| `--robot-capacity` | Capacity simulation and completion projection |
| `--robot-forecast <id\|all>` | ETA predictions with dependency-aware scheduling |

### Graph Analysis

| Command | Returns |
|---------|---------|
| `--robot-insights` | Full metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core, articulation points, slack |
| `--robot-graph` | Dependency graph as JSON/DOT/Mermaid |
| `--robot-blocker-chain <id>` | Full blocker chain analysis for an issue |
| `--robot-impact-network [id]` | Bead impact network (empty for full, or specific ID) |
| `--robot-causality <id>` | Causal chain analysis for a bead |

### Label Analysis

| Command | Returns |
|---------|---------|
| `--robot-label-health` | Per-label: `health_level`, `velocity_score`, `staleness`, `blocked_count` |
| `--robot-label-flow` | Cross-label dependency: `flow_matrix`, `dependencies`, `bottleneck_labels` |
| `--robot-label-attention [--attention-limit=N]` | Attention-ranked labels |

### History & Change Tracking

| Command | Returns |
|---------|---------|
| `--robot-history` | Bead-to-commit correlations |
| `--robot-diff --diff-since <ref>` | Changes since ref: new/closed/modified issues, cycles |
| `--robot-file-beads <path>` | Beads that touched a file |
| `--robot-file-hotspots` | Files touched by most beads |
| `--robot-file-relations <path>` | Files that frequently co-change |

### Sprint & Forecasting

| Command | Returns |
|---------|---------|
| `--robot-burndown <sprint\|current>` | Sprint burndown, scope changes, at-risk items |
| `--robot-sprint-list` | All sprints as JSON |
| `--robot-sprint-show <id>` | Specific sprint details |

### Alerts & Suggestions

| Command | Returns |
|---------|---------|
| `--robot-alerts` | Stale issues, blocking cascades, priority mismatches |
| `--robot-suggest` | Hygiene: duplicates, missing deps, label suggestions, cycles |
| `--robot-orphans` | Commit-to-bead orphan candidates |

### Search

| Command | Returns |
|---------|---------|
| `--robot-search --search "<query>"` | Semantic search results |
| `--robot-related <id>` | Beads related to a specific bead |

### Export & Visualization

| Command | Returns |
|---------|---------|
| `--export-graph <file.html>` | Interactive HTML dependency visualization |
| `--export-md <file.md>` | Issues exported to Markdown |
| `--export-pages <dir>` | Static site for sharing |
| `--agent-brief <dir>` | Agent brief bundle (triage.json, insights.json, brief.md, helpers.md) |
| `--priority-brief <file.md>` | Priority brief to Markdown |

### Documentation

| Command | Returns |
|---------|---------|
| `--robot-docs guide` | Full usage guide for AI agents |
| `--robot-docs commands` | All commands reference |
| `--robot-docs examples` | Usage examples |
| `--robot-docs env` | Environment variables |
| `--robot-docs exit-codes` | Exit code meanings |
| `--robot-help` | AI agent help summary |
| `--robot-schema` | JSON Schema for all robot commands |

## Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank
bv --robot-triage --robot-triage-by-track    # Group by parallel work streams
bv --robot-triage --robot-triage-by-label    # Group by domain
bv --robot-by-assignee "agent-a"             # Filter by assignee
bv --robot-by-label "frontend"               # Filter by label
```

## Understanding Robot Output

All robot JSON includes:
- `data_hash` -- fingerprint of source beads.jsonl
- `status` -- per-metric state: `computed|approx|timeout|skipped` + elapsed ms
- `as_of` / `as_of_commit` -- present when using `--as-of`

Two-phase analysis:
- **Phase 1 (instant):** degree, topo sort, density
- **Phase 2 (async, 500ms timeout):** PageRank, betweenness, HITS, eigenvector, cycles

## Output Formats

```bash
bv --robot-triage --format json    # JSON (default)
bv --robot-triage --format toon    # Token-Optimized Output Notation (compact for agents)
```

Environment variables: `BV_OUTPUT_FORMAT`, `TOON_DEFAULT_FORMAT`

## jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-triage | jq '.quick_wins'                       # Low-effort high-impact
bv --robot-triage | jq '.blockers_to_clear'                # Unblock most work
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.status'                         # Check metric readiness
bv --robot-insights | jq '.Cycles'                         # Circular deps (must fix!)
```

## Feedback Loop

bv supports recommendation tuning:
```bash
bv --feedback-accept <id>     # Tune weights: this was a good recommendation
bv --feedback-ignore <id>     # Tune weights: this was not useful
bv --feedback-show            # View current weight adjustments
bv --feedback-reset           # Reset to defaults
```

## Baseline & Drift Detection

```bash
bv --save-baseline "sprint-42 start"   # Save current metrics
bv --check-drift                       # Check for drift (exit 0=OK, 1=critical, 2=warning)
bv --robot-drift --check-drift         # Drift as JSON
bv --baseline-info                     # Show baseline details
```

## Typical Agent Workflow

1. **Triage:** `bv --robot-triage` to understand the landscape
2. **Pick:** Use `recommendations[0]` or `bv --robot-next` for top pick
3. **Plan:** `bv --robot-plan` for parallel execution tracks
4. **Claim:** `br update <id> --claim` (via beads-rust)
5. **Work:** Implement the task
6. **Close:** `br close <id> --reason "..." --suggest-next`
7. **Re-triage:** `bv --robot-triage` to update priorities
