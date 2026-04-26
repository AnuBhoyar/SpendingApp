# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate with Spendly. This step upgrades the stub `GET /login` route into a fully functional POST handler that verifies credentials against the `users` table, stores the user's id and name in Flask's signed cookie session, and redirects to the expenses dashboard. The stub `GET /logout` route is implemented to clear the session and redirect to the landing page. These two routes are the gateway to all future authenticated features.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, hashed passwords stored in DB)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — process login form, verify credentials, set session, redirect to `/` — public
- `GET /logout` — clear session, redirect to `/` — public (already exists as stub, implement it)

## Database changes
No new tables or columns. The existing `users` table covers all requirements.

A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — fetches a single row from `users` by email using a parameterised query. Returns a `sqlite3.Row` (or `None` if not found). The caller is responsible for password verification.

## Templates
- **Modify**: `templates/login.html`
  - Set form `action` to `url_for('login')` with `method="post"`
  - Add `name` attributes to inputs: `email`, `password`
  - Add a block to display flash error messages (e.g. "Invalid email or password")
  - Keep all existing visual design

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST`; implement `logout()`; import `session` from Flask and `check_password_hash` from werkzeug; import `get_user_by_email` from `database.db`
- `database/db.py` — add `get_user_by_email()` helper
- `templates/login.html` — wire up form action/method and flash message display

## Files to create
None.

## New dependencies
No new dependencies. Uses Flask's built-in `session`, `flash`, `redirect`, `url_for`, and `werkzeug.security.check_password_hash` (already installed).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plaintext
- Use Flask's `session` (signed cookie) — store only `user_id` (int) and `user_name` (str)
- Use a deliberate, non-specific error message on failure: "Invalid email or password" — never reveal which field is wrong
- On any validation failure, re-render the login form with a flashed error — do not redirect
- On success, `session['user_id']` and `session['user_name']` must be set before redirecting
- `logout()` must call `session.clear()` and redirect to `url_for('landing')`
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid credentials sets `session['user_id']` and redirects to `/`
- [ ] Submitting an unregistered email re-renders the form with "Invalid email or password"
- [ ] Submitting a wrong password for a valid email re-renders the form with "Invalid email or password"
- [ ] Submitting with any empty field re-renders the form with a validation error
- [ ] `GET /logout` clears the session and redirects to the landing page
- [ ] After logout, `session['user_id']` is no longer present in the session
- [ ] No stub strings ("coming in Step 3") remain in the app
