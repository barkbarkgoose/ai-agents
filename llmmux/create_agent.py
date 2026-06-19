#!/usr/bin/env python3
"""
create_agent.py - Spawn a new agent window in the current tmux session

This script is called by the orchestrator (or manually) to create new agent
windows within an existing llmmux session.

Usage:
    python create_agent.py --name vue-agent --prompt "Setup Vue 3 frontend"
    python create_agent.py --name django-agent --provider codex --skill django-backend-dev
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from utils import (
    LLMMUX_HOME,
    VALID_PROVIDERS,
    load_environment,
    session_exists,
    resolve_state_dir,
    resolve_pi_model,
    verify_pi_environment,
    write_agents_md,
    get_provider_command,
)


INIT_AGENT_FILENAME = "INIT_AGENT.md"


def load_agent_init_text() -> str:
    """Load shared agent instructions from INIT_AGENT.md if present."""
    candidates = [
        LLMMUX_HOME / INIT_AGENT_FILENAME,
        Path(__file__).resolve().parent / INIT_AGENT_FILENAME,
    ]

    for path in candidates:
        if path.exists():
            return path.read_text().strip()

    return ""


def get_current_session() -> str:
    """
    Detect current tmux session from environment.
    Returns session name or None if not in tmux.
    """
    tmux_pane = os.getenv("TMUX_PANE")
    
    if not tmux_pane:
        return None
    
    # Get current session name
    result = subprocess.run(
        ["tmux", "display-message", "-p", "#S"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return result.stdout.strip()
    
    return None


def get_session_name(args_session: str = None) -> str:
    """
    Get session name from args, environment, or prompt.
    Priority: args > current session > prompt
    """
    if args_session:
        if not session_exists(args_session):
            print(f"Error: Session '{args_session}' does not exist")
            sys.exit(1)
        return args_session
    
    # Try to detect current session
    current = get_current_session()
    if current:
        return current
    
    # Prompt user
    print("Not in a tmux session. Available sessions:")
    result = subprocess.run(
        ["tmux", "list-sessions", "-F", "#S"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        sessions = result.stdout.strip().split("\n")
        if sessions and sessions[0]:
            for i, session in enumerate(sessions, 1):
                print(f"  {i}. {session}")
            
            while True:
                choice = input("\nSelect session (name or number): ").strip()
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(sessions):
                        return sessions[idx]
                elif choice in sessions:
                    return choice
                else:
                    print("Invalid choice")
    
    print("No tmux sessions found. Create one with orchestrator.py first.")
    sys.exit(1)


def get_agent_name(args_name: str = None) -> str:
    """Get agent name from args or prompt"""
    if args_name:
        return args_name
    
    while True:
        name = input("Enter agent window name: ").strip()
        if name:
            return name
        print("Agent name cannot be empty")


def get_provider(args_provider: str = None) -> str:
    """Get provider from args, environment, or prompt"""
    # Check args
    if args_provider:
        if args_provider not in VALID_PROVIDERS:
            print(f"Error: Invalid provider '{args_provider}'")
            print(f"Valid providers: {', '.join(VALID_PROVIDERS)}")
            sys.exit(1)
        return args_provider
    
    # Check environment for default
    env_provider = os.getenv("LLMMUX_DEFAULT_PROVIDER")
    if env_provider and env_provider in VALID_PROVIDERS:
        use_default = input(f"Use default provider '{env_provider}'? [Y/n]: ").strip().lower()
        if use_default in ["", "y", "yes"]:
            return env_provider
    
    # Prompt
    print("\nAvailable providers:")
    for i, provider in enumerate(VALID_PROVIDERS, 1):
        print(f"  {i}. {provider}")
    
    while True:
        choice = input("\nSelect provider (name or number): ").strip().lower()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(VALID_PROVIDERS):
                return VALID_PROVIDERS[idx]
        elif choice in VALID_PROVIDERS:
            return choice
        else:
            print(f"Invalid choice. Choose from: {', '.join(VALID_PROVIDERS)}")


def get_prompt_text(args_prompt: str = None, args_skill: str = None) -> str:
    """
    Get prompt text from args or construct from skill reference.
    Priority: explicit prompt > skill reference > interactive prompt
    """
    if args_prompt:
        return args_prompt
    
    if args_skill:
        # Try to find skill file in provider directories
        provider_dirs = [
            Path.home() / ".cursor" / "skills" / args_skill,
            Path.home() / ".claude" / "skills" / args_skill,
            Path.home() / ".gemini" / "skills" / args_skill,
            Path.home() / ".codex" / "skills" / args_skill,
        ]
        
        for skill_dir in provider_dirs:
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                return f"refer to skill: {skill_file}"
        
        # Skill not found, use generic reference
        return f"use skill: {args_skill}"
    
    # Interactive prompt
    print("\nEnter agent prompt (press Ctrl+D when done):")
    print("(or press Enter to use a generic task prompt)")
    
    try:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        prompt = "\n".join(lines).strip()
        if prompt:
            return prompt
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(0)
    
    # Default generic prompt
    return "You are a specialized agent. Ask the user what task you should work on."


def create_agent_window(
    session_name: str,
    agent_name: str,
    provider: str,
    prompt: str,
    worker_dir: Path,
    mode: str = "interactive",
):
    """
    Create a new tmux window for the agent and send the `pi` command.

    The window is created with `-c worker_dir` so `pi` boots in the right
    working directory and auto-loads the AGENTS.md we wrote there.

    Args:
        mode: "interactive" -> pane stays in pi TUI.
              "oneshot"     -> pi runs the task and exits (window will close).
    """
    # Check if window already exists
    result = subprocess.run(
        ["tmux", "list-windows", "-t", session_name, "-F", "#W"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        existing_windows = result.stdout.strip().split("\n")
        if agent_name in existing_windows:
            print(f"Warning: Window '{agent_name}' already exists in session '{session_name}'")
            overwrite = input("Create anyway (will rename existing)? [y/N]: ").strip().lower()
            if overwrite not in ["y", "yes"]:
                print("Cancelled")
                return

    # Create new window rooted at worker_dir so pi picks up AGENTS.md.
    worker_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nCreating window '{agent_name}' in session '{session_name}' (cwd: {worker_dir})...")
    subprocess.run([
        "tmux", "new-window",
        "-t", session_name,
        "-n", agent_name,
        "-c", str(worker_dir),
    ], check=True)

    # Build the `pi` command.
    pi_model = resolve_pi_model(provider)
    command = get_provider_command(provider, prompt, mode=mode)
    print(f"Launching agent via `pi` (model: {pi_model}, mode: {mode})...")

    try:
        subprocess.run([
            "tmux", "send-keys",
            "-t", f"{session_name}:{agent_name}",
            command,
            "C-m",  # Enter key
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: failed to send command to tmux window: {e}", file=sys.stderr)
        sys.exit(1)

    # Create agent state file
    state_dir = resolve_state_dir(session_name) / "agents"
    if state_dir.exists():
        from datetime import datetime

        agent_state = {
            "name": agent_name,
            "provider": provider,
            "pi_model": pi_model,
            "mode": mode,
            "worker_dir": str(worker_dir),
            "prompt": prompt,
            "created_at": datetime.now().isoformat(),
            "status": "running",
            "last_action": "created",
            "last_run_ts": datetime.now().isoformat()
        }

        state_file = state_dir / f"{agent_name}.last.json"
        with open(state_file, "w") as f:
            json.dump(agent_state, f, indent=2)

    print(f"\n✓ Agent '{agent_name}' created successfully!")
    print(f"\nSwitch to agent window:")
    print(f"  Ctrl+b w   (then select {agent_name})")
    print(f"  Ctrl+b '   (then type {agent_name})")


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Create a new agent window in an existing llmmux tmux session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --name vue-agent --prompt "Setup Vue 3 frontend"
  %(prog)s --name django-agent --skill django-backend-dev
  %(prog)s --name researcher --provider gemini
  
  # When called from within a tmux session, --session is auto-detected
  %(prog)s --name coder --provider codex --prompt "Implement user auth"

Provider Skills:
  Skills are located in provider-specific directories:
    ~/.cursor/skills/
    ~/.claude/skills/
    ~/.gemini/skills/
    ~/.codex/skills/
        """
    )
    
    parser.add_argument(
        "--name",
        type=str,
        help="Name for the agent window"
    )
    
    parser.add_argument(
        "--provider",
        type=str,
        choices=VALID_PROVIDERS,
        help="LLM provider to use (gemini, agent, codex, claude, opencode)"
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="Initial prompt/task for the agent"
    )
    
    parser.add_argument(
        "--skill",
        type=str,
        help="Skill name to reference (e.g., 'vue3-typescript', 'django-backend-dev')"
    )
    
    parser.add_argument(
        "--session",
        type=str,
        help="Target tmux session (auto-detected if running in tmux)"
    )

    parser.add_argument(
        "--oneshot",
        action="store_true",
        help="Run `pi -p` (non-interactive) instead of the interactive TUI. "
             "The tmux window will close once the task completes."
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()

    # Verify `pi` (node >= 20 and the `pi` binary) is available.
    if not verify_pi_environment():
        sys.exit(1)

    # Load environment
    load_environment()

    # Get configuration
    session_name = get_session_name(args.session)
    agent_name = get_agent_name(args.name)
    provider = get_provider(args.provider)
    prompt = get_prompt_text(args.prompt, args.skill)
    state_dir = resolve_state_dir(session_name)
    agent_state_path = state_dir / "agents" / f"{agent_name}.last.json"
    init_text = load_agent_init_text()
    if init_text:
        prompt = f"{init_text}\n\nAgent state file: {agent_state_path}\n\n---\n\n{prompt}"
    else:
        prompt = f"Agent state file: {agent_state_path}\n\n{prompt}"

    # Worker dir = per-agent subdirectory under the session's state dir.
    # We write AGENTS.md here so `pi` boots with the right context.
    worker_dir = state_dir / "agents" / agent_name
    agents_md_content = (
        f"# llmmux Agent: {agent_name} (session: {session_name})\n\n"
        f"{prompt}\n"
    )
    write_agents_md(worker_dir, agents_md_content)
    print(f"Wrote {worker_dir / 'AGENTS.md'}")

    mode = "oneshot" if args.oneshot else "interactive"

    # Create the agent window
    create_agent_window(session_name, agent_name, provider, prompt, worker_dir, mode=mode)


if __name__ == "__main__":
    main()
