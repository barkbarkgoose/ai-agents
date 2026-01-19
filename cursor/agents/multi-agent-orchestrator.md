---
# --- my usual model options ---
# claude-4.5-sonnet: This is the daily driver, the one that is smart but not "too" smart
# claude-4.5-haiku: I use this when I want the agent to follow instructions and not ask questions
# claude-4.5-opus-high: This is when I want the agent to have autonomy and to figure things out as it goes
# grok-code-fast-1: A ferrari with the brakes taken off (because if go fast why slow down?)
# composer-1
# fast - cursor chooses whatever it deems (fast)
# inherit - will spin off subagent with the model from the chat or agent that invoked it
name: multi-agent-orchestrator
model: claude-4.5-haiku  # I consider this a "dumb" agent, it is just here to build a to-do list and double check that the other agents are working
description: Whenver asked for something that is likely to require multiple steps in development, or more than just a few files or what could be handled by a basic planning mode: then always use this agent. Current setup: django (db agnostic), vue, tailwinds
readonly: true # makes sure this agent runs with restricted write permissions
is_background: false
# NOTE - `readonly` and `is_background` are cursor specific.  `tools` and `color` would be unique to claude.
---
refer to the multi-agent-orchestrator skill for instructions
refer to the **[Multi Agent Orchestrator](../skills/multi-agent-orchestrator/SKILL.md)** for instructions