#!/usr/bin/env python3
"""
llmmux orchestrator - Create and manage tmux-based multi-agent sessions

This script creates a tmux session with an orchestrator window that bootstraps
a multi-agent workflow using various LLM providers (Cursor, Claude, Codex, etc.)

Usage:
    python orchestrator.py --provider agent
    python orchestrator.py --provider gemini --session-name my-project
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from shutil import copy2
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv


# Constants
LLMMUX_HOME = Path.home() / ".llmmux"
REQUIRED_FILES = [
    "orchestrator.py",
    "create_agent.py",
    "INIT_AGENT.md",
    "INIT_ORCHESTRATOR.md",
    "TMUX_CHEATSHEET.md",
    ".default_env",
]
VALID_PROVIDERS = ["gemini", "agent", "codex", "claude", "opencode"]


def ensure_llmmux_setup():
    """
    Ensure ~/.llmmux exists and has all required files.
    Copy missing files from the current directory.
    """
    if not LLMMUX_HOME.exists():
        print(f"Creating {LLMMUX_HOME}...")
        LLMMUX_HOME.mkdir(parents=True)
    
    # Create state and artifacts directories
    (LLMMUX_HOME / "state").mkdir(exist_ok=True)
    (LLMMUX_HOME / "artifacts").mkdir(exist_ok=True)
    
    # Copy missing files from current directory
    current_dir = Path(__file__).parent
    copied = []
    
    for file in REQUIRED_FILES:
        target = LLMMUX_HOME / file
        source = current_dir / file
        
        if not target.exists() and source.exists():
            copy2(source, target)
            copied.append(file)
    
    if copied:
        print(f"Copied to {LLMMUX_HOME}: {', '.join(copied)}")
    
    return True


def load_environment():
    """
    Load environment variables from .default_env and .env
    .env overrides .default_env values
    """
    default_env = LLMMUX_HOME / ".default_env"
    user_env = LLMMUX_HOME / ".env"
    
    # Load defaults first
    if default_env.exists():
        load_dotenv(default_env, override=False)
    
    # Override with user settings
    if user_env.exists():
        load_dotenv(user_env, override=True)


def check_tmux_available():
    """Check if tmux is installed and available"""
    try:
        subprocess.run(
            ["tmux", "-V"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: tmux is not installed or not in PATH")
        print("Install tmux with: brew install tmux (macOS) or apt install tmux (Linux)")
        return False


def session_exists(session_name: str) -> bool:
    """Check if a tmux session exists"""
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        capture_output=True
    )
    return result.returncode == 0


def handle_existing_session(session_name: str) -> str:
    """
    Handle conflict when session already exists.
    Returns the final session name to use.
    """
    print(f"\nSession '{session_name}' already exists.")
    print("Options:")
    print("  1. Keep old and add new (adds suffix like 'name(1)')")
    print("  2. Stop old and start new")
    print("  3. Quit")
    
    while True:
        choice = input("\nChoice [1/2/3]: ").strip()
        
        if choice == "1":
            # Find available suffix
            i = 1
            new_name = f"{session_name}({i})"
            while session_exists(new_name):
                i += 1
                new_name = f"{session_name}({i})"
            
            print(f"Using session name: {new_name}")
            return new_name
        
        elif choice == "2":
            # Kill existing session
            subprocess.run(
                ["tmux", "kill-session", "-t", session_name],
                stderr=subprocess.DEVNULL
            )
            print(f"Killed existing session '{session_name}'")
            return session_name
        
        elif choice == "3":
            print("Exiting...")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_session_name(args_name: str = None) -> str:
    """Get session name from args or prompt user"""
    if args_name:
        return args_name
    
    default = "llmmux"
    response = input(f"Enter session name [{default}]: ").strip()
    return response or default


def get_project_root(args_root: str = None) -> str:
    """Get project root from args or prompt user"""
    if args_root:
        return args_root
    
    default = os.getcwd()
    print(f"\nCurrent directory: {default}")
    response = input(f"Enter project root [{default}]: ").strip()
    return response or default


def get_provider(args_provider: str = None) -> str:
    """
    Get provider from args or prompt user.
    Optionally save as default.
    """
    # Check if we have a default in environment
    env_provider = os.getenv("LLMMUX_DEFAULT_PROVIDER")
    
    if args_provider:
        if args_provider not in VALID_PROVIDERS:
            print(f"Error: Invalid provider '{args_provider}'")
            print(f"Valid providers: {', '.join(VALID_PROVIDERS)}")
            sys.exit(1)
        return args_provider
    
    # Use env default if available
    if env_provider and env_provider in VALID_PROVIDERS:
        use_default = input(f"Use default provider '{env_provider}'? [Y/n]: ").strip().lower()
        if use_default in ["", "y", "yes"]:
            return env_provider
    
    # Prompt user
    print("\nAvailable providers:")
    for i, provider in enumerate(VALID_PROVIDERS, 1):
        print(f"  {i}. {provider}")
    
    while True:
        choice = input("\nSelect provider (name or number): ").strip().lower()
        
        # Handle numeric choice
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(VALID_PROVIDERS):
                provider = VALID_PROVIDERS[idx]
                break
        # Handle name choice
        elif choice in VALID_PROVIDERS:
            provider = choice
            break
        else:
            print(f"Invalid choice. Choose from: {', '.join(VALID_PROVIDERS)}")
    
    # Ask to save as default
    save = input("\nSave as default provider? [y/N]: ").strip().lower()
    if save in ["y", "yes"]:
        env_file = LLMMUX_HOME / ".env"
        
        # Read existing content
        existing_lines = []
        if env_file.exists():
            with open(env_file, "r") as f:
                existing_lines = [line for line in f if not line.startswith("LLMMUX_DEFAULT_PROVIDER=")]
        
        # Write back with new default
        with open(env_file, "w") as f:
            f.write(f"LLMMUX_DEFAULT_PROVIDER={provider}\n")
            f.writelines(existing_lines)
        
        print(f"Saved '{provider}' as default provider")
    
    return provider


def get_provider_command(provider: str, prompt: str) -> str:
    """
    Get the command to run for a given provider.
    Uses environment variables with format: PROVIDER_<name>
    """
    env_key = f"PROVIDER_{provider}"
    template = os.getenv(env_key)
    
    if not template:
        # Fallback defaults
        defaults = {
            "gemini": "gemini -p '{prompt}'",
            "agent": "agent '{prompt}'",
            "codex": "codex '{prompt}'",
            "claude": "claude '{prompt}'",
            "opencode": "opencode '{prompt}'",
        }
        template = defaults.get(provider, f"{provider} '{prompt}'")
    
    # Replace {prompt} placeholder
    return template.replace("{prompt}", prompt)


def create_session_state_dirs(session_name: str):
    """Create state and artifacts directories for the session"""
    state_dir = LLMMUX_HOME / "state" / session_name
    artifacts_dir = LLMMUX_HOME / "artifacts" / session_name
    
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "agents").mkdir(exist_ok=True)
    (state_dir / "logs").mkdir(exist_ok=True)
    
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    (artifacts_dir / "patches").mkdir(exist_ok=True)
    (artifacts_dir / "reports").mkdir(exist_ok=True)

    return state_dir, artifacts_dir


def generate_session_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"session_{timestamp}_{uuid4().hex[:8]}"


def update_session_index(tmux_session_name: str, session_id: str):
    index_path = LLMMUX_HOME / "state" / "session_index.json"
    if index_path.exists():
        with open(index_path, "r") as f:
            index = json.load(f)
    else:
        index = {}

    index[tmux_session_name] = session_id
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)


def initialize_run_state(state_dir: Path, session_id: str, tmux_session_name: str, project_root: str, provider: str):
    run_state = {
        "run_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repo_root": project_root,
        "tmux_session_name": tmux_session_name,
        "provider": provider,
        "agents": {},
        "artifacts": [],
        "task_queue": [],
        "constraints": []
    }
    with open(state_dir / "run_state.json", "w") as f:
        json.dump(run_state, f, indent=2)


def launch_orchestrator_session(session_name: str, session_id: str, project_root: str, provider: str):
    """
    Create tmux session and launch orchestrator agent
    """
    # Create state directories
    state_dir, _ = create_session_state_dirs(session_id)
    update_session_index(session_name, session_id)
    initialize_run_state(state_dir, session_id, session_name, project_root, provider)
    
    # Create tmux session
    print(f"\nCreating tmux session '{session_name}'...")
    subprocess.run([
        "tmux", "new-session",
        "-d",                    # detached
        "-s", session_name,      # session name
        "-n", "orchestrator",    # window name
        "-c", project_root       # starting directory
    ], check=True)
    
    # Prepare the orchestrator prompt
    init_file = LLMMUX_HOME / "INIT_ORCHESTRATOR.md"
    prompt = f"orchestrator agent: refer to {init_file}"
    
    # Get the provider command
    command = get_provider_command(provider, prompt)
    
    # Send the command to the orchestrator window
    print(f"Launching orchestrator with provider '{provider}'...")
    subprocess.run([
        "tmux", "send-keys",
        "-t", f"{session_name}:orchestrator",
        command,
        "C-m"  # Enter key
    ], check=True)
    
    print(f"\n✓ Orchestrator session '{session_name}' created successfully!")
    print(f"\nAttach with:")
    print(f"  tmux attach -t {session_name}")
    print(f"\nOr list all sessions:")
    print(f"  tmux ls")
    print(f"\nState directory: {LLMMUX_HOME / 'state' / session_id}")
    print(f"Session ID: {session_id}")


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Create and manage tmux-based multi-agent orchestrator sessions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --provider agent
  %(prog)s --provider gemini --session-name my-project
  %(prog)s --provider codex --session-name backend --project-root /path/to/project

Valid providers: gemini, agent (cursor), codex, claude, opencode

After the session is created, attach with:
  tmux attach -t <session-name>
        """
    )
    
    parser.add_argument(
        "--provider",
        type=str,
        choices=VALID_PROVIDERS,
        help="LLM provider to use (gemini, agent, codex, claude, opencode)"
    )
    
    parser.add_argument(
        "--session-name",
        type=str,
        help="Name for the tmux session (default: llmmux)"
    )
    
    parser.add_argument(
        "--project-root",
        type=str,
        help="Project root directory (default: current directory)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()
    
    # Check tmux availability
    if not check_tmux_available():
        sys.exit(1)
    
    # Ensure ~/.llmmux is set up
    ensure_llmmux_setup()
    
    # Load environment
    load_environment()
    
    # Get configuration
    session_name = get_session_name(args.session_name)
    
    # Handle existing session
    if session_exists(session_name):
        session_name = handle_existing_session(session_name)
    
    project_root = get_project_root(args.project_root)
    provider = get_provider(args.provider)
    session_id = generate_session_id()
    
    # Launch the orchestrator
    launch_orchestrator_session(session_name, session_id, project_root, provider)


if __name__ == "__main__":
    main()
