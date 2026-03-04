# Blueprint Guide

Template and rules for the `PROJECT_BLUEPRINT.md` document produced by greenfield-init.

## Blueprint Template

```markdown
# Project Blueprint: [Project Name]

**Created:** [YYYY-MM-DD]
**Status:** Draft | Approved
**Stack:** [Backend] / [Frontend] / [Database]

---

## 1. Overview

[2-3 paragraph description of what the project is, who it's for, and the core problem it solves.]

## 2. Requirements

### Functional Requirements

- [FR-01] [Requirement description]
- [FR-02] ...

### Non-Functional Requirements

- [NFR-01] [Requirement description]
- [NFR-02] ...

### Assumptions

- [Things assumed but not explicitly stated by the user]

### Out of Scope

- [Things explicitly excluded from this build]

## 3. Tech Stack

Versions for all technologies are defined in `VERSIONS.md` — do not hardcode versions here.

| Layer | Choice | Deviation from default? |
|-------|--------|------------------------|
| Backend | Python + Django + DRF | No |
| Frontend | Node.js LTS + Vue 3 + TypeScript | No |
| State | Pinia | No |
| Styling | Tailwind CSS + SASS/BEM | No |
| Database | PostgreSQL | No |
| Auth | simplejwt | No |

[Note any deviations and justify them here.]

## 4. Data Model

### Entities

#### [Entity Name]

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField | max_length=255 |
| ... | ... | ... |

**Relationships:**
- [FK/M2M description]

#### [Entity Name]
...

### Entity Relationship Summary

[Text description showing how entities relate. Keep it simple — focus on FKs and M2M.]

## 5. Development Phases

### Phase 1: [Name]

- **Goal:** [What this accomplishes]
- **Depends on:** None
- **Parallel streams:** [Yes/No — if yes, which]
- **Validation gate:** [Executable check that proves this phase works]
- **Scope:**
  - [Bullet list of what gets built in this phase]

### Phase 2: [Name]
...

### Phase N: [Name]
...

## 6. API Contract Reference

See: `API_CONTRACT.md`

[Omit this section if no parallel streams exist.]

## 7. Risks & Open Questions

- [Risk or question that may affect the plan]
- [Decisions deferred and when they need resolution]
```

## Phase Design Rules

### 1. Scaffolding First

First phase is always project scaffolding — both projects created, dependencies installed, dev servers confirmed running. This is the cheapest phase and catches environment issues immediately.

`backend/` and `frontend/` are always treated as independent services with separate dependency management. Even when running as a monolith, they must never share a virtualenv, node_modules, or `.env`.

**Backend scaffolding includes:**
- `backend/` directory with its own `venv/` created via `uv venv --python <version>` (see `VERSIONS.md`)
- `.python-version` file set to the pinned Python version from `VERSIONS.md`
- Dependencies installed via `uv pip install -r requirements.txt`
- `backend/.env` configured
- Django dev server running at `localhost:8000`

**Frontend scaffolding includes:**
- `frontend/` directory with its own `node_modules/` via `npm install`
- `.nvmrc` set to the Node LTS version from `VERSIONS.md`
- `frontend/.env` configured
- Vite dev server running at `localhost:5173`

### 2. Every Phase Produces Something Runnable

Not "write 12 models", but "write User and Team models, run migrations, confirm tables exist via admin". The validation gate enforces this.

### 3. Phases Build On Each Other

Phase N should never invalidate work from Phase N-1. Each phase extends the working system.

### 4. Max 5-7 Phases for an MVP

If you have more, the scope is too large. Either trim features or combine related phases.

### 5. Core Features Before Polish

Error handling, loading states, and edge cases come after the happy path works end-to-end.

## Validation Gate Rules

Every validation gate must be **executable**, not subjective:

| Good | Bad |
|------|-----|
| "Run `uv run python manage.py migrate` — no errors" | "Database is set up" |
| "POST to `/api/auth/login/` returns a JWT token" | "Auth works" |
| "Vue dev server starts, home route renders" | "Frontend is done" |
| "Task board shows seeded tasks from API" | "Feature looks good" |

## Requirements Rules

- Use IDs (FR-01, NFR-01) so phases and tasks can reference them
- Every functional requirement must map to at least one phase
- Non-functional requirements apply across phases — note where they're relevant

## Data Model Rules

- Only define core entities needed for the MVP
- Include field types and constraints (unique, nullable, etc.)
- Show relationships explicitly (FK, M2M)
- This informs both Django models and TypeScript types — keep them in sync
