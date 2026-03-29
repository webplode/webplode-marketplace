# bv CLI Complete Reference

## Overview

bv is a graph-aware triage engine for beads projects (`.beads/beads.jsonl`). It computes graph metrics deterministically for AI-powered issue prioritization.

**Critical:** Always use `--robot-*` flags. Bare `bv` launches an interactive TUI.

## Global Options

| Flag | Purpose |
|------|---------|
| `--format <json\|toon>` | Structured output format (env: `BV_OUTPUT_FORMAT`) |
| `--label <label>` | Scope analysis to label's subgraph |
| `--as-of <ref>` | View state at point in time (commit SHA, branch, tag, date) |
| `--recipe <name>` | Apply named recipe (triage, actionable, high-impact) |
| `--force-full-analysis` | Compute all metrics regardless of graph size |
| `--repo <prefix>` | Filter issues by repository prefix |
| `--workspace <file>` | Load from workspace config (.bv/workspace.yaml) |
| `--help` | Show help |
| `--version` | Show version |
| `--check-update` | Check for new version |
| `--update` | Update bv |
| `--rollback` | Rollback to previous version |

## Triage Commands

### `--robot-triage` (THE MEGA-COMMAND)
Returns unified triage: quick_ref, recommendations, quick_wins, blockers_to_clear, project_health, commands.

| Modifier | Purpose |
|----------|---------|
| `--robot-triage-by-track` | Group by parallel work streams |
| `--robot-triage-by-label` | Group by domain label |
| `--robot-by-assignee <name>` | Filter by assignee |
| `--robot-by-label <label>` | Filter by label |
| `--robot-max-results <N>` | Limit output count |
| `--robot-min-confidence <0-1>` | Filter by confidence |

### `--robot-next`
Minimal output: single top pick with claim command.

## Planning Commands

### `--robot-plan`
Dependency-respecting execution plan with parallel tracks.

### `--robot-priority`
Priority misalignment detection with confidence scores.

### `--robot-capacity`
Capacity simulation and completion projection.

| Modifier | Purpose |
|----------|---------|
| `--agents <N>` | Number of parallel agents (default: 1) |
| `--capacity-label <label>` | Filter by label |

### `--robot-forecast <id\|all>`
ETA predictions with dependency-aware scheduling.

| Modifier | Purpose |
|----------|---------|
| `--forecast-agents <N>` | Parallel agents for capacity (default: 1) |
| `--forecast-label <label>` | Filter by label |
| `--forecast-sprint <id>` | Filter by sprint |

## Graph Analysis Commands

### `--robot-insights`
Full graph metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core, articulation points, slack.

### `--robot-graph`
Dependency graph export.

| Modifier | Purpose |
|----------|---------|
| `--graph-format <json\|dot\|mermaid>` | Output format (default: json) |
| `--graph-root <id>` | Subgraph from specific root |
| `--graph-depth <N>` | Max depth (0 = unlimited) |
| `--graph-preset <compact\|roomy>` | Layout preset |
| `--graph-title <title>` | Custom title |

### `--robot-blocker-chain <id>`
Full blocker chain analysis for a specific issue.

### `--robot-impact-network [id]`
Impact network (empty for full graph, or specific bead ID).

| Modifier | Purpose |
|----------|---------|
| `--network-depth <1-3>` | Subnetwork depth (default: 2) |

### `--robot-causality <id>`
Causal chain analysis for a bead.

### `--robot-impact <paths>`
Analyze impact of modifying files (comma-separated paths).

## Label Analysis Commands

### `--robot-label-health`
Per-label health: health_level, velocity_score, staleness, blocked_count.

### `--robot-label-flow`
Cross-label dependency: flow_matrix, dependencies, bottleneck_labels.

### `--robot-label-attention`
Attention-ranked labels.

| Modifier | Purpose |
|----------|---------|
| `--attention-limit <N>` | Limit labels (default: 5) |

## History & File Commands

### `--robot-history`
Bead-to-commit correlations.

| Modifier | Purpose |
|----------|---------|
| `--history-limit <N>` | Max commits (default: 500, 0 = unlimited) |
| `--history-since <date\|ref>` | Limit to commits after date |

### `--robot-diff`
Changes since a reference point.

| Modifier | Purpose |
|----------|---------|
| `--diff-since <ref>` | Required: commit SHA, branch, tag, or date |

### `--robot-file-beads <path>`
Beads that touched a specific file.

| Modifier | Purpose |
|----------|---------|
| `--file-beads-limit <N>` | Max results (default: 20) |

### `--robot-file-hotspots`
Files touched by most beads.

| Modifier | Purpose |
|----------|---------|
| `--hotspots-limit <N>` | Max results (default: 10) |

### `--robot-file-relations <path>`
Files that frequently co-change with given file.

