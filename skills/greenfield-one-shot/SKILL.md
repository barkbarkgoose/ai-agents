---
name: greenfield-one-shot
description: One-shot greenfield build orchestration. Takes a project blueprint and executes the full build pipeline using subagents for each phase, including intermediate verification gates. Use when you want to run an entire greenfield project build in one session without manual intervention between phases.
---

# Greenfield One-Shot Orchestrator

Execute a complete greenfield project build from blueprint to working system using phased subagent execution.

**You own the full project lifecycle** — not just individual task orchestration, but all phases from initial decomposition through final polish and verification.

## When to Use

- You have a `PROJECT_BLUEPRINT.md` from `greenfield-init`
- You want to build the entire project in one session without manual intervention
- You want intermediate verification gates between major phases

**This is a full-lifecycle skill.** One invocation handles decomposition, task creation, task execution across all phases, gate verification, and polish — until the project is complete.

## Input Requirements

- **Project path**: `.agent-tasks/tasks/[YYYYMMDD-project-name]/`
- **Project blueprint**: `research/PROJECT_BLUEPRINT.md`
- **API contract** (if parallel streams): `research/API_CONTRACT.md`

## Prerequisites

Read and internalize these skill files before starting:

1. **Decomposition logic**: `./greenfield-decomposer/DECOMPOSITION_GUIDE.md`
2. **Validation gates**: `./greenfield-decomposer/VALIDATION_GATES.md`
3. **Task structure**: `./task-creator/TASK_STRUCTURE_GUIDE.md`
4. **Task creation**: `./task-creator/TASK_CREATION_GUIDE.md`
5. **Tailwind auditing**: `./tailwind-auditor/SKILL.md` (read during Phase 2)
6. **Vue3 frontend**: `./vue3-typescript/SKILL.md` (read during frontend work)
7. **Django backend**: `./django-backend-dev/SKILL.md` (read during backend work)

## Orchestration Architecture

**You ARE the full project orchestrator.** You do NOT spawn a separate orchestrator subagent. You own the entire greenfield project from Phase 0 through Phase 5 — including decomposition, task creation, task execution, gate verification, and phase transitions.

---

## Critical Rules

- **MUST use subagents for ALL work** — Never execute tasks directly yourself; every action must be a subagent. Your only direct actions are: spawning subagents, moving task files between folders, updating ORCHESTRATOR.md, and verifying gates.
- **MUST include stack context in every subagent prompt** — Always prefix with the Project Stack block (template below)
- **MUST verify subagent completion** — After each subagent finishes, immediately move task file and update ORCHESTRATOR.md
- **MUST respect phase order** — Tasks execute in the order defined by the blueprint; do not start a phase until its gate passes
- **MUST save transcripts** — Every subagent must save a transcript to `agent-transcripts/`

---

Your role:
1. Read and understand the blueprint (stack is defined in PROJECT_BLUEPRINT.md)
2. Decompose each phase into work items using greenfield-decomposer
3. Create task files via task-creator subagents
4. Spawn subagents to execute tasks
5. Verify phase gates before proceeding
6. Run tailwind-auditor at the appropriate phase
7. Repeat until the full project is complete

---

## Execution Flow

### Phase 0: Project Setup

1. Read `PROJECT_BLUEPRINT.md` to understand the full scope
2. Read `API_CONTRACT.md` if it exists
3. Create the project folder structure:
   ```
   .agent-tasks/tasks/[YYYYMMDD-project-name]/
   ├── ORCHESTRATOR.md          # Main tracking document (you maintain this)
   ├── research/                # Blueprint and contracts
   ├── pending/                 # Tasks not yet started
   ├── in-progress/             # Currently active tasks
   ├── complete/                # Finished tasks
   ├── testing/                 # Testing strategies
   └── agent-transcripts/       # Sub-agent execution transcripts
   ```
4. Create `ORCHESTRATOR.md` with project overview, phases, and task tracking table

### Pre-Scaffold Validation (if using existing scaffold)

