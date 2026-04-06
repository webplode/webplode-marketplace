#!/usr/bin/env python3
"""Check or apply Khuym repo onboarding for Claude Code."""

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


SCRIPT_PATH = Path(__file__).resolve()
USING_KHUYM_DIR = SCRIPT_PATH.parent.parent
AGENTS_TEMPLATE_PATH = USING_KHUYM_DIR / "references" / "AGENTS.template.md"
HOOK_TEMPLATES_DIR = USING_KHUYM_DIR / "templates"
ONBOARDING_SCHEMA_VERSION = "2.0"
MANAGED_HOOK_COMMAND_PREFIX = (
    'python3 "$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.claude/hooks/'
)

# Markers for managed sections
AGENTS_MARKER_START = "<!-- KHUYM:START -->"
AGENTS_MARKER_END = "<!-- KHUYM:END -->"
CLAUDE_MD_MARKER_START = "<!-- KHUYM:CLAUDE_MD:START -->"
CLAUDE_MD_MARKER_END = "<!-- KHUYM:CLAUDE_MD:END -->"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_plugin_version() -> str:
    for parent in [USING_KHUYM_DIR.parent.parent, *USING_KHUYM_DIR.parents]:
        for name in (".claude-plugin", ".codex-plugin"):
            manifest = parent / name / "plugin.json"
            if manifest.exists():
                return json.loads(manifest.read_text(encoding="utf-8"))["version"]
    return "unknown"


def resolve_repo_root(explicit_root: Optional[str]) -> Path:
    if explicit_root:
        return Path(explicit_root).resolve()
    cwd = Path.cwd().resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip()).resolve()
    except Exception:
        for candidate in [cwd, *cwd.parents]:
            if (candidate / ".git").exists():
                return candidate
        return cwd


def read_template() -> str:
    return AGENTS_TEMPLATE_PATH.read_text(encoding="utf-8").rstrip() + "\n"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# AGENTS.md merging
# ---------------------------------------------------------------------------

def managed_agents_present(text: str) -> bool:
    return AGENTS_MARKER_START in text and AGENTS_MARKER_END in text


def merge_agents_content(existing: str, template: str) -> Tuple[str, str]:
    stripped = existing.strip()
    if not stripped:
        return template, "created_from_template"

    if managed_agents_present(existing):
        updated = re.sub(
            rf"{re.escape(AGENTS_MARKER_START)}.*?{re.escape(AGENTS_MARKER_END)}\n?",
            template,
            existing,
            flags=re.DOTALL,
        )
        return updated.rstrip() + "\n", "updated_managed_block"

    glue = "\n\n" if not existing.endswith("\n\n") else ""
    return existing.rstrip() + glue + template, "appended_managed_block"


# ---------------------------------------------------------------------------
# CLAUDE.md context-recovery block
# ---------------------------------------------------------------------------

def render_claude_md_block() -> str:
    return "\n".join([
        CLAUDE_MD_MARKER_START,
        "## Khuym Context Recovery",
        "",
        "After context compaction, STOP and do this before anything else:",
        "",
        "1. Read AGENTS.md completely.",
        "2. If present, read .khuym/HANDOFF.json and .khuym/STATE.md.",
        "3. Re-open the active feature CONTEXT.md before more planning or edits.",
        "4. Re-open the current bead or task before running more implementation commands.",
        "5. Check the current worktree state with git status before resuming.",
        "",
        "After completing these steps, briefly confirm what context you restored and only then continue.",
        CLAUDE_MD_MARKER_END,
        "",
    ])


def merge_claude_md(path: Path) -> Tuple[str, str]:
    """Merge Khuym context recovery block into project CLAUDE.md."""
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    block = render_claude_md_block()

    if CLAUDE_MD_MARKER_START in existing and CLAUDE_MD_MARKER_END in existing:
        updated = re.sub(
            rf"{re.escape(CLAUDE_MD_MARKER_START)}.*?{re.escape(CLAUDE_MD_MARKER_END)}\n?",
            block,
            existing,
            flags=re.DOTALL,
        )
        return updated.rstrip() + "\n", "updated"

    if not existing.strip():
        return "# CLAUDE.md\n\n" + block, "created"

    glue = "\n\n" if not existing.endswith("\n\n") else ""
    return existing.rstrip() + glue + block, "appended"


# ---------------------------------------------------------------------------
# .claude/settings.local.json  (hooks)
# ---------------------------------------------------------------------------

def render_managed_hook_entries() -> Dict[str, List[Dict]]:
    return {
        "SessionStart": [
            {
                "matcher": "startup|resume",
                "hooks": [
                    {
                        "type": "command",
                        "command": MANAGED_HOOK_COMMAND_PREFIX + 'khuym_session_start.py"',
                        "statusMessage": "Khuym: session bootstrap",
                    }
                ],
            }
        ],
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": MANAGED_HOOK_COMMAND_PREFIX + 'khuym_pre_tool_use.py"',
                        "statusMessage": "Khuym: shell guardrails",
                    }
                ],
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": MANAGED_HOOK_COMMAND_PREFIX + 'khuym_stop.py"',
                        "statusMessage": "Khuym: end-of-turn check",
                    }
                ],
            }
        ],
    }


def is_khuym_hook_entry(entry: Dict) -> bool:
    for hook in entry.get("hooks", []):
        command = hook.get("command", "")
        status = hook.get("statusMessage", "")
        if "/.claude/hooks/khuym_" in command or status.startswith("Khuym:"):
            return True
    return False


