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
When the user asks for an HTML document or self-contained guide, generate a single `.html` file that opens beautifully without any local server or build tools:
- **Tailwind CSS CDN:** Load via `<script src="https://cdn.tailwindcss.com"></script>`.
- **Mermaid.js CDN:** Include client-side Mermaid rendering:
  ```html
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
  </script>
  ```
- **Styling Requirements:**
  - Responsive container: `max-w-4xl mx-auto px-6 py-10`.
  - Clean typography and palette (e.g. `bg-slate-50 text-slate-800` with dark-friendly options).
  - Component cards with soft borders (`bg-white rounded-xl border border-slate-200 shadow-sm p-6 mb-8`).
  - Styled callouts with clear colored borders and badges for `Tip` and `Sharp Edge`.
  - Dark-styled code blocks (`bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-sm overflow-x-auto`).
  - Pre-rendered or containerized `<div class="mermaid">` blocks ready for Mermaid.js to hydrate.
  - Standalone: zero external local dependencies, instantly readable offline or when opened directly in a browser (`file://`).
