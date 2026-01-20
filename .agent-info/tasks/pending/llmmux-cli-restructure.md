# Task: Restructure CLI into Subcommands

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 8

## Goal
Consolidate the two scripts into a single `llmmux` CLI with subcommands for orchestrator, agent creation, and session management.

## Acceptance Criteria
- [ ] A single `llmmux` entrypoint supports subcommands similar to the audit example.
- [ ] Existing functionality from `orchestrator.py` and `create_agent.py` is preserved under subcommands.
- [ ] Session listing/attach commands are included as described in the audit.

## Context
Priority 3.2 from `.agent-info/audits/llmmux-audit.md`. This is a medium refactor intended to reduce cognitive load. Keep to the subcommands described in the audit.

## Expected Outputs
- New consolidated CLI entrypoint and updated script structure.
- Updated documentation for new CLI usage.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 3.2 and refactor to a single `llmmux` CLI with subcommands (orchestrator, agent create, session list/attach). Preserve existing behavior and keep scope limited to the audit recommendation.
