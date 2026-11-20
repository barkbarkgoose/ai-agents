# Task: Implement Robust Skill Resolution

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 5

## Goal
Make skill resolution reliable by validating skill files and supporting explicit overrides.

## Acceptance Criteria
- [ ] Skill files are validated for existence before use.
- [ ] Support `SKILL_<name>` environment override pointing to a custom `SKILL.md`.
- [ ] If a skill is not found, fall back to a generic prompt rather than a broken reference.

## Context
Priority 2.2 from `.agent-info/audits/llmmux-audit.md`. The current skill resolution is naive and unvalidated. Prefer implementing this within the shared utilities module from Priority 1.2.

## Expected Outputs
- Updated skill resolution logic in `llmmux/create_agent.py` (and shared utils if used).
- Clear fallback behavior when skills are missing.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 2.2 and implement robust skill resolution. Validate skill files, add `SKILL_<name>` overrides, and fall back to a generic prompt if not found. Do not expand scope beyond the audit recommendation.
