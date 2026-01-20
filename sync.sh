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

# Sync llmmux
echo "  -> Syncing llmmux..."
mkdir -p ~/.llmmux

# Ensure llmmux subdirectories exist (but don't overwrite existing ones)
mkdir -p ~/.llmmux/state
mkdir -p ~/.llmmux/artifacts

# Sync core files, excluding state and artifacts (preserve user data)
rsync -av --exclude='state' --exclude='artifacts' ./llmmux/ ~/.llmmux/

# Ensure shared agent init file is present
if [ -f ./llmmux/INIT_AGENT.md ]; then
  cp ./llmmux/INIT_AGENT.md ~/.llmmux/INIT_AGENT.md
fi

# Set up Python virtual environment
echo "  -> Setting up Python virtual environment..."
if [ ! -d ~/.llmmux/venv ]; then
    python3 -m venv ~/.llmmux/venv
fi

# Activate venv and install dependencies
source ~/.llmmux/venv/bin/activate
pip install --quiet --disable-pip-version-check -r ~/.llmmux/requirements.txt

# Create wrapper scripts
cat > ~/.llmmux/orchestrator << 'EOF'
#!/bin/bash
# llmmux orchestrator wrapper - activates venv before running Python script
source ~/.llmmux/venv/bin/activate
exec python3 ~/.llmmux/orchestrator.py "$@"
EOF

cat > ~/.llmmux/create_agent << 'EOF'
#!/bin/bash
# llmmux create_agent wrapper - activates venv before running Python script
source ~/.llmmux/venv/bin/activate
exec python3 ~/.llmmux/create_agent.py "$@"
EOF

# Make wrapper scripts executable
chmod +x ~/.llmmux/orchestrator
chmod +x ~/.llmmux/create_agent

# Make Python scripts executable (fallback)
chmod +x ~/.llmmux/orchestrator.py 2>/dev/null || true
chmod +x ~/.llmmux/create_agent.py 2>/dev/null || true

echo "Sync complete!"
