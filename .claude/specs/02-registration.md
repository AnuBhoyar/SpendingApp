# Spec: Registration

## Overview
Implement user registration so that new visitors can create a Spendly account. This step wires the existing `register.html` form to a POST handler in `app.py` that validates input, hashes the password with `werkzeug`, and inserts a new row into the `users` table. On success the user is redirected to the login page; on failure the form is re-rendered with an inline error message. This is the first step where user-generated data flows all the way from the browser to the database.

## Depends on
- Step 1 (Database Setup) — `users` table and `get_db()` must exist and work.

## Routes
- `POST /register` — handles registration form submission — public

The existing `GET /register` route stays unchanged (it already renders `register.html`).

## Database changes
No database changes. The `users` table created in Step 1 already has all required columns (`id`, `name`, `email`, `password`, `created_at`).

## Templates
- **Modify:** `templates/register.html`
  - Already contains the form and an `{% if error %}` block — no structural changes needed.
  - Ensure `value="{{ name }}"` and `value="{{ email }}"` are added to the name and email inputs so field values survive a failed submission.

## Files to change
- `app.py` — add POST handler for `/register`, import `get_db` and `generate_password_hash`

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security` is already installed as part of Flask.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Hash passwords with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side: name, email, and password must all be non-empty; password must be at least 8 characters
- Catch `sqlite3.IntegrityError` to detect duplicate email and return a friendly error
- After successful registration redirect to `url_for('login')` — do not log the user in automatically
- Re-render `register.html` with `error`, `name`, and `email` template variables on any failure so the user does not have to retype everything

## Definition of done
- [ ] `GET /register` still renders the form (no regression)
- [ ] Submitting the form with valid data inserts a new row in `users` with a hashed password (not plaintext)
- [ ] Submitting with a duplicate email shows "Email already registered" error on the form
- [ ] Submitting with an empty name, email, or password shows a validation error
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] After successful registration the browser is redirected to `/login`
- [ ] Name and email field values are preserved on a failed submission
- [ ] App starts without errors (`python app.py`)
