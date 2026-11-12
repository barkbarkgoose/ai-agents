# Mode: EXPLAIN — How It Works, as a Reference Doc

For when the user wants something **explained or diagrammed as a document**, not taught to them:
"diagram the API", "explain the round-trip logic of this app", "document how auth works", "map out
the job pipeline", "how does X get from A to B". The reader may be the user, a teammate or a future
maintainer; they want to find how it works, fast, and come back to it later.

Default accent: `emerald`. Kicker: what kind of doc it is ("Architecture", "API map", "Request round trip").

## What it keeps from LEARN, and what it drops

It keeps the parts that explain the system: the path diagram with step-through, division of labor,
components, the lifecycle trace, explorers, and the field guide.

It drops the parts that exist to make a reader *learn*: no conceptual ladder, no anchor analogy, no
predict-then-see, no check-yourself quiz, no "you'll remember this" framing. If the user later says
"now teach me this", rebuild in LEARN mode from the same source.

## Ground it in the source first

Read the actual code, routes, schemas, configs and docs before drawing anything. Every box in a
diagram and every step in a trace should map to something you can point at (`file:line`, a route,
a table, a queue name). Run things when you can to capture real payloads and responses; otherwise
take them from the code or docs and say which. Never invent an endpoint, field, or hop.

## Sections

Include what the request is about, not every section by default. Minimum: a diagram plus either the
trace or the contract table. Block names refer to `references/blocks.html`.

| # | Section | Block(s) | Include when |
|---|---------|----------|--------------|
| 1 | **Hero**: headline names the system and what's explained; standfirst is the 1–2 sentence plain-English anchor + category/core job | template hero; optional *Stat row* (real counts: endpoints, services, hops) or *Meta bar* (repo, commit, date) | always |
| 2 | **The path**: route one real request takes, side systems hanging off the step they touch | *Path diagram + stepper* (stepper carries the one real example) | always, unless the subject has no flow (then a *Layer stack*) |
| 3 | **Who owns what** | *Division of labor* | 3+ components |
| 4 | **Components**: role, owns, doesn't touch, interface, file | *Component cards* | the reader will need to find or change the pieces |
| 5 | **The round trip / lifecycle**: one concrete scenario, trigger → stages → what comes back and what state remains | *Stages diagram*, *Trace steps* (each ending in `file:line`) | "explain the logic / flow / round trip" requests: this is the centrepiece |
| 6 | **Contracts**: method · path · request · response · auth/errors; or message/event schemas | *Wide table*, *Code + commentary* for one representative payload | "diagram/document the API" requests: this is the centrepiece |
| 7 | **Data transforms** | *Explorer* | the system maps input to output in a way worth poking at |
| 8 | **What changed** | *Before / After* | the request is about a migration, refactor or version change |
| 9 | **Field guide**: symptoms → cause → fix, silent traps, deep-dive coordinates | *Symptom table*, *Sharp edge* callouts, *Deep-dive coordinates* | known failure modes exist; coordinates almost always |

Shape by request:
- **"Diagram the API"** → 1, 2, 6, then 3/4 if the API spans services, 9.
- **"Explain the round-trip logic"** → 1, 2, 5 (both legs: out and back), 3, 9.
- **"Document how X works"** → 1, 2, 3, 4, 5, 9.

## Rules

1. **One real example, carried through.** Pick one concrete request and use its actual values in the
   stepper notes, the trace, and the payload samples, so the page agrees with itself.
2. **Every claim has a coordinate.** A step, box or row the reader can't locate in the code or docs is
   a liability. Put `file:line` (or a doc link) in trace steps, component cards and contract rows.
3. **Headings say what's under them.** This is a reference people will skim and come back to:
   "Auth token refresh" beats "Act 2". Nav links mirror the headings.
4. **No teaching scaffolding.** No ladder, no quiz, no "imagine a restaurant" analogies. A single
   one-line comparison is fine if it genuinely saves a paragraph.
5. **Show the return leg.** For anything request-shaped, say what comes back, what state persists,
   and what the caller sees on failure. Half a round trip is the commonest gap in these docs.
6. **Prose is allowed** for genuine reasoning (why it's designed this way) — keep it short and put it
   next to the diagram it explains.

## Tone & length

Pragmatic staff engineer writing it down for the team: concise, direct, no melodrama. Paragraphs 2–3
sentences. Each section one screen or less; a doc that's scrollable in about two minutes.

## Markdown output (on request only)

Same as LEARN's Markdown output: Mermaid `flowchart TD` for the path, a sequence diagram for the
round trip, tables as GFM tables. Validate with `scripts/validate_mermaid.sh`.
