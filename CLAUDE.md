# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server (port 5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Install dependencies
pip install -r requirements.txt
```

## Project Overview

**Spendly** is a Flask-based expense tracking web application built as part of a CampusX course. The project is incrementally developed — backend features (auth, database, expense CRUD) are added step by step. The frontend shell (landing page, auth forms, legal pages) is already in place.

## Architecture

### Backend (`app.py`, `database/`)
- Single `app.py` file with all Flask routes; no blueprints currently
- Routes map directly to Jinja2 templates — no API layer
- `database/db.py` is a stub where students implement `get_db()`, `init_db()`, and `seed_db()` for SQLite
- Planned features (stub routes already exist): logout, profile, expense add/edit/delete

### Frontend (`templates/`, `static/`)
- All pages extend `templates/base.html` (Jinja2 template inheritance)
- Single CSS file at `static/css/style.css` — uses CSS custom properties for the design system
- Vanilla JavaScript only (`static/js/main.js`)
- Design tokens: teal accent `#1a472a`, orange accent `#c17f24`, DM Serif Display / DM Sans fonts

### Planned route structure (as stubs exist in `app.py`)
| Route | Purpose |
|---|---|
| `GET /` | Landing page |
| `GET /register` | Register form |
| `GET /login` | Login form |
| `GET /logout` | Session logout (Step 3) |
| `GET /profile` | User profile (Step 4) |
| `GET /expenses/add` | Add expense (Step 7) |
| `GET /expenses/<id>/edit` | Edit expense (Step 8) |
| `GET /expenses/<id>/delete` | Delete expense (Step 9) |

## Key Conventions
- Database file: `expense_tracker.db` (gitignored)
- Flask runs in debug mode on port 5001
- No `.env` setup yet; secrets should go in `.env` (already gitignored) when added
