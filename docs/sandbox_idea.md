Alternative to running a sandbox with a docker container, here is how you could transition to a lighter-weight setup and what you would gain or lose compared to Docker.

1. The "Python + Shell" Alternative Since the harness is primarily a collection of shell scripts, binaries (in seed/bin and seed/tools/bin), and configuration files, you could implement a "Local Native" version.

## How to do it:
- Environment: Instead of a Dockerfile, you would use a Python Virtual Environment (for zmem or other Python-based tools) and potentially Homebrew (on macOS) or apt (on Linux) to install system dependencies like jq, ripgrep, gh, and fzf.
- Setup: You would run the ./setup.sh script directly on your host. This script appears to move files from seed/ into ~/.ai/.
- Isolation: You would use direnv or a custom source .env approach to manage the environment variables(like AI_HOME, DOC_VAULT_ROOT, etc.) per project.

## What you gain (The "Lighter" part)

- Instant Start: No docker run overhead; your tools are just commands in your path.
- Direct Filesystem Access: No need to worry about volume mounts or permission mismatches between the container and host.
- Resource Efficiency: No Docker Desktop overhead (which can be significant on macOS).
- Ollama Connectivity: You wouldn't need host.docker.internal or OLLAMA_HOST=0.0.0.0; tools could just
  talk to localhost.

## What you lose (The "Docker" Benefits)

- Tool Versioning: The Dockerfile ensures everyone has the exact same version of bun, node, python, and gh. On your host, you'll have to manage these yourself.
- Security (SSH Keys): The sandbox uses a dedicated, isolated SSH key. If you run locally, you are likely using your primary SSH keys, which increases risk if an AI agent runs a malicious command.
- Dependency Conflict: If the harness requires a specific version of a tool that conflicts with your work tools, a Python venv only solves this for Python, not for binaries like git or jq.
- Clean Uninstalls: Deleting a Docker image is cleaner than hunting down files placed in ~/.ai, /usr/local/bin, and your shell profile.

## Recommendation: "Hybrid" Approach

If you want something lighter than Docker but safer than a raw host install, consider Nix or Devbox.

- Devbox/Nix: You can create a devbox.json that defines all the tools (ripgrep, jq, python, etc.). When you enter that folder, the environment is instantly "isolated" for that session without the heavy virtualization of Docker.


**Summary Comparison:**

| Feature          | Docker (Current)          | Python Venv / Local    | Devbox / Nix         |
|------------------|---------------------------|------------------------|----------------------|
| Speed            | Slowest (Startup)         | Fastest                | Fast                 |
| Isolation        | High (Filesystem/Network) | Low (Python only)      | Medium (Environment) |
| Setup Complexity | Low (One build command)   | High (Manual installs) | Medium (Declarative) |
| Security         | Excellent                 | Poor                   | Fair                 |
|                  |                           |                        |                      |


  Would you like me to help you draft a setup-local.sh or a devbox.json to try this without Docker?