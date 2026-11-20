# llmmux

Spin up parallel chat panes in tmux, each running a local-agent CLI (default `pi`).
No orchestrator, no shared state, no handoff protocol — just tmux panes you control.

## What it does

```
llmmux new work                       # create a tmux session named "work"
llmmux chat refactor --cwd ~/myapp    # open a pi pane rooted in ~/myapp
llmmux chat review   --cwd ~/myapp --prompt "watch the refactor pane"
llmmux attach work                    # hop in, Ctrl+b n/p/w to switch panes
```

That's it. Each `chat` command opens a new tmux window in the session, runs the
agent CLI in it, and (if you pass `--prompt`) writes the prompt as an
`AGENTS.md` in the pane's working directory so the agent boots with context.

You are the orchestrator. Switch between panes, copy/paste between them,
interject follow-ups. When you detach (`Ctrl+b d`), everything keeps running.

## Install

Requirements:

- **tmux** — `brew install tmux` / `apt install tmux`
- **bash 4+** (macOS ships 3.2; the script uses `set -euo pipefail` + arrays, no bashisms beyond that)
- **pi** (default agent CLI) — node >= 20, then `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`
  - Or skip and set `LLMMUX_AGENT_CMD` to whatever CLI you prefer (`claude`, `codex`, `aider`, …).

Put `llmmux` on your `$PATH`:

```bash
# Either symlink it:
ln -s /path/to/llmmux/llmmux ~/bin/llmmux

# Or call it directly:
/path/to/llmmux/llmmux --help
```

Authenticate `pi` (or your replacement CLI) however it expects — env vars like
`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc., or `--api-key`
flags. llmmux doesn't manage credentials.

## Usage

### Create a session

```bash
llmmux new <name> [--cwd DIR]
```

Creates a detached tmux session. `<name>` is the tmux session name. `--cwd`
sets the starting directory for the first window (defaults to `$PWD`).

```bash
llmmux new work
llmmux new myapp --cwd ~/code/myapp
```

### Open a chat pane

```bash
llmmux chat <name> [--cwd DIR] [--provider P] [--prompt "..."] [--oneshot] [--write-agents-md] [--cmd "..."]
```

Opens a new tmux window named `<name>` in the current/auto-detected session
and runs the agent CLI in it.

| Flag | Default | Purpose |
|---|---|---|
| `--cwd DIR` | `$PWD` | Working directory for the pane. Where `pi` boots and where it auto-reads `AGENTS.md`. |
| `--provider P` | `$LLMMUX_DEFAULT_PROVIDER` (or `gemini-flash`) | Provider shortcut or raw `pi --model` string. |
| `--prompt "..."` | — | Initial task. Written to `AGENTS.md` in `--cwd` so the agent boots with it as context (append-only if `AGENTS.md` exists; requires `--write-agents-md` to create a new file). |
| `--oneshot` | off | Run a non-interactive task: `pi --model X -p "..."`. Window closes when the task finishes. |
| `--write-agents-md` | off | Allow llmmux to create a new `AGENTS.md` in `--cwd` when one doesn't exist. Without this flag, a fresh `--prompt` is silently dropped at the file layer (the pane still gets the prompt via the agent CLI's own argv). |
| `--cmd "..."` | — | Override the entire agent command. Useful for non-`pi` CLIs or custom wrappers. |

If you run `llmmux chat` from inside a tmux session, it auto-targets that
session. From outside, it targets the only existing session, or fails if
there are multiple (set `LLMMUX_SESSION=<name>` to disambiguate).

**Examples:**

```bash
# Interactive pane, default model, just opens a fresh pi TUI in ~/myapp
llmmux chat refactor --cwd ~/myapp

# Same, but pre-seeded with a task
llmmux chat refactor --cwd ~/myapp \
    --provider gemini-pro \
    --prompt "Refactor the auth module. Don't touch tests."

# One-shot: run a task and close the window
llmmux chat format --cwd ~/myapp \
    --provider gemini-flash \
    --prompt "Run prettier --write on src/" \
    --oneshot

# Persist the prompt into a fresh AGENTS.md in the project (otherwise only an
# existing AGENTS.md is appended to).
llmmux chat refactor --cwd ~/myapp \
    --provider gemini-pro \
    --prompt "Refactor the auth module." \
    --write-agents-md

# Use a different model for one pane
llmmux chat deep-review --cwd ~/myapp --provider opus

# Use a completely different CLI
llmmux chat claude-review --cwd ~/myapp --cmd "claude --model sonnet"
```

### List, attach, kill

```bash
llmmux ls                # list all tmux sessions
llmmux attach <name>     # attach to session (Ctrl+b d to detach)
llmmux kill <name>       # kill the whole session
llmmux kill-window <s> <w>   # kill just one window
```

### Inside tmux

The `TMUX_CHEATSHEET.md` covers everything. The short version:

| Action | Keys |
|---|---|
| Switch panes by name | `Ctrl+b '` then type name |
| Pane picker | `Ctrl+b w` |
| Next / prev window | `Ctrl+b n` / `Ctrl+b p` |
| Detach (keep running) | `Ctrl+b d` |
| Scroll / copy | `Ctrl+b [` then `Space` to select, `Enter` to copy |
| Paste | `Ctrl+b ]` |

## Configuration

Two env files, loaded in order (later wins):

