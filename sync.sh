#!/bin/bash
# sync.sh - Sync top-level project directories to all harness home directories
# Agents sync to: cursor, claude, gemini, codex
# Commands sync to: cursor, claude, gemini
# Skills sync to: cursor, claude, gemini, codex, kilocode

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Syncing project files to all harnesses..."

# Function to sync a directory if it exists
sync_if_exists() {
  local source="$1"
  local destination="$2"
  local label="$3"

  if [[ -d "$source" ]]; then
    echo "    -> Syncing $label..."
    mkdir -p "$destination"
    rsync -av --delete "$source/" "$destination/"
  fi
}

# Define harnesses by concern
agent_harnesses=("cursor" "claude" "gemini" "codex")
commands_harnesses=("cursor" "claude" "gemini")
skills_harnesses=("cursor" "claude" "gemini" "codex" "kilocode")

# Sync agents
echo "  -> Syncing agents..."
for harness in "${agent_harnesses[@]}"; do
  echo "    -> .$harness/agents"
  sync_if_exists "./agents" ~/.$harness/agents "agents"

  # Inject harness-specific frontmatter into synced agent files
  if [[ -d "./agents" && -d "./agent-frontmatter" ]]; then
    bash "$SCRIPT_DIR/inject-harness-frontmatter.sh" "$harness" ~/.$harness/agents
  fi
done

# Sync commands
echo "  -> Syncing commands..."
for harness in "${commands_harnesses[@]}"; do
  echo "    -> .$harness/commands"
  sync_if_exists "./commands" ~/.$harness/commands "commands"
done

# Sync skills
echo "  -> Syncing skills..."
for harness in "${skills_harnesses[@]}"; do
  echo "    -> .$harness/skills"
  sync_if_exists "./skills" ~/.$harness/skills "skills"
done

echo "Sync complete!"
