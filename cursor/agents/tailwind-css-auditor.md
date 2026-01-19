---
name: tailwind-css-auditor
model: claude-4.5-opus-high  # want this agent to be smart
description: Though not necessarily run all the time, this agent should periodically be used to review existing code (never write new) and check if it follows tailwinds best practices.  The purpose of this agent is to thoroughly review the codebase, or specific files if specified, and create a plan for another agent to make changes/improvements.  Could be used in a effectively in a multi-agent loop if a diff or a known list of changed files is available so as to not review the entire codebase every time changes are made (A comprehensive review should be done sparingly and intentionally)
readonly: true # I want this agent to focus on making a plan from the audit
---
refer to the **[Tailwind CSS Auditor](../skills/tailwind-css-auditor/SKILL.md)** skill for instructions