# Agent & Skill Setup Guide

A reference for setting up agentic workflows with **OpenCode** (and Kilo via OpenCode compatibility) and **Claude Code**.

**Note:** AI tooling evolves rapidly. Always check the official documentation for the latest requirements.
- [OpenCode Docs](https://opencode.ai/docs)
- [Kilo Docs](https://kilo.ai/docs)
- [Claude Code Docs](https://code.claude.com/docs)
  - [Claude Agents Docs](https://code.claude.com/docs/en/sub-agents)

---

## Quick Reference

| Feature | OpenCode / Kilo | Claude Code |
|---------|----------------|-------------|
| **Concept** | Agents + Skills | Agents + Skills |
| **File Structure** | Agents: `<name>.md`<br>Skills: `<name>/SKILL.md` | Agents: `<name>.md`<br>Skills: `<name>/SKILL.md` |
| **Global Location (OpenCode)** | `~/.config/opencode/agents/`<br>`~/.config/opencode/skills/` | — |
| **Global Location (Kilo)** | `~/.kilo/agents/`<br>`~/.kilo/skills/` | — |
| **Global Location (Claude Code)** | — | `~/.claude/agents/`<br>`~/.claude/skills/` |
| **Required Fields (agents)** | `name`, `description` (recommended: `mode`, `model`, `tools`, `permission`) | `name`, `description` (recommended: `tools`, `model`, `color`) |
| **Required Fields (skills)** | `name`, `description` | `name`, `description` |

---

## Agent Modes (OpenCode / Kilo only)

| Mode | Behavior |
|------|----------|
| `primary` | Selectable as the main agent from the UI. |
| `subagent` | Hidden from the main UI; only invocable via the `Task` tool by another agent. |
| `all` | Both primary and subagent. |

Claude Code has no `mode` concept — every agent under `~/.claude/agents/` is invocable via the `Task` tool.

---

## Agent Frontmatter

### OpenCode / Kilo

```yaml
---
name: my-agent
description: When to use this agent
mode: primary          # primary | subagent | all
model: provider/model  # e.g., openai/gpt-5.4
permission:            # optional, agent-level permissions
  write: deny
  edit: deny
  bash: ask
---
```

Permission actions: `allow`, `ask`, `deny`.

### Claude Code

```yaml
---
name: my-agent
description: When to use this agent
tools: Read, Grep, Glob, Bash   # comma-separated allowlist, not a YAML array
model: sonnet                   # sonnet | opus | haiku | inherit
color: cyan                     # optional UI color
---
```

Claude Code has no `permission` map and no `mode` field — grant capability with `tools` instead, and note that `model` only accepts Claude model aliases (not `provider/model` strings or local-model references).

---

## Skill Frontmatter

```yaml
---
name: my-skill
description: When to use this skill
---
```

---

## Setting Up a Local Model (e.g., LM Studio)

Configure the LM Studio provider in `~/.config/kilo/opencode.json` (or the equivalent OpenCode config) so the `small-subagent` can pin to it:

```json
{
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LM Studio (local)",
      "options": {
        "baseURL": "http://<tailscale-host>:1234/v1",
        "apiKey": "lm-studio"
      },
      "models": {
        "gemma-4-26b": {
          "name": "Gemma 4 26B (local)",
          "tool_call": true
        }
      }
    }
  }
}
```

Then the `small-subagent` frontmatter can reference `lmstudio/gemma-4-26b`.

---

## Setup Workflow

1. **Decide agent vs skill**
- Top-level persona with a specific model/permissions → agent.
- Reusable domain expertise shared across agents → skill.
2. **Write the file** under `./agents/` or `./skills/<name>/`.
3. **Add frontmatter JSON** under `./agent-frontmatter/<name>.json` if you want harness-specific overrides. The `.defaults` block applies to all harnesses; add a `harnesses.claude` block (and set OpenCode-only keys like `mode`/`permission` to `null` there) if the agent needs Claude-specific `tools`/`model`/`color`.
4. **Run `./sync.sh`** to deploy to `~/.config/opencode/` (stock OpenCode), `~/.kilo/` (Kilo), and `~/.claude/` (Claude Code).
5. **Test** by selecting the agent in OpenCode, Kilo, or Claude Code.

---

## Notes on OpenCode Agent Configuration

- The `tools` field is **deprecated** in favor of `permission`. Do not use `tools: [...]` arrays in agent frontmatter; instead, grant/deny actions via the `permission` map.
- `tools: ["task", "read", "grep", "glob", "bash"]` in YAML is rejected by OpenCode's strict parser as a malformed value. Use `permission: { task: "allow", bash: "allow", edit: "deny", write: "deny" }` instead.
- This is the opposite of Claude Code, where `tools` is the mechanism and `permission` doesn't exist — keep the two harness blocks separate in `agent-frontmatter/*.json` rather than sharing keys between them.

---

## Migration Tips

### From a multi-harness setup

- Keep per-harness frontmatter blocks for `opencode` and `claude`; Kilo reuses the `opencode` block.
- Remove Cursor-, Gemini-, Codex-, and oh-my-pi-specific keys — those harnesses aren't targeted by `sync.sh`.
- The `sync.sh` script writes to `~/.config/opencode/`, `~/.kilo/`, and `~/.claude/`. Kilo does **not** read `~/.config/opencode/`; it uses `~/.kilo/` as its XDG global root.

### From agents-heavy to skill-first

- Keep only a handful of top-level agents (advisor, orchestrator, research).
- Move domain-specific instructions into skills.
- Reference skills by name from agent prompts rather than linking to skill files.
