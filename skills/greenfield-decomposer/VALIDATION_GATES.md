# Validation Gates

Standard validation patterns for each type of work. Every task must include at least one gate.

## Principle

A validation gate answers: **"Is this working?"** — not "is this done?"

"Done" is subjective. "Working" is provable.

## Gate Patterns

### Environment / Scaffolding

| Gate | How to verify |
|------|---------------|
| Django project created | `python manage.py check` exits 0 |
| Django dev server starts | `python manage.py runserver` — no errors, serves response |
| Vue project created | `npm run dev` — dev server starts, page loads |
| Dependencies installed | No import errors in either project |
| CORS configured | Frontend can reach backend API without CORS errors |
| Environment files work | `.env` loaded, settings reflect values |

### Database / Models

| Gate | How to verify |
|------|---------------|
| Models defined | `python manage.py makemigrations` — no errors |
| Migrations applied | `python manage.py migrate` — no errors |
| Tables exist | Model visible and browsable in Django admin |
| Seed data loaded | Records visible in Django admin or shell query |
| Relationships work | Related objects queryable (e.g., `team.members.all()`) |

### API Endpoints

| Gate | How to verify |
|------|---------------|
| Endpoint exists | `curl` or API client returns non-404 response |
| CRUD works | POST creates, GET retrieves, PATCH updates, DELETE removes |
| Auth enforced | Unauthenticated request returns 401 |
| Permissions work | Wrong-role request returns 403 |
| Validation works | Bad input returns 400 with field errors |
| Pagination works | List endpoint returns `count`, `results`, `next`, `previous` |

### Frontend Components

| Gate | How to verify |
|------|---------------|
| Component renders | Navigate to route, component visible in browser |
| Form submits | Fill form, submit, observe state change or network request |
| Navigation works | Click link/button, correct view renders |
| State updates | Pinia action triggers visible UI change |
| Responsive layout | Component doesn't break at common breakpoints |

### Integration

| Gate | How to verify |
|------|---------------|
| Auth flow end-to-end | Register → login → token stored → authenticated request succeeds |
| Data flow end-to-end | Create via frontend → visible in backend admin (and reverse) |
| Error handling | API error → user sees meaningful message in UI |
| Contract compliance | All endpoint responses match `API_CONTRACT.md` shapes |

### General

| Gate | How to verify |
|------|---------------|
| No lint errors | Linter returns clean |
| No type errors | TypeScript compiles without errors |
| Tests pass | `pytest` / `npm run test` — all green |

## Writing Custom Gates

If the standard gates don't cover a case, follow these rules:

1. **Make it a command or action** — Something the agent can execute
2. **Make the result binary** — Pass or fail, no "looks okay"
3. **Include the expected output** — "Returns 200 with `{ token: string }`" not just "returns a response"

### Template

```markdown
## Validation
- [ ] [Action to perform]
  - Expected: [Specific expected result]
  - Failure: [What it looks like if broken]
```

### Examples

```markdown
## Validation
- [ ] POST /api/v1/auth/login/ with valid credentials
  - Expected: 200 with { "access": "jwt_string", "refresh": "jwt_string" }
  - Failure: 401 or 500 response

- [ ] Navigate to /dashboard after login
  - Expected: Dashboard view renders with user name in nav
  - Failure: Redirect to login or blank page
```
