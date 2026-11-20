# Task: Implement Agent Status Tracking

**Target Agent:** codex-generic
**Created:** 2026-01-20
**Priority:** 3

## Goal
Add agent status tracking and optional waiting behavior so the orchestrator can monitor agent lifecycle.

## Acceptance Criteria
- [ ] Implement `get_agent_status(session_name, agent_name)` using tmux state.
- [ ] `run_state.json` is updated when agents complete (polling or wrapper-based update).
- [ ] `create_agent.py` supports a `--wait` flag to block until an agent completes.

## Context
Priority 1.3 from `.agent-info/audits/llmmux-audit.md`. The audit notes no agent lifecycle monitoring exists. This should build on the state files introduced in Priority 1.1.

## Expected Outputs
- Updates to `llmmux/orchestrator.py` and/or `llmmux/create_agent.py` for status tracking.
- Status updates written into `run_state.json`.
- `--wait` flag behavior in `create_agent.py`.

## Orchestrator Suggestions
- Consider writing initial agent status into `run_state.json` at launch, not only on completion.
- For `--wait`, use `tmux wait-for` or polling `tmux list-panes -F` with a timeout to detect process exit.
- Store `last_run_ts` and `exit_code` in the agent entry when a pane finishes.
- Add a lightweight schema version in `run_state.json` to help future migrations.

## Agent Prompt
Read `.agent-info/audits/llmmux-audit.md` Priority 1.3 and implement agent status tracking plus a `--wait` flag in `create_agent.py`. Use tmux to determine status and update `run_state.json` on completion. Do not add features beyond the audit recommendation.
