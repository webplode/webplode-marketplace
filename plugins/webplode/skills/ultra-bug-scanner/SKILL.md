---
name: ultra-bug-scanner
description: Static analysis meta-runner that catches 1000+ bug patterns across 8+ languages before they reach production. Use when the user wants to scan code for bugs, run static analysis, check code quality before committing, set up CI quality gates, or detect security vulnerabilities. Triggers on keywords like "ubs", "bug scanner", "static analysis", "scan for bugs", "code quality", "lint", "security scan", "pre-commit check".
---

# Ultimate Bug Scanner (ubs) -- Static Analysis Meta-Runner

ubs is an industrial-grade static analysis meta-runner that catches 1000+ bug patterns across 8+ programming languages. It auto-detects languages, fans out to per-language scanner modules concurrently, and merges results into a unified report.

**Golden Rule:** `ubs <changed-files>` before every commit. Exit 0 = safe. Exit >0 = fix & re-run.

## When to Use This Skill

- User wants to scan code for bugs before committing
- User asks about static analysis or code quality
- User wants to set up CI quality gates
- User needs security vulnerability scanning
- User asks to check for common bug patterns
- User wants pre-commit quality checks

## 4-Layer Analysis Engine

1. **Lexical analysis** -- pattern/regex-based checks
2. **Syntactic analysis** -- AST-powered detection via ast-grep
3. **Semantic validation** -- scope-aware, type-narrowing, resource lifecycle
4. **Heuristic behavioral** -- cross-language async errors, concurrency bugs

## Essential Commands

```bash
# Scan specific files (fastest -- USE THIS)
ubs file.rs file2.rs

# Scan staged files before commit
ubs $(git diff --name-only --cached)

# Scan with language filter (3-5x faster)
ubs --only=rust,toml src/

# CI mode -- strict, fail on warnings
ubs --ci --fail-on-warning .

# Scan entire project
ubs .
```

## Output Formats

```bash
ubs .                        # Text (default, human-readable)
ubs . --format=json          # Machine-readable JSON
ubs . --format=toon          # Token-Optimized (compact for AI agents)
ubs . --format=sarif         # SARIF (GitHub Code Scanning compatible)
ubs . --format=jsonl         # JSON Lines (streaming)
```

## Reporting & Baselines

```bash
# Generate HTML report
ubs . --html-report=report.html

# Generate enriched JSON summary
ubs . --report-json=summary.json

# Compare against baseline (regression detection)
ubs . --comparison=baseline.json

# Output in beads JSONL format
ubs . --beads-jsonl
```

## Profiles

| Profile | Use Case |
|---------|----------|
| `--profile=strict` | Production: fail on warnings |
| `--profile=loose` | Prototyping: relaxed checks |
| `--ci` | CI mode: deterministic timestamps, strict |
| `--fail-on-warning` | Exit non-zero on warnings |

## Supported Languages

| Language | Module | Key Capabilities |
|----------|--------|-----------------|
| JavaScript/TypeScript | `ubs-js.sh` | React hook deps, AST via ast-grep, promise chains |
| Python | `ubs-python.sh` | Resource lifecycle, context managers |
| Go | `ubs-golang.sh` | Return/defer, context leaks, goroutine leaks |
| C/C++ | `ubs-cpp.sh` | C++20 patterns, RAII, buffer overflows |
| Rust | `ubs-rust.sh` | Type narrowing, cargo integration, unwrap panics |
| Java | `ubs-java.sh` | JDBC lifecycle, CompletableFuture, try-with-resources |
| Ruby | `ubs-ruby.sh` | Block/ensure analysis |
| Swift | `ubs-swift.sh` | Guard-let analysis, AST rules |

## Detection Categories

18 categories covering:
- **Security:** XSS, SQL injection, command injection, eval injection
- **Null Safety:** Unguarded null access, null pointer crashes
- **Async/Await:** Missing await, unhandled rejections, fire-and-forget
- **Error Handling:** Empty catch blocks, swallowed exceptions
- **Resource Lifecycle:** Unclosed handles, missing context managers
- **Memory Safety:** Buffer overflows, use-after-free, dangling pointers
- **Concurrency:** Race conditions, goroutine leaks, deadlocks
- **Type Safety:** Type narrowing gaps, always-false comparisons
- **Correctness:** Logic errors, off-by-one, always-true conditions
- **Performance:** Inefficient patterns, unnecessary allocations

## Output Format

```
Warning Category (N errors)
    file.rs:42:5 -- Issue description
    Suggested fix

Exit code: 0 (pass) or 1 (fail)
```

Parse: `file:line:col` for location | suggested fix follows each finding | exit 0/1 for pass/fail.

## Fix Workflow

1. Read finding -- category + fix suggestion
2. Navigate `file:line:col` -- view context
3. Verify real issue (not false positive)
4. Fix root cause (not symptom)
5. Re-run `ubs <file>` -- confirm exit 0
6. Commit

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Pass -- no issues found |
| 1 | Fail -- bugs/issues found |
| 2 | Environment error (missing tools) |

## Bug Severity Guide

- **Critical (always fix):** Memory safety, use-after-free, data races, SQL injection
- **Important (production):** Unwrap panics, resource leaks, overflow checks
- **Contextual (judgment):** TODO/FIXME, println! debugging

## Inline Suppression

Supported markers in code comments:
- `ubs:ignore`
- `nolint`
- `noqa`

## Maintenance

```bash
ubs doctor              # Audit environment
ubs doctor --fix        # Redownload missing/corrupt modules
ubs --update            # Update ubs itself
ubs --update-modules    # Force module re-download
```

## CI Integration

```bash
# GitHub Actions / CI pipeline
ubs . --ci --fail-on-warning --format=sarif    # SARIF for GitHub Code Scanning
ubs . --ci --format=json --report-json=ubs-results.json  # JSON for custom gating
ubs --staged --format=json                     # Pre-commit: staged files only
ubs . --comparison=baseline.json               # Regression detection
```

## Installation

```bash
# Quick install
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/master/install.sh?$(date +%s)" | bash

# Easy mode (auto-install deps, auto-detect agents, wire guardrails)
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/master/install.sh?$(date +%s)" | bash -s -- --easy-mode

# Homebrew
brew install dicklesworthstone/tap/ubs
```

## Agent Integration Rules

1. **Scan before committing:** Always run `ubs $(git diff --name-only --cached)` on staged files
2. **Use JSON for parsing:** `--format=json` for programmatic consumption
3. **Check exit codes:** 0 = safe to commit, 1 = fix issues first
4. **Focus scans:** Use `--only=<lang>` or specific file paths for speed
5. **Track baselines:** Use `--report-json` and `--comparison` for regression detection
6. **Respect suppressions:** Don't remove `ubs:ignore` comments without understanding why
