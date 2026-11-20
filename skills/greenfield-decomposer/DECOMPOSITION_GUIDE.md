# Decomposition Guide

Rules and patterns for breaking blueprint phases into task-creator-ready work items.

## Work Item Categories

### Scaffolding

Project setup, directory creation, configuration files, dependency installation.

**Pattern:**
1. Create project structure
2. Install dependencies
3. Configure settings/environment
4. **Validate:** Dev server starts

**Example items:**
- Create Django project with split settings
- Create Vue 3 project with TypeScript + Vite
- Install and configure Tailwind CSS 4.x + SASS
- Configure CORS between frontend and backend
- Configure Vite proxy for /api, /admin, and /static
- Configure Django static files (STATICFILES_DIRS, static directory)
- Configure `APPEND_SLASH = False` in Django settings
- Set up environment files (`.env`)

### Models / Data Layer

Database models, migrations, admin configuration, seed data.

**Pattern:**
1. Define models
2. Run migrations
3. Register in admin
4. Create seed data (optional)
5. **Validate:** Tables exist, admin shows data

**Sizing rule:** Group related models that reference each other into one item. Split unrelated model groups into separate items.

**Example items:**
- Create User model with custom fields + migration
- Create Team and Membership models + migration
- Create Project and Task models + migration
- Register all models in Django admin

### API Endpoints

Serializers, views, URL routing, permissions.

**Pattern:**
1. Create serializer
2. Create viewset/view
3. Add URL route
4. Set permissions
5. **Validate:** Endpoint returns expected response

**Sizing rule:** One item per resource (all CRUD operations for that resource). Split only if a resource has complex custom actions.

**Example items:**
- Create User registration and login endpoints
- Create Team CRUD endpoints with membership
- Create Project CRUD with team scoping
- Create Task CRUD with assignment and status

### Frontend Components

Vue components, views, routing, state management.

**Pattern:**
1. Create component/view
2. Add route (if view)
3. Wire up Pinia store (if needed)
4. **Validate:** Component renders, interactions work

**Sizing rule:** One item per view/page. Shared components extracted as separate items only if used across multiple views.

**Design system integration:** Every frontend component should use BEM classes from the `@layer components` section (see `DEFAULT_STACK.md`) instead of inline Tailwind utility clusters. Use theme tokens (primary, secondary) instead of hardcoded colors (blue-600, gray-500).

**Example items:**
- Create login/register views with forms (use .form-input, .btn--primary, .alert--error)
- Create dashboard view with project list
- Create task board view with columns
- Create shared navigation component (use .nav-link, .nav-link--active, .nav-link--inactive)

### Design System / UI Architecture

Establishing the component layer, theme tokens, and BEM architecture.

**Pattern:**
1. Set up @layer components with BEM classes
2. Configure tailwind.config.js with theme tokens
3. Create CSS custom properties for colors
4. Document component usage patterns

**Sizing rule:** One item per concern (forms, buttons, alerts, navigation). Include in scaffolding phase.

**Example items:**
- Set up form input BEM classes (.form-input, .form-input--first, .form-input--last, .form-input--error)
- Set up button BEM classes (.btn, .btn--primary, .btn--secondary, .btn--disabled)
- Set up alert BEM classes (.alert, .alert--error, .alert--success, .alert__text, .alert__title)
- Set up navigation BEM classes (.nav-link, .nav-link--active, .nav-link--inactive)

### Integration

Connecting frontend to backend, replacing mock/placeholder data with API calls.

**Pattern:**
1. Create/update API service module (Axios)
2. Replace mock data with API calls
3. Handle loading/error states
4. **Validate:** Data flows end-to-end, matches API contract

**Sizing rule:** One item per feature area (auth integration, project integration, etc.)

**Example items:**
- Wire up auth flow (register, login, token storage, interceptors)
- Connect project list view to project API
- Connect task board to task API with real-time updates

### Configuration / DevOps

Environment setup, Docker, CI/CD, deployment config.

**Pattern:**
1. Create configuration files
2. Test locally
3. **Validate:** Process runs successfully

**Example items:**
- Create Docker Compose for local development
- Configure CI pipeline for linting and tests
- Set up production deployment config

## Ordering Within a Phase

### Dependency Flow

```
Scaffolding → Design System → Models → Endpoints → Components → Integration
```

Items within each category can often run in parallel. Design System items (if not done in Scaffolding) should precede Frontend Components.

### Dependency Declaration

When writing work items, explicitly state dependencies:

- **"Depends on: none"** — Can start immediately
- **"Depends on: User model item"** — Needs that item complete first
- **"Parallel with: Frontend scaffolding"** — Can run alongside

### Frontend / Backend Parallelism

When a phase includes both frontend and backend work:

1. Backend builds the real endpoints
2. Frontend builds against the API contract with mock data or placeholder services
3. Integration items connect them — these depend on both sides completing
4. The API contract is the shared reference for both streams

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Build the entire auth system" | Split: models → endpoints → frontend views → integration |
| "Set up the database" | Specify: which models, which migrations, verify via admin |
| No validation gate | Add one from `VALIDATION_GATES.md` |
| Mixing frontend and backend in one item | Separate into parallel items with contract reference |
| Two items that modify the same files | Make them sequential, or merge into one item |
| Item requires multiple sessions | Break it down further — it's too big |
