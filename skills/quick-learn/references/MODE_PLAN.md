# Mode: PLAN — Development & Project Plans

For a why-and-how plan built from a repo, PRD, or brief ("plan how we'd build X", "write up the
migration plan"). Default accent: `emerald`. Write `NAME.md` first, then render `NAME.html` from it
(see SKILL.md workflow).

The goal of a plan doc is not to list work. It is to make a reader understand
**why** the approach is right and **how** it will be executed, well enough that
they could defend it to someone else.

A plan that only answers *what* is a task list. Put task lists in the tracker.

---

## Ground the doc in the real thing first

Before writing a single section, read the actual artefact — the repo, the PRD,
the existing service. A plan written from the prompt alone produces adjectives
("modern", "scalable", "clean"). A plan written from the source produces
findings ("0 lines of codegen exist", "this component is defined in 3 files,
already drifting on one field").

Findings are what make a plan credible. Budget real effort here.

---

## Section vocabulary

Not every doc needs every section, and order can flex. But each section you do
include must map to a block in `references/blocks.html` — that mapping is the
forcing function that keeps the doc visual instead of a styled wall of text.

| # | Section | Answers | Block |
|---|---------|---------|-------|
| 1 | **Thesis** | The one sentence that governs every later decision | Hero + stat row |
| 2 | **Acceptance test** | How we'll know the whole thing worked | Flow steps |
| 3 | **Non-goals** | What we're deliberately not building, and why | Non-goals grid |
| 4 | **Architecture** | The shape, and the one rule that keeps it honest | Layer stack, file tree |
| 5 | **The pivotal decision** | The choice everything else follows from | Before/After |
| 6 | **Key mechanism** | The part a reader would otherwise get wrong | Code+commentary, pipeline chips |
| 7 | **Phases** | Sequence, and how each one ends | Phase timeline |
| 8 | **Risks** | What could go wrong and the mechanism that prevents it | Two-column table |
| 9 | **Keep / discard** | Honest inheritance from what exists | Keep/discard |
| 10 | **Definition of done** | Checkable exit conditions for v1 | Numbered criteria |

**Sections 1, 5, 7, and 8 are the load-bearing four.** If you only have room for
four, use those. A doc with a thesis, a pivotal before/after, gated phases, and
defused risks is a plan. Without them it's a brochure.

---

## The rules that separate a good plan doc from a styled one

**1. The thesis is one sentence and it must be arguable.**
"Build a great component builder" is not a thesis — nobody would argue the
opposite. "This is a code generator that happens to have a canvas, not a canvas
that happens to export code" is a thesis, because the inverse is a real position
someone actually took.

**2. Hero numbers are counts, not adjectives.**
Pull them from the source: line counts, file counts, duplicate definitions,
test coverage, open bugs. Three real numbers establish more credibility than a
page of prose.

**3. Every phase states its exit condition.**
"Phase 3: Editing" is a wish. "Exit · a marketing page with a responsive
3-column grid, built through the UI, exported, compiling, visually identical at
all three widths" is a gate. The bold `Exit ·` line is non-negotiable.

**4. Every risk names a mechanism, not a posture.**
"We'll be careful about scope" is not a defusal. "The non-goals list is the
contract; reversing one requires an explicit decision" is. If you can't name a
mechanism, the risk is unmitigated — say so.

**5. Non-goals need reasons.**
An unexplained exclusion gets re-litigated in week 3.

**6. Be honest in keep/discard.**
If prior work exists, something in it is good. An empty "keep" column reads as
not having looked. Name the best thing in the old code specifically.

**7. Show the bad output next to the good output.**
The Before/After block earns its place by making the argument concrete. Abstract
claims about maintainability convince nobody; two code samples side by side
convince immediately.

**8. Make decisions.**
When the requester has given decision authority, decide. A plan full of
"we could either X or Y" transfers the work back to the reader. State the call
and the reasoning; note the discarded option in one clause if it's genuinely close.

---

## Length

Aim for a doc that is **scrollable in about two minutes** and rewards a second,
slower pass. In practice: 8–11 sections, each one screen or less. If a section
needs more than that, it's probably two sections, or it belongs only in the
markdown.
