---
name: greenfield-decomposer
description: Break down a greenfield project blueprint into executable task-creator-ready research documents. Use after greenfield-init has produced a project blueprint, or when a project plan needs to be decomposed into buildable chunks with validation gates.
---

# Greenfield Decomposer

Recursively break down project blueprint phases into task-creator-ready research documents.

## When to Use

- A `PROJECT_BLUEPRINT.md` exists from `greenfield-init`
- You need to decompose a specific phase into executable work
- Work items are too large for task-creator to handle directly

## Input Requirements

1. **Project path** — The `.agent-tasks/tasks/[YYYYMMDD-project-name]/` folder
2. **Phase** — Which phase to decompose (or "next" to pick the first incomplete phase)

## Behavior

### 1. Read the Guides

Read and internalize (located in this skill folder):
- `DECOMPOSITION_GUIDE.md` — Rules for breaking phases into chunks
- `VALIDATION_GATES.md` — Standard validation patterns per task type

### 2. Read Project Context

Read from the project folder:
- `research/PROJECT_BLUEPRINT.md` — Full project plan
- `research/API_CONTRACT.md` — Interface contract (if it exists)
- Any existing phase research docs (to understand what's already been decomposed)
- Any completed tasks (for context on what's already built)

### 3. Decompose the Phase

For the target phase:

1. **List the work** — Everything that needs to happen in this phase
2. **Categorize each item** using categories from `DECOMPOSITION_GUIDE.md`:
   - Scaffolding, Models, Endpoints, Components, Integration, Configuration
3. **Order by dependency** — What depends on what within the phase
4. **Size check each item** — Can a single sub-agent complete this in one session?
   - **Yes** → It's task-creator-ready
   - **No** → Break it down further, then size check again

### 4. Attach Validation Gates

Every work item gets a validation gate from `VALIDATION_GATES.md`:

- **Executable** — A command, a request, or a visible result
- **Binary** — Pass or fail, no subjective judgment
- **Immediate** — Verifiable right after the work is done

### 5. Identify Parallel Tracks

Within the phase, determine what can run in parallel:

- Items with no shared dependencies can be parallelized
- Items touching the same files must be sequential
- Frontend and backend items referencing the API contract can be parallel
- Group parallel items explicitly in the research document

### 6. Produce Research Document

Write a research document for the phase to:
`research/PHASE-[N]-[phase-name].md`

This document is the input for task-creator. Structure it so task-creator can read it and produce task files directly.

### Research Document Format

```markdown
# Phase [N]: [Phase Name]

**Source:** PROJECT_BLUEPRINT.md, Phase [N]
**Goal:** [Phase goal from blueprint]
**Validation gate:** [Phase-level gate from blueprint]

---

## Work Items

### [N.1] [Item Name]

**Category:** [scaffolding/models/endpoints/components/integration/config]
**Dependencies:** None | [Item N.X]
**Parallel with:** [Item N.X] | None

**What to do:**
[Clear description of the work]

**Scope:**
[Files/directories involved]

**Validation:**
- [ ] [Executable gate]

---

### [N.2] [Item Name]
...

## Execution Order

1. Items N.1-N.3 can run in parallel (no shared dependencies)
2. Item N.4 depends on N.1 completing
3. ...

## Phase Complete When

- [ ] All work items complete
- [ ] Phase validation gate passes: [gate from blueprint]
```

### 7. Hand Off

After producing the research document:

> Phase [N] decomposed into [X] work items. Next step: use the `task-creator` skill to generate task files.
>
> ```
> Use the task-creator skill to generate tasks from:
> - task: [YYYYMMDD-project-name]
> - Source: .agent-tasks/tasks/[YYYYMMDD-project-name]/research/PHASE-[N]-[phase-name].md
> ```

## Decomposition Rules

### The "Single Session" Test

A chunk is small enough when a sub-agent can:
1. Read the task
2. Make the changes
3. Verify the result
4. All within a single conversation session

If a chunk requires the agent to "come back later" or "check after restart", it's too big.

### The "Runnable System" Rule

After all tasks in a phase are complete, the system must be in a runnable state. Never leave the system broken between phases.

### Recursion Depth

| Level | Artifact | Produced by |
|-------|----------|-------------|
| Blueprint | Phases | greenfield-init |
| Phase | Work items | greenfield-decomposer |
| Work item | Task files | task-creator |
| Task file | Execution | task-orchestrator |

If a work item is still too large, break it into sub-items at the same level. Flatten into sequential work items with dependencies — do not create deeper nesting.

### One Phase at a Time

Decompose and complete one phase before starting the next. This ensures the validation gate passes and the system is in a known-good state before building on top of it.

## Quality Checklist

Before finalizing a phase research document:

- [ ] Every item passes the "single session" test
- [ ] Every item has a validation gate
- [ ] Items are ordered by dependency
- [ ] Parallel tracks are identified and labeled
- [ ] The phase ends with a runnable system
- [ ] Document follows the research document format above
