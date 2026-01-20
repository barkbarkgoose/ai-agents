# Task: Add Tmux Convenience Wrappers

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 9

## Goal
Reduce direct tmux dependency by adding convenience wrapper commands for attach and agent listing.

## Acceptance Criteria
- [ ] `llmmux attach [session]` (or equivalent) is implemented to replace manual `tmux attach` usage.
- [ ] `llmmux list-agents` (or equivalent) shows agent windows without requiring tmux knowledge.
- [ ] Documentation references wrappers rather than relying on a tmux cheatsheet.

## Context
Priority 3.3 from `.agent-info/audits/llmmux-audit.md`. If the CLI restructure (Priority 3.2) is implemented, integrate these as subcommands; otherwise implement as standalone wrappers.

## Expected Outputs
- Wrapper commands for attach and list-agents.
- Documentation updated to prefer wrapper commands.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 3.3 and add tmux convenience wrappers for attaching to sessions and listing agents. Integrate with the `llmmux` CLI if available; otherwise add standalone wrappers. Keep scope to the audit recommendation.
