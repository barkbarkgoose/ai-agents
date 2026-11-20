---
name: quick-learn
description: Turns a topic, codebase, API, plan, or markdown file into one self-contained HTML page (Tailwind CDN, light/dark toggle, built-in flow diagrams, works from disk), in one of four modes chosen by what the reader wants. LEARN, when the user wants to learn it themselves ("teach me", "I want to learn", "help me understand", "I'm new to", "crash course"): a progressively scaffolded guide with a plain-English anchor, conceptual ladder, step-through diagrams, lifecycle trace, predict-then-see exercises and a self-check quiz. EXPLAIN, when the user wants it documented or diagrammed ("diagram the API", "explain the round-trip logic of this app", "document how auth works", "map out the pipeline"): a reference doc of path diagrams, ownership, components, request traces, API contracts and sharp edges, without the teaching scaffolding. PLAN: a why-and-how project or architecture plan from a repo, PRD or brief (thesis, non-goals, before/after, gated phases, risks, definition of done). MARKDOWN: converts any existing .md file, technical or not (meeting notes, research, recipes, grocery lists), into a styled page. Markdown output on request. Use for learning guides, architecture explainers, API maps, visual plan docs, "make this markdown into an HTML page", or any shareable single-file doc.
---

# Quick-Learn

Produces **one self-contained `.html` file**: no build step, no local assets, no server. Open it in a
browser, email it, drop it in a repo, print it. Every mode uses the same shell
(`assets/template.html`) and the same block catalogue (`references/blocks.html`); the mode decides
which sections go in.

---

## 1. Pick the mode

Decide from the **goal of the request**, not the topic. The same subject (say, an auth flow) can be
a LEARN page or an EXPLAIN page.

| The user wants… | Signals | Mode | Read |
|---|---|---|---|
| to learn it themselves | "teach me", "I want to learn", "help me understand", "I'm new to", "crash course", "quiz me", "get me up to speed" | **LEARN** | `references/MODE_LEARN.md` |
| it explained or diagrammed, as a doc | "explain", "diagram", "document", "map out", "walk through", "how does X work", "write up how" | **EXPLAIN** | `references/MODE_EXPLAIN.md` |
| a plan for building or changing something | "plan", "how would we build / migrate", a PRD or brief | **PLAN** | `references/MODE_PLAN.md` |
| an existing `.md` turned into a page | a `.md` file + "make this into HTML / a page" | **MARKDOWN** | `references/MODE_MARKDOWN.md` |

Tie-breakers:
- **The default is a doc, not a lesson.** LEARN only when the request is about the user's own
  understanding. "Explain the round-trip logic of this app" → EXPLAIN. "Teach me the round-trip
  logic" → LEARN.
- A `.md` that is itself a plan → MARKDOWN for the content, borrowing PLAN's section vocabulary where it fits.
- A `.md` the user wants to *learn from* ("teach me what's in this") → LEARN, with the file as the source.
- Say which mode you picked in one line when you start, so the user can redirect.

Then read that mode's file and `references/components.md` (LEARN, EXPLAIN; PLAN if it has a path diagram).

---

## 2. What each mode includes

Same shell for all four. These are the sections the mode puts in `<main>`:

| Section (block in `blocks.html`) | LEARN | EXPLAIN | PLAN | MARKDOWN |
|---|:-:|:-:|:-:|:-:|
| Hero: kicker, headline, standfirst | ✓ | ✓ (standfirst = the anchor) | ✓ (headline = thesis) | ✓ |
| Stat row / meta bar | – | optional | ✓ stat row | meta bar from frontmatter |
| Anchor card | ✓ | – | – | – |
| Conceptual ladder | ✓ | – | – | – |
| Path diagram + stepper | ✓ | ✓ | optional | – |
| Division of labor | ✓ | ✓ | – | – |
| Component cards | ✓ | ✓ | – | – |
| Stages diagram + trace steps | ✓ | ✓ | – | – |
| Explorer | if data transforms | if data transforms | – | – |
| Contract table (wide table) | – | API requests | – | – |
| Predict, then see | ✓ | – | – | – |
| Field guide: symptoms, sharp edges, coordinates | ✓ | ✓ | – (risks table instead) | – |
| Check yourself quiz | ✓ | – | – | – |
| Plan blocks (Part B) | – | before/after if "what changed" | ✓ | where the content has that shape |
| General blocks (Part C) | callouts | callouts, tables, code | callouts, tables | ✓ |

---

## 3. Workflow

**1. Gather from the real thing.** Read the repo, code, routes, PRD, docs or the `.md` before writing.
Pull real numbers, real payloads, real outputs. A page written from the prompt alone produces
adjectives; one written from the source produces findings.

**2. Decide the source of record.**
- LEARN / EXPLAIN: write the HTML directly. Markdown only when asked (see the mode file).
- PLAN: write `NAME.md` first, then render `NAME.html` from it. Never author the prose twice.
- MARKDOWN: the source `.md` already exists. Never modify it.

