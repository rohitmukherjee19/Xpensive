# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

Spendly is a Flask-based expense-tracking web app. It is structured as a teaching project where students build features step by step (Steps 1–9). The app lets users register, log in, and manage personal expenses by category. The UI targets Indian users (amounts in ₹). At any point, only some routes are fully functional — stub routes intentionally return placeholder strings until a student implements them.

## Architecture

All routes live in a single `app.py`. There are no blueprints. The database layer is isolated in `database/db.py` and exposed via `database/__init__.py`.

### Project structure

```
expense-tracker/
├── app.py                  # all Flask routes
├── main.py                 # entrypoint stub (not used by Flask)
├── pyproject.toml          # dependencies and project metadata
├── requirements.txt        # pip-compatible mirror of pyproject deps
├── database/
│   ├── __init__.py         # exposes get_db, init_db, seed_db to app
│   └── db.py               # SQLite layer (student-authored)
├── templates/
│   ├── base.html           # shared layout (navbar, footer, font links)
│   ├── landing.html        # marketing/home page
│   ├── login.html          # sign-in form
│   ├── register.html       # sign-up form
│   ├── terms.html          # terms and conditions
│   └── privacy.html        # privacy policy
└── static/
    ├── css/
    │   └── style.css       # global styles
    └── js/
        └── main.js         # global JS entry point
```

### Key files

- `app.py` — all Flask routes. Complete: `/`, `/register`, `/login`, `/terms`, `/privacy`. Stubs (return placeholder strings): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.
- `database/db.py` — SQLite layer. Must expose exactly three functions: `get_db()`, `init_db()`, `seed_db()`.
- `templates/base.html` — Jinja2 base layout. All other templates extend this.
- `static/css/style.css` — global styles.
- `static/js/main.js` — global vanilla JS entry point; page-scoped JS goes in `{% block scripts %}`.

### Template pattern

Every template extends `base.html` and overrides `{% block title %}` and `{% block content %}`. Use `{% block head %}` for page-scoped CSS and `{% block scripts %}` for page-scoped JS.

### Database

SQLite; DB file is `expense_tracker.db` (git-ignored). `get_db()` must set `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. Tables are created with `CREATE TABLE IF NOT EXISTS` so `init_db()` is safe to call on every startup.

## Code Style

- Python: follow PEP 8. Use 4-space indentation. Keep route functions short — database calls belong in `database/db.py`, not inline in `app.py`.
- Jinja2: use `url_for()` for all internal links, never hardcode paths.
- JS: vanilla ES6, no frameworks. Scope page-specific scripts inside an IIFE `(function () { ... }())` to avoid global pollution.
- CSS: styles that apply to a single page go in `{% block head %}` inside a `<style>` tag; global styles go in `style.css`.

## Preferred Libraries and Tools

- **Runtime**: Python 3.12, managed with `uv` (`uv sync` to install, `uv run` to execute).
- **Web framework**: Flask 3.1.3.
- **Password hashing**: Werkzeug's `generate_password_hash` / `check_password_hash` (already a dependency).
- **Testing**: pytest 8.3.5 + pytest-flask 1.3.0.
- **Database**: SQLite via the stdlib `sqlite3` module — no ORM.
- **Frontend**: vanilla JS and CSS only. Google Fonts: DM Serif Display + DM Sans (loaded in `base.html`).

Do not introduce new dependencies without updating `pyproject.toml` and running `uv sync`.

## Commands

```bash
# Install dependencies
uv sync

# Run the development server (port 5001)
uv run flask --app app run --port 5001
# or directly:
python app.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_auth.py

# Run a single test by name
uv run pytest -k "test_login"
```

## Critical Rules

- **Never remove stub routes.** Routes like `/logout` and `/expenses/add` must remain in `app.py` even while unimplemented — removing them breaks `url_for()` calls in templates.
- **`database/db.py` is student-authored.** Do not auto-generate a full implementation unless the student explicitly asks. Preserve the comment header in that file so students know what to write.
- **No ORM.** All database access uses raw SQL via `sqlite3`. Do not introduce SQLAlchemy or any ORM.
- **Foreign keys must be enabled per-connection.** Always include `PRAGMA foreign_keys = ON` in `get_db()` — SQLite disables them by default.
- **`expense_tracker.db` is git-ignored.** Never commit the DB file. Call `init_db()` and optionally `seed_db()` at startup or via a CLI command, not by checking in data.
- **Port 5001.** The dev server always runs on 5001; do not change this without updating any documentation that references it.
