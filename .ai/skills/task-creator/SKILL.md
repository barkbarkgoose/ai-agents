# Skill: Task Creator

Create implementation tasks from research and audit documents.

## When to Use

Use this skill when:
- You have research or audit documents that identify work to be done
- You need to break down a larger effort into individual, actionable tasks
- You're preparing work for an orchestrator to execute via sub-agents

## Input Requirements

You must be provided:
1. **Project name** — Used to locate/create the task directory
2. **Source document(s)** — Path(s) to research or audit documents in `research/`

## Behavior

### 1. Read the Guides

Read and internalize (located in this skill folder):
- `TASK_STRUCTURE_GUIDE.md` — Folder conventions and project layout
- `TASK_CREATION_GUIDE.md` — Task file format and writing rules

### 2. Analyze Source Documents

Read the provided research/audit documents and identify:
- Discrete pieces of work that can be completed independently
- Dependencies between pieces of work
- Any work that requires further research (separate from implementation)

### 3. Create Task Files

For each piece of work identified:

1. Determine the next available task number (check existing files in `pending/`)
2. Create task file: `.agent-tasks/tasks/[YYYYMMDD-project-name]/pending/XXX-[action]-[subject].md`
3. Follow the task format defined in `TASK_CREATION_GUIDE.md`
4. Set appropriate category (`implementation` or `research`)

### 4. Report Results

After creating all tasks, provide:
- List of created task files
- Brief description of each task
- Any suggested execution order or dependencies
- Any items that couldn't be turned into tasks (and why)

## Task Numbering

- Check existing files in `pending/`, `in-progress/`, and `complete/`
- Use the next available 3-digit number (001, 002, ...)
- Numbers should be sequential within the project

## Quality Checklist

Before finalizing each task, verify:
- [ ] Follows format from `TASK_CREATION_GUIDE.md`
- [ ] Objective is clear and actionable
- [ ] Scope tells the executing agent where to look
- [ ] Change Required is unambiguous
- [ ] Verification criteria are specific
- [ ] Category is set correctly
- [ ] Dependencies reference other task IDs (if any)

## Example Invocation

```
Use the task-creator skill to generate tasks from:
- Project: facebook-api-v24-upgrade-20260130
- Source: .agent-tasks/tasks/facebook-api-v24-upgrade-20260130/research/facebook-api-upgrade-guide.md
```

## Output Format

```markdown
## Tasks Created

| Task ID | File | Description |
|---------|------|-------------|
| 001 | `pending/001-remove-deprecated-method.md` | Remove deprecated Instagram method |
| 002 | `pending/002-migrate-actor-id.md` | Migrate instagram_actor_id to instagram_user_id |
| ... | ... | ... |

## Suggested Execution Order

1. Tasks 001-003 can run in parallel (no dependencies)
2. Task 004 depends on 001-003 completing
3. ...

## Notes

- [Any items that couldn't become tasks]
- [Any ambiguities that need human clarification]
```
