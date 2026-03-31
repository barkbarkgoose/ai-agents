# Node Environment — npm

This spec covers working with Node.js frontends using **npm** for package management.

## Existing Projects — Detect First

Before applying any setup, inspect the project to determine what's already in use:

| Signal | Tool to use |
|--------|-------------|
| `package.json` + `yarn.lock` | Yarn — use `yarn`, not `npm` |
| `package.json` + `pnpm-lock.yaml` | pnpm — use `pnpm`, not `npm` |
| `package.json` + `package-lock.json` | npm |
| `volta` key in `package.json` | Volta — use it for version management |
| `.nvmrc` or `.node-version` | nvm — respect the pinned version |

**Rule:** Always detect before scaffolding. Treat existing artifacts as the source of truth.

## Setup

```bash
cd frontend
echo "<node-version>" > .nvmrc
nvm use
npm install
```

## Running Commands

```bash
npm run dev       # Vite dev server
npm run build     # production build
npm run test      # Vitest
```

## Installing Packages

```bash
npm install package-name
npm install --save-dev package-name
```

## Agent Guidance

- **Always operate from `frontend/`** — never run npm commands from the project root
- **Never use uv or pip** for anything frontend-related
- Use `.nvmrc` to pin the Node version; match what's already present in existing projects
