# Diagrams & Interactive Pieces

All of this ships in `assets/template.html` (CSS in the `<style>` block, behaviour in the closing
`<script>`). New pieces need markup only. Copyable blocks are in `references/blocks.html`.

Used by: **LEARN** and **EXPLAIN** (everything here); **PLAN** (path diagram, optionally);
**MARKDOWN** (only if the source already describes a flow; never invent one).

---

## Diagrams in HTML

HTML pages draw diagrams with the flow components, not Mermaid. They read top to bottom, use the
page's own fonts at full size, follow the theme, and need no script. Two patterns:

**Path** (`.flow`): the route one request takes through the system.
- The spine is the main path, top to bottom, 3–6 `.node`s in `.flow-row`s joined by `.flow-down`
  arrows. Label an arrow with the protocol, route or payload in four words or fewer, or leave it empty.
- Everything else hangs off the spine node it touches, in a `.flow-side` list. Use `.edge` (solid
  arrow out) for what the node sends or serves, and `.edge.in` (dashed arrow in) for something acting
  on it, like a supervisor, scheduler or cron job.
- Node variants: `.side` for side nodes, `.helper` (dashed border) for background actors, `.db` for
  storage. Put the location (path, port, host) in a `<small>` inside the node.
- Always follow it with the Division of Labor table: the diagram shows *where* things are, the table
  *who owns what*.

**Stages** (`.flow stages`): one lifecycle, in 2–4 stages.
- Each stage is a `.node.stage` with a numbered `.stage-head` and 2–5 short steps (or one `.cmd`
  line). The arrows between stages say what has to be true to move on ("tests passed", "lock acquired").
- Beside each stage, a `.flow-note` holds the one thing to remember about it. Use `.flow-note.warn`
  for failure behaviour ("Fails here? Nothing live changed"). These notes are the reason for the
  diagram, so don't leave them generic.
- End with a `.node.result` showing what the caller gets back.
- It works on its own. Add the numbered trace steps underneath only when the steps need more detail
  than fits in the boxes.

**Round trips** (EXPLAIN's "explain the round-trip logic"): draw the outbound leg as the path
diagram's spine and the return as the stages diagram, or as one stages diagram whose last stages
are the response leg. Mark where state is written and what the caller can observe at each point.

If the system isn't a single path (cycles, many-to-many), draw the path the reader will meet first
and hang the rest off it. For a state machine, use stages with a note like "back to 2 when the token
expires". Two small diagrams beat one crowded one. Every diagram needs an `aria-label` that says in
words what it shows.

Restyle through the `--flow-*` variables (they already follow the `brand` accent), not by rewriting
the rules, so the layout and phone behaviour stay intact.

---

## Interactive pieces

**Linked highlights and steppers** (`data-explore`). Inside a `data-explore` box:
- `data-id="x"` marks something that can light up: a diagram node, a table cell, one bit or
  character in a value.
- `data-show="x y"` makes an element pickable. Picking it lights up those ids and puts its
  `data-note` (HTML allowed) into the box's `data-note-out` element. The first pickable element starts picked.
- Optional `data-step="prev"`, `data-step="next"` and `data-step-label` buttons walk the pickable
  elements in page order. That's the step-through on the path diagram.

**Explorer** (same attributes): for permutations, lookup tables, encodings, routing tables, config
that maps to behaviour. Show the table and let the reader pick a row or cell to light up exactly
which parts of the input and output it affects, with a one-line note. Example, a permutation table
where picking an output position lights up the input bit it came from and the output bit it fills:

```html
<div data-explore class="rounded-lg border border-slate-200 dark:border-slate-800 p-4">
  <p class="text-sm font-semibold">The IP table: top = output position, bottom = the input bit that fills it</p>
  <div class="mt-2 grid grid-cols-8 gap-1">
    <button type="button" data-show="in-58 out-1" data-note="Output bit 1 is input bit 58, which is <b>1</b> in this run."
      class="flex flex-col items-center rounded border border-slate-200 dark:border-slate-700 py-0.5">
      <span class="text-[0.6rem] text-slate-400">1</span><span class="text-xs font-semibold">58</span>
    </button>
    <!-- …one button per table cell -->
  </div>
  <p data-note-out class="explore-note mt-3 rounded-lg bg-brand-50 dark:bg-brand-950/40 px-3 py-2 text-sm"></p>
  <p class="mt-2 font-mono text-sm">input:  <span data-id="in-1">0</span><span data-id="in-2">0</span>…</p>
  <p class="font-mono text-sm">output: <span data-id="out-1">1</span><span data-id="out-2">1</span>…</p>
</div>
```

- **Use real values.** Compute them by running the real code (or a few lines of in-page JS), never by hand.
- **Generate long markup with a short script.** Don't hand-write 64 `<span data-id>` bits: build
  them from the value string with a few lines of JS, placed in the template's slot *before* the
  behaviours script. Static markup is fine for short values.
- **Mark changes in a before/after** with `<span class="chg">` (no script needed), e.g. the bits a round changed.
- When the topic is something the page can compute (an encoding, a hash, a cipher, a regex),
  consider a "try your own value" input that reruns it. Optional; only when the computation is small and certain.

**Predict, then see** (LEARN only) uses `<details class="reveal">`: no script, works in Markdown too.

**Self-check cards** (LEARN only, `data-quiz`): buttons with `data-correct="true"` or `"false"`, and
an explanation `<p data-explain hidden>`. The first pick locks the card, marks the right answer (and
a wrong pick), and shows the explanation.

**Checklists** (`data-checklist="name"`): real checkboxes whose state persists per page and list.