def merge_settings_json(path: Path) -> Tuple[str, List[str]]:
    """Merge Khuym hooks into .claude/settings.local.json."""
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RuntimeError(f"Unable to parse JSON at {path}: {exc}") from exc

    hooks = existing.get("hooks", {})
    changes: List[str] = []
    managed = render_managed_hook_entries()

    for event_name, entries in managed.items():
        current_entries = hooks.get(event_name, [])
        filtered = [e for e in current_entries if not is_khuym_hook_entry(e)]
        hooks[event_name] = filtered + entries
        changes.append(f"upsert_{event_name}")

    merged = dict(existing)
    merged["hooks"] = hooks
    return json.dumps(merged, indent=2, sort_keys=True) + "\n", changes


# ---------------------------------------------------------------------------
# Hook script installation
# ---------------------------------------------------------------------------

def write_hook_scripts(repo_root: Path) -> List[str]:
    hooks_dir = repo_root / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name in ("khuym_session_start.py", "khuym_pre_tool_use.py", "khuym_stop.py"):
        source = HOOK_TEMPLATES_DIR / name
        target = hooks_dir / name
        shutil.copyfile(source, target)
        target.chmod(0o755)
        written.append(str(target.relative_to(repo_root)))
    return written


# ---------------------------------------------------------------------------
# Check / Apply
# ---------------------------------------------------------------------------

def check_repo(repo_root: Path) -> Dict:
    plugin_version = load_plugin_version()
    agents_path = repo_root / "AGENTS.md"
    settings_path = repo_root / ".claude" / "settings.local.json"
    claude_md_path = repo_root / "CLAUDE.md"
    onboarding_path = repo_root / ".khuym" / "onboarding.json"

    agents_exists = (
        agents_path.exists()
        and agents_path.read_text(encoding="utf-8").strip() != ""
    )
    managed_agents = agents_exists and managed_agents_present(
        agents_path.read_text(encoding="utf-8")
    )

    settings_data: Dict = {}
    if settings_path.exists():
        try:
            settings_data = json.loads(settings_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    onboarding: Dict = {}
    if onboarding_path.exists():
        try:
            onboarding = json.loads(onboarding_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    has_managed_hooks = False
    for entries in settings_data.get("hooks", {}).values():
        if any(is_khuym_hook_entry(e) for e in entries):
            has_managed_hooks = True
            break

    has_claude_md_block = False
    if claude_md_path.exists():
        has_claude_md_block = CLAUDE_MD_MARKER_START in claude_md_path.read_text(
            encoding="utf-8"
        )

    actions: List[str] = []
    if not agents_exists:
        actions.append("create_AGENTS.md")
    elif not managed_agents:
        actions.append("append_khuym_managed_block_to_AGENTS.md")

    if not settings_path.exists():
        actions.append("create_.claude/settings.local.json")
    elif not has_managed_hooks:
        actions.append("install_khuym_hooks")

    if not has_claude_md_block:
        actions.append("install_khuym_claude_md_block")

    if onboarding.get("plugin_version") != plugin_version:
        actions.append("write_.khuym/onboarding.json")

    status = "up_to_date" if not actions else "needs_onboarding"
    return {
        "repo_root": str(repo_root),
        "status": status,
        "actions": actions,
        "requires_confirmation": False,
        "details": {
            "plugin_version": plugin_version,
            "agents_exists": agents_exists,
            "agents_managed_block": managed_agents,
            "settings_exists": settings_path.exists(),
            "has_managed_hooks": has_managed_hooks,
            "has_claude_md_block": has_claude_md_block,
            "onboarding_state": onboarding or None,
        },
    }


def apply_repo(repo_root: Path) -> Dict:
    plugin_version = load_plugin_version()
    template = read_template()

    agents_path = repo_root / "AGENTS.md"
    settings_path = repo_root / ".claude" / "settings.local.json"
    claude_md_path = repo_root / "CLAUDE.md"
    onboarding_path = repo_root / ".khuym" / "onboarding.json"

    ensure_parent(agents_path)
    ensure_parent(settings_path)
    ensure_parent(onboarding_path)

    # 1. Merge AGENTS.md
    existing_agents = (
        agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    )
    merged_agents, agents_status = merge_agents_content(existing_agents, template)
    agents_path.write_text(merged_agents, encoding="utf-8")

    # 2. Merge .claude/settings.local.json (hooks)
    settings_text, settings_changes = merge_settings_json(settings_path)
    settings_path.write_text(settings_text, encoding="utf-8")

    # 3. Write hook scripts to .claude/hooks/
    hook_scripts = write_hook_scripts(repo_root)

    # 4. Merge CLAUDE.md context recovery block
    claude_md_text, claude_md_status = merge_claude_md(claude_md_path)
    claude_md_path.write_text(claude_md_text, encoding="utf-8")

    # 5. Write onboarding manifest
    onboarding_payload = {
        "schema_version": ONBOARDING_SCHEMA_VERSION,
        "plugin": "khuym",
        "plugin_version": plugin_version,
        "installed_at": utc_now(),
        "status": "complete",
        "target": "claude-code",
        "managed_assets": {
            "agents_mode": agents_status,
            "settings_changes": settings_changes,
            "hook_scripts": hook_scripts,
            "claude_md_status": claude_md_status,
        },
        "notes": [],
    }
    onboarding_path.write_text(
        json.dumps(onboarding_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    final_summary = check_repo(repo_root)
    return {
        **final_summary,
        "applied": True,
        "result": onboarding_payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or apply Khuym repo onboarding for Claude Code."
    )
    parser.add_argument("--repo-root", help="Repository root to inspect or modify.")
    parser.add_argument(
        "--apply", action="store_true", help="Apply onboarding changes."
    )
    args = parser.parse_args()

    repo_root = resolve_repo_root(args.repo_root)
    payload = apply_repo(repo_root) if args.apply else check_repo(repo_root)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
