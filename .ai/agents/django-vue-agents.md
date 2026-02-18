---
name: django-vue-agents
description: Use this skill when coordinating tasks for work across multiple specialized agents needing vue3, django, or tailwinds
model: sonnet
color: red
---

## EXECUTION

The available agents are to be used based on the task that is being worked on, it is up to the orchestrator to determine which.

## AGENTS AND SKILLS

Within the project, first look for a `.ai` directory for any agents, skills, or commands referenced.  If not present: then search in the typical locations

## AVAILABLE AGENTS
- **django-backend-dev**: Backend API, models, serializers, permissions, business logic
- **vue3-typescript**: Frontend components, composables, state management, API integration
- **tailwind-bem-stylist**: Styling new components, refactoring Tailwind utilities into BEM classes
- **tailwind-auditor**: Comprehensive Tailwind CSS audits and consolidation analysis


## DEFAULT AGENT ORDER
1. django-backend-dev
2. vue3-typescript
3. tailwind-bem-stylist

**Deviations allowed:**
- Frontend-only task → skip django-backend-dev
- Backend-only task → skip frontend and tailwind agents
- Styling-only task → only tailwind-bem-stylist