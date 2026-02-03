# Task: Align INIT_ORCHESTRATOR Documentation

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 11

## Goal
Adjust `INIT_ORCHESTRATOR.md` so it no longer over-promises unimplemented state management and coordination features.

## Acceptance Criteria
- [ ] `INIT_ORCHESTRATOR.md` is updated to reflect implemented capabilities.
- [ ] If features remain unimplemented, documentation is toned down or marked as design/spec only.
- [ ] Documentation changes align strictly with audit findings.

## Context
Priority 4.2 from `.agent-info/audits/llmmux-audit.md`. This should be done after the team decides whether Priority 1.1 is implemented; the doc must match reality.

## Expected Outputs
- Updated `INIT_ORCHESTRATOR.md` with aligned expectations or split design/spec sections.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 4.2 and update `INIT_ORCHESTRATOR.md` to align with actual implementation status. Tone down over-promises or mark sections as design spec where appropriate, based only on the audit.
