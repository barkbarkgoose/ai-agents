---
name: coursework
description: >-
  Runs the user's university coursework workflow end-to-end from any directory: locates the
  per-machine study vault, the semester code workspace, and the `planner` assignment tracker
  (documented defaults first, then `planner resources`, then ask); triages gaps and late work;
  answers "what are we working on next"; pulls an assignment's brief and rubric by ref; builds it
  in the correct repo; captures a real evidence run; and submits. Use whenever the user mentions
  coursework, a course code (CS 3540, CS 2900, …), the planner, an assignment / Forge / devlog /
  homework / Canvas submission, gaps, late work, or studying for a course.
version: 1.0
updated: 2026-11-08
---

# Coursework

Jake's coursework is run through a **gap-aware assignment tracker** (`planner`) whose source of
truth is markdown in a personal Obsidian-style **vault**. Code and repos live in a separate
**workspace** directory; notes, study guides, and trackers live in the vault. This skill is the
portable entry point: it says **where to look** on any machine, then hands off to the authoritative
files that must be read for the current term.

> **Two hard rules that never change across machines or terms:**
> 1. **Code and repos live under the workspace (`~/dev/uvu/...`); notes and trackers live in the
>    vault.** Never put a markdown note in the workspace, never put build output in the vault.
> 2. **Status is never inferred.** `done` / `missing` / `skipped` / `na` come only from Jake's
>    words, never from a file existing, a commit landing, or Canvas. Pass `--confirm` only when he
>    actually said it.

---

## 0. Locate the environment (do this first, every session — never answer from memory)

Resolve each path in the order below and **stop at the first hit**. The vault and `write_as_me`
are registered per machine, so the registry is authoritative for those; the workspace and planner
have conventional defaults.

| Thing | Default (this machine) | Look-up order |
|---|---|---|
| `planner` CLI | `~/dev/uvu/course-planner/bin/planner` | `$PLANNER_BIN` → `command -v planner` → `~/dev/uvu/course-planner/bin/planner` |
| **Vault** (notes + trackers) | `~/Gdrive/notebook/uvu/2026_fall` | `$PLANNER_VAULT` → `planner resources` key `vault` → `~/.config/course-planner/config.json` → `~/Gdrive/notebook/uvu/<term>` |
| **Workspace** (code + repos) | `~/dev/uvu/2026-fall` | the workspace's own `AGENTS.md`/`CLAUDE.md` is authoritative; look for `~/dev/uvu/<term>` where `<term>` is e.g. `2026-fall` |
| `write_as_me` (voice repo) | `~/dev/programs/write-as-me` | `planner resources` key `write_as_me` → default |
| ai-agents (this repo) | `~/dev/common/ai-agents` | default |

The term appears in two spellings: **vault uses `2026_fall` (underscore)**, **workspace uses
`2026-fall` (hyphen)**. Don't assume they match.

Resolve and verify with one shell pass:

```bash
P="${PLANNER_BIN:-$(command -v planner || echo "$HOME/dev/uvu/course-planner/bin/planner")}"
"$P" doctor        # setup check: vault, Canvas auth (required for sync), gh (if a course has a repo)
"$P" resources     # prints the per-machine 'vault' and 'write_as_me' paths
```

**Then you MUST read the authoritative protocol files before doing course work** (they are the
source of truth and go stale faster than this skill):

1. `<workspace>/AGENTS.md` (or `CLAUDE.md`) — the full per-term briefing: pipeline, repos, rules.
2. `<vault>/README.md` — how the vault is structured, what an assignment note contains.
3. `<vault>/_handoff.md` — session handoff: what's in flight, decisions not to relitigate.
4. `<vault>/<COURSE>/course.md` — the confirmed policy for that course (late rules, exceptions).

### If a path can't be resolved → ask, then persist

If the vault or workspace isn't found, **stop and ask, don't guess**. Ask one grouped question:
_"Where is your study vault? Where is your semester workspace (the code dir)?"_ Once answered:

- Persist the vault: `"$P" resources --set vault <path>` (the CLI writes `~/.config/course-planner/config.json`).
- The workspace has no registry key yet — **suggest adding one** (`workspace`) to `RESOURCES` in
  `course-planner/planner/vault.py`, then `planner resources --set workspace <path>`, so the next
  agent finds it without asking.

---

## 1. Every session starts with these

```bash
P=~/dev/uvu/course-planner/bin/planner   # or the resolved path from §0
"$P" doctor               # vault, Canvas auth, gh
"$P" next                 # gaps first, then confirmed late work, then upcoming
"$P" grades <course>      # what the autograder said (issues via gh) — only for a course with a repo:
"$P" policy <course>      # late policy, exceptions, late-pass count
```

