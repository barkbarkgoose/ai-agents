# Default Technology Stack

> **Greenfield projects only.** This file defines the default stack for new projects scaffolded from scratch. For existing projects, inspect the project's dependency files to determine what's actually in use — do not apply these defaults.

Standard stack for all greenfield projects. Use these defaults unless project requirements specifically demand otherwise. When deviating, document the reason in the blueprint.

For specific versions of all technologies, see `VERSIONS.md` (at repo root).

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
| Database | SQLite | Default for local dev; swappable via Django ORM to PostgreSQL/MySQL/etc. |
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
| Utility | Tailwind CSS 4.x | Use framework classes over custom CSS — version in `VERSIONS.md` |
| Preprocessor | SASS/SCSS | For component-scoped styles |
| Naming | BEM | Block__Element--Modifier convention |

### Tailwind CSS 4.x Setup

Tailwind 4.x requires the `@tailwindcss/vite` plugin, NOT the PostCSS approach.

**Installation:**
```bash
npm install @tailwindcss/vite tailwindcss
```

**vite.config.ts:**
```typescript
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
})
```

**CSS import — use `@import "tailwindcss"` in your main CSS file (NOT SCSS `@use`):**
```css
@import "tailwindcss";
```

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

## Dev Server Configuration

| Service | Port | Notes |
|---------|------|-------|
| Backend (Django) | 8800 | Avoids port conflicts with common services |
| Frontend (Vite) | 5177 | Default Vite port, change if occupied |

### Frontend Environment

In `frontend/.env`:

```env
VITE_API_URL=http://localhost:8800
```

### Vite Proxy Configuration

When configuring vite.config.ts, proxy not just /api but also /admin and /static:

```typescript
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5177,
    proxy: {
      '/api': {
        target: 'http://localhost:8800',
        changeOrigin: true,
      },
      '/admin': {
        target: 'http://localhost:8800',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:8800',
        changeOrigin: true,
      },
    },
  },
})
```

### Django Settings for Static Files

In `config/settings/base.py`:

```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]  # Required for dev server
APPEND_SLASH = False  # Required — frontend calls /api/v1/auth/login without trailing slash
```

Create `backend/static/` directory (can be empty, Django populates it).

### Django Custom User Model

When using a custom User model with a required FK to Organization (or similar), auto-create the organization in `UserManager.create_superuser()`:

```python
def create_superuser(self, email, password, organization=None, **extra_fields):
    if organization is None:
        from apps.organizations.models import Organization
        organization = Organization.objects.create(
            name=f"Superuser Org ({email})"
        )
    # ... rest of method
```

### Required Dependencies

Always include these in `requirements.txt`:

```
django-filter>=25.0
requests>=2.31
```

Add project-specific dependencies as needed (e.g., `twilio` for SMS auth).

## When to Deviate

| Scenario | Deviation |
|----------|-----------|
| Real-time features | Add `django-channels` + WebSocket support |
| Background tasks | Add Celery + Redis |
| File uploads | Add `django-storages` + S3/cloud storage |
| Full-text search | Add Elasticsearch or SQLite FTS5 |
| GraphQL requirement | Replace DRF with Strawberry or Graphene |
| Mobile app | Add Django Ninja or keep DRF, consider React Native for frontend |
