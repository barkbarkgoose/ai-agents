---
name: quick-learn
description: Transforms dense technical readings, documentation, architectures, or unfamiliar concepts into high-retention, progressively scaffolded visual learning guides. Starts with a crisp 1-2 sentence definition and a conceptual ladder of progressive statements before moving to visual architecture (Mermaid), concrete lifecycle traces, hands-on sparks, and sharp edges. Designed for visual, ADHD-friendly learning without forced narrative fluff. Supports self-contained HTML outputs styled with Tailwind CDN. Use when learning new concepts, previewing documentation, preparing to dive into unfamiliar codebases, or unpacking complex topics.
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
- **Lean Physical Anchors & Visual Maps:** Use a 1-sentence physical anchor and a clear Mermaid diagram to show boundaries and flow.
- **Trace the Byte:** Trace one concrete operation end-to-end to cement how pieces interact.
- **Hands-on Spark:** Provide a 60-second command or experiment to touch the system directly.

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
- **Mermaid Diagram:** Clean flowchart or architecture diagram showing boundaries, data flow, ports, and protocols. Keep it scannable in 5 seconds.
- **The Division of Labor (Contrast Table):** Clarify boundaries early to prevent confusion.
  - E.g., *Control Plane vs. Data Plane*, or *What it Does vs. What it Does NOT Do*.

### 4. The Cast of Characters
List the 3–5 key components or concepts, ordered from foundation/storage to orchestrator/caller:
- **Role:** Plain-English description.
- **Owns:** 1–2 bullet points on what it is responsible for.
- **Doesn't Touch:** What it explicitly leaves to other components.
- **Contract / Interface:** The primary API, schema, event, or CLI command it uses.

### 5. The Lifecycle Walkthrough ("Follow the Request")
Pick ONE realistic, concrete scenario and trace it step-by-step:
1. **The Trigger:** Who initiates the action and what payload/command is sent.
2. **Step-by-Step Flow:** Numbered chronological steps showing handoffs, state changes, and disk/network operations.
3. **Sequence Diagram:** A clean Mermaid sequence diagram showing message passing between actors.
4. **The Resolution:** What returns to the caller and what persistent state remains.

### 6. The 60-Second Hands-On Spark
A tiny, concrete experiment or mental sandbox:
- A 3-line `curl` command, CLI invocation, REPL snippet, or minimal config showing how to touch, test, or verify the system with your own hands.

### 7. The Field Guide (Gotchas & Sharp Edges)
- **Traps & Plot Twists:** 2–4 subtle bugs, hidden default assumptions, or common misconceptions that trip people up.
- **When to Reach for This vs. When to Walk Away:** Clear, bulleted decision criteria.
- **Deep-Dive Coordinates:** Exact files, lines, or official doc sections to inspect next.

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

### 1. Markdown (Default)
Standard GitHub-flavored Markdown with Mermaid code blocks, bullet points, and callout quotes.

### 2. Self-Contained HTML Document (When Requested)
When the user asks for an HTML document or self-contained guide, generate a single `.html` file that opens beautifully without any local server or build tools.

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
      if (window.renderDiagrams) {
        window.renderDiagrams();
      }
    }
  </script>

  <!-- Mermaid.js CDN with Dynamic Theme Switching -->
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

    // Capture raw diagram source before rendering
    const diagramElements = Array.from(document.querySelectorAll('.mermaid')).map((el, i) => {
      return {
        el,
        code: el.textContent.trim(),
        baseId: `mermaid-diagram-${i}`
      };
    });

    async function renderDiagrams() {
      const isDark = document.documentElement.classList.contains('dark');
      mermaid.initialize({
        startOnLoad: false,
        theme: isDark ? 'dark' : 'neutral',
        securityLevel: 'loose',
        flowchart: { curve: 'basis' }
      });

      for (let i = 0; i < diagramElements.length; i++) {
        const item = diagramElements[i];
        const renderId = `${item.baseId}-${Date.now()}-${i}`;
        try {
          const { svg, bindFunctions } = await mermaid.render(renderId, item.code);
          item.el.innerHTML = svg;
          if (bindFunctions) bindFunctions(item.el);
        } catch (err) {
          console.error('Mermaid render error for diagram', i, err);
        }
      }
    }

    // Initial render
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', renderDiagrams);
    } else {
      renderDiagrams();
    }

    // Expose for theme toggle button
    window.renderDiagrams = renderDiagrams;
  </script>
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

        <!-- Mermaid Diagram Container -->
        <div class="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg p-4 mb-6 overflow-x-auto">
          <div class="mermaid">
            <!-- Mermaid diagram code -->
          </div>
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
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-4">4. The Cast of Characters</h2>
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

        <!-- Sequence Diagram -->
        <div class="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg p-4 mb-6 overflow-x-auto">
          <div class="mermaid">
            <!-- Mermaid sequence diagram -->
          </div>
        </div>

        <ol class="text-xs text-slate-600 dark:text-slate-400 space-y-2.5 list-decimal list-inside">
          <li><strong>Step 1:</strong> [Description]</li>
        </ol>
      </div>
    </section>

    <!-- SECTION 6: The 60-Second Hands-On Spark -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-1">6. The 60-Second Hands-On Spark</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">[How to poke or test it directly]</p>
        <div class="bg-slate-900 text-slate-100 rounded-lg p-4 font-mono text-xs overflow-x-auto">
          <!-- Minimal code/cli/curl command -->
        </div>
      </div>
    </section>

    <!-- SECTION 7: The Field Guide & Gotchas -->
    <section class="mb-10">
      <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
        <h2 class="text-xs font-bold text-teal-600 dark:text-teal-400 tracking-wider uppercase mb-4">7. Field Guide &amp; Sharp Edges</h2>

        <!-- Sharp Edge Box -->
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

    <!-- Footer -->
    <footer class="text-center text-xs text-slate-400 dark:text-slate-600 py-6">
      Generated via Quick-Learn &bull; Self-contained &bull; Works offline with zero local server dependencies
    </footer>

  </div>

</body>
</html>
```
