#!/usr/bin/env python3
"""
utils.py - Shared utilities and state management for llmmux
"""
import os
import json
import shlex
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Shared Constants
LLMMUX_HOME = Path.home() / ".llmmux"

PI_PACKAGE = "@earendil-works/pi-coding-agent"
PI_MIN_NODE_MAJOR = 20

# Provider registry: provider-name -> pi --model argument.
# All llmmux subagents route through the `pi` binary; the provider flag
# simply selects which model `pi` should use.
PI_PROVIDER_MODELS = {
    "gemini":   "google/gemini-2.5-pro",
    "agent":    "openai-codex/gpt-5.4",
    "codex":    "openai-codex/gpt-5.4",
    "claude":   "anthropic/claude-sonnet-4-5",
    "opencode": "openai-codex/gpt-5.4",
    "kilo":     "openai-codex/gpt-5.4",
    "minimax":  "minimax/MiniMax-M2.7",
    "gpt":      "openai-codex/gpt-5.5",
    "sonnet":   "anthropic/claude-sonnet-4-5",
    "opus":     "anthropic/claude-opus-4-1",
}

# Backward-compat: argparse `choices=` still needs an iterable.
VALID_PROVIDERS = list(PI_PROVIDER_MODELS.keys())


def load_environment():
    """Load environment variables from .default_env and .env"""
    default_env = LLMMUX_HOME / ".default_env"
    user_env = LLMMUX_HOME / ".env"

    if default_env.exists():
        load_dotenv(default_env, override=False)
    if user_env.exists():
        load_dotenv(user_env, override=True)


def session_exists(session_name: str) -> bool:
    """Check if a tmux session exists reliably"""
    result = subprocess.run(
        ['tmux', 'list-sessions', '-F', '#{session_name}'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False
    return session_name in result.stdout.strip().split("\n")


def resolve_state_dir(session_name: str) -> Path:
    """Resolve the specific session ID uuid subdirectory from the index"""
    index_path = LLMMUX_HOME / "state" / "session_index.json"
    if index_path.exists():
        with open(index_path, "r") as f:
            index = json.load(f)
        session_id = index.get(session_name)
        if session_id:
            return LLMMUX_HOME / "state" / session_id
    return LLMMUX_HOME / "state" / session_name


def _node_major_version() -> int | None:
    """Return the major version of `node` on PATH, or None if missing."""
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    version = result.stdout.strip().lstrip("v")
    try:
        return int(version.split(".")[0])
    except (ValueError, IndexError):
        return None


def _pi_installed() -> bool:
    """Return True if the `pi` binary is on PATH."""
    try:
        subprocess.run(
            ["pi", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def verify_pi_environment() -> bool:
    """
    Verify that node >= 20 and the `pi` CLI are installed.
    Prints actionable setup instructions on failure.
    Returns True if everything is ready, False otherwise.
    """
    ok = True

    node_major = _node_major_version()
    if node_major is None:
        print("Error: `node` is not installed or not on PATH.", file=sys.stderr)
        print("Install Node.js 20+ from https://nodejs.org/ or via your package manager.", file=sys.stderr)
        ok = False
    elif node_major < PI_MIN_NODE_MAJOR:
        print(
            f"Error: node v{node_major} is installed, but llmmux requires node >= {PI_MIN_NODE_MAJOR}.",
            file=sys.stderr,
        )
        print("Upgrade Node.js: https://nodejs.org/ or `nvm install 20`.", file=sys.stderr)
        ok = False

    if not _pi_installed():
        print("Error: `pi` is not installed or not on PATH.", file=sys.stderr)
        print("Install with:", file=sys.stderr)
        print(f"  npm install -g --ignore-scripts {PI_PACKAGE}", file=sys.stderr)
        print("Authentication is handled via env vars (e.g. GEMINI_API_KEY,", file=sys.stderr)
        print("DEEPSEEK_API_KEY) or by passing --api-key to pi.", file=sys.stderr)
        ok = False

    if not ok:
        print("\nllmmux requires the `pi` coding agent. See https://github.com/earendil-works/pi", file=sys.stderr)

    return ok


def resolve_pi_model(provider: str) -> str:
    """
    Translate an llmmux provider name into a `pi --model` argument.

    Resolution order:
      1. LLMMUX_PI_MODEL_<PROVIDER> env var (full override).
      2. PI_PROVIDER_MODELS registry.
      3. Pass-through (assume the user already gave a pi model string).
    """
    env_key = f"LLMMUX_PI_MODEL_{provider.upper()}"
    override = os.getenv(env_key)
    if override:
        return override
    if provider in PI_PROVIDER_MODELS:
        return PI_PROVIDER_MODELS[provider]
    return provider


def write_agents_md(worker_dir: Path, content: str) -> Path:
    """
    Write an AGENTS.md file into the target worker directory so that `pi`
    (which auto-discovers AGENTS.md from cwd) ingests it on startup.
    Creates the directory if missing. Returns the path written.
    """
    worker_dir.mkdir(parents=True, exist_ok=True)
    target = worker_dir / "AGENTS.md"
    target.write_text(content)
    return target


def get_provider_command(provider: str, prompt: str, *, mode: str = "interactive") -> str:
    """
    Build a `pi` invocation string for tmux send-keys.

    Args:
        provider: llmmux provider name (gemini, codex, claude, ...) or a raw
                  `pi` model string (e.g. "google/gemini-2.5-pro:high").
        prompt:   The task / instructions for the subagent.
        mode:     "interactive" -> `pi "<prompt>"` (stays in TUI).
                  "oneshot"     -> `pi -p "<prompt>"` (run task and exit).
    """
    model = resolve_pi_model(provider)
    safe_prompt = shlex.quote(prompt)

    if mode == "oneshot":
        return f"pi --model {shlex.quote(model)} -p {safe_prompt}"
    if mode == "interactive":
        return f"pi --model {shlex.quote(model)} {safe_prompt}"
    raise ValueError(f"Unknown mode: {mode!r} (expected 'interactive' or 'oneshot')")
