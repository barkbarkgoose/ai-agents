## From a fresh clone to a running orchestrator

### 1. Prerequisites (one-time per machine)

You need four things on your `PATH`:

| Tool | Why | Install |
|------|-----|---------|
| **Python 3.7+** | Runs `orchestrator.py` / `create_agent.py` | `brew install python` / system pkg / pyenv |
| **Node.js 20+** | Runs `pi` (verified by `verify_pi_environment`) | `brew install node@20` or nvm |
| **`pi`** | The actual subagent harness | `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` |
| **`tmux`** | Manages the agent panes | `brew install tmux` |

You'll also want `uv` for the Python deps: `brew install uv` (or `pipx install uv`).

Authenticate `pi` by exporting at least one provider key. Which keys you need depends on which models you pick (see step 5):

```bash
export GEMINI_API_KEY=...       # for --provider gemini
export ANTHROPIC_API_KEY=...   # for --provider claude / sonnet / opus
export DEEPSEEK_API_KEY=...    # for deepseek models
# etc. — see https://github.com/earendil-works/pi for the full env-var list
```

### 2. Get the code

```bash
git clone <repo-url> llmmux
cd llmmux
```

### 3. Install Python deps

```bash
uv venv
uv pip install -r requirements.txt
```

That's one Python package: `python-dotenv`.

### 4. (Optional) configure defaults

Edit `.default_env` for system-wide defaults, or copy it to `.env` for per-user overrides:

```bash
cp .default_env .env
$EDITOR .env   # set LLMMUX_DEFAULT_PROVIDER=claude, etc.
```

### 5. Pick a provider

The `llmmux` "provider" is just shorthand for a `pi --model <value>` argument. The default registry:

| `--provider` | `pi --model` | Needs |
|---|---|---|
| `claude` (default recommended) | `anthropic/claude-sonnet-4-5` | `ANTHROPIC_API_KEY` |
| `gemini` | `google/gemini-2.5-pro` | `GEMINI_API_KEY` |
| `codex` / `agent` / `opencode` / `kilo` | `openai-codex/gpt-5.4` | OpenAI auth |
| `sonnet` | `anthropic/claude-sonnet-4-5` | `ANTHROPIC_API_KEY` |
| `opus` | `anthropic/claude-opus-4-1` | `ANTHROPIC_API_KEY` |
| `gpt` | `openai-codex/gpt-5.5` | OpenAI auth |
| `minimax` | `minimax/MiniMax-M2.7` | `MINIMAX_API_KEY` |

You can also override the model for any provider via env var (without editing code):

```bash
export LLMMUX_PI_MODEL_CLAUDE=anthropic/claude-opus-4-1
```

Or pass a raw `pi` model string straight through `--provider google/gemma-4:high`.

### 6. Boot a session

From the project you want to work on:

```bash
cd ~/projects/myapp
uv run orchestrator.py --provider claude --session-name myapp
```

What happens behind the scenes:

1. `verify_pi_environment()` checks node ≥ 20 and `pi --version`. If either is missing, you get a clean install message and it exits.
2. `~/.llmmux/state/<session-id>/` and `~/.llmmux/artifacts/<session-id>/` are created.
3. An `AGENTS.md` is written into `~/projects/myapp/` containing bootstrap pointers to `INIT_ORCHESTRATOR.md`.
4. `tmux new-session -d -s myapp -n orchestrator -c ~/projects/myapp` creates the tmux session rooted at your project.
5. `tmux send-keys` runs `pi --model anthropic/claude-sonnet-4-5 'orchestrator agent: refer to ~/.llmmux/INIT_ORCHESTRATOR.md'` inside that pane. `pi` boots in the project dir, auto-loads `AGENTS.md`, and starts its interactive TUI.

### 7. Drive the orchestrator

```bash
tmux attach -t myapp
```

You're now inside `pi`. Tell it what you want ("build a Vue 3 todo app with a Django REST backend") and it will:

- Plan tasks in `~/.llmmux/state/<session-id>/tasks.json`
- Spawn specialized subagents via `create_agent.py`

### 8. Spawn subagents

The orchestrator does this for you, but you can also do it manually from inside any tmux pane:

```bash
# Interactive coder pane (stays in pi TUI)
uv run create_agent.py --name django-coder --skill django-backend-dev

# One-shot task (pi -p; pane closes when the task is done)
uv run create_agent.py --name code-formatter \
    --provider claude --prompt "Run black on src/" --oneshot
```

For each agent, `create_agent.py`:

1. Resolves the worker dir: `~/.llmmux/state/<session-id>/agents/<agent-name>/`
2. Writes an `AGENTS.md` there with the agent's prompt + session metadata
3. `tmux new-window -t myapp -n django-coder -c <worker_dir>` so `pi` boots in the right cwd and picks up that `AGENTS.md`
4. Sends the `pi --model ... '<prompt>'` (or `pi -p '<prompt>'` if `--oneshot`) into the pane

### 9. Work the workflow

```
┌─ tmux session: myapp ────────────────────────────────────┐
│                                                           │
│  ┌─ orchestrator (pi, interactive) ─────────────────────┐ │
│  │  AGENTS.md in ~/projects/myapp/                      │ │
│  │  Planning, spawning agents, updating run_state.json  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─ django-coder (pi) ──────────┐  ┌─ vue-coder (pi) ──┐ │
│  │  AGENTS.md in worker dir     │  │  ...               │ │
│  │  interactive TUI             │  │  interactive TUI   │ │
│  └──────────────────────────────┘  └────────────────────┘ │
│                                                           │
│  ┌─ code-formatter (pi -p) ─────────────────────────────┐ │
│  │  one-shot: ran, output captured, window closed       │ │
│  └──────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

Switch panes with `Ctrl+b w`. State persists in `~/.llmmux/state/<session-id>/` between sessions, so you can `Ctrl+b d`, walk away, and `tmux attach -t myapp` later.

### 10. Tear down

```bash
tmux kill-session -t myapp
```

State and artifacts are preserved on disk for re-attach or next session.

### TL;DR

```bash
# one-time setup
brew install uv node@20 tmux
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
export ANTHROPIC_API_KEY=...   # or whichever provider you use

# per repo
cd llmmux && uv venv && uv pip install -r requirements.txt
cd ~/your-project
uv run /path/to/llmmux/orchestrator.py --provider claude --session-name myapp
tmux attach -t myapp
```

---

