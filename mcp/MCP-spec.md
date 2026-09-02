# Document 1: `MCP-spec.md`

```markdown
# Architectural Specification: Hybrid MCP & Harness Distribution

## 1. Executive Summary
This document specifies the target architecture for transitioning `ai-agents` from a pure filesystem-synced repository (`sync.sh`) into a **Two-Tier Hybrid Architecture**:
1. **Tier 1 (Universal MCP Server):** Protocol-standard MCP server exposing deterministic tools, reusable domain knowledge (resources), and prompt templates distributed directly from GitHub via `uvx`/`npx`.
2. **Tier 2 (Harness Subagent Core):** A streamlined local synchronization layer for proprietary agent personas, frontmatter injection, and subagent orchestration primitives.

---

## 2. Skill & Tool Decomposition Analysis

| Skill / Component | Target Layer | Execution Mechanism | Rationale & Migration Path |
| :--- | :--- | :--- | :--- |
| **`task-archiver`** | **Deterministic Script / MCP Tool** | Pure Python/Bash Script | **Shift to 100% script.** Archiving directories, running `tar -czvf`, and verifying files is deterministic logic. A small Python CLI or MCP tool `archive_task_directory(path)` eliminates LLM hallucinations during file deletion. |
| **`environments`** | **Deterministic Script / MCP Tool** | Shell / Python Probe | **Shift to script / MCP Tool.** Probing whether a project uses `uv`, `poetry`, `npm`, `pnpm`, or `docker` is best handled by deterministic file detection (`detect_environment()`) returning JSON/text. |
| **`coding-architect`** | **MCP Resource & Prompt** | `resource://skills/coding-architect` | **Standalone Knowledge.** Static rules, architecture patterns, and review checklists. Can be read by any agent across any harness without filesystem coupling. |
| **`gemini-researcher`** | **MCP Tool & Prompt** | MCP Tool + Prompt wrapper | **MCP Tool.** Wraps external search / Gemini API calls. Exposing it as an MCP tool standardizes research capabilities across all harnesses. |
| **`django-backend-dev`** | **MCP Resource / Prompt** | `resource://skills/django-backend-dev` | **Standalone Knowledge.** Backend conventions, security rules, and ORM guidelines. |
| **`vue3-typescript`** | **MCP Resource / Prompt** | `resource://skills/vue3-typescript` | **Standalone Knowledge.** Pinia, TypeScript, and Vue 3 composition conventions. |
| **`tailwind-bem-stylist`** | **MCP Resource / Prompt** | `resource://skills/tailwind-bem-stylist` | **Standalone Knowledge.** BEM class mapping and Tailwind `@apply` rules. |
| **`tailwind-auditor`** | **Hybrid (Script + Resource)** | Python regex script + Markdown rules | **Hybrid.** A deterministic script can scan for inline class string lengths (>50 chars) or duplicate utility clusters, while the LLM generates the refactored BEM classes. |
| **`prd-creator`** | **MCP Prompt Template** | `prompt://prd-creator` | **Interactive Prompt.** Guiding conversations from vague ideas to PRDs can be an MCP Prompt without local filesystem binding. |
| **`greenfield-init`** | **MCP Resource / Prompt** | `resource://skills/greenfield-init` | **Project Scaffold Knowledge.** Stack definitions and blueprint guides. |
| **`greenfield-decomposer`**| **MCP Resource / Prompt** | `resource://skills/greenfield-decomposer` | **Planning Knowledge.** Validation gate templates and decomposition rules. |
| **`task-creator`** | **Hybrid / Script-backed Skill**| Embedded script template + skill | **Hybrid.** Keep the task formatting rules in prompt/skill, but embed a small python helper to validate task directory numbering and schema. |
| **`task-orchestrator`** | **Local Harness Skill** | Local `~/.config/opencode/` / `~/.claude/` | **Harness-Bound.** Orchestrators spawn native subagents using harness-specific tools (`task` in OpenCode, subagents in Claude Code). Must remain local. |
| **`greenfield-one-shot`** | **Local Harness Skill** | Local `~/.config/opencode/` / `~/.claude/` | **Harness-Bound.** Chaining subagent phases across validation gates relies on harness-level agent lifecycle management. |

---

## 3. Repurposing Small Models & Subagents

### 3.1 The Problem with LLM Code Generation on Small Models
`small-subagent` and `small-model-orchestrator` faced reliability issues because small local LLMs (e.g., 7B–14B parameters) struggle with multi-file contextual awareness, strict AST adherence, and nuanced code generation.

### 3.2 The Shift: Deterministic Tasks & Micro-Validations
Instead of retiring local models or trying to force them to write complex code, repurpose local scripts/small models for:
1. **Deterministic Script Replacements:** Turn repetitive file manipulations (archiving, environment probing, lint formatting) into standard Python/Bash scripts rather than agent workflows.
2. **Fast Micro-Tasks:** Use local small models purely for:
   * Generating commit messages from `git diff`.
   * Summarizing raw terminal logs.
   * Classifying error messages.
   * Checking JSON/YAML syntax validation.

---

## 4. Referencing MCP Resources from Local Agent Personas

When an agent persona remains local (e.g., `agents/advisor.md`), it can reference MCP resources rather than hardcoded filesystem paths:

### Old Pattern (Filesystem-coupled):
```markdown
- When asked about coding plans, refer to the `coding-architect` skill (read `../skills/coding-architect/SKILL.md` if necessary).
```

### New Pattern (MCP-decoupled):
```markdown
- When asked about coding plans, inspect the MCP resource `resource://ai-agents/coding-architect` or invoke the `get_architecture_guidelines` tool.
```

---

## 5. Deployment & Distribution Architecture

```
GitHub Repo (github.com/your-username/ai-agents)
   │
   ├── [stdio MCP Server via uvx/npx]
   │      ├── Prompts:  prd-creator, quick-learn, framework guides
   │      ├── Resources: coding-architect, django-backend-dev, vue3-ts
   │      └── Tools:    detect_environment, archive_task_folder, audit_tailwind
   │
   └── [sync.sh / CLI Installer]
          └── Deploys to ~/.config/opencode/ and ~/.claude/:
                 ├── Native Agent Personas (advisor.md, research.md)
                 └── Orchestration Skills (task-orchestrator, greenfield-one-shot)
```

### 5.1 Client Configuration (Zero External Hosting)
No cloud hosting or HTTP server required. Harnesses spawn the MCP server via `stdio` over `uvx`:

```json
{
  "mcpServers": {
    "agent-toolkit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/your-username/ai-agents", "agent-toolkit-mcp"]
    }
  }
}
```

