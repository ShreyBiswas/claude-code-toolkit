#!/bin/bash
# Bootstrap the Claude Code Toolkit on a new machine
# Usage: ./install.sh
# Requires: claude CLI, gh CLI authenticated

set -euo pipefail

echo "Adding Claude Code Toolkit marketplace..."
claude plugin marketplace add ShreyBiswas/claude-code-toolkit

echo "Installing setup plugin..."
claude plugin install setup@ShreyBiswas-claude-code-toolkit --scope user

echo ""
echo "Marketplace added and setup plugin installed."
echo "Run /toolkit-setup inside Claude Code to complete installation."
