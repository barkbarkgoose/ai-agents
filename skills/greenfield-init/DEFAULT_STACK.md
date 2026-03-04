# Default Technology Stack

Standard stack for all greenfield projects. Use these defaults unless project requirements specifically demand otherwise. When deviating, document the reason in the blueprint.

For specific versions of all technologies, see `VERSIONS.md` in this folder.

## Project Structure Philosophy

All projects are structured as **independent services from day one**, even when developed as a monolith:
- `backend/` and `frontend/` are separate directories with their own dependency management, virtualenvs, and `.env` files
- Backend uses Python/uv; frontend uses Node/npm — never share a single environment
- This ensures the project can be split into separate repos or deployed independently without restructuring

## Backend

For versions, see `VERSIONS.md`.

| Layer | Technology | Notes |
|-------|------------|-------|
| Language | Python | Pinned — see `VERSIONS.md` |
| Framework | Django | LTS release — see `VERSIONS.md` |
| API | Django REST Framework (DRF) | Serializers, viewsets, permissions |
| Auth | djangorestframework-simplejwt | JWT tokens for API auth |
| Database | PostgreSQL | Default; swappable via Django ORM |
| CORS | django-cors-headers | Required for separate frontend |
| Environment | django-environ | `.env` file support |
| Testing | pytest + pytest-django | Over Django's built-in test runner |

### Backend Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── .python-version        # pins Python version for uv — see VERSIONS.md
├── venv/                  # uv-managed virtualenv (gitignored)
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── [app_name]/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       └── tests/
└── .env
```

## Frontend

For versions, see `VERSIONS.md`.

| Layer | Technology | Notes |
|-------|------------|-------|
| Runtime | Node.js LTS | LTS release — see `VERSIONS.md` |
| Framework | Vue 3 | Composition API, `<script setup>` |
| Language | TypeScript | Strict mode |
| Build | Vite | Default Vue scaffolding tool |
| State | Pinia | Official Vue state management |
| Routing | Vue Router 4 | Standard routing |
| HTTP | Axios | API client with interceptors |
| Testing | Vitest | Vite-native test runner |

### Frontend Project Structure

```
frontend/
├── package.json
├── .nvmrc                 # pins Node LTS version — see VERSIONS.md
├── vite.config.ts
├── tsconfig.json
├── index.html
├── public/
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   └── [store].ts
│   ├── views/
│   │   └── [View].vue
│   ├── components/
│   │   └── [Component].vue
│   ├── composables/
│   │   └── use[Feature].ts
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── [entity].ts
│   └── assets/
│       └── styles/
│           ├── main.scss
│           └── _variables.scss
└── .env
```

## Styling

For versions, see `VERSIONS.md`.

| Layer | Technology | Notes |
|-------|------------|-------|
| Utility | Tailwind CSS | Use framework classes over custom CSS — version in `VERSIONS.md` |
| Preprocessor | SASS/SCSS | For component-scoped styles |
| Naming | BEM | Block__Element--Modifier convention |

### Styling Rules

- Use Tailwind utility classes whenever possible over custom SCSS
- Component `<style>` blocks use `lang="scss"` and `scoped`
- Nest all SASS under the root component class for scoping
- Use full class names for each BEM selector (no `&` nesting except pseudo-selectors and element selectors)

## API Conventions

| Convention | Standard |
|------------|----------|
| Format | REST (JSON) |
| Auth header | `Authorization: Bearer <jwt_token>` |
| Pagination | `?page=1&page_size=20` → `{ results: [], count: N }` |
| Errors | `{ detail: "message" }` for single, `{ field: ["errors"] }` for validation |
| Status codes | 200 ok, 201 created, 204 deleted, 400 validation, 401 unauth, 403 forbidden, 404 not found |
| URL style | `/api/v1/resource-name/` — plural, kebab-case, trailing slash |

## Dev Environment

| Tool | Purpose |
|------|---------|
| Git | Version control, feature branches |
| uv | Python package and virtualenv management — see `environments` skill (`python-uv.md`) |
| `.env` files | Environment-specific config (never committed) |
| Docker (optional) | Only when service dependencies require it (Redis, Celery, etc.) |

## When to Deviate

| Scenario | Deviation |
|----------|-----------|
| Real-time features | Add `django-channels` + WebSocket support |
| Background tasks | Add Celery + Redis |
| File uploads | Add `django-storages` + S3/cloud storage |
| Full-text search | Add Elasticsearch or PostgreSQL full-text search |
| GraphQL requirement | Replace DRF with Strawberry or Graphene |
| Mobile app | Add Django Ninja or keep DRF, consider React Native for frontend |
