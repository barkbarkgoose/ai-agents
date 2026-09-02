# Harness config

Reference configuration for AI coding harnesses, one folder per harness.
Unlike `agents/`, `commands/`, and `skills/`, **nothing here is synced by
`sync.sh`** — config changes rarely and often mixes with machine-local
settings, so it's applied by hand. Each harness folder has its own README
saying exactly what goes where.

```
config/
  claude/     # Claude Code  -> ~/.claude/
  <harness>/  # add more as needed
```

## How harness settings generally work

Every harness follows the same broad shape:

- **A user-level config root** holding a main JSON settings file plus support
  files (scripts, agents, skills):
  - Claude Code: `~/.claude/` with `settings.json`
  - OpenCode: `~/.config/opencode/` with `opencode.json`
  - Kilo: `~/.kilo/` (reads OpenCode-compatible config as its XDG root)
- **Project-level overrides** that layer on top of user settings. Claude Code
  reads `.claude/settings.json` (committed, team-shared) and
  `.claude/settings.local.json` (gitignored, personal) in the project root;
  more specific scopes win. OpenCode similarly reads a project
  `opencode.json`.
- **Machine-local vs. shareable keys.** Settings files mix both. Keys like
  `model`, `permissions`, and API/auth config usually differ per device —
  don't put them in this repo. Keys that alter behavior you want everywhere
  (status line, hooks, MCP servers) are what belongs here, as *snippets* to
  merge, never full files to copy over.

## MCP servers

MCP is the one config concept that's genuinely portable across harnesses: a
server definition is the same idea everywhere (a stdio command or a remote
URL), only the file it lives in differs.

A stdio server is defined by `command` + `args` + optional `env`; a remote
server by a `url` (HTTP/SSE) and optional headers.

- **Claude Code**: managed with the CLI, *not* by editing `settings.json`:

  ```bash
  claude mcp add my-server -- npx -y some-mcp-package   # local stdio
  claude mcp add --transport http my-api https://example.com/mcp
  claude mcp list
  ```

  Scope flags decide where it's stored: `--scope user` (all projects, stored
  in `~/.claude.json` — note: a different file than settings.json),
  `--scope project` (writes a committed `.mcp.json` in the repo), or the
  default local scope (this project, this machine).

- **OpenCode**: an `mcp` block in `opencode.json`:

  ```json
  "mcp": {
    "my-server": { "type": "local", "command": ["npx", "-y", "some-mcp-package"] },
    "my-api":    { "type": "remote", "url": "https://example.com/mcp" }
  }
  ```

Because the underlying server is identical, a good pattern for this repo is to
document the server definition once (command, args, env vars it needs) in the
harness README and translate it into each harness's syntax.

## Hooks

Hooks run your shell commands at fixed points in the harness's loop — the
main way to alter base-level behavior (auto-format after edits, block
dangerous commands, inject context). They are **not portable** between
harnesses; each has its own events and config shape.

Claude Code hooks live under a `hooks` key in `settings.json`. Events include
`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`, and
`Notification`. Each entry pairs a `matcher` (which tool names it applies to)
with commands; the command gets event JSON on stdin, and for PreToolUse a
non-zero "block" exit code (2) can veto the tool call:

```json
"hooks": {
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "~/.claude/hooks/format.sh" }]
    }
  ]
}
```

Things to know before adding hooks:

- Hooks execute arbitrary shell with your user's permissions, on every
  matching event — treat hook scripts with the same care as anything else
  that runs unattended, and keep them fast (they run inline in the loop).
- Hooks are configured in settings files, so they *can* be shipped from this
  repo as snippets. Ship the script file alongside (like `claude/statusline.sh`)
  and reference it by `~/...` path so the snippet works on any machine.
- Status lines are configured the same way (a `statusLine` command in
  `settings.json`) and follow the same pattern: script file + settings snippet.

## Adding a new harness folder

1. Create `config/<harness>/` with a `README.md` that states:
   - the harness's user-level config root and main settings filename,
   - a table of files in the folder and where each one goes,
   - which settings keys are machine-local and deliberately *not* synced.
2. Keep settings fragments as **valid standalone JSON** snippet files (e.g.
   `settings.snippet.json`) so they can be hand-pasted or jq-merged
   (`jq -s '.[0] * .[1]' dest snippet`) — see `claude/README.md` for the full
   jq explanation and its caveats (arrays replace, comments break jq).
3. Ship support files (scripts, hook scripts) whole, note any `chmod +x`, and
   reference them from snippets by home-relative path.
4. If the harness should also receive agents/commands/skills, wire its
   destination root into `sync.sh` — that part stays automated; config stays
   manual.
