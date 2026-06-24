# tmux Cheatsheet

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
tmux attach -t mysession        # attach to existing
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

**Switching by name** (handy when you name windows after their agent):
```
Ctrl+b '          # then type the window name and Enter
```

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
capture-pane -t name -p          # print visible pane content
capture-pane -t name -p -S -100  # last 100 lines of pane
send-keys -t name "cmd" Enter    # type a command into another window
```

---

## Quick Reference

```
Sessions contain Windows contain Panes

┌─────────────────────────────────────────────┐
│ Session: work                               │
│ ┌─────────────┬─────────────┬─────────────┐ │
│ │ Window 0    │ Window 1    │ Window 2    │ │
│ │ shell       │ refactor    │ tests       │ │
│ │ ┌─────────┐ │             │ ┌────┬────┐ │ │
│ │ │  pane   │ │   (single   │ │pane│pane│ │ │
│ │ │         │ │    pane)    │ ├────┴────┤ │ │
│ │ │         │ │             │ │  pane     │ │
│ │ └─────────┘ │             │ └─────────┘ │
│ └─────────────┴─────────────┴─────────────┘ │
└─────────────────────────────────────────────┘
```

**Status bar anatomy:**
```
[work] 0:shell  1:refactor  2:tests* 3:review-
   │        │         │          │        │
   │        │         │          │        └─ * = current window
   │        │         │          └─ - = last active window
   │        └─────────┴─ window number:name
   └─ session name
```

---

## Tips

1. **Detach freely** — `Ctrl+b d` leaves everything running.
2. **Name your windows** — easier than remembering numbers.
3. **Use `Ctrl+b '`** to jump to a window by name.
4. **Zoom for focus** — `Ctrl+b z` toggles a pane fullscreen.
5. **Capture before switching** — `tmux capture-pane -t sess:win -p -S -200`
   saves the last 200 lines before you lose them off the screen.

---

## llmmux notes

llmmux uses vanilla tmux — no server config, no custom prefix, no extra
sockets. Your existing `~/.tmux.conf` keeps working. The two commands worth
remembering alongside llmmux:

```bash
# What windows are in my llmmux session?
tmux list-windows -t work -F '#{window_index}: #{window_name}'

# Dump the last bit of an agent's output to a file
tmux capture-pane -t work:refactor -p -S -500 > refactor.log

# Type a follow-up into another agent's pane from your shell
tmux send-keys -t work:refactor "stop and re-read tests/ first" Enter
```