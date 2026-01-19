# Agent & Skill Setup Guide

A comprehensive reference for setting up agentic workflows across different AI providers: **Cursor**, **Claude**, and **Gemini**.

**Note:** AI tooling evolves rapidly. Always check the official documentation for the latest requirements.
- [Cursor Docs](https://docs.cursor.com/)
  - [Cursor Subagents](https://cursor.com/docs/context/subagents)
- [Claude Code Docs](https://code.claude.com/docs)
  - [Claude Agents Docs](https://code.claude.com/docs/en/sub-agents)
- [Gemini CLI Repo](https://github.com/google-gemini/gemini-cli)
  - [Gemini Skills Docs](https://geminicli.com/docs/cli/skills/)

---

## Quick Reference

| Feature | Cursor | Claude | Gemini |
|---------|--------|--------|--------|
| **Concept** | Skills only | Agents only | Both Agents & Skills |
| **File Structure** | `<skill-name>/SKILL.md` | `<agent-name>.md` | Agents: `<name>.md`<br>Skills: `<name>/SKILL.md` |
| **Global Location** | `~/.cursor/skills/` | `~/.claude/agents/` | `~/.gemini/agents/`<br>`~/.gemini/skills/` |
| **Required Fields** | `name`, `description` | `name`, `description`, `tools`, `model`, `color` | `name`, `description`, `tools`, `model`, `color` |
| **Example Tags** | In description | In description | In description |

---

## Table of Contents

- [Agent \& Skill Setup Guide](#agent--skill-setup-guide)
  - [Quick Reference](#quick-reference)
  - [Table of Contents](#table-of-contents)
  - [Cursor](#cursor)
    - [Cursor Directory Structure](#cursor-directory-structure)
    - [Cursor Frontmatter Requirements](#cursor-frontmatter-requirements)
    - [Cursor Example](#cursor-example)
  - [Claude](#claude)
    - [Claude Directory Structure](#claude-directory-structure)
    - [Claude Frontmatter Requirements](#claude-frontmatter-requirements)
    - [Claude Example Tags](#claude-example-tags)
    - [Claude Example](#claude-example)
  - [Gemini](#gemini)
    - [Gemini Agents vs Skills](#gemini-agents-vs-skills)
    - [Gemini Directory Structure](#gemini-directory-structure)
    - [Gemini Frontmatter Requirements](#gemini-frontmatter-requirements)
    - [Gemini Example](#gemini-example)
  - [Setup Workflow](#setup-workflow)
    - [Creating a New Agent/Skill](#creating-a-new-agentskill)
  - [Migration Tips](#migration-tips)
    - [Cursor → Claude](#cursor--claude)
    - [Cursor → Gemini](#cursor--gemini)
    - [Claude → Cursor](#claude--cursor)
    - [Claude → Gemini](#claude--gemini)
    - [Maintaining Consistency](#maintaining-consistency)
  - [Appendix: Common Frontmatter Values](#appendix-common-frontmatter-values)
    - [Tools (Claude/Gemini)](#tools-claudegemini)
    - [Models](#models)
    - [Colors](#colors)

---

## Cursor

Cursor uses **Skills** to extend its capabilities. Skills are specialized instruction sets that guide the AI for specific tasks.

### Cursor Directory Structure

```
~/.cursor/skills/
└── <skill-name>/
    └── SKILL.md
```

**Key points:**
- Each skill lives in its own directory named after the skill
- The instruction file must be named exactly `SKILL.md` (case-sensitive)
- Global skills go in `~/.cursor/skills/`
- Project-level skills can be placed in `.cursor/skills/` within your project

**Tip:** You can symlink from `~/.cursor/skills/` to another directory if you want to manage skills in a different location (e.g., a version-controlled repo).

### Cursor Frontmatter Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the skill (kebab-case recommended) |
| `description` | Yes | When to use this skill; helps Cursor select the right skill |

### Cursor Example

```yaml
---
name: tailwind-bem-stylist
description: Use this skill when you need to style UI components using Tailwind CSS with BEM naming conventions. This includes tasks like creating new component styles, refactoring existing Tailwind utility clusters into maintainable BEM classes, organizing CSS layers, improving template readability, or ensuring consistent styling patterns across a codebase.
---

# Tailwind BEM Stylist

You are an expert Tailwind CSS styling specialist...
```

---

## Claude

Claude Code uses **Agents** to handle specialized tasks. Agents are defined with frontmatter that specifies their capabilities, tools, and visual identity.

### Claude Directory Structure

```
~/.claude/agents/
├── django-backend-dev.md
├── vue3-typescript-agent.md
└── tailwind-css-auditor.md
```

**Key points:**
- Flat file structure (no subdirectories required)
- Files use `.md` extension
- Agent name is typically the filename (kebab-case)
- Global agents go in `~/.claude/agents/`
- Project-level agents can be placed in `.claude/agents/` within your project

### Claude Frontmatter Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the agent |
| `description` | Yes | When to use this agent; include `<example>` tags for better selection |
| `tools` | Yes | Comma-separated list of available tools (e.g., `Read, Write, Glob, Grep`) |
| `model` | Yes | Model to use (e.g., `sonnet`, `haiku`, `opus`) |
| `color` | Yes | UI color for the agent (e.g., `yellow`, `green`, `purple`, `cyan`) |

**Available Tools:**
- `Read` - Read file contents
- `Write` - Write/create files
- `Edit` - Edit existing files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `TodoWrite` - Manage task lists

**Available Colors:**
- `yellow`, `green`, `purple`, `cyan`, `red`, `blue`, `orange`

### Claude Example Tags

Claude uses `<example>` tags in the description to help with agent selection. Format:

```
<example>
Context: Brief context about the situation.
user: "Example user message"
assistant: "Example assistant response explaining agent selection"
<commentary>
Why this agent is appropriate for this request.
</commentary>
</example>
```

### Claude Example

```yaml
---
name: tailwind-css-auditor
description: Use this agent when you need to audit and improve Tailwind CSS usage in an existing project. This includes identifying class duplication, consolidating repetitive patterns into BEM components using @apply, standardizing spacing/typography/design tokens, and improving template readability.\n\n<example>\nContext: User has completed a feature and wants to clean up the Tailwind usage before merging.\nuser: "I just finished the dashboard feature. Can you review the Tailwind CSS usage?"\nassistant: "I'll use the tailwind-css-auditor agent to review the Tailwind CSS patterns in your dashboard feature and identify consolidation opportunities."\n<commentary>\nSince the user wants to review Tailwind CSS usage in completed code, use the tailwind-css-auditor agent to analyze patterns and propose refactors.\n</commentary>\n</example>
tools: Glob, Grep, Read, Write
model: sonnet
color: yellow
---

You are an expert Tailwind CSS auditor specializing in codebase hygiene...
```

---

## Gemini

Gemini CLI supports both **Agents** and **Skills**, giving you flexibility in how you organize your workflows.

### Gemini Agents vs Skills

| Aspect | Agents | Skills |
|--------|--------|--------|
| **Purpose** | Standalone task handlers | Reusable instruction sets |
| **Structure** | Flat `.md` files | Directory with `SKILL.md` |
| **Invocation** | Called directly by name | Referenced by other agents/skills |
| **Use Case** | Complete workflows | Specialized capabilities |

**When to use Agents:**
- Self-contained tasks that don't need to be composed
- Direct user-facing workflows
- Tasks with specific tool requirements

**When to use Skills:**
- Reusable expertise that multiple agents might need
- Specialized knowledge domains
- Composable building blocks

### Gemini Directory Structure

**Agents:**
```
~/.gemini/agents/
├── django-backend-dev.md
├── vue3-typescript-agent.md
└── tailwind-css-auditor.md
```

**Skills:**
```
~/.gemini/skills/
└── <skill-name>/
    └── SKILL.md
```

**Key points:**
- Agents use flat file structure
- Skills use directory structure (like Cursor)
- Global location: `~/.gemini/agents/` and `~/.gemini/skills/`
- Project-level: `.gemini/agents/` and `.gemini/skills/`

### Gemini Frontmatter Requirements

**Agents:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the agent |
| `description` | Yes | When to use this agent; include `<example>` tags |
| `tools` | Yes | Comma-separated list of available tools |
| `model` | Yes | Model to use (e.g., `sonnet`, `haiku`) |
| `color` | Yes | UI color for the agent |

**Skills:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the skill |
| `description` | Yes | When to use this skill; can include `<example>` tags |

### Gemini Example

**Agent (`gemini/agents/tailwind-css-auditor.md`):**

```yaml
---
name: tailwind-css-auditor
description: Use this agent when you need to audit and improve Tailwind CSS usage in an existing project.\n\n<example>\nContext: User notices their project has inconsistent button styles.\nuser: "Our buttons look inconsistent everywhere. Can you help?"\nassistant: "I'll launch the tailwind-css-auditor agent to audit your button patterns."\n</example>
tools: Glob, Grep, Read, Write
model: sonnet
color: yellow
---

You are an expert Tailwind CSS auditor...
```

**Skill (`gemini/skills/tailwind-css-auditor/SKILL.md`):**

```yaml
---
name: tailwind-css-auditor
description: |
  Use this skill when you need to audit and improve Tailwind CSS usage in an existing project.

  <example>
  Context: User has completed a feature and wants to clean up the Tailwind usage.
  user: "I just finished the dashboard feature. Can you review the Tailwind CSS usage?"
  assistant: "I'll use the tailwind-css-auditor skill to review the patterns."
  </example>
---

You are an expert Tailwind CSS auditor...
```

**Note:** Skills can use YAML multiline strings (`|`) for cleaner formatting of the description.

---

## Setup Workflow

### Creating a New Agent/Skill

1. **Decide on the scope**
   - What specific tasks will this agent/skill handle?
   - What tools does it need?
   - Should it be global or project-specific?

2. **Choose the provider format**
   - Cursor: Skill only
   - Claude: Agent only
   - Gemini: Agent or Skill (or both)

3. **Create the file structure**
   ```bash
   # Cursor skill
   mkdir -p ~/.cursor/skills/my-skill
   touch ~/.cursor/skills/my-skill/SKILL.md

   # Claude agent
   touch ~/.claude/agents/my-agent.md

   # Gemini agent
   touch ~/.gemini/agents/my-agent.md

   # Gemini skill
   mkdir -p ~/.gemini/skills/my-skill
   touch ~/.gemini/skills/my-skill/SKILL.md
   ```

4. **Write the frontmatter**
   - Start with required fields for your provider
   - Write a clear, specific description
   - Add example tags for better selection (Claude/Gemini)

5. **Write the system prompt**
   - Define the agent's role and expertise
   - Specify scope boundaries (what it does and doesn't do)
   - Include methodology and output format expectations
   - Add quality checklists if appropriate

6. **Test the agent/skill**
   - Try various prompts that should trigger it
   - Verify it stays within its defined scope
   - Check that outputs match expected format

---

## Migration Tips

### Cursor → Claude

1. Change directory structure from `<name>/SKILL.md` to `<name>.md`
2. Add required frontmatter fields: `tools`, `model`, `color`
3. Consider adding `<example>` tags to the description
4. Replace "skill" terminology with "agent" in the prompt

### Cursor → Gemini

**As Agent:**
1. Change to flat file structure
2. Add required frontmatter fields: `tools`, `model`, `color`
3. Add `<example>` tags to description

**As Skill:**
1. Keep the same directory structure
2. Optionally add `<example>` tags
3. Consider using YAML multiline (`|`) for description

### Claude → Cursor

1. Create directory structure: `<name>/SKILL.md`
2. Remove `tools`, `model`, `color` from frontmatter
3. Remove `<example>` tags from description (or keep for context)
4. Replace "agent" terminology with "skill" in the prompt

### Claude → Gemini

1. Structure is nearly identical for agents
2. Verify tool names match Gemini's available tools
3. Verify model names are valid for Gemini
4. Optionally create a skill version as well

### Maintaining Consistency

When managing the same agent/skill across multiple providers:

1. **Keep a canonical version** - Pick one provider as the source of truth
2. **Document differences** - Note provider-specific adaptations
3. **Use symlinks for Cursor** - Point `~/.cursor/skills/` to your repo
4. **Version control everything** - Keep all definitions in a single repo
5. **Automate sync** - Consider scripts to propagate changes

---

## Appendix: Common Frontmatter Values

### Tools (Claude/Gemini)

https://platform.claude.com/docs/en/agent-sdk/overview#capabilities

| Tool | Description |
|------|-------------|
| `Read` | Read file contents |
| `Write` | Create or overwrite files |
| `Edit` | Modify existing files |
| `Glob` | Find files by pattern |
| `Grep` | Search file contents |
| `TodoWrite` | Manage task lists |

### Models

| Provider | Options |
|----------|---------|
| Claude | `opus`, `sonnet`, `haiku` |
| Gemini | `sonnet`, `haiku` (may vary) |

### Colors

Available colors for agent UI: `yellow`, `green`, `purple`, `cyan`, `red`, `blue`, `orange`
