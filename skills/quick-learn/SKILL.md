---
name: quick-learn
description: Transforms dense technical readings, documentation, architectures, or unfamiliar concepts into high-retention, progressively scaffolded visual learning guides. Starts with a crisp 1-2 sentence definition and a conceptual ladder of progressive statements before moving to visual architecture diagrams (Mermaid in Markdown, built-in HTML/CSS flow diagrams in HTML), concrete lifecycle traces, predict-then-see exercises, symptom-first sharp edges, and a short self-check. Designed for visual, hands-on, ADHD-friendly learning without forced narrative fluff, including crash courses where reading is the only option. Outputs a single self-contained HTML file by default (Tailwind CDN, with step-through diagrams and click-to-highlight explorers), or Markdown on request. Use when learning new concepts, previewing documentation, preparing to dive into unfamiliar codebases, or unpacking complex topics.
---

# Quick-Learn: Progressive Technical Scaffolding

Quick-Learn turns abstract, dense, or unfamiliar technical topics into intuitive, memorable mental models.

## Why This Skill Exists (Cognitive Philosophy)

When jumping into something completely new—especially when learning multiple concepts at once—two failure modes frequently happen:

1. **The Spec Sheet Trap:** Dry reference documentation dumps raw jargon, API tables, and syntax before the brain has any context. Without an existing mental filing cabinet, words float unanchored and eyes glaze over.
2. **The Forced Story Trap:** Overly elaborate storytelling (novel-like narratives, villains, epiphanies, multi-character kitchen sagas) forces "dual-mapping." You have to track the metaphor *and* map it to the tech, adding cognitive tax instead of reducing it.

### The Cognitive Fix: Progressive Scaffolding
- **Immediate Anchor:** State what the thing is in 1–2 plain-English sentences right away.
- **The Conceptual Ladder:** Give the brain 3–5 progressive bullet points that build the concept from first principles before getting into mechanics.
- **Lean Physical Anchors & Visual Maps:** Use a 1-sentence physical anchor and a clear diagram to show boundaries and flow.
- **Trace the Byte:** Trace one concrete operation end-to-end to cement how pieces interact.
- **One Real Example:** Carry one concrete example's actual values through the trace, the step-through and the predictions, so every number on the page is something the system really produces.
- **Predict, Then See:** Ask the reader to guess what a real command or input produces before showing the real output. Committing to a guess is the closest reading gets to doing.
- **Check Yourself:** End with a few why-questions. Recalling something minutes after reading it is what makes a single read stick.

---

## Guide Structure Template

When explaining an unfamiliar system, architecture, codebase, or concept, produce the guide following this structure:

### 1. The 10-Second Anchor (Plain-English Definition)
- **What it is:** 1–2 plain-English sentences defining the system without buzzwords or forced metaphors.
- **Category & Core Job:** Category (e.g. *Local Daemon / Wire Protocol / State Machine / Library*) + the single core problem it solves.

### 2. The Conceptual Ladder (Progressive Understanding)
A sequence of 3–5 bullet points where each statement builds on the previous one:
- **Baseline:** The familiar starting point or foundational reality everyone recognizes.
- **The Friction:** The exact bottleneck or point of failure that occurs as complexity grows.
- **The Core Shift:** The missing concept or architectural leap that resolves that friction.
- **How This Tool Does It:** How the specific subject implements that breakthrough.
- **The Mental Takeaway:** The final, stable mental model to hold onto.

