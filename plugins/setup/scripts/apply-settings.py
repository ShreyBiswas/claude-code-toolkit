#!/usr/bin/env python3
"""Apply Claude Code shared settings to ~/.claude/settings.json.

Idempotent — safe to run multiple times. Merges into existing settings
without overwriting unrelated keys.

Settings applied:
  - attribution.commit: ""  (disable commit attribution)
  - attribution.pr: ""      (disable PR attribution)
  - env.ENABLE_CLAUDEAI_MCP_SERVERS: "false"  (disable claude.ai MCP servers)
  - showClearContextOnPlanAccept: true  (show "clear context" on plan accept)

Run:  python3 apply-settings.py [--dry-run]
"""

import json
import os
import sys
from pathlib import Path

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

WANTED = {
    "attribution": {"commit": "", "pr": ""},
    "env": {"ENABLE_CLAUDEAI_MCP_SERVERS": "false"},
    "showClearContextOnPlanAccept": True,
}

# Keys to remove if present (stale / superseded settings)
REMOVE_KEYS = ["disableBypassPermissionsMode", "skipDangerousModePermissionPrompt"]


def deep_merge(base: dict, overlay: dict) -> dict:
    """Merge overlay into base, recursing into nested dicts."""
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def remove_keys(d: dict, keys: list[str]) -> list[str]:
    """Remove top-level keys from dict. Returns list of keys actually removed."""
    removed = []
    for key in keys:
        if key in d:
            del d[key]
            removed.append(key)
    return removed


def main():
    dry_run = "--dry-run" in sys.argv

    # Read existing settings
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            settings = json.load(f)
    else:
        settings = {}

    # Apply
    deep_merge(settings, WANTED)
    removed = remove_keys(settings, REMOVE_KEYS)

    if dry_run:
        print("DRY RUN — would write:")
        print(json.dumps(settings, indent=2))
        if removed:
            print(f"\nRemoved keys: {', '.join(removed)}")
        return

    # Write
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")

    print("Settings applied to", SETTINGS_PATH)
    for key, value in WANTED.items():
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"  ✓ {key}.{k}: {v!r}")
        else:
            print(f"  ✓ {key}: {value!r}")
    if removed:
        for key in removed:
            print(f"  ✗ {key}: removed")


if __name__ == "__main__":
    main()
