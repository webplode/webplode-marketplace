# Webplode Marketplace

A Claude Code plugin marketplace with curated skills for AI-powered workflows.

## Installation

### Add the marketplace

```shell
/plugin marketplace add webplode/webplode-marketplace
```

### Install plugins

```shell
/plugin install webplode@webplode-marketplace    # Core tools (beads, triage, scanner, prompt-leverage)
/plugin install khuym@webplode-marketplace        # Multi-agent coordination skills
```

### Browse available plugins

Run `/plugin` in Claude Code and go to the **Discover** tab to see all available skills.

After installing, run `/reload-plugins` to activate.

## Plugins

### Webplode

Original skills built by the Webplode team.

#### prompt-leverage

Strengthen a raw user prompt into an execution-ready instruction set. Automatically detects task type (coding, research, writing, review, planning, analysis), infers intensity level, and adds structured scaffolding for better execution.

**Usage:**

Invoke as a skill in Claude Code:
```
/webplode:prompt-leverage
```

Or use the Python script directly:
```bash
python plugins/webplode/skills/prompt-leverage/scripts/augment_prompt.py "your raw prompt here"
```

**Framework blocks applied selectively:**
- Objective, Context, Work Style, Tool Rules, Output Contract, Verification, Done Criteria

**Output modes:**
- Inline upgrade, Upgrade + rationale, Template extraction, Hook spec

#### beads-rust

Agent-first issue tracking with the `br` CLI (beads_rust). Manage local-first, git-friendly issues, dependencies, and task workflows directly from Claude Code.

**Usage:**
```
/webplode:beads-rust
```

**Key capabilities:**
- Initialize and manage beads workspaces (`br init`, `br create`, `br close`)
- Query actionable work (`br ready`), blocked issues (`br blocked`), and stale tasks (`br stale`)
- Dependency-aware planning with `br dep` and `br graph`
- Git-friendly sync with `br sync --flush-only` / `--import-only`
- Full CLI reference and workflow patterns included

#### beads-viewer

Graph-aware triage engine for beads projects using the `bv` CLI. Computes PageRank, betweenness, critical path, and other graph metrics to help decide what to work on next.

**Usage:**
```
/webplode:beads-viewer
```

**Key capabilities:**
- Unified triage with `bv --robot-triage` (the mega-command)
- Dependency-respecting execution plans with `--robot-plan`
- Priority misalignment detection, sprint burndowns, ETA forecasts
- Label health, cross-label flow, and attention analysis
- Alerts, suggestions, and baseline drift detection

#### ultra-bug-scanner

Static analysis meta-runner that catches 1000+ bug patterns across 8+ languages before they reach production.

**Usage:**
```
/webplode:ultra-bug-scanner
```

**Key capabilities:**
- 4-layer analysis: lexical, syntactic (AST), semantic, and heuristic
- Supports JS/TS, Python, Go, C/C++, Rust, Java, Ruby, Swift
- Multiple output formats: text, JSON, SARIF, TOON, JSONL
- CI integration with `--ci --fail-on-warning`
- Baseline comparison for regression detection
- Pre-commit quality gate: `ubs $(git diff --name-only --cached)`

---

### Khuym (v2.2.1)

**Author:** [hoangnb24](https://github.com/hoangnb24) ([source repository](https://github.com/hoangnb24/skills))
**License:** MIT

Khuym is a validate-first, multi-agent coordination skill suite for agentic software delivery. It provides a complete workflow pipeline — from feature exploration through planning, validation, parallel execution, review, and learning capture. All Khuym skills are authored by **hoangnb24** and ported into this marketplace with full attribution.

#### Workflow Skills (run in order)

| Skill | Description |
|-------|-------------|
| `using-khuym` | Bootstrap meta-skill. Load first on any khuym project. Routes to the right skill, supports go-mode (full-auto) and quick-mode. |
| `exploring` | Socratic dialogue to extract locked decisions from the user BEFORE research or planning begins. |
| `gkg` | Codebase intelligence — architecture snapshots, dependency graphs, module relationships. |
| `planning` | Research, synthesize, and decompose features into executable beads with risk maps. |
| `validating` | Critical gate between planning and execution. Verifies plan soundness across 8 dimensions. |
| `swarming` | Orchestrates parallel worker agents for feature execution with file reservation and conflict handling. |
| `executing` | Per-agent worker loop (Flywheel). Register, claim bead, reserve files, implement, verify, close, report. |
| `reviewing` | Post-execution quality verification. 5 parallel specialist reviewers, 3-level artifact checks, UAT. |
| `compounding` | Captures learnings from completed work to make future work easier. |

#### Standalone Skills

| Skill | Description |
|-------|-------------|
| `debugging` | Systematic debugging for blocked workers, test failures, build errors, and runtime crashes. |
| `dream` | Dream-style consolidation pass over artifacts and learnings with ambiguity resolution. |
| `prompt-leverage` | Strengthen raw prompts into execution-ready instruction sets for AI agents. |
| `book-sft-pipeline` | Fine-tuning pipeline for books — ePub extraction, SFT dataset creation, style transfer, LoRA training. |
| `writing-khuym-skills` | Meta-skill for creating and pressure-testing new khuym skills. |

**Usage:**
```
/khuym:using-khuym          # Start here — routes to the right skill
/khuym:exploring             # Begin feature exploration
/khuym:planning              # Decompose into executable plan
/khuym:swarming              # Parallel execution
```

## License

MIT
