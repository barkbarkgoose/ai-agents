"""
run with `python tmux_test.py && tmux attach -t agents`

To see all agents running: ctrl+b then w (n = next, p = previous, 0-n = numbered agent)

--- w" should look something like this: ---

    (0) - agents: 4 windows (attached)
    (1) ├─> + 0: orchestrator-
    (2) ├─> + 1: researcher
    (3) ├─> + 2: coder*
    (4) └─> + 3: reviewer

-----

The tmux windows are completely independent from the Python process that spawned them. Once created, they live entirely within tmux and have no connection back to the parent script.

You can:

1. Break a pane into its own window (if you split a window into panes):
    `Ctrl+b` then `!` — breaks current pane into a new window

2. Move a window to a different session:
    `Ctrl+b` then `:` then type `move-window -t other_session`

3. Detach and the agents keep running:
    - `Ctrl+b` then `d` — detaches you from tmux, but all agents stay alive
    - Reattach anytime with `tmux attach -t agents`

4. Kill the Python script — doesn't affect the tmux windows at all

5. Link a window to multiple sessions (view same window from different sessions):
    - `tmux link-window -s agents:0 -t another_session`

The key insight: `subprocess.run()` just sends a command to the tmux server. After that, tmux owns those windows completely. The Python process could exit, crash, or be killed — the tmux session persists independently.

This is actually one of the big advantages of using tmux for agents: you get process isolation and persistence for free. Each agent's bash shell is its own process tree, managed by tmux, not by your Python orchestrator.
"""
import subprocess
import os


SESSION_NAME = "agents"


def kill_session_if_exists(session: str):
    """Kill existing tmux session to start fresh."""
    subprocess.run(
        ["tmux", "kill-session", "-t", session],
        stderr=subprocess.DEVNULL
    )


def spawn_agent(name: str, cmd: str, session: str = SESSION_NAME, new_window: bool = True):
    """
    Spawn an agent in a tmux window.
    
    Args:
        name: Window name for this agent
        cmd: Command to run in the window
        session: tmux session name
        new_window: If True, create new window in existing session; if False, create new session
    """
    if new_window:
        subprocess.run([
            "tmux", "new-window",
            "-t", session,
            "-n", name,
            cmd
        ])
    else:
        subprocess.run([
            "tmux", "new-session",
            "-d",
            "-s", session,
            "-n", name,
            cmd
        ])


def main():
    # Start fresh
    kill_session_if_exists(SESSION_NAME)
    
    # Define agents
    agents = [
        ("orchestrator", "gemini -p '🎯 Orchestrator Agent started'; exec bash"),
        ("researcher", "echo '🔍 Research Agent started'; exec bash"),
        ("coder", "echo '💻 Coder Agent started'; exec bash"),
        ("reviewer", "echo '📝 Reviewer Agent started'; exec bash"),
    ]
    
    # Spawn first agent as new session, rest as windows
    for i, (name, cmd) in enumerate(agents):
        spawn_agent(name, cmd, new_window=(i > 0))
    
    print(f"✅ Spawned {len(agents)} agents in tmux session '{SESSION_NAME}'")
    print(f"\nAttach with: tmux attach -t {SESSION_NAME}")
    print("Switch windows with: Ctrl+b then n (next) or p (previous)")
    print("List windows with: Ctrl+b then w")
    
    # Optionally auto-attach (uncomment if you want this behavior)
    # os.execvp("tmux", ["tmux", "attach", "-t", SESSION_NAME])


if __name__ == "__main__":
    main()