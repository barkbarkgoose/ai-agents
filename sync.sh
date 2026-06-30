#!/bin/bash
# sync.sh - Sync top-level project directories to OpenCode-compatible home
# directories. Targets both stock OpenCode and Kilo (which reads its own XDG
# root at ~/.config/kilo/, not ~/.config/opencode/).
#
# Agents sync to:   ~/.config/opencode/agents/, ~/.config/kilo/agents/
# Commands sync to: ~/.config/opencode/commands/, ~/.config/kilo/commands/
# Skills sync to:   ~/.config/opencode/skills/, ~/.config/kilo/skills/
#
# Note: oh-my-pi (omp) is not targeted here. omp does not expose a
# user-level agents/commands/skills directory; it uses ~/.omp/agent/ for
# YAML settings and inherits rules from other harnesses on first run.

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Two destination roots. Kilo reads ~/.config/kilo/ as its XDG global root;
# stock OpenCode reads ~/.config/opencode/. Both must be kept in sync.
OPENCODE_DEST="$HOME/.config/opencode"
KILO_DEST="$HOME/.kilo"

# Function to sync a directory if it exists. Files in the destination that are
# not present in the source are preserved -- this avoids pruning files the
# user has added to their harness home directories. Adding or removing
# agents/skills/commands is the user's responsibility; rerun sync.sh after
# such changes.
sync_if_exists() {
  local source="$1"
  local destination="$2"
  local label="$3"

  if [[ -d "$source" ]]; then
    echo "    -> Syncing $label..."
    mkdir -p "$destination"
    rsync -av "$source/" "$destination/"
  fi
}

# Sync agents to both roots
echo " ------ Syncing agents ------"
for dest_root in "$OPENCODE_DEST" "$KILO_DEST"; do
  dest_dir="$dest_root/agents"
  echo "    -> ${dest_dir/#$HOME/~}"
  sync_if_exists "$SCRIPT_DIR/agents" "$dest_dir" "agents"

  if [[ -d "$SCRIPT_DIR/agents" && -d "$SCRIPT_DIR/agent-frontmatter" ]]; then
    bash "$SCRIPT_DIR/subscripts/inject-harness-frontmatter.sh" opencode "$dest_dir"
  fi
done

# Sync commands to both roots
echo " ------ Syncing commands ------"
for dest_root in "$OPENCODE_DEST" "$KILO_DEST"; do
  dest_dir="$dest_root/commands"
  echo "    -> ${dest_dir/#$HOME/~}"
  sync_if_exists "$SCRIPT_DIR/commands" "$dest_dir" "commands"
done

# Sync skills to both roots
echo " ------ Syncing skills ------"
for dest_root in "$OPENCODE_DEST" "$KILO_DEST"; do
  dest_dir="$dest_root/skills"
  echo "    -> ${dest_dir/#$HOME/~}"
  sync_if_exists "$SCRIPT_DIR/skills" "$dest_dir" "skills"
done

echo "Sync complete!"