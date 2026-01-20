# tmux Cheatsheet for Agent Development

All commands start with the **prefix**: `Ctrl+b`

---

## Sessions

| Action | Command |
|--------|---------|
| New session | `Ctrl+b` `:` `new-session -s name` |
| List sessions | `Ctrl+b` `s` |
| Next session | `Ctrl+b` `)` |
| Previous session | `Ctrl+b` `(` |
| Detach (leave running) | `Ctrl+b` `d` |
| Rename session | `Ctrl+b` `$` |
| Kill session | `Ctrl+b` `:` `kill-session` |

**From shell:**
```bash
tmux new -s mysession           # create and attach
tmux new -d -s mysession        # create detached
tmux attach -t mysession        # attach to existing (can open a new tab, attach to existing session, pull up window for specific agent)
tmux ls                         # list all sessions
tmux kill-session -t mysession  # kill session
```

---

## Windows (tabs within a session)

| Action | Command |
|--------|---------|
| New window | `Ctrl+b` `c` |
| Next window | `Ctrl+b` `n` |
| Previous window | `Ctrl+b` `p` |
| Window by number | `Ctrl+b` `0-9` |
| List windows (picker) | `Ctrl+b` `w` |
| Rename window | `Ctrl+b` `,` |
| Close window | `Ctrl+b` `&` |
| Move window to session | `Ctrl+b` `:` `move-window -t session` |
| Link window to session | `Ctrl+b` `:` `link-window -t session` |

---

## Panes (splits within a window)

| Action | Command |
|--------|---------|
| Split horizontal | `Ctrl+b` `"` |
| Split vertical | `Ctrl+b` `%` |
| Navigate panes | `Ctrl+b` `arrow keys` |
| Next pane | `Ctrl+b` `o` |
| Zoom pane (toggle) | `Ctrl+b` `z` |
| Break pane to window | `Ctrl+b` `!` |
| Close pane | `Ctrl+b` `x` |
| Resize pane | `Ctrl+b` `Ctrl+arrow` |
| Swap panes | `Ctrl+b` `{` or `}` |
| Rename pane title | `Ctrl+b` `:` `select-pane -T "title"` |
| Clear pane title | `Ctrl+b` `:` `select-pane -T ""` |
| Rename other pane | `Ctrl+b` `:` `select-pane -t 1 -T "title"` |

---

## Copy Mode (scrolling & copying)

| Action | Command |
|--------|---------|
| Enter copy mode | `Ctrl+b` `[` |
| Exit copy mode | `q` |
| Scroll up/down | `arrow keys` or `Page Up/Down` |
| Search forward | `/` then type search |
| Search backward | `?` then type search |
| Start selection | `Space` |
| Copy selection | `Enter` |
| Paste | `Ctrl+b` `]` |

---

## Useful Command Mode Commands

Enter command mode with `Ctrl+b` `:`

```
new-session -s name              # create new session
new-window -n name               # create named window
rename-window name               # rename current window
move-window -t session           # move window to session
link-window -t session           # link window to session (shared)
swap-window -t 0                 # swap with window 0
kill-window                      # kill current window
kill-session                     # kill current session
list-sessions                    # list all sessions
list-windows                     # list windows in session
```

---

## Python Spawning Reference

```python
import subprocess

SESSION = "agents"

# Kill existing session (clean start)
subprocess.run(["tmux", "kill-session", "-t", SESSION], stderr=subprocess.DEVNULL)

# Create new session with first window
subprocess.run([
    "tmux", "new-session", "-d",
    "-s", SESSION,
    "-n", "orchestrator",
    "echo 'Agent started'; exec bash"
])

# Add more windows to the session
subprocess.run([
    "tmux", "new-window",
    "-t", SESSION,
    "-n", "worker",
    "echo 'Worker started'; exec bash"
])

# Send command to a running window
subprocess.run([
    "tmux", "send-keys",
    "-t", f"{SESSION}:worker",
    "echo 'Hello from Python'",
    "Enter"
])

# Capture output from a pane
result = subprocess.run(
    ["tmux", "capture-pane", "-t", f"{SESSION}:worker", "-p"],
    capture_output=True, text=True
)
print(result.stdout)
```

