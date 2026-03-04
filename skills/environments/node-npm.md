# Node Environment — npm

> **Stub** — to be expanded. Core conventions below.

All Vue/Node frontends use **npm** for package management. The Node version is defined in the `greenfield-init` skill's `VERSIONS.md`.

## Setup

```bash
cd frontend
echo "<node-version>" > .nvmrc   # matches VERSIONS.md
nvm use                           # or use the version manager of your choice
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
- Use `.nvmrc` to pin the Node version; match the version in `VERSIONS.md`
