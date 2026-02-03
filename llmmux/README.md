# llmmux - tmux-based Multi-Agent Orchestrator

A tmux-based orchestration system for managing multiple LLM agents in isolated windows with persistent state management.

## Overview

llmmux creates tmux sessions where each agent runs in its own window. An orchestrator agent coordinates the workflow, spawning specialized agents as needed and maintaining state across sessions.

## Quick Start

### 1. Sync to Home Directory

From the project root:

```bash
./sync.sh
```

This copies llmmux files to `~/.llmmux/` and sets up a Python virtual environment with required dependencies.

### 2. Create an Orchestrator Session

```bash
cd /path/to/your/project
~/.llmmux/orchestrator --provider agent
```

**Note:** Use the wrapper scripts (not `python3`) to automatically activate the virtual environment with required dependencies.

Available providers:
- `agent` - Cursor AI
- `codex` - OpenAI Codex CLI
- `claude` - Anthropic Claude CLI
- `gemini` - Google Gemini CLI (note: may run in headless mode)
- `opencode` - OpenCode CLI

### 3. Attach to Session

```bash
tmux attach -t llmmux
```

### 4. Interact with Orchestrator

The orchestrator will ask what you want to build and coordinate the necessary agents.

## Architecture

```
llmmux Session
├── orchestrator (window)    - Coordinates workflow
├── django-agent (window)    - Backend development
├── vue-agent (window)       - Frontend development
└── researcher (window)      - Research tasks
```

## State Management

llmmux maintains persistent state in `~/.llmmux/state/<session-id>/`:

- **handoff.md** - Human-readable narrative for LLM continuity
- **run_state.json** - Machine-readable state index
- **tasks.json** - Task queue and planning
- **agents/*.last.json** - Per-agent state snapshots (name, provider, status, last_action, last_run_ts as ISO 8601 UTC)
- **logs/*.log** - Agent output logs

Artifacts are stored in `~/.llmmux/artifacts/<session-id>/`.
The mapping from tmux session name to session id is stored in `~/.llmmux/state/session_index.json`.
Each orchestrator launch generates a new `<session-id>` and records the tmux session name inside `run_state.json`.

## Creating Additional Agents

From within your tmux session:

```bash
# Using a skill
~/.llmmux/create_agent --name vue-agent --skill vue3-typescript

# With custom prompt
~/.llmmux/create_agent --name django-agent --prompt "Create REST API"

# Specific provider
~/.llmmux/create_agent --name researcher --provider gemini
```

From outside tmux (specify session):

```bash
~/.llmmux/create_agent --session llmmux --name coder --prompt "Implement auth"
```

## Configuration

### Default Settings

Edit `~/.llmmux/.default_env` to change system-wide defaults.

### User Overrides

Create `~/.llmmux/.env` to override defaults:

```bash
# Set default provider
LLMMUX_DEFAULT_PROVIDER=agent

# Set default session name
LLMMUX_DEFAULT_SESSION=myproject

# Enable auto-attach
LLMMUX_AUTO_ATTACH=true
```

## Available Skills

Skills are located in provider-specific directories:

- `~/.cursor/skills/` - Cursor/Agent skills
- `~/.claude/skills/` - Claude skills
- `~/.gemini/skills/` - Gemini skills
- `~/.codex/skills/` - Codex skills

Common skills include:
- `vue3-typescript` - Vue 3 + TypeScript frontend
- `django-backend-dev` - Django backend development
- `tailwind-bem-stylist` - Tailwind CSS styling
- `multi-agent-orchestrator` - Complex project orchestration

## tmux Basics

See [TMUX_CHEATSHEET.md](TMUX_CHEATSHEET.md) for comprehensive tmux reference.

Quick commands:
- `Ctrl+b w` - List and switch windows
- `Ctrl+b n` - Next window
- `Ctrl+b p` - Previous window
- `Ctrl+b d` - Detach (keeps session running)
- `Ctrl+b [` - Enter copy mode (scroll)

## Workflow Example

```bash
# 1. Create session
cd ~/projects/myapp
~/.llmmux/orchestrator --provider agent --session-name myapp

# 2. Attach
tmux attach -t myapp

# 3. Tell orchestrator: "Build a todo app with Vue and Django"

# 4. Orchestrator creates plan and spawns agents:
#    - django-agent for backend
#    - vue-agent for frontend

# 5. Monitor progress in separate windows (Ctrl+b w to switch)

# 6. Create additional agents (from within tmux)
~/.llmmux/create_agent --name researcher --skill research-analyst

# 6. Detach when done (Ctrl+b d) - agents keep running

# 7. Re-attach later
tmux attach -t myapp

# 8. Clean up when complete
tmux kill-session -t myapp
```

Tip: say “please setup handoff for the next session” to prompt the orchestrator to write `handoff.md`, `run_state.json`, and `tasks.json` for an easy resume.

## Files in this Directory

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main entry point - creates sessions |
| `create_agent.py` | Spawns agent windows |
| `INIT_ORCHESTRATOR.md` | Bootstrap instructions for orchestrator LLM |
| `TMUX_CHEATSHEET.md` | Comprehensive tmux reference |
| `.default_env` | Default configuration |
| `README.md` | This file |

## Troubleshooting

### "tmux not found"

Install tmux:
```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt install tmux
```

### "Session already exists"

The orchestrator will prompt you to:
1. Keep old and create new with suffix (e.g., `llmmux(1)`)
2. Kill old and start fresh
3. Quit

### "python-dotenv not found"

Install required Python package:
```bash
pip install python-dotenv
```

### Checking Session State

```bash
# View current state
cat ~/.llmmux/state/llmmux/handoff.md
cat ~/.llmmux/state/llmmux/run_state.json

# List all sessions
tmux ls

# List windows in session
tmux list-windows -t llmmux
```

## Advanced Usage

### Multiple Projects

Use unique session names for different projects:

```bash
~/.llmmux/orchestrator --provider agent --session-name project-a
~/.llmmux/orchestrator --provider codex --session-name project-b
```

### Capture Agent Output

```bash
# Save output to file
tmux capture-pane -t llmmux:vue-agent -p > vue_output.txt

# Monitor in real-time (from another terminal)
tmux capture-pane -t llmmux:django-agent -p -S -100
```

### Provider-Specific Commands

The default commands can be overridden in `~/.llmmux/.env`:

```bash
PROVIDER_agent=agent --verbose '{prompt}'
PROVIDER_gemini=gemini -p '{prompt}' --temperature 0.7
```

## Dependencies

### Python Virtual Environment

llmmux automatically creates a virtual environment in `~/.llmmux/venv/` during sync and installs required dependencies:

- `python-dotenv` - For loading environment configuration

The wrapper scripts (`~/.llmmux/orchestrator` and `~/.llmmux/create_agent`) automatically activate this virtual environment before running the Python scripts.

### System Requirements

- Python 3.7+
- tmux
- curl/wget (for provider CLIs if not already installed)

## Related Projects

This system is inspired by:
- [codex-cli-farm](https://github.com/waskosky/codex-cli-farm)
- [cmux](https://github.com/manaflow-ai/cmux)
- [workmux](https://raine.dev/blog/introduction-to-workmux/)
