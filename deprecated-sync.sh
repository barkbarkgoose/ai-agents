#!/bin/bash
# sync.sh - Sync specific project directories to home directory
# Only updates specified subdirectories, leaves everything else alone

set -e  # Exit on error

echo "Syncing project files to home directory..."

# Function to ensure directories exist
ensure_dirs() {
  mkdir -p "$1"
  mkdir -p "$2"
}

# Sync cursor
echo "  -> Syncing cursor agents..."
ensure_dirs "./cursor/agents" ~/.cursor/agents
rsync -av --delete ./cursor/agents/ ~/.cursor/agents/

echo "  -> Syncing cursor commands..."
ensure_dirs "./cursor/commands" ~/.cursor/commands
rsync -av --delete ./cursor/commands/ ~/.cursor/commands/

echo "  -> Syncing cursor skills..."
ensure_dirs "./cursor/skills" ~/.cursor/skills
rsync -av --delete ./cursor/skills/ ~/.cursor/skills/

# Sync claude
echo "  -> Syncing claude agents..."
ensure_dirs "./claude/agents" ~/.claude/agents
rsync -av --delete ./claude/agents/ ~/.claude/agents/

echo "  -> Syncing claude commands..."
ensure_dirs "./claude/commands" ~/.claude/commands
rsync -av --delete ./claude/commands/ ~/.claude/commands/

echo "  -> Syncing claude skills..."
ensure_dirs "./claude/skills" ~/.claude/skills
rsync -av --delete ./claude/skills/ ~/.claude/skills/

# Sync gemini
echo "  -> Syncing gemini agents..."
ensure_dirs "./gemini/agents" ~/.gemini/agents
rsync -av --delete ./gemini/agents/ ~/.gemini/agents/

echo "  -> Syncing gemini commands..."
ensure_dirs "./gemini/commands" ~/.gemini/commands
rsync -av --delete ./gemini/commands/ ~/.gemini/commands/

echo "  -> Syncing gemini skills..."
ensure_dirs "./gemini/skills" ~/.gemini/skills
rsync -av --delete ./gemini/skills/ ~/.gemini/skills/

echo "Sync complete!"