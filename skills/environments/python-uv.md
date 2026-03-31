# Python Environment — uv

This spec covers working with Python backends using **uv** for environment and dependency management.

## Existing Projects — Detect First

Before applying any setup, inspect the project to determine what's already in use:

| Signal | Tool to use |
|--------|-------------|
| `pyproject.toml` + `poetry.lock` | Poetry — do not force uv |
| `pyproject.toml` + `uv.lock` | uv (pyproject-based) |
| `requirements.txt` + `.python-version` | uv with requirements.txt |
| `Pipfile` | Pipenv — adapt to what's there |

**Rule:** Always detect before scaffolding. Treat existing artifacts as the source of truth.

## Setup

When creating a new Python environment:

1. **Create virtualenv:**
   ```bash
   cd backend
   uv venv --python <version> venv
   ```

2. **Create a `.python-version` file:**
   ```bash
   echo "<version>" > .python-version
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Activate (for multi-step workflows):**
   ```bash
   source venv/bin/activate
   ```

## Running Commands

### With an activated virtualenv
```bash
source backend/venv/bin/activate
python manage.py migrate
python manage.py runserver
pytest
```

### Without activating (one-off commands)
```bash
uv run --project backend python manage.py migrate
uv run --project backend pytest
```

### From inside `backend/`
```bash
uv run python manage.py migrate
uv run pytest
uv run python manage.py runserver 0.0.0.0:8800
```

## Installing Packages

Add to `requirements.txt`, then install:
```bash
uv pip install -r requirements.txt
```

Or install directly and freeze:
```bash
uv pip install package-name
uv pip freeze > requirements.txt
```

## Agent Guidance

- **Always operate from `backend/`** — do not run Django commands from the project root
- **Use `uv run`** for one-off commands when virtualenv is not activated
- **Use `uv pip`** instead of `pip` for all package management
- **Never use system Python** — always use the `uv`-managed venv

## .gitignore (backend)

```
venv/
.venv/
__pycache__/
*.pyc
.env
```
