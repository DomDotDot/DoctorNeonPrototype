#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Pre-Commit Hook Installer
=============================
Installs a git hook in .git/hooks/pre-commit to automatically update
story dialogue stats in README.md and README.ru.md upon committing.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_DIR = os.path.join(BASE_DIR, ".git", "hooks")
PRE_COMMIT_PATH = os.path.join(HOOKS_DIR, "pre-commit")

HOOK_SCRIPT_CONTENT = """#!/bin/sh
# Auto-update story stats badges and tables in README files before commit
echo "[Git Hook] Updating script dialogue stats in READMEs..."

# Try Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
elif command -v py >/dev/null 2>&1; then
    PYTHON_CMD="py"
fi

if [ -n "$PYTHON_CMD" ]; then
    $PYTHON_CMD tools/script_stats_linter.py --silent
    git add README.md README.ru.md 2>/dev/null || true
fi

exit 0
"""

def install_hook():
    if not os.path.exists(HOOKS_DIR):
        print(f"[Error] .git/hooks directory not found at: {HOOKS_DIR}")
        return False

    with open(PRE_COMMIT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(HOOK_SCRIPT_CONTENT)

    try:
        # Make executable on Unix/Mac/Git Bash
        os.chmod(PRE_COMMIT_PATH, 0o755)
    except Exception:
        pass

    print(f"[Success] Git pre-commit hook installed to: {PRE_COMMIT_PATH}")
    print("Every `git commit` will now automatically refresh and stage script statistics in README files.")
    return True

if __name__ == "__main__":
    install_hook()
