# Task: Create Single Bootstrap Command

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 7

## Goal
Replace the multi-step setup flow with a single bootstrap command as recommended by the audit.

## Acceptance Criteria
- [ ] A single command (e.g., `llmmux-init`) performs dependency checks, directory creation, install to `~/.llmmux`, and venv setup.
- [ ] `sync.sh` is removed or deprecated in favor of the new bootstrap command.
- [ ] Documentation is updated to reference the new bootstrap workflow.

## Context
Priority 3.1 from `.agent-info/audits/llmmux-audit.md`. The audit recommends simplifying setup to a single command. Keep scope limited to the bootstrap flow.

## Expected Outputs
- New bootstrap command/script.
- Removal or deprecation of `sync.sh` usage in docs.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 3.1 and implement a single bootstrap command (e.g., `llmmux-init`) that replaces the multi-step setup. Update docs accordingly and deprecate/remove `sync.sh` usage.
