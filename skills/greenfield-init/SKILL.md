---
name: greenfield-init
description: Plan and structure a new application from a vague prompt or PRD. Use when starting a greenfield project, building an app from scratch, or when the user provides a project idea or PRD that needs to be broken down into a structured development plan.
---

# Greenfield Init

Transform a vague project idea or PRD into a structured, phase-gated project blueprint.

## When to Use

- User describes a new application they want to build
- User provides a PRD or feature spec for a new project
- User says "build me...", "I want to create...", or similar greenfield language
- A project needs structured planning before any code is written

## Input Requirements

One of:
1. **Vague prompt** — A description of what the user wants to build
2. **PRD file** — Path to a product requirements document

## Behavior

### 1. Read the Guides

Read and internalize:
- `DEFAULT_STACK.md` — Standard tech stack and packages (in this skill folder)
- `VERSIONS.md` — Canonical versions for all technologies (**greenfield only** — this file lives at the ai-agents repo root, not inside the skill folder)
- `BLUEPRINT_GUIDE.md` — Blueprint document structure and template (in this skill folder)
- `CONTRACT_GUIDE.md` — API interface contract format (in this skill folder)

Also read the relevant skill:
- `environments` skill — environment setup specs for each stack layer (Python/uv, Node/npm, Docker)

### 2. Parse Input & Gap Analysis

Read the user's prompt or PRD and extract:
- **Stated requirements** — What's explicitly described
- **Implied requirements** — What the description assumes (auth, persistence, etc.)
- **Missing requirements** — What's not addressed but needed

Categorize gaps as:
- **Blocking** — Cannot plan without this (core user flows, data entities)
- **Assumable** — Can use sensible defaults (stack, auth method, deployment)

### 3. Fill Gaps

For **blocking gaps**, use the AskQuestion tool to get targeted answers. Group related questions together. Focus on:

- Who are the users? Are there roles/permissions?
- What are the 3-5 core user flows?
- What are the main data entities and their relationships?
- Any third-party integrations?
- Real-time requirements?
- Scale expectations (small team tool vs. public SaaS)?

For **assumable gaps**, apply defaults from `DEFAULT_STACK.md` and state assumptions explicitly in the blueprint.

### 4. Define the Stack

Start with `DEFAULT_STACK.md` as the baseline. Adjust only if the project requirements demand it (e.g., real-time heavy → add django-channels + WebSocket support).

Present the stack to the user for confirmation. If they have no opinion, use the defaults.

### 5. Define Development Phases

Break the project into sequential phases. Each phase must have:

| Field | Description |
|-------|-------------|
| **Name** | Short descriptive name |
| **Goal** | What this phase accomplishes |
| **Depends on** | Which prior phases must be complete |
| **Validation gate** | How to prove this phase works before moving on |
| **Parallel streams** | Whether frontend/backend can run independently |

Standard phase pattern (adjust per project):

1. **Project scaffolding** — Both projects created, dependencies installed, dev servers running
2. **Data layer** — Models, migrations, admin, seed data
3. **Auth** — Registration, login, permissions
4. **Core features** — The 2-3 main features, usually parallelizable by stream
5. **Integration** — Connect frontend to backend using the API contract
6. **Polish & edge cases** — Error handling, loading states, validation

### 6. Map Parallelism

For any phase where frontend and backend can proceed independently:

1. Identify the API surface that connects them
2. Produce an API contract following `CONTRACT_GUIDE.md`
3. Both streams build against the contract
4. Integration phase verifies contract compliance

### 7. Establish Design System

Before scaffolding, define the design system to prevent the duplication issues found in audits (form inputs copy-pasted with 45+ character utility strings, buttons repeated across views, hardcoded colors instead of theme tokens).

**Include in the blueprint:**
- **Theme tokens:** primary, secondary, error, success colors defined as CSS custom properties
- **BEM component classes:** Pre-defined in `@layer components` for forms, buttons, alerts, navigation
- **Spacing scale:** Limited steps (2, 4, 6, 8, 12, 16, 24, 32)
- **Typography ramp:** Heading levels, body, caption sizes

**Reference:** See `DEFAULT_STACK.md` for the standard `@layer components` setup with BEM classes.

### 8. Output

Create the project folder structure and produce artifacts:

```
.agent-tasks/tasks/[YYYYMMDD-project-name]/
├── research/
│   ├── PROJECT_BLUEPRINT.md    # The full plan
│   └── API_CONTRACT.md         # Interface contract (if parallel streams)
├── pending/
├── in-progress/
├── complete/
├── testing/
└── agent-transcripts/
```

Follow the blueprint structure defined in `BLUEPRINT_GUIDE.md`.

### 9. Hand Off

After producing the blueprint, instruct the user:

> Blueprint complete. Next step: use the `greenfield-decomposer` skill to break Phase 1 into executable tasks.
>
> ```
> Use the greenfield-decomposer skill for .agent-tasks/tasks/[YYYYMMDD-project-name]/, starting with Phase 1.
> ```

## Quality Checklist

Before finalizing the blueprint:

- [ ] All blocking gaps are resolved (asked user or documented assumption)
- [ ] Stack is confirmed or defaults applied with assumptions stated
- [ ] Design system established with theme tokens and BEM component classes
- [ ] Every phase has a validation gate
- [ ] Phases are ordered by dependency
- [ ] Parallel streams have an API contract
- [ ] Blueprint follows `BLUEPRINT_GUIDE.md` format
- [ ] No more than 5-7 phases for an MVP
