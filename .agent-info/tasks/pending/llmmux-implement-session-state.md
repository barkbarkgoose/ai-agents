# Task: Implement Session State Initialization

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 1

## Goal
Implement session state file generation in the llmmux orchestrator so the documented state management exists in practice.

## Acceptance Criteria
- [ ] `initialize_session_state()` (or equivalent) is invoked during orchestrator session launch.
- [ ] `handoff.md`, `run_state.json`, and `tasks.json` are created for each session.
- [ ] JSON schemas are defined and used to validate the state files (via `jsonschema`).
- [ ] State files are created in the documented session directory structure.

## Context
Priority 1.1 from `.agent-info/audits/llmmux-audit.md`. The audit notes state management is documented but not implemented. Implement only what is recommended in the audit; do not introduce new behaviors. No dependencies.

## Expected Outputs
- Updates in `llmmux/orchestrator.py` to initialize state files.
- New or updated schema definitions for `run_state.json` and `tasks.json`.
- Session state files created on orchestrator startup.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 1.1 and implement session state file generation as recommended. Ensure `handoff.md`, `run_state.json`, and `tasks.json` are created and validated at session initialization. Do not add new features beyond the audit.
