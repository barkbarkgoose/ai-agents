# Task: Propose Handoff Auto-Scan Scripts

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 4

## Goal
Draft a short proposal for helper scripts or orchestrator hooks that would automate handoff scanning and tasks.json generation.

## Acceptance Criteria
- [ ] Suggest script(s) or hook points with brief purpose and inputs/outputs
- [ ] Include where each script would live in the repo and how it would be invoked
- [ ] Keep scope limited to the handoff auto-scan described in INIT_ORCHESTRATOR.md

## Context
We want future automation for: scanning `.agent-info/tasks/`, `.agent-info/audits/`, and `.agent-info/patches/` to populate `tasks.json`, `run_state.json`, and `handoff.md`. This task is only for proposing scripts, not implementing them.

## Expected Outputs
- A short proposal document, e.g., `.agent-info/reports/handoff-auto-scan-proposal.md`

## Agent Prompt
Propose helper scripts or orchestrator hook(s) to automate handoff auto-scan. Keep it concise and actionable. Include suggested filenames/locations, inputs, outputs, and invocation flow. Do not implement code.