Only if Canvas data may be stale (new assignments expected): `"$P" sync && "$P" reconcile`
(needs Canvas auth from the planner's keychain; **never print or commit the ICS URL**). `reconcile`
never touches status, `## Brief`, or `## Log`.

---

## 2. The tracker rules (the whole point)

- State lives in `<vault>/<COURSE>/assignments/<slug>.md` frontmatter. **`## Brief` is Jake's and
  wins over everything**; agents never overwrite it. `## Generated` is agent-written and never
  overrides Brief. `## Log` is append-only.
- A **past-due item with no confirmed outcome is a gap**. Resolve gaps *before* planning new work.
- `missing` / `skipped` need **both** a policy ruling **and** an exceptions check, recorded:
  `"$P" set <ref> --status missing --late-credit yes|no --exceptions-checked [--exception late-pass|instructor-permission|none]`.
  `late_credit: yes` → it stays **late work** (actionable); `no` → it must become `skipped`.
- Changing a status without `--confirm` deliberately resets confirmation. **Never** pass `--confirm`
  unless Jake said it.
- `policy_confirmed` on a `course.md` is `false` until Jake confirms the drafted text — treat the
  drafted policy as a claim, not fact.
- Batch updates work: `"$P" set ref1 ref2 --status done --confirm`.

Commands: `sync, reconcile, next, gaps, show, set, add, policy, status, grades, doctor, resources`.

---

## 3. Doing an assignment (the pipeline)

1. `"$P" show "<title>"` → ref, Canvas link, due, status.
2. **Brief + rubric come from the course content source, not memory.** For CS 3540 that's the
   instructor's read-only content repo (`<workspace>/3540/course_builder/content/cs3540/2026/{assignments,rubrics,lectures,cheatsheets}/`);
   for CS 2900 it's the vault tracker's Canvas feed plus the `learn/` guides. If a subagent exists
   for the job (`assignment-worker`), hand it steps 2–4 for one named assignment.
3. **Build in the right repo** (§4), in the layout that repo documents (artifact + evidence + devlog).
4. **Evidence is half of every graded run and must be a real captured run — never written by hand.**
   Technique: a fresh headless session that does *not* name the tool, captured verbatim:
   ```bash
   claude -p "<prompt that does not name the tool>" \
     --allowedTools "<permissions only>" \
     --output-format stream-json --verbose < /dev/null > run.jsonl
   python3 <workspace>/tools/render_session.py run.jsonl "<prompt>"
   ```
   Show the real tool calls and verbatim output; state plainly what `--allowedTools` pre-approved.
   Block / refusal cases come first.
5. **Run the repo's gate** (`./check.sh` where present) — it must pass; a push-guard hook blocks
   pushes that fail it.
6. **Commit only the specific files.** **Push is Jake's go-ahead, per batch** ("push X"). Then mark
   it done, unconfirmed until he or the grader confirms: `"$P" set <ref> --status done`.

---

## 4. Repos and their rules

Discover repos from `<vault>/<COURSE>/course.md` (`repo:`) and the workspace tree — **don't
hard-code beyond the defaults below**, they drift.

| Path | Rules |
|---|---|
| `<workspace>/3540/assignments/barkerjake` | CS 3540 submission repo (`repo: uvucs3540/barkerjake`). **Push to `main` only** — a PreToolUse hook blocks branch/force pushes and pushes failing `check.sh`. Everything outside `games/` and `.claude/` must be **markdown** (no `.pptx`/`.py` there). Commit timestamp = submission time. |
| `<workspace>/3540/assignments/engine-spec` | shared class repo — work via **branch + PR**, touch only your section's paths. |
| `<workspace>/3540/course_builder` | instructor's content pipeline — **read-only** (source of briefs/rubrics/policy). |
| `<workspace>/2900/…` | CS 2900 has **no `repo:`** — it is graded on Canvas. Coding lives in plain repos under `<workspace>/2900/` (e.g. `homework/`, the `des-rsa-lab/` interactive teaching app, `Vault-Lock/` group project). Submit source files + a PDF per the Canvas brief. |
| `<workspace>/3540/study-agent` | **superseded** by the planner; only `course_context.py` is still live. Don't extend it. |

Notes vs code: a study guide is a **vault** note (`<vault>/<COURSE>/learn/…`); the program you
submit is **workspace** code. Keep them apart.

---

## 5. Working agreements

- **Writing as Jake** → use the `write_as_me` repo: read its `AGENTS.md` and
  `skills/draft-in-my-voice/SKILL.md` first.
- **Devlog reflections** may be drafted *as Jake* (he authorized it): voice from earlier real
  devlogs, facts from real artifacts. **Flag anything inferred, mark backfills, and let him read
  before pushing. Never invent events.**
- **Don't re-derive decided things.** Statuses are in the trackers; game direction and scope live in
  note files, not memory. Check before you plan.
- **Prefer deterministic enforcement over asking nicely** — a hook beats an AGENTS.md line; a
  read-only tool beats a promise.
- **Study/notes work** goes in the vault next to the related notes (a `learn/` folder if there's no
  better home). Never create notes in the workspace, and never answer a content question from a
  folder alone if it says its real content is elsewhere — say what's missing instead of filling it in.

---

## 6. Path drift & self-healing (do this instead of failing silently)

If a documented default is wrong — vault moved, workspace renamed, planner in a new spot, a course
directory spelled differently — treat that as **skill rot to report, not a reason to give up**:

1. Re-run the §0 look-up ladder; try `"$P" doctor` and `"$P" resources`.
2. Ask Jake only for the specific path you can't find.
3. Persist it (`"$P" resources --set <key> <path>`) so the next session is silent.
4. **Propose updating this skill**: fix the default in the §0 table (and bump `updated:` in the
   frontmatter), or add the missing key to the planner's `RESOURCES`. State what changed and why.
5. If the workspace's `AGENTS.md` disagrees with this skill, **the workspace file wins** — this skill
   is the locator and the invariants, not the per-term record.

---

## Boundaries

**Always:** locate the environment first; read `<workspace>/AGENTS.md`, `<vault>/README.md`,
`<vault>/_handoff.md`, and the course's `course.md`; resolve gaps before new work; capture evidence
as a real run; ask before changing a status; commit only the files in scope.

**Ask first:** marking anything `done`/`missing`/`skipped`/`na`; `--confirm`; `--late-credit`;
pushing (Jake says "push X" per batch); writing as Jake; editing `course.md` policy text.

**Never:** infer status; overwrite `## Brief`; put notes in the workspace or build output in the
vault; put personal data or secrets (Canvas ICS URL, `keychain.key`, `.env`) in any repo; push a
branch in `barkerjake` or force-push; touch another student's `engine-spec` section; hand-write an
"evidence" session; manipulate git history.
