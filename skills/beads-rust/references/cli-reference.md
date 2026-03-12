# br CLI Complete Reference

## Global Options

All commands accept these flags:

| Flag | Purpose |
|---|---|
| `--db <DB>` | Database path (auto-discovers `.beads/*.db` if not set) |
| `--actor <ACTOR>` | Actor name for audit trail |
| `--json` | Output as JSON |
| `--no-auto-flush` | Skip auto JSONL export |
| `--no-auto-import` | Skip auto import check |
| `--allow-stale` | Allow stale DB (bypass freshness check) |
| `--lock-timeout <MS>` | SQLite busy timeout in ms |
| `--no-db` | JSONL-only mode (no DB connection) |
| `-v, --verbose` | Increase logging verbosity (`-v`, `-vv`) |
| `-q, --quiet` | Quiet mode (errors only) |
| `--no-color` | Disable colored output |

## Commands

### init -- Initialize a beads workspace

```bash
br init [--prefix <PREFIX>] [--force]
```

Creates `.beads/` directory with SQLite database.

### create -- Create a new issue

```bash
br create [TITLE] [OPTIONS]
```

| Flag | Purpose |
|---|---|
| `--title <TITLE>` | Title (alternative to positional) |
| `-t, --type <TYPE>` | Issue type (task, bug, feature, epic, chore, spike, doc) |
| `-p, --priority <N>` | Priority 0-4 or P0-P4 |
| `-d, --description <DESC>` | Description (alias: `--body`) |
| `-a, --assignee <NAME>` | Assign to person |
| `--owner <EMAIL>` | Set owner email |
| `-l, --labels <LABELS>` | Labels (comma-separated) |
| `--parent <ID>` | Parent issue ID |
| `--deps <DEPS>` | Dependencies (format: `type:id,type:id`) |
| `-e, --estimate <MIN>` | Time estimate in minutes |
| `--due <DATE>` | Due date (RFC3339 or relative) |
| `--defer <DATE>` | Defer until date |
| `--external-ref <REF>` | External reference |
| `--ephemeral` | Not exported to JSONL |
| `-s, --status <STATUS>` | Initial status |
| `--dry-run` | Preview without creating |
| `--silent` | Output only issue ID |
| `-f, --file <FILE>` | Bulk import from markdown file |

### q -- Quick capture

```bash
br q [TITLE]... [-p PRIORITY] [-t TYPE] [-l LABELS] [-d DESC] [--parent ID] [-e MIN]
```

Creates issue and prints only the ID. Ideal for rapid capture.

### show -- Show issue details

```bash
br show [IDS]... [--format text|json|toon] [--wrap]
```

### list -- List issues

```bash
br list [OPTIONS]
```

| Flag | Purpose |
|---|---|
| `-s, --status <STATUS>` | Filter by status (repeatable) |
| `-t, --type <TYPE>` | Filter by type (repeatable) |
| `--assignee <NAME>` | Filter by assignee |
| `--unassigned` | Unassigned only |
| `--id <ID>` | Filter by specific IDs (repeatable) |
| `-l, --label <LABEL>` | Filter by label (AND logic, repeatable) |
| `--label-any <LABEL>` | Filter by label (OR logic) |
| `-p, --priority <N>` | Filter by priority (repeatable) |
| `--priority-min / --priority-max` | Priority range |
| `--title-contains <STR>` | Title substring filter |
| `--desc-contains <STR>` | Description substring filter |
| `-a, --all` | Include closed issues |
| `--limit <N>` | Max results (default: 50, 0=unlimited) |
| `--sort <FIELD>` | Sort by priority, created_at, updated_at, title |
| `-r, --reverse` | Reverse sort order |
| `--deferred` | Include deferred issues |
| `--overdue` | Overdue issues only |
| `--long` | Long output format |
| `--pretty` | Tree/pretty format |
| `--format <FMT>` | text, json, csv, toon |
| `--fields <FIELDS>` | CSV fields to include |

### search -- Search issues

```bash
br search <QUERY> [same options as list]
```

### update -- Update an issue

```bash
br update [IDS]... [OPTIONS]
```

| Flag | Purpose |
|---|---|
| `--title <TITLE>` | Update title |
| `--description <DESC>` | Update description (alias: `--body`) |
| `--design <DESIGN>` | Update design notes |
| `--acceptance-criteria <AC>` | Update acceptance criteria |
| `--notes <NOTES>` | Update additional notes |
| `-s, --status <STATUS>` | Change status |
| `-p, --priority <N>` | Change priority |
| `-t, --type <TYPE>` | Change issue type |
| `--assignee <NAME>` | Assign (empty string clears) |
| `--claim` | Atomic: assignee=actor + status=in_progress |
| `--force` | Update even if blocked |
| `--due / --defer / --estimate` | Date and time fields |
| `--add-label / --remove-label / --set-labels` | Label management |
| `--parent <ID>` | Reparent (empty string removes) |
| `--session <SESSION>` | Session ID for tracking |

### close -- Close an issue

```bash
br close [IDS]... [-r REASON] [-f] [--suggest-next] [--session SESSION]
```