### 3. Visual Architecture & Boundary Map
- **The Anchor Analogy (1 sentence max):** A quick physical anchor grounding the system (e.g., *"Think of it like an order rail pinned between a head chef and line cooks, not a shared brain"*).
- **Path Diagram:** The route one request (or byte, or event) takes, top to bottom, with everything else hanging off the step it touches: boundaries, data flow, ports, protocols. Keep it scannable in 5 seconds. HTML uses the path flow component (see [Diagrams in HTML](#diagrams-in-html)); Markdown uses a Mermaid `flowchart TD`.
- **The Division of Labor (Contrast Table):** Clarify boundaries early to prevent confusion.
  - E.g., *Control Plane vs. Data Plane*, or *What it Does vs. What it Does NOT Do*.
- **Step Through It (HTML):** Make the path diagram steppable: prev/next buttons walk the one real example through it a node at a time, lighting up where it is and showing the actual data at that point. See [Interactive pieces in HTML](#interactive-pieces-in-html).

### 4. The Cast of Characters
NOTE: don't just call it "the cast of characters"

List the 3–5 key components or concepts, ordered from foundation/storage to orchestrator/caller:
- **Role:** Plain-English description.
- **Owns:** 1–2 bullet points on what it is responsible for.
- **Doesn't Touch:** What it explicitly leaves to other components.
- **Contract / Interface:** The primary API, schema, event, or CLI command it uses.

### 5. The Lifecycle Walkthrough ("Follow the Request")
Pick ONE realistic, concrete scenario and trace it step-by-step:
1. **The Trigger:** Who initiates the action and what payload/command is sent.
2. **Step-by-Step Flow:** Numbered chronological steps showing handoffs, state changes, and disk/network operations.
3. **Stage Diagram:** The steps grouped into 2–4 stages, with the one thing to remember about each stage beside it (where a failure stops, what gets saved, what's irreversible). HTML uses the stages flow component; Markdown uses a Mermaid sequence diagram.
4. **The Resolution:** What returns to the caller and what persistent state remains.
5. **Explorer (HTML, when the topic transforms data):** For permutations, lookup tables, encodings, routing tables, config that maps to behaviour: show the table, and let the reader pick a row or cell to light up exactly which parts of the input and output it affects, with a one-line note saying what happened. Start with the first one picked so the mapping is visible before any click.

### 6. Predict, Then See
2–3 small exercises. Each one:
- **The input:** a real command, request, snippet, config change or value, short enough to read at a glance.
- **The question:** "What comes back?", "What happens to X?", "Which of these changes?". Ask before showing anything.
- **The reveal (hidden until opened):** the real output, then 1–2 sentences tying it back to the ladder or the trace.
- **Real output only:** run it to capture the output when you can. If you can't run it here, take it from official docs and say so. Never present made-up output as real.
- When the reader can run things too, add one line telling them how to try it themselves.

Pick inputs where the answer teaches something: a surprising default, the step most people get wrong, the "what if I change this one thing" case.

### 7. The Field Guide (Gotchas & Sharp Edges)
- **You'll See → It Means → Fix:** A table led by the exact error message or visible symptom (the way the reader will actually run into the problem), then the cause, then the fix. 2–5 rows.
- **Silent Traps:** Gotchas with no symptom to search for (a wrong default that "works", a security hole), as sharp-edge callouts.
- **When to Reach for This vs. When to Walk Away:** Clear, bulleted decision criteria.
- **Deep-Dive Coordinates:** Exact files, lines, or official doc sections to inspect next.

### 8. Check Yourself
3–5 questions to answer straight after reading:
- Ask **why** and **what if**, not trivia: aim them at the ladder's core shift, the trace, and the sharp edges. Include at least one "what changes if…" question.
- Multiple choice, with wrong answers drawn from real misconceptions, so a wrong pick teaches something. Vary where the right answer sits.
- After a pick, show why the right answer is right in 1–2 sentences.

---

## Tone & Delivery Guidelines

- **Concise, punchy, and direct:** Write like a pragmatic staff engineer whiteboarding with you.
- **No forced melodrama:** Keep metaphors light and functional. Avoid forced story labels ("The Villain", "The Climax", "Act I").
- **Chunked & Scannable:** Keep paragraphs short (2–3 sentences max). Use bold anchors for key terms.
- **Callout badges:**
  - `> 💡 **Tip**`: Mental shortcuts, practical habits, or memory hooks.
  - `> ⚠️ **Sharp Edge**`: Gotchas, failure modes, or breaking assumptions.

---

## Output Formats & Delivery

### 1. Self-Contained HTML Document (Default)
Unless the user asks for Markdown, generate a single `.html` file that opens straight from disk, with no local server or build step.

#### HTML Skeleton & Design System

Use this exact boilerplate structure for HTML output, ensuring all cards, text, tables, and callouts support both light and dark mode:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Quick-Learn: [Topic Title]</title>
  
  <!-- Tailwind CSS CDN with class-based Dark Mode -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f0fdfa',
              100: '#ccfbf1',
              500: '#14b8a6',
              600: '#0d9488',
              700: '#0f766e',
              900: '#134e4a',
            }
          }
        }
      }
    }

    // Apply stored theme or fallback to system preference early to avoid flash
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.theme = isDark ? 'dark' : 'light';
    }
  </script>

  <!-- Flow diagrams (see "Diagrams in HTML"): the main path runs down the left, side
       connections hang off to the right. Plain CSS, so they follow the theme with no re-render. -->
  <style>
    :root {
      --flow-ink: #0f172a; --flow-muted: #475569; --flow-line: #64748b; --flow-accent: #0d9488;
      --flow-node: #ffffff; --flow-side: #cbd5e1; --flow-ok: #047857;
      --flow-note: #f0fdfa; --flow-note-line: #14b8a6; --flow-warn: #fffbeb; --flow-warn-line: #f59e0b;
      --flow-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
    .dark {
      --flow-ink: #e2e8f0; --flow-muted: #94a3b8; --flow-line: #94a3b8; --flow-accent: #2dd4bf;
      --flow-node: #0f172a; --flow-side: #334155; --flow-ok: #6ee7b7;
      --flow-note: rgb(4 47 46 / 0.6); --flow-warn: rgb(69 26 3 / 0.5);
    }
    .flow { --spine: 220px; display: flex; flex-direction: column; min-width: 0; font-size: 15px; color: var(--flow-ink); }
    .flow.stages { --spine: 300px; }
    .flow-row { display: grid; grid-template-columns: var(--spine) minmax(0, 1fr); align-items: center; }
    .flow .node { border: 1.5px solid var(--flow-accent); background: var(--flow-node); border-radius: 8px;
      padding: 9px 12px; font-weight: 600; text-align: center; line-height: 1.35; }
    .flow .node small { display: block; font-family: var(--flow-mono); font-size: 12px; font-weight: 400;
      color: var(--flow-muted); overflow-wrap: break-word; }
    .flow .node.db { border-radius: 50% / 16px; padding-block: 14px; }
    .flow .node.side { border-color: var(--flow-side); text-align: left; }
    .flow .node.helper { border-style: dashed; }
    .flow .node.result { font-family: var(--flow-mono); font-weight: 500; font-size: 13.5px; border-color: var(--flow-ok); color: var(--flow-ok); }
    .flow .node.stage { text-align: left; }
    .flow .stage-head { display: flex; align-items: baseline; flex-wrap: wrap; gap: 4px 8px; }
    .flow .stage-head .num { display: inline-grid; place-items: center; flex: 0 0 auto; width: 22px; height: 22px;
      border-radius: 50%; background: var(--flow-accent); color: var(--flow-node); font-size: 12px; }
    .flow .stage-head small { display: inline; }
    .flow .node.stage ul { margin: 6px 0 0; padding-left: 30px; list-style: disc; font-weight: 400; font-size: 14px; }
    .flow .node.stage .cmd { display: block; margin: 6px 0 0 30px; font-family: var(--flow-mono); font-weight: 400; font-size: 13px; }
    .flow-down { position: relative; width: var(--spine); min-height: 34px; display: flex; align-items: center;
      padding: 6px 0 6px calc(var(--spine) / 2 + 12px); color: var(--flow-muted); font-family: var(--flow-mono); font-size: 12.5px; }
    .flow-down::before { content: ""; position: absolute; left: calc(var(--spine) / 2 - 1px); top: 0; bottom: 6px; border-left: 2px solid var(--flow-line); }
    .flow-down::after { content: ""; position: absolute; left: calc(var(--spine) / 2 - 6px); bottom: 0;
      border: 6px solid transparent; border-top: 7px solid var(--flow-line); border-bottom: 0; }
    .flow-down span { white-space: nowrap; }
    .flow-side { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; min-width: 0; }
    .flow-side li { display: flex; align-items: center; min-width: 0; }
    .flow-side .node.side { flex: 0 1 auto; min-width: 0; }
    .edge { position: relative; flex: 0 0 auto; min-width: 140px; padding: 0 14px 14px; color: var(--flow-muted);
      font-family: var(--flow-mono); font-size: 12px; white-space: nowrap; text-align: center; }
    .edge::before { content: ""; position: absolute; left: 0; right: 7px; bottom: 5px; border-top: 2px solid var(--flow-line); }
    .edge::after { content: ""; position: absolute; right: 0; bottom: 0; border: 6px solid transparent; border-left: 7px solid var(--flow-line); border-right: 0; }
    .edge.in::before { left: 7px; right: 0; border-top-style: dashed; }
    .edge.in::after { left: 0; right: auto; border-left: 0; border-right: 7px solid var(--flow-line); }
    .flow-note { margin-left: 18px; padding: 8px 12px; border-left: 3px solid var(--flow-note-line); background: var(--flow-note);
      border-radius: 0 8px 8px 0; font-size: 13.5px; max-width: 34ch; }
    .flow-note.warn { border-left-color: var(--flow-warn-line); background: var(--flow-warn); }
    @media (max-width: 620px) {
      .flow { --spine: 180px; }
      .flow.stages { --spine: 100%; }
      .flow-row { grid-template-columns: minmax(0, 1fr); row-gap: 8px; }
      .flow-row > .node { width: var(--spine); }
      .flow-side { padding-left: 16px; }
      .flow-side .node.side { flex: 1 1 0; }
      .edge { flex: 0 0 66px; min-width: 0; padding-inline: 6px; font-size: 11.5px; white-space: normal; }
      .flow-down span { white-space: normal; }
      .flow-note { margin-left: 16px; max-width: none; }
    }

    /* Interactive pieces (see "Interactive pieces in HTML"): linked highlights and steppers
       ([data-explore]), self-check cards ([data-quiz]), predict-then-see reveals. */
    :root { --hl-bg: #fcd34d; --hl-ink: #78350f; --hl-line: #f59e0b; --chg: #b45309; }
    .dark { --hl-bg: #fbbf24; --hl-ink: #451a03; --hl-line: #fbbf24; --chg: #fbbf24; }
    [data-id].is-lit { background: var(--hl-bg); color: var(--hl-ink); border-radius: 3px; }
    [data-id].is-lit * { color: inherit; }
    .flow .node[data-id].is-lit { background: var(--flow-node); color: var(--flow-ink); outline: 3px solid var(--hl-line); outline-offset: 2px; }
    .flow .node[data-id].is-lit small { color: var(--flow-muted); }
    [data-show] { cursor: pointer; }
    [data-show]:focus-visible, [data-step]:focus-visible, [data-quiz] button:focus-visible, details.reveal > summary:focus-visible {
      outline: 2px solid var(--flow-accent); outline-offset: 2px; }
    [data-show].is-picked { border-color: var(--flow-accent); box-shadow: inset 0 0 0 1px var(--flow-accent); }
    [data-step]:disabled { opacity: 0.4; cursor: default; }
    .explore-note:empty { display: none; }
    .chg { font-weight: 700; color: var(--chg); }  /* what changed, in a before/after pair */
    details.reveal > summary { cursor: pointer; width: fit-content; }
    [data-quiz] button.is-right { border-color: #86efac; background: #f0fdf4; color: #166534; }
    [data-quiz] button.is-wrong { border-color: #fca5a5; background: #fef2f2; color: #991b1b; }
    .dark [data-quiz] button.is-right { border-color: #15803d; background: rgb(20 83 45 / 0.4); color: #bbf7d0; }
    .dark [data-quiz] button.is-wrong { border-color: #b91c1c; background: rgb(127 29 29 / 0.4); color: #fecaca; }
    [data-quiz] button.is-out { opacity: 0.55; }
    [data-quiz][data-answered] button { cursor: default; }
  </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-200 antialiased font-sans transition-colors duration-200">

  <!-- Main Container -->
  <div class="max-w-4xl mx-auto px-6 py-12">

    <!-- Header with Theme Toggle -->
    <header class="border-b border-slate-200 dark:border-slate-800 pb-8 mb-10 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-teal-100 dark:bg-teal-950 text-teal-800 dark:text-teal-300 mb-3 border border-teal-200 dark:border-teal-800">
          Quick-Learn Architecture Guide
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-3">
          [Topic Title]
        </h1>
        <p class="text-base sm:text-lg text-slate-600 dark:text-slate-400 leading-relaxed max-w-2xl">
          [1-line context describing what system/repo/protocol this covers].
        </p>
      </div>

      <!-- Light / Dark Toggle Button -->
      <button onclick="toggleTheme()" type="button" aria-label="Toggle Theme" class="flex-none inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-medium transition-colors shadow-sm cursor-pointer self-start">
        <!-- Sun icon (shown in dark mode) -->
        <svg class="hidden dark:block w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 9h-1m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <!-- Moon icon (shown in light mode) -->
        <svg class="block dark:hidden w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
        <span class="dark:text-slate-200">Theme</span>
      </button>
    </header>

    <!-- SECTION 1: The 10-Second Anchor -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-2">1. The 10-Second Anchor</h2>
        <div class="text-xl font-medium text-slate-900 dark:text-white leading-snug mb-3">
          [1–2 plain-English sentences defining what the thing is without buzzwords or analogies.]
        </div>
        <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
          <strong>Category &amp; Core Job:</strong> [e.g. Wire protocol / Local daemon] that [single problem solved].
        </p>
      </div>
    </section>

    <!-- SECTION 2: The Conceptual Ladder -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-4">2. The Conceptual Ladder</h2>
        <div class="space-y-4">
          <!-- Repeat ladder steps 1 through 5 -->
          <div class="flex items-start gap-3">
            <span class="flex-none w-7 h-7 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-bold flex items-center justify-center border border-slate-300 dark:border-slate-700">1</span>
            <div>
              <p class="text-sm font-semibold text-slate-900 dark:text-white">[Baseline: Known Reality]</p>
              <p class="text-xs text-slate-600 dark:text-slate-400">[Description]</p>
            </div>
          </div>
          <!-- More steps... -->
        </div>
      </div>
    </section>

    <!-- SECTION 3: Visual Architecture & Boundary Map -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-1">3. Visual Architecture &amp; Boundary Map</h2>
        <p class="text-xs italic text-slate-500 dark:text-slate-400 mb-6">
          <strong>Anchor Analogy:</strong> [1-sentence physical anchor].
        </p>

        <!-- Path diagram, steppable: the main path down the left, side connections to the right.
             Each spine node is a step (data-show + data-note); prev/next walk the one real example
             through it. Without the stepper, drop the data-* attributes, the controls and the note,
             and use role="img" instead of role="group". -->
        <div data-explore class="mb-6">
          <div class="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg p-4 overflow-x-auto">
            <div class="flow" role="group" aria-label="[One or two sentences saying what the diagram shows]">
              <div class="flow-row"><div class="node" data-id="caller" data-show="caller" data-note="[What the caller sends: the real request or value]">[Caller]</div></div>
              <div class="flow-down"><span>[how it gets there: protocol, port]</span></div>
              <div class="flow-row">
                <div class="node" data-id="component" data-show="component" data-note="[What this step does to it, and the real value after]">[Component] <small>[where it runs]</small></div>
                <ul class="flow-side">
                  <li><span class="edge">[what it sends]</span><span class="node side">[Target] <small>[detail]</small></span></li>
                  <li><span class="edge in">[what it does to this]</span><span class="node side helper">[Background actor]</span></li>
                </ul>
              </div>
              <div class="flow-down"></div>
              <div class="flow-row"><div class="node db" data-id="store" data-show="store" data-note="[What gets stored, and what goes back]">[Store] <small>[detail]</small></div></div>
            </div>
          </div>
          <div class="mt-3 flex flex-wrap items-center gap-2">
            <button type="button" data-step="prev" class="rounded-md border border-slate-300 dark:border-slate-700 px-2.5 py-1 text-xs">&larr; prev</button>
            <span data-step-label class="text-xs font-medium text-slate-600 dark:text-slate-400"></span>
            <button type="button" data-step="next" class="rounded-md border border-slate-300 dark:border-slate-700 px-2.5 py-1 text-xs">next &rarr;</button>
          </div>
          <p data-note-out class="explore-note mt-2 rounded-lg bg-teal-50 dark:bg-teal-950/40 px-3 py-2 text-sm text-slate-800 dark:text-slate-200"></p>
        </div>

        <!-- Division of Labor Table -->
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wide mb-3">Division of Labor</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-slate-700 dark:text-slate-300">
                <th class="py-2.5 px-3 font-semibold">Component / Layer</th>
                <th class="py-2.5 px-3 font-semibold">What It Owns</th>
                <th class="py-2.5 px-3 font-semibold">What It Does NOT Touch</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-600 dark:text-slate-400">
              <tr>
                <td class="py-2.5 px-3 font-mono font-medium text-slate-900 dark:text-slate-200">[Component]</td>
                <td class="py-2.5 px-3">[Owns]</td>
                <td class="py-2.5 px-3">[Does not touch]</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- SECTION 4: The Cast of Characters -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-4">4. [A name that fits the subject, e.g. The Pieces You Touch]</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Card per character -->
          <div class="border border-slate-200 dark:border-slate-800 rounded-lg p-4 bg-slate-50/50 dark:bg-slate-800/40">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">1. [Layer]</span>
              <span class="text-xs font-mono bg-slate-200 dark:bg-slate-700 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">[File/Location]</span>
            </div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm mb-1">[Name]</h3>
            <p class="text-xs text-slate-600 dark:text-slate-400 mb-2">[Job description]</p>
            <ul class="text-xs text-slate-500 dark:text-slate-400 space-y-1 list-disc list-inside">
              <li><strong>Owns:</strong> [Responsibility]</li>
              <li><strong>Interface:</strong> [Contract]</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: The Lifecycle Walkthrough -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-1">5. The Lifecycle Walkthrough</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">[Description of single realistic scenario]</p>

        <!-- Stage diagram: 2–4 stages, the key fact about each beside it -->
        <div class="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg p-4 mb-6 overflow-x-auto">
          <div class="flow stages" role="img" aria-label="[One or two sentences saying what happens in each stage]">
            <div class="flow-row">
              <div class="node stage"><span class="stage-head"><span class="num">1</span>[Trigger]</span>
                <code class="cmd">[command or call]</code></div>
              <div class="flow-note">[What the reader should know about this stage]</div>
            </div>
            <div class="flow-down"><span>[how it hands off]</span></div>
            <div class="flow-row">
              <div class="node stage"><span class="stage-head"><span class="num">2</span>[Stage] <small>[where]</small></span>
                <ul><li>[step]</li><li>[step]</li></ul></div>
              <div class="flow-note warn"><strong>Fails here?</strong> [what happens, what's left untouched]</div>
            </div>
            <div class="flow-down"><span>[condition to move on]</span></div>
            <div class="flow-row">
              <div class="node stage"><span class="stage-head"><span class="num">3</span>[Stage]</span>
                <ul><li>[step]</li><li>[step]</li></ul></div>
              <div class="flow-note">[what's saved or irreversible]</div>
            </div>
            <div class="flow-down"></div>
            <div class="flow-row"><div class="node result">[what the caller gets back]</div></div>
          </div>
        </div>

        <!-- Optional: only when the steps need more detail than fits in the stage boxes -->
        <ol class="text-xs text-slate-600 dark:text-slate-400 space-y-2.5 list-decimal list-inside">
          <li><strong>Step 1:</strong> [Description]</li>
        </ol>
      </div>
    </section>

    <!-- SECTION 6: Predict, Then See -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-1">6. Predict, Then See</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">Make a guess before opening each answer. [If the reader can run things: "Or run it yourself: …"]</p>
        <div class="space-y-4">
          <!-- One per exercise, 2–3 in all -->
          <div class="rounded-lg border border-slate-200 dark:border-slate-800 p-4">
            <p class="text-sm font-semibold text-slate-900 dark:text-white">[Question: you run this. What comes back, and why?]</p>
            <pre class="mt-2 bg-slate-900 text-slate-100 rounded-lg p-3 font-mono text-xs overflow-x-auto">[command, request or input]</pre>
            <details class="reveal mt-3">
              <summary class="text-sm font-semibold text-teal-700 dark:text-teal-300">Show what actually happens</summary>
              <pre class="mt-2 bg-slate-900 text-slate-100 rounded-lg p-3 font-mono text-xs overflow-x-auto">[real output, trimmed but not edited]</pre>
              <p class="mt-2 text-xs leading-relaxed text-slate-600 dark:text-slate-400">[1–2 sentences tying the output back to the ladder or the trace]</p>
            </details>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 7: The Field Guide & Gotchas -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-4">7. Field Guide &amp; Sharp Edges</h2>

        <!-- Symptom table: led by what the reader will actually see -->
        <h3 class="text-sm font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wide mb-3">You'll See &rarr; It Means &rarr; Fix</h3>
        <div class="overflow-x-auto mb-6">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-slate-700 dark:text-slate-300">
                <th class="py-2.5 px-3 font-semibold">You'll see</th>
                <th class="py-2.5 px-3 font-semibold">It means</th>
                <th class="py-2.5 px-3 font-semibold">Fix</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-600 dark:text-slate-400">
              <tr>
                <td class="py-2.5 px-3 font-mono text-slate-900 dark:text-slate-200">[exact error message or symptom]</td>
                <td class="py-2.5 px-3">[the cause]</td>
                <td class="py-2.5 px-3">[the fix]</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Sharp Edge Box: silent traps, with no symptom to search for -->
        <div class="mb-4 rounded-lg border-l-4 border-amber-500 bg-amber-50 dark:bg-amber-950/30 p-4">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300">⚠️ Sharp Edge: [Title]</span>
          </div>
          <p class="text-xs text-amber-900 dark:text-amber-200 leading-relaxed">[Gotcha explanation]</p>
        </div>

        <!-- Tip Box -->
        <div class="rounded-lg border-l-4 border-teal-500 bg-teal-50 dark:bg-teal-950/30 p-4 mb-6">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-bold uppercase tracking-wider text-teal-800 dark:text-teal-300">💡 Tip / Blueprint: [Title]</span>
          </div>
          <p class="text-xs text-teal-900 dark:text-teal-200 leading-relaxed">[Tip explanation]</p>
        </div>

        <!-- Coordinates -->
        <div class="border-t border-slate-200 dark:border-slate-800 pt-4">
          <h3 class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">Deep-Dive Coordinates</h3>
          <ul class="text-xs text-slate-600 dark:text-slate-400 space-y-1 font-mono">
            <li>[File:line — Topic]</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- SECTION 8: Check Yourself -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-1">8. Check Yourself</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">Pick an answer to see why.</p>
        <div class="space-y-4">
          <!-- One card per question, 3–5 in all; vary where the right answer sits -->
          <div data-quiz class="rounded-lg border border-slate-200 dark:border-slate-800 p-4">
            <p class="text-sm font-semibold text-slate-900 dark:text-white">[A why or what-if question]</p>
            <div class="mt-3 grid gap-2">
              <button type="button" data-correct="false" class="w-full rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 text-left text-sm">[A real misconception]</button>
              <button type="button" data-correct="true" class="w-full rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 text-left text-sm">[The right answer]</button>
              <button type="button" data-correct="false" class="w-full rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 text-left text-sm">[Another misconception]</button>
            </div>
            <p data-explain hidden class="mt-3 rounded-lg bg-slate-100 dark:bg-slate-800 px-3 py-2 text-xs leading-relaxed text-slate-700 dark:text-slate-300">[Why the right answer is right, in 1–2 sentences]</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center text-xs text-slate-400 dark:text-slate-600 py-6">
      Generated via Quick-Learn &bull; Single file &bull; Opens straight from disk (styles load from the Tailwind CDN)
    </footer>

  </div>

  <script>
    // Linked highlights and steppers. In a [data-explore] box, picking an element with
    // data-show="a b" (click, Enter or Space, or the box's prev/next buttons) highlights
    // every [data-id] it names and shows its data-note in the box's [data-note-out].
    // The first one starts picked, so the box never opens empty.
    document.querySelectorAll('[data-explore]').forEach((box) => {
      const picks = [...box.querySelectorAll('[data-show]')];
      const note = box.querySelector('[data-note-out]');
      const label = box.querySelector('[data-step-label]');
      const prev = box.querySelector('[data-step="prev"]');
      const next = box.querySelector('[data-step="next"]');
      let current = 0;
      function pick(i) {
        current = Math.max(0, Math.min(picks.length - 1, i));
        const ids = picks[current].dataset.show.split(/\s+/);
        box.querySelectorAll('[data-id]').forEach((el) => el.classList.toggle('is-lit', ids.includes(el.dataset.id)));
        picks.forEach((el, j) => {
          el.classList.toggle('is-picked', j === current);
          el.setAttribute('aria-pressed', String(j === current));
        });
        if (note) note.innerHTML = picks[current].dataset.note || '';
        if (label) label.textContent = `Step ${current + 1} of ${picks.length}`;
        if (prev) prev.disabled = current === 0;
        if (next) next.disabled = current === picks.length - 1;
      }
      picks.forEach((el, i) => {
        if (el.tagName !== 'BUTTON') { el.setAttribute('role', 'button'); el.tabIndex = 0; }
        el.addEventListener('click', () => pick(i));
        el.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); pick(i); }
        });
      });
      if (prev) prev.addEventListener('click', () => pick(current - 1));
      if (next) next.addEventListener('click', () => pick(current + 1));
      if (picks.length) pick(0);
    });

    // Self-check cards: the first pick locks the card, marks the right answer (and a wrong
    // pick), and shows the explanation.
    document.querySelectorAll('[data-quiz]').forEach((card) => {
      const options = [...card.querySelectorAll('button[data-correct]')];
      options.forEach((button) => button.addEventListener('click', () => {
        if (card.dataset.answered) return;
        card.dataset.answered = 'true';
        options.forEach((option) => option.classList.add(
          option.dataset.correct === 'true' ? 'is-right' : option === button ? 'is-wrong' : 'is-out'));
        card.querySelector('[data-explain]').hidden = false;
      }));
    });
  </script>

</body>
</html>
```

#### Diagrams in HTML

HTML guides draw diagrams with the flow components in the skeleton's `<style>` block, not Mermaid. They read top to bottom, use the page's own fonts at full size, follow the theme, and need no script. There are two patterns:

**Path** (`.flow`, section 3): the route one request takes through the system.
- The spine is the main path, top to bottom, 3–6 `.node`s in `.flow-row`s joined by `.flow-down` arrows. Label an arrow with the protocol, route or payload in four words or fewer, or leave it empty.
- Everything else hangs off the spine node it touches, in a `.flow-side` list. Use `.edge` (solid arrow out) for what the node sends or serves, and `.edge.in` (dashed arrow in) for something acting on it, like a supervisor, scheduler or cron job.
- Node variants: `.side` for side nodes, `.helper` (dashed border) for background actors, `.db` for storage. Put the location (path, port, host) in a `<small>` inside the node.
- Always follow it with the Division of Labor table: the diagram shows *where* things are, the table *who owns what*.

**Stages** (`.flow stages`, section 5): one lifecycle, in 2–4 stages.
- Each stage is a `.node.stage` with a numbered `.stage-head` and 2–5 short steps (or one `.cmd` line). The arrows between stages say what has to be true to move on ("tests passed", "lock acquired").
- Beside each stage, a `.flow-note` holds the one thing to remember about it. Use `.flow-note.warn` for failure behaviour ("Fails here? Nothing live changed"). These notes are the reason for the diagram, so don't leave them generic.
- End with a `.node.result` showing what the caller gets back.
- It works on its own. Add the numbered step list underneath only when the steps need more detail than fits in the boxes.

If the system isn't a single path (cycles, many-to-many), draw the path the reader will meet first and hang the rest off it. For a state machine, use stages with a note like "back to 2 when the token expires". Two small diagrams beat one crowded one. Every diagram needs an `aria-label` that says in words what it shows.

#### Interactive pieces in HTML

The skeleton's closing `<script>` runs two small behaviours. Everything is set up with `data-` attributes, so new pieces need markup only.

**Linked highlights and steppers** (`data-explore`). Inside a `data-explore` box:
- `data-id="x"` marks something that can light up: a diagram node, a table cell, one bit or character in a value.
- `data-show="x y"` makes an element pickable. Picking it lights up those ids and puts its `data-note` (HTML allowed) into the box's `data-note-out` element. The first pickable element starts picked.
- Optional `data-step="prev"`, `data-step="next"` and `data-step-label` buttons walk the pickable elements in page order. That's the step-through on the section 3 diagram.

The explorer from section 5 uses the same attributes. For example, a permutation table where picking an output position lights up the input bit it came from and the output bit it fills:

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
  <p data-note-out class="explore-note mt-3 rounded-lg bg-teal-50 dark:bg-teal-950/40 px-3 py-2 text-sm"></p>
  <p class="mt-2 font-mono text-sm">input:  <span data-id="in-1">0</span><span data-id="in-2">0</span>…</p>
  <p class="font-mono text-sm">output: <span data-id="out-1">1</span><span data-id="out-2">1</span>…</p>
</div>
```

- **Use real values.** Compute them by running the real code (or a few lines of in-page JS), never by hand.
- **Generate long markup with a short script.** Don't hand-write 64 `<span data-id>` bits: build them from the value string with a few lines of JS, placed before the skeleton's script. Static markup is fine for short values.
- **Mark changes in a before/after** with `<span class="chg">` (no script needed), e.g. the bits a round changed.
- When the topic is something the page can compute (an encoding, a hash, a cipher, a regex), consider a "try your own value" input that reruns it. That's optional; only add it when the computation is small and certain.

**Predict, then see** uses `<details class="reveal">`: no script, works in Markdown too.

**Self-check cards** (`data-quiz`): buttons with `data-correct="true"` or `"false"`, and an explanation `<p data-explain hidden>`. The first pick locks the card, marks the right answer (and a wrong pick), and shows the explanation.

#### Render Check (Required)

After writing the final HTML file, look at it the way a reader will before reporting completion:

```bash
bash /Users/jake/dev/common/ai-agents/skills/quick-learn/scripts/render_check.sh /path/to/guide.html
```

It screenshots the page in headless Chrome at desktop width in light and dark themes, and at phone width (390px), into a folder it prints. It cuts the screenshots into slices you can read. It also reports anything wider than the phone screen. Read every slice and check:
- each diagram is drawn as intended (arrows meet their nodes, labels aren't clipped, nothing overlaps) in both themes;
- no text runs off the right edge at phone width (the overflow report is empty);
- placeholders like `[Component]` are all gone;
- interactive pieces start on their first step (the screenshots show step 1 picked), so check that the highlight lands on the right element and that its note says the right thing.

Fix what you find and rerun. For a Markdown guide, run `validate_mermaid.sh` instead (see Markdown above).

#### Design Customization

Treat the boilerplate as the required **functional baseline**, not a visual ceiling. Keep its light/dark behavior, persisted theme preference, responsive layout, flow diagram components, interactive scripts, and accessible theme toggle intact. Then adapt the presentation to the subject so guides do not all look interchangeable.

- Establish a deliberate visual identity that fits the material: for example, a systems guide may use a restrained technical-console feel, while an algorithm walkthrough can use strong step markers, color-coded data-flow stages, and monospace trace cards.
- Improve scanability when it helps learning: a compact table of contents, sticky desktop navigation, section progress, grouped callouts, or clearly separated trace stages are all appropriate additions.
- Add an explorer or "try your own value" sandbox only when it directly reinforces the concept, such as an S-box row/column lookup, a parser input, or a request trace. Build it on the `data-explore` attributes where they fit; keep it dependency-free and usable on mobile.
- Restyle the flow components through their `--flow-*` variables (for both `:root` and `.dark`) rather than rewriting them, so the layout and phone behaviour stay intact.
- Preserve the guide's content structure and avoid decoration that competes with the conceptual ladder, diagrams, or concrete trace. The reader should see the learning path before the visual flourishes.
- Maintain contrast, visible keyboard focus, readable line lengths, and mobile behavior. Use Tailwind utilities or a small embedded stylesheet when the template needs a subject-specific component that utilities alone do not express clearly.

> 💡 **Design test:** If the same theme could be dropped unchanged onto any unrelated guide, add one or two subject-driven visual or interactive cues. If a visual element does not help comprehension or navigation, remove it.

### 2. Markdown (When Asked)
Standard GitHub-flavored Markdown with Mermaid code blocks, bullet points, and callout quotes. Predict-then-see reveals and self-check answers go in `<details>` blocks; skip the step-through and explorers, which need the HTML page. For the path diagram use `flowchart TD` and declare the main path's edges first, so it runs down one side.

Validate the diagrams before reporting completion:

```bash
bash /Users/jake/dev/common/ai-agents/skills/quick-learn/scripts/validate_mermaid.sh /path/to/guide.md
```

It extracts every `mermaid` code block (or `.mermaid` element in an HTML file), checks each with the pinned Mermaid version, and exits nonzero with the diagram number and parser error if one fails. Fix and rerun until it passes.
