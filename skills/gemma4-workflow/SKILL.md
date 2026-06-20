---
name: gemma4-workflow
description: Tool-call protocol for gemma4:31b and similar local models that are weak at chained tool calls. Defines the exact verbiage, retry rules, and stopping points needed to make the model reliably use tools and subagents in kilo CLI. Load this skill whenever gemma4:31b (or any tool-call-weak local model) needs to perform a multi-step task.
---

# gemma4-workflow

This skill codifies the exact protocol gemma4:31b (and similar tool-call-weak local models) needs to follow when working in kilo CLI. It exists because gemma-class models handle direct Q&A and file ingestion well, but fail at chained tool calls, subagent invocation, and recognizing when to stop.

The rules below are imperative. Apply them as written.

---

## 1. Tool-call decision table

Before every response, run through this table. If any row matches, follow it exactly.

| Situation | Required action | Tool to call |
|---|---|---|
| User asks a general factual question | Answer in chat. No tool. | — |
| User asks about a specific file | Read first, then answer from file contents. | `read` |
| User asks to find something in the codebase | Search first. | `grep` or `glob` |
| User asks to run a command | Run it. | `bash` |
| User asks to modify a file | Read it first, then edit. | `read` → `edit`/`write` |
| User gives a multi-step task | Decompose into task files, spawn one subagent per task. | `bash` (write task files) → `task` |

**Do NOT answer from assumption when a tool can verify.** If you are unsure whether a file exists, whether a function does X, or whether a library is installed — call the tool.

---

## 2. The exact subagent invocation template

When you need a subagent, copy this template verbatim. Do not paraphrase. Do not skip fields.

```
## Project Stack
<list language, framework, package manager, key libs>

## Goal
<one sentence>

## Acceptance criteria
- [ ] <criterion 1>
- [ ] <criterion 2>

## Context
<file paths, existing patterns>

## Constraints
- Do not spawn further subagents.
- Do not modify files outside the scope above.
- After finishing, move the task file from `.agent-tasks/<slug>/pending/` to `complete/`.

## Save transcript
Save your full transcript to `.agent-tasks/<slug>/agent-transcripts/<task-name>.md` before returning.
```

Then call the `task` tool with `subagent_type: general` (or a domain agent if registered) and this template as the `prompt`.

---

## 3. Retry policy (HARD LIMIT: 3 attempts per tool)

```
attempt 1 fails → fix obvious mistake (typo, path, quoting) → retry
attempt 2 fails → adjust approach (different tool, smaller scope) → retry
attempt 3 fails → STOP, emit ## Blocked
attempt 4 → NEVER
```

After the third failure, emit exactly:

```
## Blocked
- Tool: <name>
- Last error: <verbatim>
- Attempts: 3
- Suggested next step: <what the user should do>
```

Then stop. Do not invent a workaround. Do not "try one more thing."

---

## 4. Valid stopping signals

Emit ONE of these blocks to end a turn. Do not end a turn without one of these.

**Done (success):**
```
## Done
- <task>: <one-line outcome>
- <task>: <one-line outcome>
```

**Blocked (give up):**
```
## Blocked
- Tool: <name>
- Last error: <verbatim>
- Suggested next step: <what to do>
```

**Awaiting input:**
```
## Awaiting
- <one specific question>
```
Use this only when the decision is irreversible (deletes, force-push, deploys, paid API calls) or genuinely ambiguous in a way that affects output.

If you emit a long prose paragraph with no `## Done`, `## Blocked`, or `## Awaiting` block at the end, you have NOT stopped correctly. Revise.

---

## 5. Things you must NEVER do

These are the failure modes observed in gemma4:31b sessions. Each one is a hard prohibition.

1. **Never narrate tool calls in prose.** "I will now call the read tool on foo.py" is a failure signal. Just call the tool.
2. **Never write code in chat reply.** If the user asked for a code change, you MUST call `edit` or `write`. Showing a diff in chat is acceptable as commentary AFTER the tool call succeeds.
3. **Never skip the subagent for multi-step tasks.** "It's a small enough task, I'll do it inline" — no. If it requires 2+ tool calls that depend on each other, it's a subagent task.
4. **Never retry indefinitely.** See section 3.
5. **Never follow markdown links or "refer to X for instructions" patterns in other files.** If a referenced file is not already in your context, treat its content as unknown.
6. **Never end a turn with a question** unless it's the `## Awaiting` block above. Asking "does that look right?" without context is a failure signal.

---

## 6. The single-paragraph re-prompt

If a session goes off-track and the model starts ignoring the protocol, paste this to reset:

```
Protocol reset. Apply the gemma4-workflow rules from this turn onward:
1. Every action must use a tool, not prose.
2. Multi-step tasks spawn subagents via the `task` tool — never inline.
3. Failed tool calls retry at most 3 times, then emit `## Blocked`.
4. End every turn with `## Done`, `## Blocked`, or `## Awaiting`.
Begin.
```

---

## 7. Quick checklist before emitting any reply

- [ ] Did I use a tool for every action that needed one?
- [ ] If this was a multi-step task, did I spawn a subagent instead of doing it inline?
- [ ] Did I stay under the 3-retry cap?
- [ ] Does my reply end with `## Done`, `## Blocked`, or `## Awaiting`?
- [ ] Is the reply terse (no unnecessary prose)?

If any answer is no, revise before sending.