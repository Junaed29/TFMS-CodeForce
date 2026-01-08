# Local Development Setup Guide

Follow these steps to run the TFMS-CodeForce project on your local machine.

## 1. Prerequisites
*   **Python 3.10+**: Ensure you have Python installed (`python3 --version`).
*   **Git**: To manage the code (`git --version`).

## 2. Environment Setup

It is best practice to use a virtual environment to isolate dependencies.

**Open you Terminal/Command Prompt in the project folder:**

```bash
# MacOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

*You should see `(venv)` appear at the start of your command line.*

## 3. Install Dependencies

Install all required packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

The project needs a `.env` file for email configuration.

1.  Create a file named `.env` in the root folder (same level as `manage.py`).
2.  Add the following content (replace with your values if needed):

```ini
# .env
DEBUG=True
SECRET_KEY=django-insecure-kqy6p+e6f57g*8f(f$+sdb6hfbq==+*5qg(y+5h)6=1%mdhl1#
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=junaed.test@gmail.com
EMAIL_HOST_PASSWORD=ozsr svyx yxsw rerg
DEFAULT_FROM_EMAIL=TFMS Support <junaed.test@gmail.com>
```

*(Note: The `SECRET_KEY` here is the default dev key. For production, keep it secret!)*

## 5. Database Setup

Initialize the local SQLite database.

```bash
# Apply migrations to create database tables
python manage.py migrate

# (Optional) Create an Admin user to log in
python manage.py createsuperuser
```
*Follow the prompts to set a username and password.*

## 6. Run the Server

Start the local Django development server.

```bash
python manage.py runserver
```

## 7. Access the Application

Open your browser and go to:
👉 **http://127.0.0.1:8000/**

*   **Login**: Use the superuser account you created.
*   **Admin Panel**: http://127.0.0.1:8000/admin/
