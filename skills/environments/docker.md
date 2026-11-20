# Docker Environment

Two modes: **service dependencies only** (default) and **full app containerization** (optional, for deployment or when the project explicitly requires it).

---

## Service Dependencies (Default)

Use Docker Compose to run backing services locally — Postgres, Redis, etc. The Django and Vue dev servers still run natively on the host.

### docker-compose.yml (service deps only)

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
      POSTGRES_USER: ${POSTGRES_USER:-appuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-apppassword}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:                          # only include if project uses Celery/caching
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Workflow

```bash
docker compose up -d        # start services in background
docker compose down         # stop services
docker compose down -v      # stop and remove volumes (wipe DB)
```

### backend/.env (matching compose)

```
DATABASE_URL=postgresql://appuser:apppassword@localhost:5432/appdb
REDIS_URL=redis://localhost:6379/0   # if redis is included
```

### Agent Guidance (service deps mode)

- Start compose services before running migrations or the dev server
- The Django app connects to `localhost` ports exposed by compose
- Never run `manage.py` inside a container in this mode — use `uv run` on the host
- Include `postgres_data` volume in `.gitignore` if bind-mounted to a local path

---

## Full App Containerization (Optional)

Use when the blueprint explicitly calls for a fully containerized setup, or for production deployment parity.

### docker-compose.yml (full app)

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
      POSTGRES_USER: ${POSTGRES_USER:-appuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-apppassword}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - db
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### backend/Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .
```

### frontend/Dockerfile

```dockerfile
FROM node:24-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
```

### Agent Guidance (full app mode)

- Run migrations inside the container: `docker compose exec backend python manage.py migrate`
- Access Django shell: `docker compose exec backend python manage.py shell`
- Rebuild after dependency changes: `docker compose build backend` or `docker compose build frontend`
- Use `depends_on` to control startup order; add `healthcheck` for production
- Never use `uv venv` inside the container — install with `uv pip --system`

---

## .gitignore additions

```
.docker/
postgres_data/
```
