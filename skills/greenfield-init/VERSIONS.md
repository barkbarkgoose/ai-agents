# Version Reference

> **Greenfield projects only.** This file defines canonical versions for new projects being scaffolded from scratch. For existing projects, always inspect the project's own dependency files (`package.json`, `requirements.txt`, `pyproject.toml`, `uv.lock`, etc.) to determine the actual stack and versions in use. Never impose versions from this file onto an existing codebase.

## Python/Django Backend


| Technology                    | Version       | Policy        | Notes                       |
| ----------------------------- | ------------- | ------------- | --------------------------- |
| Python                        | 3.13          | Pinned        | Use `uv venv --python 3.13` |
| Django                        | 5.2           | Pinned        | LTS release                 |
| Django REST Framework         | latest stable | LTS preferred |                             |
| djangorestframework-simplejwt | latest stable | —             |                             |
| django-cors-headers           | latest stable | —             |                             |
| django-environ                | latest stable | —             |                             |
| pytest                        | latest stable | —             |                             |
| pytest-django                 | latest stable | —             |                             |


## Vue Frontend (typescript for greenfield, otherwise based on existing stack)


| Technology | Version           | Policy        | Notes                                                   |
| ---------- | ----------------- | ------------- | ------------------------------------------------------- |
| Node.js    | 24.x LTS          | LTS           | Use the current LTS; check nodejs.org/en/about/releases |
| Vue        | 3.x latest stable | Latest stable |                                                         |
| TypeScript | 5.x latest stable | Latest stable | Strict mode                                             |
| Vite       | latest stable     | —             |                                                         |
| Pinia      | latest stable     | —             |                                                         |
| Vue Router | 4.x               | —             |                                                         |
| Axios      | latest stable     | —             |                                                         |
| Vitest     | latest stable     | —             |                                                         |


## Styling


| Technology   | Version       | Policy          | Notes |
| ------------ | ------------- | --------------- | ----- |
| Tailwind CSS | 4.x           | Pinned to major |       |
| SASS         | latest stable | —               |       |


## Infrastructure


| Technology | Version | Policy        | Notes                           |
| ---------- | ------- | ------------- | ------------------------------- |
| PostgreSQL | 16.x    | LTS           | Current stable major            |
| uv         | latest  | Always latest | Self-updates; no pinning needed |


---

## Policy Definitions


| Policy            | Meaning                                                                                                          |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Pinned**        | Use the exact major.minor specified. Do not upgrade without explicit decision.                                   |
| **LTS**           | Use the current LTS release. Web search to confirm. Upgrade when new LTS is available.                           |
| **Latest stable** | Use whatever the latest stable release is at project scaffold time. Pin in `requirements.txt` or `package.json`. |


---

## Checking for Current LTS

When scaffolding a new project, verify LTS status for anything marked "LTS":

- **Node.js:** [nodejs.org/en/about/releases](https://nodejs.org/en/about/releases)
- **PostgreSQL:** [postgresql.org/support/versioning](https://www.postgresql.org/support/versioning/)
- **Django:** [djangoproject.com/download](https://www.djangoproject.com/download/) — look for rows marked "LTS"