---

## Quick Reference

```
Sessions contain Windows contain Panes

┌─────────────────────────────────────────────┐
│ Session: agents                             │
│ ┌─────────────┬─────────────┬─────────────┐ │
│ │ Window 0    │ Window 1    │ Window 2    │ │
│ │ orchestrator│ researcher  │ coder       │ │
│ │ ┌─────────┐ │             │ ┌────┬────┐ │ │
│ │ │  pane   │ │   (single   │ │pane│pane│ │ │
│ │ │         │ │    pane)    │ ├────┴────┤ │ │
│ │ └─────────┘ │             │ │  pane     │ │
│ └─────────────┴─────────────┴─────────────┘ │
└─────────────────────────────────────────────┘
```

**Status bar anatomy:**
```
[agents] 0:orchestrator  1:researcher  2:coder- 3:reviewer*
   │           │              │            │          │
   │           │              │            │          └─ * = current window
   │           │              │            └─ - = last active window
   │           └──────────────┴─ window number:name
   └─ session name
```

---

## Tips for Agent Development

1. **Detach freely** — `Ctrl+b` `d` leaves everything running
2. **One session per project** — keeps agents organized
3. **Name your windows** — easier than remembering numbers
4. **Use `send-keys`** — lets Python orchestrator communicate with agents
5. **Use `capture-pane`** — lets Python read agent output
6. **Zoom for focus** — `Ctrl+b` `z` toggles fullscreen on a pane

---

## llmmux-Specific Usage

### Creating an llmmux Session

```bash
# From your project directory
cd /path/to/project
~/.llmmux/orchestrator --provider agent

# Or specify all options
~/.llmmux/orchestrator --provider codex --session-name myproject --project-root ~/projects/myapp
```

### Adding Agents to Running Session

```bash
# From within tmux (auto-detects current session)
~/.llmmux/create_agent --name vue-agent --skill vue3-typescript

# From outside tmux (specify session)
~/.llmmux/create_agent --name django-agent --session llmmux --prompt "Create REST API"

# With specific provider
python3 ~/.llmmux/create_agent.py --name researcher --provider gemini --prompt "Research best practices"
```

### Viewing Agent Output

```bash
# Switch to agent window
Ctrl+b w                    # then select from list

# Or use window list shortcut
Ctrl+b '                    # then type window name

# Capture output programmatically
tmux capture-pane -t llmmux:vue-agent -p > output.txt
```

### State Files

llmmux maintains state in `~/.llmmux/state/<session-name>/`:

- `handoff.md` - Human-readable progress narrative
- `run_state.json` - Machine-readable state index
- `tasks.json` - Task queue and planning
- `agents/*.last.json` - Per-agent state snapshots
- `logs/*.log` - Agent output logs

### Useful llmmux Commands

```bash
# List all llmmux sessions
tmux ls | grep llmmux

# Attach to specific llmmux session
tmux attach -t llmmux

# Kill llmmux session when done
tmux kill-session -t llmmux

# View state files
cat ~/.llmmux/state/llmmux/handoff.md
cat ~/.llmmux/state/llmmux/run_state.json
```

### Best Practices for llmmux

1. **One session per project** — Use meaningful session names
2. **Document in handoff.md** — Keep the narrative current for continuity
3. **Update run_state.json** — Track agent status and artifacts
4. **Check logs regularly** — Each agent writes to `logs/<agent-name>.log`
5. **Use artifacts directory** — Save diffs, reports to `~/.llmmux/artifacts/<session>/`
6. **Detach vs Kill** — Detach preserves running agents, kill stops everything
