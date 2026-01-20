# Task: Extract Shared Utilities Module

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 2

## Goal
Eliminate duplicated configuration, provider handling, and prompting logic by extracting shared utilities into a single module used by both scripts.

## Acceptance Criteria
- [ ] A shared module (e.g., `llmmux_core.py` or `utils.py`) is created under `~/.llmmux/`.
- [ ] Provider command generation, configuration loading, session/provider resolution, and interactive prompting are moved into the shared module.
- [ ] `orchestrator.py` and `create_agent.py` import and use the shared utilities.
- [ ] Duplicate logic is removed from both scripts without changing behavior.

## Context
Priority 1.2 from `.agent-info/audits/llmmux-audit.md`. The audit calls out duplicated provider/config logic in both scripts. This task should refactor only the shared logic described in the audit, with no new functionality. No dependencies.

## Expected Outputs
- New shared utilities module under `~/.llmmux/` (or equivalent location used by llmmux).
- Refactored `llmmux/orchestrator.py` and `llmmux/create_agent.py` using the shared module.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 1.2 and extract the shared configuration/provider/prompting logic into a single module. Update `orchestrator.py` and `create_agent.py` to use it, removing duplicates without changing behavior.
