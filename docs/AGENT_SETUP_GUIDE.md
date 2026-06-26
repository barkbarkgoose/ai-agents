# Agent & Skill Setup Guide

A reference for setting up agentic workflows with **OpenCode** (and Kilo via OpenCode compatibility).

**Note:** AI tooling evolves rapidly. Always check the official documentation for the latest requirements.
- [OpenCode Docs](https://opencode.ai/docs)
- [Kilo Docs](https://kilo.ai/docs)

---

## Quick Reference

| Feature | OpenCode / Kilo |
|---------|----------------|
| **Concept** | Agents + Skills |
| **File Structure** | Agents: `<name>.md`<br>Skills: `<name>/SKILL.md` |
| **Global Location (OpenCode)** | `~/.config/opencode/agents/`<br>`~/.config/opencode/skills/` |
| **Global Location (Kilo)** | `~/.config/kilo/agents/`<br>`~/.config/kilo/skills/` |
| **Required Fields (agents)** | `name`, `description` (recommended: `mode`, `model`, `tools`, `permission`) |
| **Required Fields (skills)** | `name`, `description` |

---

## Agent Modes

| Mode | Behavior |
|------|----------|
| `primary` | Selectable as the main agent from the UI. |
| `subagent` | Hidden from the main UI; only invocable via the `Task` tool by another agent. |
| `all` | Both primary and subagent. |

---

## Agent Frontmatter

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
3. **Add frontmatter JSON** under `./agent-frontmatter/<name>.json` if you want harness-specific overrides. Otherwise the `.defaults` block applies to all harnesses.
4. **Run `./sync.sh`** to deploy to both `~/.config/opencode/` (stock OpenCode) and `~/.config/kilo/` (Kilo).
5. **Test** by selecting the agent in OpenCode or Kilo.

---

## Notes on OpenCode Agent Configuration

- The `tools` field is **deprecated** in favor of `permission`. Do not use `tools: [...]` arrays in agent frontmatter; instead, grant/deny actions via the `permission` map.
- `tools: ["task", "read", "grep", "glob", "bash"]` in YAML is rejected by OpenCode's strict parser as a malformed value. Use `permission: { task: "allow", bash: "allow", edit: "deny", write: "deny" }` instead.

---

## Migration Tips

### From a multi-harness setup

- Collapse per-harness frontmatter blocks down to `opencode` only.
- Remove Cursor-, Claude-, Gemini-, Codex-, and oh-my-pi-specific keys.
- The `sync.sh` script writes to both `~/.config/opencode/` and `~/.config/kilo/`. Kilo does **not** read `~/.config/opencode/`; it uses `~/.config/kilo/` as its XDG global root.

### From agents-heavy to skill-first

- Keep only a handful of top-level agents (advisor, orchestrator, research).
- Move domain-specific instructions into skills.
- Reference skills by name from agent prompts rather than linking to skill files.
