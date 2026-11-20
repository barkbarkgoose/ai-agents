# Mode: MARKDOWN — Any Markdown → HTML Doc

Input is any `.md` file: meeting notes, research, a recipe, a reading list, a
grocery list, a postmortem, a journal entry. Output is the shared template, with
the content mapped onto Part C blocks (and Part B where the content has that shape).

The job is **structure recognition**, not decoration. Read the markdown, work
out what shape the content actually has, then pick blocks that match. Do not
pick blocks because they look impressive.

---

## Mapping table

| Markdown construct | Block | Notes |
|---|---|---|
| `# H1` | Hero headline | Only the first one; later H1s become sections |
| `## H2` | Section (`<section>` + `<h2>`) | Add an `id` and a nav link |
| First paragraph after H1 | Hero standfirst | Trim to ~2 lines |
| Frontmatter (`date`, `tags`, `author`) | Meta bar + tag chips | Never render raw YAML |
| Paragraph runs | Prose wrapper | Switch the CDN src to `?plugins=typography` |
| `- [ ]` task list | Checklist (with persistence) | Real checkboxes, not styled bullets |
| Flat `-` list, 8+ items with groupings | Category groups | Group by aisle/topic/day; add counts |
| Flat `-` list, short | Plain `<ul>` inside prose | Don't over-build a 4-item list |
| `**Term** — definition` lines | Definition cards | |
| `> blockquote` | Callout | Colour by meaning; see below |
| `> **Note:** …` / `⚠️` / "Warning:" | Callout, amber or rose | |
| One striking sentence | Pull quote | At most one per doc |
| Table | Wide table (in `overflow-x-auto`) | Wrapper is mandatory |
| Fenced code | `<pre>` card | Preserve language; no syntax-highlight lib |
| Numbered steps | Steps/recipe | Phase timeline only if there are real gates |
| A vs. B comparison | Before/After | Works for products, options, tools — not just code |
| Links list | Definition cards or prose list | Include the *why* if the note has one |
| Images | `<img class="max-w-full rounded-xl border …">` | Remote URLs are fine here |

**Callout colours:** sky = info/context · emerald = tip/recommendation ·
amber = caution/caveat · rose = danger/blocker.

---

## Rules

**1. Never invent content.** No new facts, no filled gaps, no smoothed-over
contradictions. If a note is a fragment, the doc renders a fragment. Reorganising
and re-titling for clarity is fine; adding claims is not.

**2. Don't force visuals onto prose.** If a section is genuinely three paragraphs
of reasoning, the prose wrapper is the correct answer. Forcing it into cards
makes it *harder* to read. This is the main way markdown-mode goes wrong.

**3. Match the register.** A grocery list gets a plain, fast, scannable layout —
kicker, headline, checklist grouped by aisle, done. It does not get a thesis
statement, a risk table, or a phase timeline. Ceremony on casual content reads
as parody.

**4. Keep the source order** unless the content is clearly a dump. Notes usually
have an implicit narrative; reordering destroys it. Grouping an unordered list
is different — that's the point of it.

**5. Nav only when it earns its place.** Under ~4 sections, drop the `<nav>`
links and keep just the brand and the theme toggle. Over ~8, use the TOC sidebar.

**6. Preserve checkable state.** If the source has `- [x]`, render it checked.

---

## Register presets

The Accent column is the template's `{{ACCENT}}`.

| Content type | Accent | Hero | Typical blocks |
|---|---|---|---|
| Grocery / packing / shopping | emerald | Minimal — title + count | Checklist, category groups |
| Meeting notes | sky | Title, date, attendees in meta bar | Prose, callouts, checklist for actions |
| Research / reading | sky | Title + source meta | Prose, definition cards, pull quote, links |
| Recipe | amber | Title + time/servings stats | Stat row, category groups (ingredients), steps |
| Postmortem / incident | rose | Title + timeline stats | Meta bar, steps, two-column table, numbered criteria |
| Journal / personal | violet | Title + date | Prose, pull quote, images |
| Comparison / decision | emerald | Title + the question | Before/After, two-column table, numbered criteria |

---

## Output

Write the HTML next to the source with a matching basename:
`grocery-list.md` → `grocery-list.html`. Never overwrite the markdown.
