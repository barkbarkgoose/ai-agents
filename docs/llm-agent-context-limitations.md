# LLM Agent Context — Modular File Limitations

## Problem Statement

When building a library of reusable agent definitions, skills, and orchestration
prompts, the natural instinct is to decompose them into small, modular files that
reference each other — the same way you'd structure application code. In practice,
this modularity conflicts with how LLMs consume context in tools like Cursor,
Windsurf, Cline, and similar AI coding assistants.

This document explains **why** modular file chains break down, **how** LLMs
actually receive and process file context, and **what** the industry recommends
instead.

---

## How LLMs Receive File Context

Understanding the mechanics is key to understanding the limitations.

### The Context Window Is Flat

An LLM does not have a filesystem. It receives a single, linear sequence of tokens
— the **context window**. Everything the model knows about your project comes from
what has been injected into that window before it generates a response.

When you `@`-reference a file in Cursor (or equivalent in other tools), the IDE
reads that file and pastes its contents into the context window as plain text. The
model sees it the same way it sees your chat message — as a block of characters
with no special powers.

### File References Are Not Followed

A markdown link like `[orchestrator](./generic-subagent-orchestrator.md)` is just
text to the model. The IDE does **not**:

- Crawl markdown links to load referenced files
- Resolve relative paths and inject linked content
- Build a dependency graph of skill/agent files
- Recursively expand `@` symbols found inside file contents

Each `@`-reference in the chat input is a **one-shot, flat file read**. If file A
references file B, and you only `@`-reference file A, the model never sees file B.

### The Model Can Choose to Read Files — But Often Won't

The model has access to a Read tool and *can* fetch files on its own. But this
depends on:

1. The model recognizing that it needs to read another file
2. The model deciding to spend a tool call on it (vs. just proceeding)
3. The instruction to read being explicit and imperative enough

In practice, models are biased toward acting on what they already have. If the
context window contains a file that says "refer to X for instructions," the model
frequently interprets the *reference* as sufficient context and skips the read —
especially when the surrounding content gives it enough information to start
generating a plausible (but incomplete) response.

---

## Why Modular File Chains Fail

### The Indirection Problem

Consider this chain:

```
orchestrator.md
  → "proceed as the [subagent orchestrator](./generic-orchestrator.md)"
    → "refer to the [skill](../skills/orchestrator/SKILL.md) for instructions"
      → (actual orchestration instructions)
```

When the user `@`-references `orchestrator.md`, the model sees step 1. It never
sees steps 2 or 3. The critical behavioral rules ("MUST use sub-agents," the
workflow, the file structure conventions) live at the end of a chain the model
cannot traverse on its own.

The result: the model reads a high-level description of available agents and a
vague instruction to "proceed as" something, then improvises. It has enough
context to *start* working but not enough to follow the intended delegation
pattern — so it does all the work itself.

### Declarations vs. Directives

Modular files tend to be written as **declarations** — they describe what
something is, what agents are available, what the order should be. This is useful
for human readers navigating a docs structure.

LLMs respond much better to **directives** — imperative, second-person
instructions that tell the model exactly what to do. Compare:

**Declaration (weak):**
> Available agents: django-backend-dev, vue3-typescript, tailwind-bem-stylist

**Directive (strong):**
> You MUST spawn a sub-agent for every task. Never execute tasks directly. Use
> the Task tool with `subagent_type` matching the task's target agent.

The declaration gives the model information. The directive gives it a constraint.
Without the constraint, the model defaults to its own judgment — which usually
means doing the work inline.

### Frontmatter Noise

Agent definition files often include YAML frontmatter (`name`, `description`,
`tools`, `model`, `color`). When these files are loaded by the agent framework
as configuration, the frontmatter is parsed and applied structurally. When the
same files are `@`-referenced as context, the frontmatter is just text — and
potentially confusing text that the model might try to interpret or act on
incorrectly.

---

## Industry Best Practices

### 1. Self-Contained Prompt Files

The most reliable pattern is a **single file that contains everything the model
needs** to perform its role. No links to follow, no files to discover, no
indirection.

This is the approach used by most successful agent frameworks (AutoGPT, CrewAI,
custom GPT instructions). The "system prompt" is one complete document.

**Why it works:** The model sees all constraints, workflows, and rules in a
single context injection. There is zero chance of a missed file.

**Trade-off:** Duplication. If multiple orchestrators share the same base
workflow, you maintain copies. This is acceptable because prompt files are small
and the cost of duplication is far lower than the cost of broken delegation.

### 2. Explicit Context Lists

If modularity is important (e.g., shared skills across projects), the prompt file
should include an explicit list of every file the model needs to read, with
imperative language:

```markdown
**Before proceeding, you MUST read the following files in order:**
1. `.ai/skills/generic-subagent-orchestrator/SKILL.md`
2. `.ai/skills/task-creator/SKILL.md`

Do not begin executing tasks until you have read and understood both files.
```

This works better than markdown links because:
- The instruction is imperative ("MUST read"), not passive ("refer to")
- The file paths are absolute from project root, not relative
- The model is told to read *before* acting, creating a sequencing constraint

**Trade-off:** The model still has to choose to follow the instruction. Strong
phrasing helps but is not guaranteed.

### 3. Layered Context via Multiple `@` References

The most robust modular approach is to have the **user** (or a wrapper script)
inject all required files as separate `@`-references in the chat input:

```
@.ai/agents/django-vue-orchestrator.md
@.ai/skills/generic-subagent-orchestrator/SKILL.md
@.agent-tasks/tasks/20260218-project/CONTROLLER.md
```

This guarantees every file's contents appear in the context window. The model
doesn't need to discover or read anything — it's all already there.

**Trade-off:** The user must know which files to include. This can be mitigated
with a checklist in the main prompt file or a launcher script.

### 4. Inline Expansion at Reference Time

Some teams build a simple preprocessor that resolves `@include` or similar
directives at prompt-assembly time, producing a single expanded document from
modular source files. This gives you the maintainability of separate files with
the reliability of a single prompt.

```markdown
<!-- @include ./skills/orchestrator-workflow.md -->
<!-- @include ./skills/task-creator.md -->
```

A build step concatenates these into one file before it hits the model.

**Trade-off:** Requires tooling. Not natively supported by any IDE-based agent
system today — it would need to be a custom script or pre-commit hook.

---

## Recommendation Summary

| Approach | Reliability | Modularity | Effort |
|---|---|---|---|
| Self-contained prompt | Highest | None | Low (some duplication) |
| Explicit "MUST read" instructions | High | Moderate | Low |
| Multiple `@` references | High | High | Medium (user must know files) |
| Preprocessor/include expansion | Highest | High | High (custom tooling) |

For most workflows, **self-contained prompts** are the right default. Reserve
modular approaches for cases where the same skill genuinely needs to be shared
across multiple agents or projects, and even then, prefer explicit `@`-reference
lists over markdown link chains.

---

## Key Takeaway

LLMs are not programs that execute file references. They are text processors that
act on whatever text is in their context window. Design your agent/skill
architecture around this constraint: **if the model doesn't see it, it doesn't
exist.**
