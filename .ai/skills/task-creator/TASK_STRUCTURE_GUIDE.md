# Task Structure Guide

## Project Structure

Organize tasks by project name for self-contained, referenceable work:

```
.agent-tasks/tasks/
└── [YYYYMMDD-project-name]/
    ├── CONTROLLER.md          # Main tracking document
    ├── research/                # Background materials, API docs, findings
    ├── pending/                 # Tasks not yet started
    ├── in-progress/             # Currently active tasks
    ├── complete/                # Finished tasks
    └── testing/                 # Testing strategies and test-related docs
```

### Naming Conventions

- **Project folders**: Use descriptive names (e.g., `facebook-api-v24-upgrade`)
- **Status folders**: Use semantic names (`pending`, `in-progress`, `complete`, `testing`)
- **Avoid numbered prefixes**: Skip `01-pending`, `02-in-progress` - readability over forced sorting

### Research vs Other Docs

- **`research/`**: Investigation findings, external documentation, audit results (created before tasks)
- **`testing/`**: Testing strategies, test plans (referenced during execution)
- **Project root**: Orchestrator and any cross-cutting documentation

## Workflow

### Starting a New Project

1. Create project folder: `.agent-tasks/tasks/[YYYYMMDD-project-name]/`
2. Create subdirectories: `research/`, `pending/`, `in-progress/`, `complete/`, `testing/`
3. Create `CONTROLLER.md` at project root
4. Gather research materials into `research/`
5. Break down work into task files in `pending/`

**Orchestrator Setup:**
- Include: Overview, key deadlines, simplified task summary (ID, Name, Status only)
- Include: Execution order with phases, dependencies, and parallel execution hints
- Include: Progress notes, rollback strategy, sign-off milestones
- Exclude: Research document references (research is for task creation, not execution)
- Keep lean: Orchestrator coordinates workflow; task files contain all technical context

**Starting the Orchestrator:**
- Use the generic [subagent-orchestrator](../subagent-orchestrator/SKILL.md)
- Or Prompt: "Follow `.ai/agents/subagent-orchestrator.md` for the [YYYYMMDD-project-name] project"
- The orchestrator will read the project's CONTROLLER.md and begin/resume work
- Works for both initial kickoff and resuming later (orchestrator checks current status)

### During Development

1. Orchestrator references tasks by status folder
2. Move tasks between folders as status changes
3. Keep orchestrator updated with progress
4. Add testing docs to `testing/` as needed

### Task Files

- One file per task
- Clear, descriptive filenames
- Self-contained with context, steps, and acceptance criteria

## Archiving Completed Projects

### When to Archive

- All tasks complete
- Testing finished
- No active work remaining

### Archive Process

**Option A: Archive Folder** (Recommended)

```
.agent-tasks/tasks/
├── [active-project]/
└── archive/
    └── [YYYYMMDD-project-name]/
        ├── CONTROLLER.md
        ├── SUMMARY.md              # Post-completion summary
        ├── research/
        ├── complete/
        └── testing/
```

**Steps:**
1. Create `.agent-tasks/tasks/archive/` if it doesn't exist
2. Move project folder to `.agent-tasks/archive/[YYYYMMDD-project-name]/`
3. Add `SUMMARY.md` with:
   - What was accomplished
   - Key decisions made
   - Lessons learned
   - Final status/outcome

**Option B: In-Place Archive**

Add to `CONTROLLER.md`:
```markdown
**Status**: ARCHIVED (YYYYMMDD)
```

**Option C: Git Tag**

```bash
git tag -a tasks/[project-name]-complete -m "Completed [project name]"
```

### Why Keep Archives in Repo

- Decision context stays with affected code
- Git history links decisions to changes
- Easy to reference in PRs and reviews
- No synchronization between repos needed
- Follows Architecture Decision Records (ADR) pattern

## Benefits of This Structure

- **Self-contained**: Each project is a complete historical record
- **Parallel work**: Multiple projects don't interfere
- **Context preservation**: Orchestrator scopes to specific project
- **Referenceable**: Easy to look back at what was done and why
- **Portable**: Can move/archive entire project folder

## Quick Reference

### Create New Project
```bash
mkdir -p .agent-tasks/tasks/[project-name]/{research,pending,in-progress,complete,testing}
touch .agent-tasks/tasks/[project-name]/CONTROLLER.md
```

### Start Orchestrator
```
Use `.ai/agents/subagent-orchestrator.md` for the [YYYYMMDD-project-name] project
```

### Archive Project
```bash
mkdir -p .agent-tasks/tasks/archive
mv .agent-tasks/tasks/[project-name] .agent-tasks/tasks/archive/[YYYYMMDD-project-name]
# Add SUMMARY.md to archived project
```
