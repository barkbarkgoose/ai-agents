# Task: Add Provider CLI Detection

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 4

## Goal
Detect installed provider CLIs at startup and warn users when providers are missing or misconfigured.

## Acceptance Criteria
- [ ] Startup checks verify provider CLIs exist in PATH.
- [ ] Users receive clear warnings if a provider is unavailable.
- [ ] Installation guidance is provided in the warning message or help output.

## Context
Priority 2.1 from `.agent-info/audits/llmmux-audit.md`. The audit recommends provider detection for reliability. Prefer implementing this within the shared utilities module from Priority 1.2.

## Expected Outputs
- Provider detection logic in the shared utils module (or equivalent) and used by scripts.
- User-facing warnings when providers are missing.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 2.1 and add provider CLI detection at startup. Warn users when CLIs are missing and include installation guidance. Use the shared utilities module if available.
