# Mode: LEARN — Progressive Technical Scaffolding

For when the user wants to **learn it themselves**: "teach me", "I want to learn", "help me
understand", "I'm new to", "crash course", "quiz me". The page is a lesson, not a reference.
Default accent: `teal`. Kicker: "Quick-Learn guide".

## Why this mode exists (cognitive philosophy)

When jumping into something completely new, especially several concepts at once, two failure modes
frequently happen:

1. **The Spec Sheet Trap:** Dry reference documentation dumps raw jargon, API tables, and syntax
   before the brain has any context. Without an existing mental filing cabinet, words float
   unanchored and eyes glaze over.
2. **The Forced Story Trap:** Overly elaborate storytelling (villains, epiphanies, multi-character
   kitchen sagas) forces "dual-mapping": you track the metaphor *and* map it to the tech, adding
   cognitive tax instead of reducing it.

### The fix: progressive scaffolding
- **Immediate Anchor:** State what the thing is in 1–2 plain-English sentences right away.
- **The Conceptual Ladder:** 3–5 progressive statements that build the concept from first principles before mechanics.
- **Lean Physical Anchors & Visual Maps:** A 1-sentence physical anchor and a clear diagram to show boundaries and flow.
- **Trace the Byte:** Trace one concrete operation end-to-end to cement how pieces interact.
- **One Real Example:** Carry one concrete example's actual values through the trace, the
  step-through and the predictions, so every number on the page is something the system really produces.
- **Predict, Then See:** Ask the reader to guess what a real command or input produces before
  showing the real output. Committing to a guess is the closest reading gets to doing.
- **Check Yourself:** End with a few why-questions. Recalling something minutes after reading it is what makes a single read stick.

---

## Guide structure

Block names refer to `references/blocks.html`; diagram and interactive rules are in `references/components.md`.

### 1. The 10-Second Anchor — *Anchor card*
- **What it is:** 1–2 plain-English sentences, no buzzwords or forced metaphors.
- **Category & Core Job:** Category (e.g. *Local Daemon / Wire Protocol / State Machine / Library*) + the single core problem it solves.

### 2. The Conceptual Ladder — *Conceptual ladder*
Each statement builds on the previous one:
- **Baseline:** The familiar starting point everyone recognizes.
- **The Friction:** The exact bottleneck or point of failure as complexity grows.
- **The Core Shift:** The missing concept or architectural leap that resolves that friction.
- **How This Tool Does It:** How the subject implements that breakthrough.
- **The Mental Takeaway:** The final, stable mental model to hold onto.

### 3. Visual Architecture & Boundary Map — *Path diagram + stepper, Division of labor*
- **The Anchor Analogy (1 sentence max):** e.g. *"Think of it like an order rail pinned between a head chef and line cooks, not a shared brain"*.
- **Path Diagram:** The route one request (or byte, or event) takes, top to bottom, with everything
  else hanging off the step it touches. Scannable in 5 seconds.
- **Division of Labor:** Clarify boundaries early (*Control Plane vs. Data Plane*, *What it Does vs. What it Does NOT Do*).
- **Step Through It:** prev/next walk the one real example through the diagram a node at a time, showing the actual data at each point.

### 4. The Components — *Component cards*
Don't call it "the cast of characters"; name it for the subject. 3–5 key components, ordered from
foundation/storage to orchestrator/caller: **Role**, **Owns**, **Doesn't Touch**, **Contract / Interface**.

### 5. The Lifecycle Walkthrough ("Follow the Request") — *Stages diagram, Trace steps, Explorer*
Pick ONE realistic scenario:
1. **The Trigger:** Who initiates the action and what payload/command is sent.
2. **Step-by-Step Flow:** Chronological handoffs, state changes, disk/network operations.
3. **Stage Diagram:** The steps grouped into 2–4 stages, with the one thing to remember about each
   beside it (where a failure stops, what gets saved, what's irreversible).
4. **The Resolution:** What returns to the caller and what persistent state remains.
5. **Explorer (when the topic transforms data):** Pick a row or cell to light up exactly which parts
   of the input and output it affects. Start with the first one picked.

### 6. Predict, Then See — *Predict, then see*
2–3 small exercises, each:
- **The input:** a real command, request, snippet, config change or value, short enough to read at a glance.
- **The question:** "What comes back?", "What happens to X?". Ask before showing anything.
- **The reveal (hidden until opened):** the real output, then 1–2 sentences tying it back to the ladder or the trace.
- **Real output only:** run it to capture the output when you can. If you can't, take it from
  official docs and say so. Never present made-up output as real.
- When the reader can run things too, add one line telling them how to try it themselves.

Pick inputs where the answer teaches something: a surprising default, the step most people get
wrong, the "what if I change this one thing" case.

### 7. The Field Guide — *Symptom table, Sharp edge / Tip callouts, When to reach for it, Deep-dive coordinates*
- **You'll See → It Means → Fix:** led by the exact error message or symptom. 2–5 rows.
- **Silent Traps:** gotchas with no symptom to search for, as sharp-edge callouts.
- **When to Reach for This vs. When to Walk Away.**
- **Deep-Dive Coordinates:** exact files, lines, or doc sections to inspect next.

### 8. Check Yourself — *Check yourself*
3–5 questions to answer straight after reading:
- Ask **why** and **what if**, not trivia: aim at the ladder's core shift, the trace, and the sharp
  edges. Include at least one "what changes if…" question.
- Multiple choice, wrong answers drawn from real misconceptions. Vary where the right answer sits.
- After a pick, show why the right answer is right in 1–2 sentences.

---

## Tone

- Write like a pragmatic staff engineer whiteboarding with you. Concise, punchy, direct.
- Keep metaphors light and functional. No "The Villain", "The Climax", "Act I".
- Paragraphs 2–3 sentences max. Bold anchors for key terms.

## Layout

Nav: the 8 sections fit the header nav with short labels (Anchor · Ladder · Map · Parts · Trace ·
Predict · Field guide · Check). Card-wrapping each section (`rounded-xl border bg-white
dark:bg-slate-900 p-6`) suits this mode; numbered small-caps section labels are fine.

## Markdown output (on request only)

GitHub-flavored Markdown with Mermaid blocks, bullets and `> 💡 **Tip**` / `> ⚠️ **Sharp Edge**`
callout quotes. Predict-then-see reveals and self-check answers go in `<details>` blocks; skip the
step-through and explorers. Path diagram: `flowchart TD`, main path's edges declared first so it runs
down one side. Stage diagram: a Mermaid sequence diagram. Validate with `scripts/validate_mermaid.sh`.
