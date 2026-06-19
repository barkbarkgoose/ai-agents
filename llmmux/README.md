# llmmux - tmux-based Multi-Agent Orchestrator

A tmux-based orchestration system for managing multiple LLM agents in isolated windows with persistent state management.

## Overview

llmmux creates tmux sessions where each agent runs in its own window. An orchestrator agent coordinates the workflow, spawning specialized agents as needed and maintaining state across sessions.

## Quick Start

### 1. Install Dependencies

From the project root:

```bash
uv venv
uv pip install -r requirements.txt
```

This creates a `.venv/` and installs `python-dotenv`.

### 2. Create an Orchestrator Session

```bash
cd /path/to/your/project
uv run orchestrator.py --provider claude
```

The orchestrator writes an `AGENTS.md` into your project root and launches `pi` in a tmux window. `pi` auto-loads `AGENTS.md` from cwd, so all bootstrap instructions flow through that file rather than the CLI.

Available providers (each maps to a `pi --model` value):

| Provider | pi model |
|----------|----------|
| `claude` | `anthropic/claude-sonnet-4-5` |
| `gemini` | `google/gemini-2.5-pro` |
| `codex` / `agent` / `opencode` / `kilo` | `openai-codex/gpt-5.4` |
| `sonnet` | `anthropic/claude-sonnet-4-5` |
| `opus` | `anthropic/claude-opus-4-1` |
| `gpt` | `openai-codex/gpt-5.5` |
| `minimax` | `minimax/MiniMax-M2.7` |

Override per-provider with `LLMMUX_PI_MODEL_<NAME>` (e.g. `LLMMUX_PI_MODEL_CLAUDE=anthropic/claude-opus-4-1`), or pass a raw `pi` model string directly as `--provider` (e.g. `--provider google/gemma-4:high`).

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
# Interactive TUI pane (stays open after initial prompt)
uv run create_agent.py --name vue-agent --skill vue3-typescript

# One-shot execution (pi -p, window closes when done)
uv run create_agent.py --name coder --provider claude --prompt "Fix the auth bug" --oneshot

# With a custom prompt
uv run create_agent.py --name django-agent --prompt "Create REST API"

# Specific provider
uv run create_agent.py --name researcher --provider gemini
```

Each agent gets its own working directory at `~/.llmmux/state/<session-id>/agents/<agent-name>/`. `create_agent.py` writes an `AGENTS.md` there before spawning the tmux pane, so `pi` boots with the right context.

From outside tmux (specify session):

```bash
uv run create_agent.py --session llmmux --name coder --prompt "Implement auth"
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
| `orchestrator.py` | Main entry point - creates tmux sessions, launches `pi` orchestrator |
| `create_agent.py` | Spawns agent tmux windows; writes per-agent `AGENTS.md`; supports `--oneshot` (`pi -p`) |
| `utils.py` | Shared module: env loading, session lookup, state path resolution, `pi` command templating, environment verification |
| `INIT_ORCHESTRATOR.md` | Bootstrap instructions for orchestrator LLM |
| `INIT_AGENT.md` | Bootstrap instructions for subagent LLMs |
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

llmmux has two runtime dependencies:

- `python-dotenv` (Python) — declared in `requirements.txt`
- `pi` (Node.js) — the [earendil-works/pi-coding-agent](https://github.com/earendil-works/pi) CLI, installed globally

### Install with uv (recommended)

```bash
# 1. Python deps
uv venv
uv pip install -r requirements.txt

# 2. pi CLI (node >= 20 required)
npm install -g --ignore-scripts @earendil-works/pi-coding-agent

# 3. Authenticate pi via env vars (or use `pi --api-key` at runtime)
export GEMINI_API_KEY=...
export DEEPSEEK_API_KEY=...

# 4. Run
uv run orchestrator.py --provider claude
uv run create_agent.py --name vue-agent --skill vue3-typescript
```

The Python scripts automatically verify that `node >= 20` and the `pi` binary are on PATH and print setup instructions if they're missing.

### Install with pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

### System Requirements

- Python 3.7+
- Node.js 20+
- tmux
- curl/wget (for installing provider CLIs if not already installed)

## Related Projects

This system is inspired by:
- [codex-cli-farm](https://github.com/waskosky/codex-cli-farm)
- [cmux](https://github.com/manaflow-ai/cmux)
- [workmux](https://raine.dev/blog/introduction-to-workmux/)
