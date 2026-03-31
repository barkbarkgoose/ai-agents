---
name: environments
description: Detect existing project environment and determine appropriate tools. Use when setting up a dev environment, installing dependencies, or running commands in any layer (Python, Node, Docker, etc.).
---

# Environments

This skill detects what tools and runtimes a project uses, then routes to the appropriate spec file for working with those tools.

## Detect Existing Environment

Before applying any setup, inspect the project to determine what's already in use:

| Signal | Inferred tool |
|--------|--------------|
| `venv/`, `.python-version`, `requirements.txt` | Python + uv virtualenv |
| `pyproject.toml` + `poetry.lock` | Python + Poetry |
| `pyproject.toml` + `uv.lock` | Python + uv (pyproject-based) |
| `package.json` + `package-lock.json` | Node + npm |
| `package.json` + `yarn.lock` | Node + Yarn |
| `package.json` + `pnpm-lock.yaml` | Node + pnpm |
| `volta` key in `package.json` | Node version managed by Volta |
| `.nvmrc` or `.node-version` | Node version pinned |
| `docker-compose.yml` or `compose.yaml` | Docker services defined |
| `Dockerfile` present | App may be fully containerized |

**Rule:** Always detect before scaffolding. Treat existing artifacts as the source of truth.

## Stack → Spec Mapping

These are the available spec files. Read only the ones relevant to the current stack:

| Environment | Spec file | When to read |
|-------------|-----------|-------------|
| Python (uv + virtualenv) | [python-uv.md](python-uv.md) | Python backend — installing packages, running commands, scaffolding |
| Node (npm) | [node-npm.md](node-npm.md) | Node/Vue frontend — installing packages, running scripts |
| Docker | [docker.md](docker.md) | Service dependencies or full app containerization |

If the project uses a Python or Node tool **not covered** by a spec file (e.g. Poetry, Yarn, Volta), use the detected tool's own conventions and do not force the defaults from the spec files.

## Key Rule

Each layer of the stack is always an independent environment — never mix Python package management with Node or vice versa. Each layer has its own `.env` file. See individual spec files for details.
