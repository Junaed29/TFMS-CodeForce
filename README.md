# TFMS-CodeForce

![Universiti Teknologi Malaysia (UTM) Logo](logoAndDocuments/UTM-LOGO-FULL.png)

TFMS-CodeForce is a Django-based Task Force Management System for academic departments, built as a semester project for Universiti Teknologi Malaysia (UTM). It provides role-based dashboards (Admin, HOD, PSM, Management/Dean, Lecturer), staff and department administration, task force creation and approval workflows, workload settings, audit logs with CSV export, and report exports in Excel/PDF. The UI is rendered with Django templates and Bootstrap, and data is stored in SQLite by default (PostgreSQL via `DATABASE_URL`).

## Table of Contents

- [Quick Start (Beginner, Step-by-Step)](#quick-start-beginner-step-by-step)
- [Requirements (Prerequisites)](#requirements-prerequisites)
- [Download / Clone the Project](#download--clone-the-project)
- [Setup (Local Development)](#setup-local-development)
- [Database Setup](#database-setup)
- [Create an Admin / Superuser](#create-an-admin--superuser)
- [Running the Project Locally](#running-the-project-locally)
- [Updating the Project Using AI](#updating-the-project-using-ai)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)

## Quick Start (Beginner, Step-by-Step)

These steps assume you only have an internet connection and a computer. If you already have Git and Python installed, start at step 4.

### macOS
1. Install Homebrew (skip if already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Git and Python 3.10+:
   ```bash
   brew install git python
   ```
3. Verify installs:
   ```bash
   git --version
   python3 --version
   ```
4. Download the project:
   ```bash
   git clone https://github.com/Junaed29/TFMS-CodeForce.git
   cd TFMS-CodeForce
   ```
5. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
6. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
7. Create a `.env` file for email (needed for mail service; see [Gmail App Password](#gmail-app-password-email_host_password) for password generation):
   ```bash
   cat > .env <<'EOF'
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=TFMS Support <your-email@example.com>
   EOF
   ```
   Important: If `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD` is missing, email features will not send.
8. Initialize the database:
   ```bash
   python3 manage.py migrate
   ```
9. Create an admin account:
   ```bash
   python3 manage.py createsuperuser
   ```
10. Start the server:
   ```bash
   python3 manage.py runserver
   ```
11. Open `http://127.0.0.1:8000/` in your browser and log in.

### Windows
1. Install Git (skip if already installed):
   ```powershell
   winget install --id Git.Git -e
   ```
2. Install Python 3.10+ (skip if already installed):
   ```powershell
   winget install --id Python.Python.3.11 -e
   ```
   If `winget` is not available, install from `https://git-scm.com/` and `https://python.org/`.
3. Verify installs:
   ```powershell
   git --version
   python --version
   ```
4. Download the project:
   ```powershell
   git clone https://github.com/Junaed29/TFMS-CodeForce.git
   cd TFMS-CodeForce
   ```
5. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
6. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
7. Create a `.env` file for email (needed for mail service; see [Gmail App Password](#gmail-app-password-email_host_password) for password generation):
   ```powershell
   notepad .env
   ```
   Paste and save:
   ```ini
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=TFMS Support <your-email@example.com>
   ```
   Important: If `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD` is missing, email features will not send.
8. Initialize the database:
   ```powershell
   python manage.py migrate
   ```
9. Create an admin account:
   ```powershell
   python manage.py createsuperuser
   ```
10. Start the server:
   ```powershell
   python manage.py runserver
   ```
11. Open `http://127.0.0.1:8000/` in your browser and log in.

## Requirements (Prerequisites)

You will need:
- Python 3.10+ (required for this project)
- Git
- Optional: PostgreSQL if you choose it in Database Setup

### macOS
1. Install Homebrew (if you do not have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Git and Python:
   ```bash
   brew install git python
   ```
3. Verify installs:
   ```bash
   git --version
   python3 --version
   pip3 --version
   ```

Common pitfalls:
- If `python` does not exist, use `python3` in all commands.
- If `pip` is missing, run `python3 -m ensurepip --upgrade`.

### Windows
1. Install Git:
   ```powershell
   winget install --id Git.Git -e
   ```
2. Install Python 3.10+:
   ```powershell
   winget install --id Python.Python.3.11 -e
   ```
3. Verify installs:
   ```powershell
   git --version
   python --version
   pip --version
   ```

Common pitfalls:
- If `python` opens the Microsoft Store, reinstall Python and check "Add Python to PATH", or use `py -3.11`.
- If `pip` is missing, run `python -m ensurepip --upgrade`.

## Download / Clone the Project

Git is a version control tool that downloads the project and lets you update it later with `git pull`.

### macOS
1. Open Terminal.
2. Clone the repo:
   ```bash
   git clone https://github.com/Junaed29/TFMS-CodeForce.git
   ```
3. Enter the folder:
   ```bash
   cd TFMS-CodeForce
   ```
4. You should see files like `manage.py`, `requirements.txt`, `accounts/`, `dashboard/`, `university/`, `tfms_core/`, `templates/`, `static/`, `PythonAnywhere_Update_Guide.md`, `logoAndDocuments/`.

### Windows
1. Open PowerShell or Command Prompt.
2. Clone the repo:
   ```bat
   git clone https://github.com/Junaed29/TFMS-CodeForce.git
   ```
3. Enter the folder:
   ```bat
   cd TFMS-CodeForce
   ```
4. You should see files like `manage.py`, `requirements.txt`, `accounts/`, `dashboard/`, `university/`, `tfms_core/`, `templates/`, `static/`, `PythonAnywhere_Update_Guide.md`, `logoAndDocuments/`.

## Setup (Local Development)

### Environment Variables (.env)

`manage.py` and `tfms_core/wsgi.py` load `.env` via python-dotenv. Create `.env` in the repo root (next to `manage.py`).

| Variable | Required | Purpose | Safe local default |
| --- | --- | --- | --- |
| `EMAIL_HOST` | Optional | SMTP host (hardcoded to `smtp.gmail.com` in `tfms_core/settings.py`) | `smtp.gmail.com` |
| `EMAIL_PORT` | Optional | SMTP port (hardcoded to `587` in `tfms_core/settings.py`) | `587` |
| `EMAIL_HOST_USER` | Optional | SMTP username; `DEFAULT_FROM_EMAIL` is set to this in `tfms_core/settings.py` | Leave blank to skip email sending |
| `EMAIL_HOST_PASSWORD` | Optional | SMTP password or app password | Leave blank to skip email sending |
| `DEFAULT_FROM_EMAIL` | Optional | Display name/from address (not read from env in current code) | Edit `tfms_core/settings.py` to use this |
| `DATABASE_URL` | Optional | Overrides the default SQLite DB via `dj_database_url.config` | If you use `db.sqlite3`, you do not need this |

Notes:
- Important: If `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD` is missing, email features will not send.
- `tfms_core/settings.py` hardcodes `DEBUG=True`, `SECRET_KEY`, `EMAIL_HOST=smtp.gmail.com`, `EMAIL_PORT=587`, and `EMAIL_USE_TLS=True`. To change these, edit `tfms_core/settings.py`.
- The repo does not include a `Local_Run_Guide.md` file anymore; this README is the source of truth for local setup.

Example `.env`:
```ini
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=TFMS Support <your-email@example.com>
# DATABASE_URL=postgresql://user:password@localhost:5432/tfms
```

### Gmail App Password (EMAIL_HOST_PASSWORD)

If you use Gmail as shown above, you must use a Google App Password (free) instead of your normal Gmail password.

1. Go to `https://myaccount.google.com/security` and enable **2-Step Verification**.
2. Open `https://myaccount.google.com/apppasswords` and sign in.
3. Under **Select app**, choose **Mail**. Under **Select device**, choose **Other (Custom name)** and enter `TFMS Local`.
4. Click **Generate**, then copy the 16-character password.
5. Paste it into `.env` as `EMAIL_HOST_PASSWORD`.

If the App Passwords page looks different or is not available, search the internet for "Google app password" and follow the latest official Google instructions.

### macOS
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate it:
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
4. Create `.env` if you have not already:
   ```bash
   cat > .env <<'EOF'
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=TFMS Support <your-email@example.com>
   EOF
   ```

### Windows
1. Create a virtual environment:
   ```bat
   python -m venv venv
   ```
2. Activate it:
   ```bat
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bat
   python -m pip install -r requirements.txt
   ```
4. Create `.env` if you have not already:
   ```bat
   notepad .env
   ```
   Paste and save:
   ```ini
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=TFMS Support <your-email@example.com>
   ```

## What you need to provide

Checked `requirements.txt`, `tfms_core/settings.py`, `manage.py`, and `PythonAnywhere_Update_Guide.md`. Missing items you must supply:
- SMTP credentials (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) if you want emails for account creation, password resets, and lecturer remarks.
- A `DATABASE_URL` value if you want PostgreSQL instead of SQLite.
- Production-safe settings (the repo hardcodes `SECRET_KEY` and `DEBUG=True`).
- There is no tracked `.env.example`, `Dockerfile`, or `docker-compose.yml`; setup is manual as documented here.

## Database Setup

### macOS
#### SQLite (default)
1. Run migrations:
   ```bash
   python3 manage.py migrate
   ```
2. This creates `db.sqlite3` in the repo root.

#### PostgreSQL (optional)
1. Install PostgreSQL:
   ```bash
   brew install postgresql
   brew services start postgresql
   ```
2. Create a database and user:
   ```bash
   psql postgres
   ```
   ```sql
   CREATE DATABASE tfms;
   CREATE USER tfms_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE tfms TO tfms_user;
   ```
   Exit with `\q`.
3. Add this to `.env`:
   ```ini
   DATABASE_URL=postgresql://tfms_user:your_password@localhost:5432/tfms
   ```
4. Run migrations:
   ```bash
   python3 manage.py migrate
   ```
5. Verify connection:
   ```bash
   python3 manage.py dbshell
   ```
   Then run `\dt` and exit with `\q`.

### Windows
#### SQLite (default)
1. Run migrations:
   ```bat
   python manage.py migrate
   ```
2. This creates `db.sqlite3` in the repo root.

#### PostgreSQL (optional)
1. Install PostgreSQL:
   ```powershell
   winget install --id PostgreSQL.PostgreSQL -e
   ```
2. Open "SQL Shell (psql)" or PowerShell:
   ```powershell
   psql -U postgres
   ```
3. Create a database and user:
   ```sql
   CREATE DATABASE tfms;
   CREATE USER tfms_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE tfms TO tfms_user;
   ```
   Exit with `\q`.
4. Add this to `.env`:
   ```ini
   DATABASE_URL=postgresql://tfms_user:your_password@localhost:5432/tfms
   ```
5. Run migrations:
   ```powershell
   python manage.py migrate
   ```
6. Verify connection:
   ```powershell
   python manage.py dbshell
   ```
   Then run `\dt` and exit with `\q`.

## Create an Admin / Superuser

### macOS
1. Run:
   ```bash
   python3 manage.py createsuperuser
   ```
2. Follow the prompts and choose a password that matches the rules below.

### Windows
1. Run:
   ```bat
   python manage.py createsuperuser
   ```
2. Follow the prompts and choose a password that matches the rules below.

Password rules in `tfms_core/settings.py`:
- Minimum length 8, maximum length 16
- Must contain at least one letter and one number

After you start the server (see **Running the Project Locally**), log in at `http://127.0.0.1:8000/accounts/login/` or `http://127.0.0.1:8000/`.

## Running the Project Locally

### macOS
1. Activate your virtual environment (if not already):
   ```bash
   source venv/bin/activate
   ```
2. Make sure you have completed **Create an Admin / Superuser** so the admin can enter the admin dashboard.
3. Start the server:
   ```bash
   python3 manage.py runserver
   ```
4. Open `http://127.0.0.1:8000/` and log in.
5. Stop the server with `Ctrl+C`.

### Windows
1. Activate your virtual environment (if not already):
   ```bat
   venv\Scripts\activate
   ```
2. Make sure you have completed **Create an Admin / Superuser** so the admin can enter the admin dashboard.
3. Start the server:
   ```bat
   python manage.py runserver
   ```
4. Open `http://127.0.0.1:8000/` and log in.
5. Stop the server with `Ctrl+C`.

Server logs and errors appear in the terminal where you ran `runserver`. Django will auto-reload when you change Python or template files.

## Updating the Project Using AI

If you are new and want to change this project (add a feature, fix a bug, update wording), you can use an AI coding assistant. A safe workflow:

1. Make sure the project runs first (finish **Quick Start**).
2. Tell the AI exactly what you want to change and ask it to read the relevant files (for example: `README.md`, `tfms_core/settings.py`, `accounts/`, `dashboard/`, `university/`, `templates/`).
3. Ask the AI to explain the plan before changing files, then apply the changes.
4. Review the changes before running the app.
5. Run the update steps below based on what was changed.

Important:
- Do not paste secrets into an AI chat (real passwords, tokens, or private emails).
- If the AI adds new packages, it should update `requirements.txt`.
- If the AI changes Django models, you must create migrations.

### macOS
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. If `requirements.txt` changed, reinstall dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. If models changed, create and apply migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
4. Start the server:
   ```bash
   python3 manage.py runserver
   ```

### Windows
1. Activate the virtual environment:
   ```bat
   venv\Scripts\activate
   ```
2. If `requirements.txt` changed, reinstall dependencies:
   ```bat
   python -m pip install -r requirements.txt
   ```
3. If models changed, create and apply migrations:
   ```bat
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the server:
   ```bat
   python manage.py runserver
   ```

## Testing

No automated tests were found in the tracked files (no `tests.py` or `test_*.py` files). If you add tests later, run:

```bash
python manage.py test
```

## Troubleshooting

- Symptom: `Address already in use` -> Cause: another app is using port 8000 -> Fix: `python manage.py runserver 8001` or stop the other app.
- Symptom: `ModuleNotFoundError` -> Cause: virtual environment not active or dependencies not installed -> Fix: activate `venv` and run `python -m pip install -r requirements.txt`.
- Symptom: `no such table` / `relation does not exist` -> Cause: migrations not applied -> Fix: `python manage.py migrate`.
- Symptom: `could not connect to server` (PostgreSQL) -> Cause: Postgres not running or wrong `DATABASE_URL` -> Fix: start Postgres and re-check `.env`.
- Symptom: `CSRF cookie not set` on local HTTP -> Cause: `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` are `True` in `tfms_core/settings.py` -> Fix: set them to `False` for local development.
- Symptom: email send fails -> Cause: missing or incorrect `EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` -> Fix: update `.env` or switch to the console email backend in `tfms_core/settings.py`.
- Symptom: login keeps failing or account locked -> Cause: the app locks non-admin accounts after 3 failed attempts -> Fix: log in as an admin and unlock the user in the Admin Staff list.
- Symptom: `venv\Scripts\activate` not found on Windows -> Cause: virtual environment not created in the repo folder -> Fix: run `python -m venv venv` from the project root, then activate again.

## Project Structure

- `tfms_core/` - Django settings, URLs, WSGI/ASGI entry points
- `accounts/` - Custom user model, authentication views, validators, audit logging
- `dashboard/` - Role dashboards, admin tools, exports, and API endpoints
- `university/` - Department, task force, and workload logic
- `templates/` - Django HTML templates and email templates
- `static/` - CSS and images
- `logoAndDocuments/` - Logos and use case documentation
- `manage.py` - Django management entry point
- `requirements.txt` - Python dependencies
- `PythonAnywhere_Update_Guide.md` - Notes for updating a PythonAnywhere deployment

## Tech Stack

- Python 3.10+ (required for this project)
- Django >= 5.0 (from `requirements.txt`; settings header mentions 4.2.27)
- SQLite (default via `dj-database-url`)
- PostgreSQL (optional via `psycopg2-binary` and `DATABASE_URL`)
- Bootstrap 5.3.3 and Bootstrap Icons 1.11.3 (CDN in `templates/base.html`)
- Poppins font (Google Fonts in `templates/base.html`)
- openpyxl and reportlab for Excel/PDF exports
- python-dotenv for `.env` loading
