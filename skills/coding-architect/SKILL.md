---
name: coding-architect
description: coding best-practices and architecture skill
---
# Coding Architect

Use this skill when planning, implementing, or reviewing code changes where readability, maintainability, downstream impact, or local design quality matter. This skill is intended to push beyond basic correctness and lint-style consistency checks.

## Purpose

Apply this rubric to avoid code that merely works while remaining hard to read, fragile, repetitive, or locally inconsistent. Use it both for review and for self-review after edits.

## Primary Goals

- Keep code readable and maintainable.
- Preserve or improve clarity in the touched area.
- Avoid repeating bad existing patterns when a clearer local approach is available.
- Catch adjacent impact from changed symbols, contracts, and data flow.
- Prefer minimal correct changes without ignoring broader consequences.

## Review Rubric

### Readability

- Prefer code that communicates intent quickly.
- Break up dense logic when it improves understanding.
- Avoid long lines when they reduce readability.
- Keep related logic close together.

### Documentation and Comments

- **Historic Context & Decisions:** Add documentation for anything that has historic context or where a key design decision was made.
- **Focus on Business Logic:** Comments should focus on the business logic, explaining *why* the code exists and what *should* happen, rather than merely describing what the code does line-by-line.
- **Functions & Methods:** Function and method documentation should describe in one or two lines what the function does, list out inputs, and define any expected return value.

### Naming

- Use meaningful names for functions, methods, classes, variables, types, and files.
- Avoid vague names like `data`, `item`, `value`, or `result` when a more specific name is available.
- Avoid reusing a single identifier for multiple purposes across a block of logic.
- If a value changes meaning, split it into separate variables with clearer names.

### Function and Module Design

- Prefer single-task functions.
- If a function is doing multiple conceptual jobs, consider extracting a helper when it improves clarity.
- Do not create abstractions prematurely.
- Keep modules cohesive.
- Prefer minimal interfaces and clear contracts.

### Control Flow

- Avoid deep nesting when early returns, guard clauses, or smaller helpers make the flow clearer.
- Keep happy-path logic easy to follow.
- Make exceptional or failure paths visible.
- Avoid unnecessary branching and repeated condition checks.

### DRY and Duplication

- Remove needless repetition within the touched scope.
- Do not extract tiny helpers purely to satisfy DRY if the result becomes harder to read.
- Prefer a little duplication over the wrong abstraction.
- If similar logic already exists nearby, follow the clearer pattern rather than copying a bad one.

### Data Processing and Efficiency

- Look for avoidable repeated scans, redundant conversions, and unnecessary allocations.
- Prefer straightforward and efficient data flow.
- Avoid turning simple logic into clever but opaque code.
- Consider algorithmic impact when handling collections, loops, and lookups.

### Refactoring Judgment

- Improve the touched area when a local refactor clearly reduces complexity.
- Do not broaden scope into a large cleanup unless explicitly asked.
- If surrounding code has bad patterns, avoid repeating them. If a small local improvement is safe and directly related to the task, prefer the better pattern.

### Exceptions and Failure Handling

- Handle expected error cases clearly.
- Do not swallow exceptions silently.
- Preserve useful context in errors.
- Ensure failure behavior matches business expectations.
- If cleanup, rollback, or user-facing error states matter, check them.

### Security and Privacy

- Validate inputs and outputs where appropriate.
- Avoid leaking secrets, tokens, PII, or internal-only details.
- Preserve authorization, access checks, and safe defaults.
- Be cautious with logging, serialization, interpolation, file paths, and dynamic execution.
- When changing data flow, consider what new information becomes exposed or persisted.

### Downstream Impact

- For any changed symbol, search usages and imports.
- Check callers, implementers, subclasses, consumers, tests, and config references.
- If a contract changes, verify all known touchpoints are updated.
- Do not assume the edited file is the only impacted place.

## Self-Review Checklist

Before reporting success on a code change, answer these questions:

1. Is the code easy to read without extra explanation?
2. Do the comments explain business intent, historic context, and what *should* happen rather than restating code?
3. Do all modified functions/methods have a concise summary, inputs, and expected returns documented?
4. Are names specific and stable in meaning?
5. Did I keep functions focused on one task?
6. Did I avoid unnecessary duplication while also avoiding the wrong abstraction?
7. Did I reduce or avoid deep nesting?
8. Are lines and blocks short enough to scan comfortably?
9. Did I avoid reusing one variable for multiple semantic roles?
10. Is the data processing straightforward and reasonably efficient?
11. Did I improve the touched area instead of copying a bad local pattern?
12. Are error handling, edge cases, and failure paths clear?
13. Did I consider security and privacy implications?
14. Did I search usages for changed symbols and update affected areas?
15. Is this patch the right size for the request?

## Review Output Format

When using this skill in a review, report concise findings under these headings when relevant:

- Readability
- Documentation and Comments
- Naming
- Function Design
- Control Flow
- Duplication
- Efficiency
- Error Handling
- Security and Privacy
- Downstream Impact
- Scope Judgment

If no issue is found in a category, omit it rather than padding the review.

## Biases

- Prefer simple over clever.
- Prefer clear over dense.
- Prefer local improvement over broad churn.
- Prefer preserving contracts over surprising downstream consumers.
- Prefer leaving the touched area better than it was found.
