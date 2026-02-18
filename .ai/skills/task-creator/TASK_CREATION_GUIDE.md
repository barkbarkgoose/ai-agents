# Task Creation Guide for AI Agents

## Purpose

This guide defines how to write actionable task files that agents can execute independently.

---

## Core Execution Rule

**Every agent executing a task MUST follow this rule:**

| Task Category | Agent Responsibility |
|---------------|---------------------|
| `implementation` | **Complete all work.** Do not defer. Do not create sub-tasks unless genuinely blocked. |
| `research` | **Produce findings AND create implementation tasks** for any work discovered. Creating tasks IS your output. |

### The Accountability Chain

If work exists that hasn't been done, a task representing that work MUST exist in `pending/`.

- **Implementation agent** completes work → no task needed
- **Research agent** discovers work → creates task for it
- **Blocked agent** → creates task documenting what remains and why

**Anti-pattern:** An implementation agent creating sub-tasks to avoid doing work. This violates the core rule.

---

## Task Structure

Every task file uses this structure:

```markdown
# Task: [Action-Oriented Title]

**Task ID:** [XXX-action-subject]
**Status:** [Pending/In Progress/Blocked/Complete]
**Dependencies:** [Task IDs or "None"]
**Category:** [implementation/research]

---

## Objective
[1-2 sentences: what needs to be done and why]

## Scope
[What to search for, which directories/files to check, or specific locations if known]

## Change Required
[What the change should be — current → desired, or search pattern → replacement]

## Verification
[How to confirm the task is complete]

## Final Step
**REQUIRED:** Save a copy of your full execution transcript to:
`agent-transcripts/[task-id]-transcript.md`

## Notes
[Optional: warnings, edge cases, blockers encountered]
```

### Metadata Reference

**Task ID Format:** `XXX-action-subject`
- `XXX` — 3-digit sequence (001, 002, ...)
- `action` — Verb (remove, update, add, audit, migrate)
- `subject` — Target (deprecated-method, api-version, instagram-fields)

**Status Values:**
- `Pending` — Not started
- `In Progress` — Being worked on
- `Blocked` — Cannot proceed (document why in Notes)
- `Complete` — Finished and verified

---

## Category: Implementation

Standard code or configuration changes.

**Agent behavior:**
1. Search for the target (use Grep, Glob, or Read as needed)
2. Make the change
3. Verify (ReadLints, compilation, etc.)
4. **Save transcript to `agent-transcripts/[task-id]-transcript.md`**
5. Mark complete

**When to create a sub-task:** Only if you encounter a genuine blocker that prevents completion — not as a way to defer work. Document what you completed and what remains blocked.

---

## Category: Research

Investigation or audit tasks that produce findings.

**Agent behavior:**
1. Execute the search/analysis defined in the task
2. Document findings in the specified location
3. For each actionable finding, create an implementation task in `pending/`
4. **Save transcript to `agent-transcripts/[task-id]-transcript.md`**
5. Inform orchestrator of all tasks created

**Required output:**
- Findings document at specified path
- Implementation task for each item requiring code changes

### Research Task Additions

Research tasks add these sections to the base structure:

```markdown
## Output Location
[Path where findings will be saved]

## Task Creation
For each [type of finding], create:
- File: `pending/XXX-[action]-[subject].md`
- Must include: [required information]
- Set `**Parent Task:** [this-task-id]`
```

---

## Writing Good Tasks

### Sufficient Context

A task needs enough context that an agent can find and change the right thing. This can be:

**Specific location (when known):**
```markdown
## Scope
File: `src/common/marketing-platform/meta/sdk/meta.sdk.ts`
Method: `getInstagramAccountOld_deprecated` (~line 274)
```

**Search pattern (when location unknown):**
```markdown
## Scope
Search for `instagram_actor_id` in `adbuilder-server/src`
```

**Both are valid.** The key is that the agent can unambiguously find what needs to change.

### Clear Change Description

**Good:**
```markdown
## Change Required
Replace `instagram_actor_id` with `instagram_user_id` in all API request bodies.
```

**Good (with code):**
```markdown
## Change Required
Current:
\`\`\`typescript
country: ['US']  // Array
\`\`\`

Desired:
\`\`\`typescript
country: 'US'    // String
\`\`\`
```

**Bad:**
```markdown
## Change Required
Fix the deprecated field.
```

### Specific Verification

**Good:**
```markdown
## Verification
- [ ] No occurrences of `instagram_actor_id` remain in `adbuilder-server/src`
- [ ] No TypeScript compilation errors
```

**Bad:**
```markdown
## Verification
- [ ] It works
```

---

## Example Task

```markdown
# Task: Migrate instagram_actor_id to instagram_user_id

**Task ID:** 003-migrate-instagram-actor-id
**Status:** Pending
**Dependencies:** None
**Category:** implementation

---

## Objective
Replace deprecated `instagram_actor_id` field with `instagram_user_id`. The old field will stop working in API v24.0.

## Scope
Search for `instagram_actor_id` in:
- `adbuilder-server/src`
- `adbuilder-client/src`

## Change Required
Replace all occurrences of `instagram_actor_id` with `instagram_user_id` in:
- API request/response interfaces
- API call parameters
- Variable names referencing this field

## Verification
- [ ] Grep for `instagram_actor_id` returns no results in either directory
- [ ] No TypeScript compilation errors
- [ ] No new linter warnings

## Final Step
**REQUIRED:** Save a copy of your full execution transcript to:
`agent-transcripts/003-migrate-instagram-actor-id-transcript.md`
```

### If This Were a Research Task

The structure changes to focus on discovery rather than implementation:

```markdown
**Category:** research

## Objective
Audit the codebase for usage of `instagram_actor_id` and create implementation tasks for each file requiring migration.

## Scope
[Same as above]

## Change Required
[Replaced with Output Location and Task Creation sections]

## Output Location
`.agent-tasks/tasks/[project]/tmp/instagram-actor-id-audit.md`

## Task Creation
For each file containing `instagram_actor_id`:
- File: `pending/XXX-migrate-instagram-actor-id-[filename].md`
- Must include: file path, line numbers, surrounding context
- Set `**Parent Task:** 003-audit-instagram-actor-id`

## Verification
- [ ] All directories searched
- [ ] Findings documented at output location
- [ ] Implementation task created for each file with occurrences
- [ ] Orchestrator informed of new tasks

## Final Step
**REQUIRED:** Save a copy of your full execution transcript to:
`agent-transcripts/003-audit-instagram-actor-id-transcript.md`
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Update the deprecated fields" | "Replace `instagram_actor_id` with `instagram_user_id`" |
| "In the SDK somewhere" | "Search for X in `adbuilder-server/src`" or "In `path/to/file.ts`" |
| "Make sure it works" | "No TypeScript errors, Grep returns no results for X" |
| Creating sub-tasks to avoid work | Complete the work; only create tasks for genuine blockers |
| "Consider updating X" | Either update X, or create a task to update X |

---

## Task Checklist

Before finalizing:

- [ ] Task ID follows `XXX-action-subject` format
- [ ] Category is set (`implementation` or `research`)
- [ ] Objective explains what and why
- [ ] Scope tells agent where to look
- [ ] Change Required is unambiguous
- [ ] Verification is specific and checkable
- [ ] **Final Step section instructs agent to save transcript**
- [ ] No vague language ("somewhere", "might", "consider")