| Modifier | Purpose |
|----------|---------|
| `--relations-limit <N>` | Max results (default: 10) |
| `--relations-threshold <0-1>` | Min correlation (default: 0.5) |

## Sprint & Burndown Commands

### `--robot-burndown <sprint\|current>`
Sprint burndown with scope changes and at-risk items.

### `--robot-sprint-list`
All sprints as JSON.

### `--robot-sprint-show <id>`
Specific sprint details.

## Alert & Suggestion Commands

### `--robot-alerts`
Stale issues, blocking cascades, priority mismatches.

| Modifier | Purpose |
|----------|---------|
| `--alert-type <type>` | Filter by type (e.g., stale_issue) |
| `--alert-label <label>` | Filter by label |
| `--severity <info\|warning\|critical>` | Filter by severity |

### `--robot-suggest`
Smart suggestions: duplicates, dependencies, labels, cycles.

| Modifier | Purpose |
|----------|---------|
| `--suggest-type <type>` | Filter: duplicate, dependency, label, cycle |
| `--suggest-bead <id>` | Filter for specific bead |
| `--suggest-confidence <0-1>` | Min confidence |

### `--robot-orphans`
Orphan commit candidates (commits that should be linked but aren't).

| Modifier | Purpose |
|----------|---------|
| `--orphans-min-score <0-100>` | Min suspicion score (default: 30) |

## Search Commands

### `--robot-search`
Semantic search results (requires `--search` query).

| Modifier | Purpose |
|----------|---------|
| `--search <query>` | Search query |
| `--search-limit <N>` | Max results (default: 10) |
| `--search-mode <text\|hybrid>` | Ranking mode |
| `--search-weights <json>` | Custom hybrid weights |

### `--robot-related <id>`
Beads related to a specific bead.

| Modifier | Purpose |
|----------|---------|
| `--related-max-results <N>` | Max per category (default: 10) |
| `--related-min-relevance <0-100>` | Min relevance (default: 20) |
| `--related-include-closed` | Include closed beads |

## Correlation Feedback

### `--robot-confirm-correlation <SHA:beadID>`
Confirm a commit-bead correlation is correct.

### `--robot-reject-correlation <SHA:beadID>`
Reject an incorrect correlation.

### `--robot-explain-correlation <SHA:beadID>`
Explain why a commit is linked to a bead.

### `--robot-correlation-stats`
Correlation feedback statistics.

## Export Commands

| Command | Purpose |
|---------|---------|
| `--export-graph <file.html>` | Interactive HTML visualization |
| `--export-md <file.md>` | Markdown export |
| `--export-pages <dir>` | Static site |
| `--agent-brief <dir>` | Agent brief bundle |
| `--priority-brief <file.md>` | Priority brief |
| `--emit-script` | Shell script for top-N recommendations |

| Modifier | Purpose |
|----------|---------|
| `--script-format <bash\|fish\|zsh>` | Script format (default: bash) |
| `--script-limit <N>` | Items in script (default: 5) |

## Baseline & Drift

| Command | Purpose |
|---------|---------|
| `--save-baseline <desc>` | Save current metrics as baseline |
| `--check-drift` | Check drift (exit: 0=OK, 1=critical, 2=warning) |
| `--robot-drift` | Drift as JSON (use with `--check-drift`) |
| `--baseline-info` | Show baseline details |

## Documentation Commands

| Command | Purpose |
|---------|---------|
| `--robot-docs <topic>` | AI docs: guide, commands, examples, env, exit-codes, all |
| `--robot-help` | AI agent help summary |
| `--robot-schema` | JSON Schema for all robot commands |
| `--schema-command <cmd>` | Schema for specific command |
| `--robot-recipes` | Available recipes |
| `--robot-metrics` | Performance metrics (timing, cache, memory) |

## Diagnostic Commands

| Command | Purpose |
|---------|---------|
| `--profile-startup` | Startup timing profile |
| `--profile-json` | Profile in JSON format |
| `--debug-render <view>` | Render view to file (insights, board) |
| `--cpu-profile <file>` | CPU profile |

## Feedback Commands

| Command | Purpose |
|---------|---------|
| `--feedback-accept <id>` | Mark recommendation as good |
| `--feedback-ignore <id>` | Mark recommendation as not useful |
| `--feedback-show` | View current adjustments |
| `--feedback-reset` | Reset to defaults |

## History Commands

| Command | Purpose |
|---------|---------|
| `--bead-history <id>` | Show history for specific bead |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `BV_OUTPUT_FORMAT` | Default format (json or toon) |
| `TOON_DEFAULT_FORMAT` | Alternative format env var |
| `TOON_STATS` | Show token estimates on stderr |
| `BV_SEARCH_MODE` | Default search mode (text or hybrid) |
| `BV_SEARCH_PRESET` | Default hybrid preset |
