# Webplode Marketplace

A Claude Code plugin marketplace with curated skills for AI-powered workflows.

## Installation

```bash
claude plugin add /path/to/webplode-marketplace
```

## Skills

### prompt-leverage

Strengthen a raw user prompt into an execution-ready instruction set. Automatically detects task type (coding, research, writing, review, planning, analysis), infers intensity level, and adds structured scaffolding for better execution.

**Usage:**

Invoke as a skill in Claude Code:
```
/webplode-marketplace:prompt-leverage
```

Or use the Python script directly:
```bash
python skills/prompt-leverage/scripts/augment_prompt.py "your raw prompt here"
```

**Framework blocks applied selectively:**
- Objective, Context, Work Style, Tool Rules, Output Contract, Verification, Done Criteria

**Output modes:**
- Inline upgrade, Upgrade + rationale, Template extraction, Hook spec

### beads-rust

Agent-first issue tracking with the `br` CLI (beads_rust). Manage local-first, git-friendly issues, dependencies, and task workflows directly from Claude Code.

**Usage:**
```
/webplode-marketplace:beads-rust
```

**Key capabilities:**
- Initialize and manage beads workspaces (`br init`, `br create`, `br close`)
- Query actionable work (`br ready`), blocked issues (`br blocked`), and stale tasks (`br stale`)
- Dependency-aware planning with `br dep` and `br graph`
- Git-friendly sync with `br sync --flush-only` / `--import-only`
- Full CLI reference and workflow patterns included

### beads-viewer

Graph-aware triage engine for beads projects using the `bv` CLI. Computes PageRank, betweenness, critical path, and other graph metrics to help decide what to work on next.

**Usage:**
```
/webplode-marketplace:beads-viewer
```

**Key capabilities:**
- Unified triage with `bv --robot-triage` (the mega-command)
- Dependency-respecting execution plans with `--robot-plan`
- Priority misalignment detection, sprint burndowns, ETA forecasts
- Label health, cross-label flow, and attention analysis
- Alerts, suggestions, and baseline drift detection
- Full CLI reference with all `--robot-*` commands

### ultra-bug-scanner

Static analysis meta-runner that catches 1000+ bug patterns across 8+ languages before they reach production.

**Usage:**
```
/webplode-marketplace:ultra-bug-scanner
```

**Key capabilities:**
- 4-layer analysis: lexical, syntactic (AST), semantic, and heuristic
- Supports JS/TS, Python, Go, C/C++, Rust, Java, Ruby, Swift
- Multiple output formats: text, JSON, SARIF, TOON, JSONL
- CI integration with `--ci --fail-on-warning`
- Baseline comparison for regression detection
- Pre-commit quality gate: `ubs $(git diff --name-only --cached)`

## License

MIT
