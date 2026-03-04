# Python Environment — uv

All Python backends use **uv** for environment and dependency management. The Python version is defined in the `greenfield-init` skill's `VERSIONS.md` — always use the pinned version from there.

## Setup

When scaffolding the backend:

1. **Create virtualenv pinned to the Python version in `VERSIONS.md`:**
   ```bash
   cd backend
   uv venv --python <version> venv
   ```

2. **Create a `.python-version` file matching `VERSIONS.md`:**
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
