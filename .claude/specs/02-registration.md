# Spec: Registration

## Overview
Complete the user registration feature by implementing the POST handler for `/register`. Users will fill out the registration form (name, email, password) and create an account. The route will validate inputs, check for duplicate emails, hash the password with Werkzeug, insert the user into the database, and redirect to the login page on success. Errors (missing fields, invalid email, password too short, duplicate email) will be shown on the form.

## Depends on
- Step 1: Database Setup — users table must exist with id, name, email, password_hash, created_at columns

## Routes
- `POST /register` — handle registration form submission; validate inputs, hash password, insert user, redirect to login on success; show error on registration page if validation fails (public)

## Database changes
No database changes. The users table from Step 1 is sufficient.

## Templates
- **Modify:** `templates/register.html`
  - Add error message display (already has `{% if error %}` block)
  - Ensure form fields match POST handler expectations (name, email, password)
  - Add success message or redirect notice if needed

## Files to change
- `app.py` — modify `/register` route to accept both GET (render form) and POST (process form)
- `database/db.py` — (optional) add a helper function `email_exists(email)` to check for duplicate emails, or inline the check in app.py

## Files to create
None.

## New dependencies
No new dependencies. Werkzeug (`generate_password_hash`) is already a Flask dependency.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3 via `get_db()`
- Parameterized queries only — no string formatting in SQL
- Password hashing: use `from werkzeug.security import generate_password_hash`
- Validation rules:
  - **Name:** required, non-empty, at least 2 characters
  - **Email:** required, valid email format, unique in database
  - **Password:** required, at least 8 characters
- Error messages must be user-friendly and specific (e.g., "Email already registered" not "UNIQUE constraint failed")
- `created_at` field must be set to current datetime in ISO format (`datetime.now().isoformat()`)
- On successful registration, redirect to `/login` with a success indicator (optional: flash message if Flask sessions are set up)
- Use `url_for()` for all internal links
- All templates extend `base.html`

## Definition of done
- [ ] GET `/register` renders the registration form (already works from Step 1)
- [ ] POST `/register` with valid inputs (name, email, password) creates a user in the database and redirects to `/login`
- [ ] Duplicate email shows "Email already registered" error on the form
- [ ] Password shorter than 8 characters shows "Password must be at least 8 characters" error
- [ ] Missing required fields show appropriate error messages
- [ ] Invalid email format shows "Invalid email address" error
- [ ] User password is hashed with Werkzeug (can verify via DB inspection: `SELECT password_hash FROM users WHERE email=?`)
- [ ] `created_at` timestamp is stored in ISO format
- [ ] No SQL injection vulnerabilities — all queries use parameterized placeholders
- [ ] Form re-renders with user's name and email pre-filled on error (except password for security)