**3. Copy the shell.** `assets/template.html` → output file. Replace every `{{PLACEHOLDER}}`:
`{{DOC_SLUG}}` a unique kebab-case id (namespaces saved theme and checklist state), `{{ACCENT}}` per
the mode's default or MARKDOWN's register preset.

**4. Fill sections with blocks.** Every section maps to a block in `references/blocks.html` (or the
prose wrapper, which is a legitimate answer). Copy the snippet, replace the placeholder text.
Diagram and interactive rules: `references/components.md`.

**5. Verify** (section 6), fix, re-verify, then report.

**Where to write:** MARKDOWN and PLAN go next to the source with a matching basename
(`groceries.md` → `groceries.html`). LEARN and EXPLAIN go in the current directory as
`<topic-slug>.html` unless the user names a place.

---

## 4. Shared rules (every mode)

- **Never invent content.** No made-up output, endpoints, numbers or facts. If you couldn't run it,
  take it from official docs and say so. In MARKDOWN mode: no filled gaps, no smoothed-over contradictions.
- **Content shape picks the block, never the other way round.** A comparison always looks like a
  comparison, a sequence like a sequence. Choosing blocks for visual variety destroys that.
- **Prose is allowed.** Chopping genuine reasoning into cards makes it harder to read.
- **Match the register.** A grocery list gets a fast checklist, not a thesis and a risk table. Ceremony on casual content reads as parody.
- **Disciplined palette.** Slate for structure, one accent (`brand-*`, set by `{{ACCENT}}`), and
  semantic colour only where it means something: rose = old/rejected/danger, emerald =
  new/recommended/done, amber = caution, sky = info.
- **Diagrams in HTML use the flow components, not Mermaid.** Mermaid is for Markdown output only.
- **Tone:** a pragmatic staff engineer writing it down. Concise, direct, short paragraphs, no forced melodrama.

---

## 5. The shell

`assets/template.html` already implements all of this. Start from it; don't hand-roll a shell.
These must survive every edit:

1. Tailwind via CDN with `darkMode: 'class'`, and the `brand` accent palette.
2. Theme resolved in `<head>` before first paint (saved choice per page, else the OS setting; storage wrapped in `try/catch`).
3. The theme toggle (`#themeBtn`, `aria-pressed`), which persists per page and follows the OS until the reader picks.
4. The `<style>` block (flow diagrams, interactive pieces, print) and the behaviours script
   (stepper/explorer, quiz, checklist). Unused parts are inert, so leave them in.

**Design customization.** Treat the shell as the functional baseline, not a visual ceiling. Give the
page an identity that fits the subject (a restrained console feel for a systems doc, strong step
markers and monospace trace cards for an algorithm), change the accent, add a TOC or section
progress when it helps scanning. Restyle diagrams through the `--flow-*` variables. Keep contrast,
keyboard focus, readable line lengths and phone behaviour. If a visual element doesn't help
comprehension or navigation, remove it; if the theme could be dropped unchanged onto an unrelated
page, add one or two subject-driven cues.

---

## 6. Verify before reporting done

Run the render check (path relative to this skill's directory):

```bash
bash <skill-dir>/scripts/render_check.sh /path/to/page.html
```

It screenshots the page in headless Chrome at desktop width in light and dark, and at phone width
(390px), into a folder it prints, cut into readable slices, and reports anything wider than the phone
screen. Read every slice and check:
- [ ] each diagram is drawn as intended (arrows meet nodes, labels not clipped, nothing overlaps) in both themes;
- [ ] tinted panels (rose/emerald/amber/sky/brand) are readable in both themes;
- [ ] no text runs off the right edge at phone width (the overflow report is empty);
- [ ] interactive pieces start on their first step, the highlight lands on the right element, and its note is right.

Then the mechanical checks:
- [ ] no placeholders left: `grep -n '{{' page.html` is empty, and no `[Bracketed placeholder]` text remains;
- [ ] every `href="#x"` has a matching `id="x"`;
- [ ] nothing loads from a local path (CDN and data-URIs only);
- [ ] the head theme script, `#themeBtn` and the behaviours script are intact.

For Markdown output, run `bash <skill-dir>/scripts/validate_mermaid.sh /path/to/page.md` instead. It
checks every `mermaid` block with the pinned Mermaid version and exits nonzero with the diagram number
and parser error if one fails.

Fix what you find and rerun.

---

## Files

```
quick-learn/
  SKILL.md                      this file: mode router, shared rules, workflow, verification
  assets/template.html          the shared shell: copy it, keep the head scripts, styles and behaviours
  references/blocks.html        block catalogue. Part A learn/explain, Part B plan, Part C general
  references/components.md      flow diagrams + interactive pieces (stepper, explorer, quiz, checklist)
  references/MODE_LEARN.md      the 8-section learning guide
  references/MODE_EXPLAIN.md    reference docs: diagram the API, explain the round trip
  references/MODE_PLAN.md       plan section vocabulary and rules
  references/MODE_MARKDOWN.md   markdown construct → block mapping, register presets
  scripts/render_check.sh       screenshots + overflow report (all HTML output)
  scripts/validate_mermaid.sh   Mermaid syntax check (Markdown output)
```
