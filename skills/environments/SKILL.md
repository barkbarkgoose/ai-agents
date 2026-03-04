---
name: environments
description: Environment setup and dependency management specs for each layer of the stack. Use when scaffolding a project, setting up a dev environment, installing dependencies, or running commands in any layer (Python, Node, Docker, etc.).
---

# Environments

This skill is a router. Based on which tools and runtimes are in use, read the corresponding spec file from this folder. Each file is self-contained and covers setup, running commands, and package management for that environment.

The spec files reflect our **default tooling choices**. If an existing project uses different tools (Yarn instead of npm, Poetry instead of uv, Volta instead of nvm), adapt to what's already there — the spec files are guides, not mandates.

## Existing Projects — Detect First

Before applying any spec, inspect the project to determine what's already in use:

| Signal | Inferred tool |
|--------|--------------|
| `venv/`, `.python-version`, `requirements.txt` | Python + uv virtualenv |
| `pyproject.toml` + `poetry.lock` | Python + Poetry — do not force uv |
| `pyproject.toml` + `uv.lock` | Python + uv (pyproject-based) |
| `package.json` + `package-lock.json` | Node + npm |
| `package.json` + `yarn.lock` | Node + Yarn — use `yarn`, not `npm` |
| `package.json` + `pnpm-lock.yaml` | Node + pnpm — use `pnpm`, not `npm` |
| `volta` key in `package.json` | Node version managed by Volta |
| `.nvmrc` or `.node-version` | Node version pinned — use it, don't overwrite |
| `docker-compose.yml` or `compose.yaml` | Docker services defined — read before writing |
| `Dockerfile` present | App may be fully containerized |

**Rule:** Always detect before scaffolding. Treat existing artifacts as the source of truth. Only apply spec file guidance for parts that are genuinely missing or being added fresh.

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