`--suggest-next` returns newly unblocked issues after closing.

### reopen -- Reopen an issue

```bash
br reopen [IDS]... [-r REASON]
```

### delete -- Delete an issue (tombstone)

```bash
br delete [IDS]... [--reason REASON] [--from-file FILE] [--cascade] [--force] [--hard] [--dry-run]
```

### defer / undefer -- Schedule for later

```bash
br defer [IDS]... --until <DATE>   # e.g., +1h, tomorrow, 2025-01-15
br undefer [IDS]...
```

### ready -- List actionable issues

```bash
br ready [OPTIONS]
```

Shows open, unblocked, non-deferred issues. Default sort: hybrid (priority + age).

| Flag | Purpose |
|---|---|
| `--limit <N>` | Max results (default: 20) |
| `--assignee [NAME]` | Filter (no value = current actor) |
| `--unassigned` | Unassigned only |
| `--parent <ID>` | Children of parent |
| `-r, --recursive` | All descendants |
| `--sort <POLICY>` | hybrid, priority, oldest |

### blocked -- List blocked issues

```bash
br blocked [--limit N] [--detailed] [--wrap] [-t TYPE] [-p PRIORITY] [-l LABEL]
```

### stale -- List stale issues

```bash
br stale [--days N] [--status STATUS]
```

Default: 30 days without update.

### orphans -- Issues referenced in commits but still open

```bash
br orphans [--details] [--fix]
```

### count -- Count with grouping

```bash
br count [--by status|priority|type|assignee|label] [FILTERS]
```

### stats / status -- Project statistics

```bash
br stats [--by-type] [--by-priority] [--by-assignee] [--by-label] [--activity-hours N]
```

### dep -- Dependency management

```bash
br dep add <ISSUE> <DEPENDS_ON> [-t blocks|parent-child|related]
br dep remove <ISSUE> <DEPENDS_ON>
br dep list <ISSUE> [--direction down|up|both] [-t TYPE]
br dep tree <ISSUE> [-d down|up|both] [--max-depth N] [--format text|mermaid]
br dep cycles [--blocking-only]
```

### epic -- Epic management

```bash
br epic status [--eligible-only]
br epic close-eligible [--dry-run]
```

### graph -- Dependency visualization

```bash
br graph [ISSUE] [--all] [--compact]
```

### comments -- Comment management

```bash
br comments add <ID> [TEXT] [-f FILE] [--author AUTHOR]
br comments list <ID> [--wrap]
```

### label -- Label management

```bash
br label add [IDS]... -l <LABEL>
br label remove [IDS]... -l <LABEL>
br label list [ISSUE]
br label list-all
br label rename <OLD> <NEW>
```

### sync -- Database/JSONL synchronization

```bash
br sync [OPTIONS]
```

| Flag | Purpose |
|---|---|
| `--flush-only` | Export DB to JSONL |
| `--import-only` | Import JSONL to DB |
| `--merge` | 3-way merge |
| `--status` | Show sync status (read-only) |
| `-f, --force` | Override safety guards |
| `--rebuild` | Rebuild DB from JSONL |
| `--error-policy <P>` | strict, best-effort, partial, required-core |
| `--orphans <MODE>` | strict, resurrect, skip, allow |

### audit -- Agent interaction recording

```bash
br audit record [--kind KIND] [--issue-id ID] [--model MODEL] [--prompt P] [--response R]
br audit label <ENTRY_ID> --label <LABEL> [--reason REASON]
br audit log <ID>
br audit summary [--days N]
```

### query -- Saved queries

```bash
br query save <NAME> [-d DESC] [FILTER FLAGS]
br query run <NAME> [OVERRIDE FLAGS]
br query list
br query delete <NAME>
```

### changelog -- Generate changelog

```bash
br changelog [--since DATE] [--since-tag TAG] [--since-commit COMMIT]
```

### lint -- Check for missing sections

```bash
br lint [IDS]... [-t TYPE] [-s STATUS]
```

### history -- Local backups

```bash
br history list
br history diff <FILE>
br history restore <FILE> [-f]
br history prune [--keep N] [--older-than DAYS]
```

### config -- Configuration

```bash
br config list [--project] [--user]
br config get <KEY>
br config set <KEY>=<VALUE>
br config delete <KEY>
br config edit
br config path
```

### agents -- AGENTS.md management

```bash
br agents [--add] [--remove] [--update] [--check] [--dry-run] [-f]
```

### doctor -- Diagnostics

```bash
br doctor [--repair]
```

### info -- Workspace metadata

```bash
br info [--schema] [--whats-new] [--thanks]
```

### schema -- JSON schema output

```bash
br schema [TARGET] [--format text|json|toon]
```

Targets: all, issue, issue-with-counts, issue-details, ready-issue, stale-issue, blocked-issue, tree-node, statistics, error

### upgrade -- Self-update

```bash
br upgrade [--check] [--force] [--version VERSION] [--dry-run]
```

### completions -- Shell completions

```bash
br completions <bash|zsh|fish|powershell|elvish> [-o OUTPUT_DIR]
```
