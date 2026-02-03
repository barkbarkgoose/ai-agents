# Task: Add Automated Log Capture

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 6

## Goal
Capture agent output to persistent log files for later inspection.

## Acceptance Criteria
- [ ] Agent commands are wrapped to pipe output to `~/.llmmux/logs/<session>/<agent>.log`.
- [ ] Log paths are configurable.
- [ ] Logging works without breaking existing agent execution.

## Context
Priority 2.3 from `.agent-info/audits/llmmux-audit.md`. The audit notes logging is documented but not implemented. Implement only the log capture functionality described.

## Expected Outputs
- Wrapper script or command changes that pipe agent output to log files.
- Configurable log path support in relevant scripts.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 2.3 and add automated log capture for agents. Pipe output to `~/.llmmux/logs/<session>/<agent>.log` with configurable paths, without changing agent behavior otherwise.