If a boilerplate scaffold already exists (e.g., cloned from a template), **do not assume it is valid**. Verify it works before skipping Phase 1:

**Scaffold Validation Checklist:**
- [ ] Backend: `uv run python manage.py check` exits 0
- [ ] Backend: `uv run python manage.py runserver` starts without errors
- [ ] Frontend: `npm run dev` starts without errors
- [ ] Frontend can reach backend API (CORS/proxy working)
- [ ] Django admin loads at /admin
- [ ] Custom User model and Organization model exist (if project uses them)
- [ ] Migrations have been applied (`uv run python manage.py migrate`)

**If any check fails:**
- Treat it as an incomplete scaffold — create tasks to fix the issues before proceeding
- Do not skip to Phase 2 assuming "it'll work later"
- Log failures in ORCHESTRATOR.md Progress Notes

**If all checks pass:**
- Mark Phase 1 (Scaffolding) as complete in ORCHESTRATOR.md
- Proceed directly to Phase 2 decomposition

### Phase 1: Project Scaffolding

**Decompose using greenfield-decomposer logic:**

1. Spawn a **decomposition subagent** to analyze Phase 1 and produce a research document
2. The decomposition subagent reads `DECOMPOSITION_GUIDE.md` and `VALIDATION_GATES.md` internally
3. Task creation is handled by spawning **task-creator subagents** for each work item (tasks are created in execution order per the blueprint)

**Execute Phase 1 tasks:**

For each task in Phase 1:
- Spawn a subagent with the task file contents
- Instruct the subagent to save a transcript to `agent-transcripts/[phase-#]-[task-id]-transcript.md`
- Track task completion in ORCHESTRATOR.md

**IMPORTANT — Avoid subagents for these operations:**
- **Do NOT spawn subagents for `npm install`** — it is too slow and prone to timeout. Run it directly yourself before spawning subagents, or document that dependencies should be pre-installed.
- **Do NOT spawn subagents to run dev servers** — subagents cannot reliably hold long-running processes.
- **Do NOT spawn subagents to run tests that spin up servers** — timeouts are likely. Run tests directly or use shorter-lived test commands.

**Verify Phase 1 gate:**
- Verify dev servers start for both frontend and backend
- If verification fails, troubleshoot and retry before proceeding

### Phase 2: Data Layer + Auth

**Backend: Models and Migrations**
- Spawn **django-backend-dev subagents** for model creation tasks
- Each subagent reads `./django-backend-dev/SKILL.md` internally
- Spawn a subagent to run `uv run python manage.py makemigrations` and `migrate`
- Verify tables exist via Django admin

**Frontend: Initial Components**
- Spawn **vue3-typescript subagents** for initial component creation
- Each subagent reads `./vue3-typescript/SKILL.md` internally
- Create auth forms (login, register) with mock data
- **Use BEM component classes** from the design system (`.form-input`, `.btn--primary`, `.alert--error`) instead of long Tailwind utility strings
- **Use theme tokens** (primary, secondary) instead of hardcoded colors (blue-600, gray-500)

**Run Tailwind Auditor (Mid-Phase)**
After frontend scaffolding is complete but before building out more components:
- Spawn a **tailwind-auditor subagent** to scan the project
- The subagent reads `./tailwind-auditor/SKILL.md` internally
- Verify the `@layer components` BEM classes are set up per `DEFAULT_STACK.md`
- Verify theme tokens are configured in `tailwind.config.js`
- If consolidation tasks are needed, create task files in `pending/`
- Execute consolidation tasks via **tailwind-bem-stylist subagents** (read `./tailwind-bem-stylist/SKILL.md`)

**Verify Phase 2 gate:**
- Backend: Models visible in Django admin, migrations applied
- Frontend: Auth forms render and are interactive

### Phase 3: Core Features (Backend + Frontend Parallel)

**Backend: API Endpoints**
- Spawn **django-backend-dev subagents** for each resource's CRUD endpoints
- Follow the pattern: serializer → viewset → URL route → permissions
- One subagent per resource

