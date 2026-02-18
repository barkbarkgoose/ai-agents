# Skill: Task Archiver

Archive completed task projects by compressing artifacts while preserving a human-readable summary.

## When to Use

Use this skill when:
- A task project is complete (or abandoned) and no longer actively worked on
- You want to preserve the full history but reduce clutter
- The project has already been moved to `.agent-tasks/archive/`
- The project is finished but needs to be moved to `.agent-tasks/archive` (will be requested by user)

## Input Requirements

You must be provided:
1. **Project path** — Full path to the project folder (e.g., `.agent-tasks/tasks/20260130-facebook-api-v24-upgrade`)

## Behavior

### 1. Validate Project Structure

Verify the project has:
- An `CONTROLLER.md` file (required - serves as the summary)
- At least one of: `complete/`

If `CONTROLLER.md` is missing, stop and ask the user to create one or provide an alternative summary.

### 2. Generate Archive Metadata

Create `ARCHIVE_INFO.md` with:
- Archive date
- Original project name
- File/folder inventory (what's being compressed)
- A quick one sentence summary for each of all completed tasks
- Instructions for restoring

### 3. Create Compressed Archive

Using `tar`, compress all subdirectories:
```bash
tar -czvf artifacts.tar.gz complete/ pending/ research/ testing/ agent-transcripts/ --ignore-failed-read
```

Note: `--ignore-failed-read` handles missing folders gracefully.

### 4. Clean Up Original Folders

After successful compression, remove the original folders:
- `complete/`
- `pending/`
- `research/`
- `testing/`
- `agent-transcripts/`

NOTE: you MUST delete these empty directories

Keep these files uncompressed:
- `CONTROLLER.md` — Primary summary document
- `ARCHIVE_INFO.md` — Archive metadata
- `IMPLEMENTATION_COMPLETE.md` — If present, useful summary
- `artifacts.tar.gz` — The compressed archive

### 5. move project to archive directory if not done already

```bash
mv .agent-tasks/tasks/[project-name] .agent-tasks/archive/
```

### 6. Report Results

Provide:
- Confirmation of successful archive
- List of preserved summary files
- Size comparison (before/after)
- Instructions for restoration

## Archive Structure (Final)

```
archive/[project-name]/
├── CONTROLLER.md          # Human-readable project summary
├── ARCHIVE_INFO.md          # Archive metadata and restore instructions
├── IMPLEMENTATION_COMPLETE.md  # (if present)
└── artifacts.tar.gz         # Compressed: all task folders and transcripts
```

## Restoration Instructions

To restore an archived project:

```bash
tar -xzvf .agent-tasks/archive/[project-name]/artifacts.tar.gz
mv .agent-tasks/archive/[project-name] .agent-tasks/tasks/
```

## Example Invocation

```
Use the task-archiver skill to archive:
- Project: .agent-tasks/tasks/20260130-facebook-api-v24-upgrade
```

## ARCHIVE_INFO.md Template

```markdown
# Archive Information

**Project:** [Project Name]
**Archived:** [Date]
**Archived By:** AI Agent

## Contents

The following folders have been compressed into `artifacts.tar.gz`:

| Folder | File Count | Description |
|--------|------------|-------------|
| complete/ | X files | Completed task definitions |
| pending/ | X files | Remaining/skipped tasks |
| research/ | X files | Research documents and audits |
| testing/ | X files | Testing strategies |
| agent-transcripts/ | X files | Agent execution logs |

## Restoration

To extract the archived contents:

\`\`\`bash
tar -xzvf artifacts.tar.gz
\`\`\`

## Summary

See `CONTROLLER.md` for the complete project summary, task list, and progress notes.
```

## Quality Checklist

Before archiving, verify:
- [ ] `CONTROLLER.md` exists and is complete
- [ ] All important progress notes are captured
- [ ] No active work remains (or is documented in pending/)
- [ ] Compression completed successfully
- [ ] Original folders removed only after successful compression

## Notes

- The skill preserves `CONTROLLER.md` uncompressed because it serves as the project's historical record
- Agent transcripts can be large; compression significantly reduces storage
- The archive can always be fully restored with a single `tar` command
