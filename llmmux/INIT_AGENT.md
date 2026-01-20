# INIT_AGENT

Global instructions for llmmux sub-agents:

- Task files live in `.agent-info/tasks/pending/`. Read the referenced task file first and treat it as the source of truth.
- When a task is fully satisfied, move its task file to `.agent-info/tasks/done/` and mention the move in your response.
- Do not create new task files unless the task explicitly asks.
- Keep responses concise and include relevant file paths.
- Session state and artifacts live under `~/.llmmux/state/<session-id>/` and `~/.llmmux/artifacts/<session-id>/`.
- If you only know the tmux session name, look up its session id in `~/.llmmux/state/session_index.json`.
- If you need session context (handoff, run_state, tasks), look in `~/.llmmux/state/<session-id>/`.
- Avoid concurrent edits: do not work the same task file from multiple tmux sessions at once.
- After completing a task or stage, update your agent state file with:
  - `status`: running | completed | blocked | failed
  - `last_action`: short one-line summary of what you just did
  - `last_run_ts`: ISO 8601 timestamp in UTC (e.g., 2026-01-20T00:42:30+00:00)