**Frontend: Feature Components**
- Spawn **vue3-typescript subagents** for each feature view
- Connect to API contract with mock/placeholder data initially
- Use Pinia for state management where needed
- **Use BEM component classes** from the design system instead of inline Tailwind clusters
- **Use theme tokens** (primary, secondary, error, success) for all colors

**Subagent Spawning Pattern:**
For each work item, spawn ONE subagent. Do NOT spawn subagents for sub-items within a task—the subagent handles all work in that task.

**Every subagent prompt MUST include the Project Stack block:**

```
Subagent Prompt Structure:
-----------------------
## Project Stack

This is a greenfield project.

- Language/Runtime: [from PROJECT_BLUEPRINT.md]
- Framework: [from PROJECT_BLUEPRINT.md]
- Package manager: [from PROJECT_BLUEPRINT.md]
- Key libraries: [from PROJECT_BLUEPRINT.md]
- Test runner: [from PROJECT_BLUEPRINT.md]

---

[Task file contents follow]

---

## Final Step
REQUIRED: Save your full transcript to:
`.agent-tasks/tasks/[YYYYMMDD-project-name]/agent-transcripts/[phase-#]-[task-id]-transcript.md`
```

### Phase 4: Integration

**Wire Frontend to Backend**
- Spawn **vue3-typescript subagents** to replace mock data with actual API calls
- Each subagent reads `API_CONTRACT.md` to understand endpoint shapes
- Implement error handling, loading states
- **Maintain BEM component class usage** — do not add inline Tailwind utility clusters when wiring components

**Verify Phase 4 gate:**
- End-to-end data flow works: frontend creates → backend persists → frontend displays
- Auth flow works: register → login → token storage → authenticated requests

### Phase 5: Polish

**Tailwind Audit + Consolidation**
- Run another **tailwind-auditor subagent** to check for any new class sprawl
- Verify BEM component classes are used consistently (no hardcoded color utilities replacing theme tokens)
- Execute remaining consolidation tasks via **tailwind-bem-stylist subagents**

**Error Handling + Edge Cases**
- Spawn subagents to handle edge cases identified in blueprint
- Verify all error states show meaningful messages

**Final Verification**
- Run lint/typecheck commands
- Verify all tests pass

---

## ORCHESTRATOR.md Format

Maintain this document throughout execution:

```markdown
# Project: [Project Name]

**Created:** YYYYMMDD
**Blueprint:** research/PROJECT_BLUEPRINT.md

## Project Stack

- Language/Runtime: [from blueprint]
- Framework: [from blueprint]
- Package manager: [from blueprint]
- Key libraries: [from blueprint]
- Test runner: [from blueprint]

## Phases

| Phase | Name | Status | Validation Gate |
|-------|------|--------|-----------------|
| 1 | Scaffolding | Complete | Dev servers start |
| 2 | Data Layer + Auth | Complete | Admin shows models, auth forms work |
| 3 | Core Features | In Progress | [pending] |
| 4 | Integration | Pending | [pending] |
| 5 | Polish | Pending | [pending] |

## Task Summary

| Task ID | Phase | Name | Status | Agent |
|---------|-------|------|--------|-------|
| 001 | 1 | Create Django project | Complete | subagent |
| 002 | 1 | Create Vue project | Complete | subagent |
| ... | ... | ... | ... | ... |

## Progress Notes

**[Date] - Phase N: [Phase Name]**
- Tasks completed: [list]
- Issues encountered: [list]
- Next actions: [list]

## Current Phase Tasks

### Phase 3 Tasks

| Task ID | Name | Status | Dependencies |
|---------|------|--------|-------------|
| 015 | Create Project CRUD | In Progress | None |
| 016 | Create Task CRUD | Pending | 015 |
```

---

## Subagent Prompting Rules

**Every subagent prompt MUST include the Project Stack block** — This is non-negotiable.

### Language for Spawning Subagents

When you spawn a subagent, use EXPLICIT language:

**GOOD:**
```
Spawn a vue3-typescript subagent to execute Task 015.

The subagent should:
1. Read the task file at pending/phase-3-015-create-project-crud.md
2. Execute all work described in the task
3. Save transcript to agent-transcripts/phase-3-015-create-project-crud-transcript.md
4. Move task file from pending/ to complete/
```

**BAD:**
```
Use a subagent to work on the project CRUD task.
```

### Language for Using Skills as Subagents

When a work item requires a specialized skill, spawn the appropriate agent type:

**For django-backend-dev:**
```
Spawn a django-backend-dev subagent for Task 012.
```

**For vue3-typescript:**
```
Spawn a vue3-typescript subagent for Task 015.
```

**For tailwind-bem-stylist:**
```
Spawn a tailwind-bem-stylist subagent for the button consolidation task.
```

Each specialized agent reads its corresponding SKILL.md internally. You do NOT need to include the skill file contents in the prompt—the agent knows to read it.

### Language for Decomposition Subagents

When you need to decompose a phase:

**GOOD:**
```
Spawn a subagent to decompose Phase 3 using ./greenfield-decomposer/DECOMPOSITION_GUIDE.md and ./greenfield-decomposer/VALIDATION_GATES.md.

The subagent should:
1. Read PROJECT_BLUEPRINT.md and any existing phase research docs
2. Identify all work items in Phase 3
3. Create research/PHASE-3-[phase-name].md following the format in DECOMPOSITION_GUIDE.md
4. Spawn task-creator subagents to create task files from the research document
```

---

## Verification Gates

Verify each phase gate before proceeding to the next phase. If a gate fails:

1. Identify the failing component
2. Spawn a subagent to fix the issue
3. Re-run the verification
4. Do not proceed until the gate passes

### Standard Gates by Phase Type

**Scaffolding Gate:**
- [ ] Django: `uv run python manage.py check` passes
- [ ] Vue: `npm run dev` starts without errors
- [ ] Both projects can communicate (CORS configured, proxy working)

**Data Layer Gate:**
- [ ] `uv run python manage.py makemigrations` succeeds with no issues
- [ ] `uv run python manage.py migrate` applies cleanly
- [ ] Models appear in Django admin at /admin
- [ ] Seed data (if any) loads successfully

**Auth Gate:**
- [ ] Registration endpoint returns valid response
- [ ] Login endpoint returns JWT token
- [ ] Frontend auth forms accept input and handle responses

**Feature Gate:**
- [ ] Each endpoint returns expected response shape per API_CONTRACT.md
- [ ] Frontend components render without errors
- [ ] Navigation between views works

**Integration Gate:**
- [ ] Create via frontend → appears in backend admin
- [ ] Backend data → displays in frontend
- [ ] Auth state persists across page refresh

**Polish Gate:**
- [ ] `npm run lint` passes (frontend)
- [ ] `uv run python manage.py check` passes (backend)
- [ ] No console errors in browser
- [ ] All interactive elements have proper states (loading, error, empty)

---

## Error Handling

If a subagent fails:
1. Read the transcript at `agent-transcripts/[failed-task]-transcript.md`
2. Diagnose the issue
3. Either:
   - Spawn a new subagent with the fix instructions
   - Fix it yourself if it's a configuration issue
4. Log the issue and resolution in Progress Notes

If a phase gate fails:
1. Do not proceed to the next phase
2. Create tasks for any remaining work
3. Execute those tasks via subagents
4. Re-verify the gate

---

## Progress Tracking

**MUST verify subagent completion:**
After each subagent completes:
1. **Immediately** move the task file from `in-progress/` to `complete/`
2. Update ORCHESTRATOR.md task summary table (status → Complete)
3. Add entry to Progress Notes with completion details

After each phase completes:
1. Verify the phase gate
2. Update the Phases table in ORCHESTRATOR.md
3. Mark phase as complete
4. Begin the next phase

---

## Final Step

When all phases are complete and all gates pass:

1. Verify all task files are in `complete/`
2. Run final lint/typecheck verification
3. Update ORCHESTRATOR.md with final status
4. Report completion summary to the user