1. **`<repo>/.default_env`** — checked-in defaults: provider → model mappings, default provider, agent CLI template.
2. **`~/.llmmux/.env`** — your overrides. Create this file; it's never overwritten.

### Provider shortcuts

`--provider` accepts either a shortcut or a raw `pi` model string. Shortcuts
resolve via `LLMMUX_PI_MODEL_<NAME>`:

```bash
# ~/.llmmux/.env
LLMMUX_PI_MODEL_GEMINI_FLASH=google/gemini-2.5-flash
LLMMUX_PI_MODEL_CLAUDE=anthropic/claude-sonnet-4-5
LLMMUX_PI_MODEL_MINIMAX=minimax/MiniMax-M2.7
```

Then:

```bash
llmmux chat foo --provider claude      # -> pi --model anthropic/claude-sonnet-4-5
llmmux chat bar --provider gpt-5.5     # -> pi --model openai-codex/gpt-5.5 (if mapped)
llmmux chat baz --provider raw-string  # -> pi --model raw-string (passthrough)
```

Unset shortcuts fall through as raw model strings. So `llmmux chat foo
--provider gpt-5.5` works even if you haven't configured a mapping — it
just passes `gpt-5.5` straight to `pi`.

### Defaults

```bash
# ~/.llmmux/.env
LLMMUX_DEFAULT_PROVIDER=claude   # used when --provider is omitted
```

### Swapping the agent CLI

By default, `llmmux chat` runs `pi --model <model> <prompt>`. Swap to any
other CLI by overriding the template:

```bash
# ~/.llmmux/.env
LLMMUX_AGENT_CMD='claude --model %s %s'
LLMMUX_AGENT_CMD_ONESHOT='claude --model %s -p %s'
```

Two `%s` placeholders: model, then prompt (or empty if you didn't pass
`--prompt`). Use `--cmd` per-pane to override without changing the default.

## Workflow example

You're working on `~/code/myapp` and want three parallel chats on it — one
refactoring, one writing tests, one reviewing.

```bash
# One-time setup (only if you want to customize defaults)
echo 'LLMMUX_DEFAULT_PROVIDER=gemini-flash' >> ~/.llmmux/.env

# Start a session
llmmux new work

# Open three panes, all rooted in ~/code/myapp
llmmux chat refactor --cwd ~/code/myapp --provider gemini-pro \
    --prompt "Refactor the auth module. Read README.md first. Don't touch tests."

llmmux chat tests --cwd ~/code/myapp \
    --prompt "Bring test coverage on src/auth/ to 80%. Run pytest after every change."

llmmux chat review --cwd ~/code/myapp \
    --prompt "Watch the refactor and tests panes. Flag inconsistencies."

# Hop in
llmmux attach work

# Inside: Ctrl+b ' then "refactor" to jump. Ctrl+b w for the picker.
# Interject in any pane by typing. Copy with Ctrl+b [, paste with Ctrl+b ].
# Detach with Ctrl+b d.

# Tomorrow: same command, same state, same history.
llmmux attach work

# Done? Kill the whole session.
llmmux kill work
```

## What llmmux doesn't do

- **No orchestrator.** No agent spawns other agents. You are the orchestrator.
- **No shared state files.** No `handoff.md`, `run_state.json`, `tasks.json`,
  or `agents/*.last.json`. tmux is the state. `tmux ls` tells you what's
  running. `Ctrl+b w` tells you what panes exist. That's enough.
- **No cross-pane automation.** No "agent A hands off to agent B". If you
  want one pane's output in another, copy/paste it (`Ctrl+b [`, `Space`,
  `Enter`, `Ctrl+b ]`).
- **No provider skill resolution.** Drop a `SKILL.md` reference into the
  pane's `AGENTS.md` (auto-written from `--prompt`) and the agent picks it
  up via its own skill loader.
- **No tmux config management.** llmmux uses your existing tmux server and
  config. Configure your prefix, status bar, etc. in `~/.tmux.conf` like
  always.

## Files

| File | Purpose |
|---|---|
| `llmmux` | The CLI script. Single bash file, no dependencies beyond tmux + your chosen agent CLI. |
| `.default_env` | Checked-in defaults: provider mappings, agent CLI template. |
| `~/.llmmux/.env` | Your overrides. Created by you. |
| `TMUX_CHEATSHEET.md` | tmux reference. |

## Troubleshooting

**`tmux: command not found`** — install tmux (`brew install tmux`).

**`no tmux session exists`** — run `llmmux new <name>` first.

**`multiple tmux sessions exist; specify one`** — `llmmux` targets the
current session when run from inside tmux, or the only session when there's
just one. If you're outside tmux and have multiple, set
`LLMMUX_SESSION=<name>` for the command, or `tmux attach` to the one you
want and run `llmmux chat` from there.

**`window '<name>' already exists`** — tmux window names are unique within
a session. Pick a different name, or `llmmux kill-window <session> <name>`
first.

**`pi: command not found`** — install pi (`npm install -g --ignore-scripts
@earendil-works/pi-coding-agent`) or point `LLMMUX_AGENT_CMD` at a different
CLI.

**Want to start completely fresh?** `tmux kill-server` kills all sessions;
your `~/.llmmux/.env` is untouched.

## License

Pick one — none specified. Use as you see fit.