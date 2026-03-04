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
- Install and configure Tailwind CSS + SASS
- Configure CORS between frontend and backend
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

**Example items:**
- Create login/register views with forms
- Create dashboard view with project list
- Create task board view with columns
- Create shared navigation component

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
Scaffolding → Models → Endpoints → Components → Integration
```

Items within each category can often run in parallel.

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
