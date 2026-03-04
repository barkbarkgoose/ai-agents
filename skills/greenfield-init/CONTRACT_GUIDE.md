# API Contract Guide

Template and rules for the `API_CONTRACT.md` document produced alongside the blueprint.

## Purpose

The API contract is the shared truth between frontend and backend when built in parallel. Both streams build against it. The integration phase verifies compliance.

## Contract Template

```markdown
# API Contract: [Project Name]

**Version:** 1.0
**Base URL:** `/api/v1`
**Auth:** Bearer JWT (unless noted)

---

## Authentication

### POST /api/v1/auth/register/

**Auth required:** No

**Request:**
{
  "email": "string",
  "password": "string",
  "name": "string"
}

**Response (201):**
{
  "id": "number",
  "email": "string",
  "name": "string",
  "token": "string"
}

**Errors:**
- 400: { "email": ["This email is already registered."] }

---

### POST /api/v1/auth/login/

**Auth required:** No

**Request:**
{
  "email": "string",
  "password": "string"
}

**Response (200):**
{
  "access": "string (JWT)",
  "refresh": "string (JWT)"
}

**Errors:**
- 401: { "detail": "No active account found with the given credentials" }

---

## [Resource Group Name]

### GET /api/v1/resources/

**Auth required:** Yes

**Query params:**
- page (number, default: 1)
- page_size (number, default: 20)
- search (string, optional)
- ordering (string, optional)

**Response (200):**
{
  "count": "number",
  "next": "string | null",
  "previous": "string | null",
  "results": [
    {
      "id": "number",
      "name": "string",
      "created_at": "ISO 8601 datetime"
    }
  ]
}

### POST /api/v1/resources/

**Auth required:** Yes

**Request:**
{
  "name": "string",
  ...
}

**Response (201):**
{
  "id": "number",
  "name": "string",
  "created_at": "ISO 8601 datetime"
}

**Errors:**
- 400: { "name": ["This field is required."] }

### GET /api/v1/resources/:id/

**Auth required:** Yes

**Response (200):**
{
  "id": "number",
  "name": "string",
  "created_at": "ISO 8601 datetime",
  ...detail fields...
}

**Errors:**
- 404: { "detail": "Not found." }

### PATCH /api/v1/resources/:id/

**Auth required:** Yes

**Request:** (partial update)
{
  "name": "string"
}

**Response (200):**
{ ...updated resource... }

### DELETE /api/v1/resources/:id/

**Auth required:** Yes

**Response:** 204 No Content

**Errors:**
- 404: { "detail": "Not found." }
```

## Rules

### Completeness

- Every endpoint the frontend will call must be listed
- Include all query parameters, request bodies, and response shapes
- Include error responses with status codes and body format

### Types

Use these type annotations:

| Annotation | Meaning |
|------------|---------|
| `string` | Text value |
| `number` | Integer or float |
| `boolean` | true/false |
| `null` | Explicit null |
| `ISO 8601 datetime` | Date/timestamp string |
| `Type[]` | Array of Type |
| `string \| null` | Nullable string |

### Naming

- Resource names: plural, kebab-case in URLs (`/api/v1/task-boards/`)
- Field names: snake_case (matching Django serializer output)
- Frontend translates to camelCase via Axios interceptor or type mapping

### Pagination

All list endpoints use the standard DRF pagination format:

```json
{
  "count": 42,
  "next": "/api/v1/resources/?page=2",
  "previous": null,
  "results": []
}
```

### Versioning

- All URLs prefixed with `/api/v1/`
- Contract includes a version number
- Breaking changes require a version bump and updated contract
