---
name: prd-creator
description: Transforms a vague project idea into a structured PRD through targeted conversation, then hands off to greenfield-init for full project planning. Use when a user has a rough app idea, wants to build something new, or needs to turn a concept into a documented scope before planning begins.
---

# PRD Creator

Turn a rough idea into a structured Product Requirements Document, then feed it directly into the greenfield planning pipeline.

## Pipeline

```
user prompt → [prd-creator] → PRD.md → [greenfield-init] → PROJECT_BLUEPRINT.md → [greenfield-decomposer] → phase research docs
```

## Behavior

### 1. Receive the Seed Prompt

Accept the user's basic description. It can be one sentence or a paragraph — whatever they have.

### 2. Round 1 — Core Discovery

Use `AskQuestion` to gather the essentials. Group related questions. Target 4–6 questions max:

- **Who are the users?** Are there multiple roles (e.g. admin vs. end user)?
- **What problem does this solve?** What pain point or workflow is being addressed?
- **What are the 3–5 core user flows?** (e.g. "user signs up → creates a project → invites teammates")
- **What are the main data entities?** (e.g. users, projects, tasks, reports)
- **Any hard constraints?** Third-party integrations, specific platforms, existing systems to connect to?
- **Scale expectation?** Internal tool / small team, or public-facing SaaS?

### 3. Round 2 — Boundary Setting

After Round 1, ask a focused follow-up to define scope edges:

- **What is explicitly out of scope for v1?** (Push back on scope creep early)
- **Any known non-functional requirements?** (Performance targets, accessibility, mobile-first, offline support)
- **Nice-to-haves vs. must-haves?** Flag anything that should be post-MVP

Use `AskQuestion` again if the answers will branch the PRD significantly. Otherwise, ask conversationally.

### 4. Draft the PRD

Using answers from both rounds, write a PRD following the template in [PRD_TEMPLATE.md](PRD_TEMPLATE.md).

Show the user a summary of the PRD and ask for confirmation or corrections before saving.

### 5. Save the PRD

Save the confirmed PRD to:

```
.agent-tasks/prd-drafts/[project-slug]-PRD.md
```

Where `[project-slug]` is a lowercase-hyphenated short name derived from the project title.

Create the directory if it doesn't exist.

### 6. Hand Off to greenfield-init

After saving, instruct the user:

> PRD saved. Next step: use the `greenfield-init` skill to turn this into a project blueprint.
>
> ```
> Use the greenfield-init skill with PRD: .agent-tasks/prd-drafts/[project-slug]-PRD.md
> ```

The user can trigger this immediately, or you can invoke it directly if they confirm they're ready to proceed.

## Quality Checklist

Before saving the PRD:

- [ ] All 5 sections of the template are populated
- [ ] At least 3 core user flows are defined
- [ ] Users/roles are clearly identified
- [ ] Out-of-scope items are explicitly listed
- [ ] No implementation decisions made (tech stack is greenfield-init's job)
- [ ] User has confirmed the draft

## Additional Resources

- For the PRD structure and template, see [PRD_TEMPLATE.md](PRD_TEMPLATE.md)
