# Django Server Monitor
A Django-based server monitoring tool that tracks parent/child servers, categories, tools, uptime, logs, and more. This project is part of a larger, multi-container Docker environment, but can also run independently.

## Table of Contents
1. [Overview](#Overview)
1. [Features](#Features)
1. [Requirements](#Requirements)
1. [Project Structure](#Project%20Structure)
1. [Setup (Docker)](#Setup%20(Docker))
1. [Local Setup (Without Docker)](#Local%20Setup%20(Without%20Docker))
1. [Usage](#Usage)
1. [Environment Variables](#Environment%20Variables)
1. [Running Migrations](#%20Migrations)
1. [Creating a Superuser](#Creating%20a%20Superuser)
1. [API Endpoints](#API%20Endpoints)
1. [Next Steps](#Next%20Steps)
1. [License](#License)
## Overview
This Django application provides a REST API (using Django REST Framework) to:

- Register servers (with optional parent-child relationships).
- Assign categories (e.g., Mail Server, Web Server) and attach tools (e.g., Docker, MySQL).
- Capture and store logs (system logs, Docker logs, etc.) for each server.
- Check uptime and gather metrics (e.g. CPU/Memory usage) for local or remote servers.

It is designed to be used within a Docker Compose environment that already includes PostgreSQL and other services (Rails, Angular, Node, etc.). You can also run it standalone on your machine using a virtual environment.

## Features
- Parent/Child Server Hierarchy: Link child servers to parent servers for grouped monitoring.
- Categories & Tools: Tag each server with a category (Mail Server, Web Server) and relevant tools (MySQL, Docker).
- Logs: Store server logs in a dedicated table (e.g. Docker logs, system logs).
- Metrics: Basic CPU/memory usage endpoints via psutil (for local system) or remote checks (HTTP ping).
- PostgreSQL support out of the box.

## Requirements
- Python 3.10+ (if running locally)
- Docker & Docker Compose (if running in containers)
- PostgreSQL (containerized or local)
- Django & Django REST Framework
- psycopg2 for connecting to Postgres

## Project Structure
```bash
sys_admin_toolbox/
├── manage.py                   # Django's CLI utility
├── dev-Dockerfile.django       # Dockerfile for Django dev environment
├── requirements.txt            # Python dependencies
├── run.py                      # (Optional) A custom Flask-style entrypoint, if used
├── sys_admin_toolbox/             # Django project folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Main settings (DB config, installed apps, etc.)
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
└── toolbox/                 # Your Django app for toolbox
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── ...
```
## Setup (Docker)
1. Add/Update Docker Compose
In your `docker-compose.yml`, ensure you have a service named `sys_admin_toolbox` (or similar) pointing to `dev-Dockerfile.django`. For example:

```yaml
sys_admin_toolbox:
  build:
    context: .
    dockerfile: dev-Dockerfile.django
  volumes:
    - ./sys_admin_toolbox:/usr/src/app
  ports:
    - "8000:8000"
  depends_on:
    - caller-db
  environment:
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    POSTGRES_DB: ${PYTHON_POSTGRES_DB}
    POSTGRES_HOST: caller-db
    SECRET_KEY: ${SECRET_KEY}
  networks:
    - caller-network
```

2. Build & Run
```bash
docker-compose build sys_admin_toolbox
docker-compose up -d sys_admin_toolbox
```
This will start your Django app and map port `8000` on your host to the Django dev server inside the container.

3. Check Logs
```bash
docker-compose logs -f sys_admin_toolbox
```
Once you see “Starting development server at http://0.0.0.0:8000/…”, the app is running.

4. Visit the App
Go to http://localhost:8000 in your browser to confirm the application is live.

## Local Setup (Without Docker)
If you prefer to run Django directly on your host (for testing or development):

1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Update `settings.py`
Make sure your `DATABASES` config points to a reachable Postgres instance (e.g. `localhost` or a Docker IP).

3. Run Migrations
```bash
python manage.py migrate
```

4. Start the Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

5. Verify
Visit http://127.0.0.1:8000 to see your Django app.

## Usage
- Creating Servers:<br />
Send a POST request to `/api/servers/` with JSON data (name, description, category_id, etc.).
- Fetching Metrics:<br />
Visit `/api/system-metrics/` for local CPU/memory usage.
- Logs:<br />
POST logs to `/api/logs/` or GET logs from `/api/logs/{id}/`.

## Environment Variables
The Django server monitor relies on the following environment variables in `docker-compose.yml` or your local environment:

- `POSTGRES_USER` (e.g., `django_user`)
- `POSTGRES_PASSWORD` (e.g., `django_password`)
- `POSTGRES_DB` (e.g., `django_db`)
- `POSTGRES_HOST` (e.g., `caller-db` in Docker, or `localhost` in local dev)
- `SECRET_KEY` (Django’s secret key)
All of these are read in `sys_admin_toolbox/sys_admin_toolbox/settings.py` like so:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django_db'),
        'USER': os.getenv('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'django_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': '5432',
    }
}

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
```
## Running Migrations
Within the Docker container (recommended):
```bash
docker-compose exec sys_admin_toolbox python manage.py migrate
```
Or locally (if not using Docker):
```bash
python manage.py migrate
```

## Creating a Superuser
If you want to access the Django admin panel (/admin):
```bash
docker-compose exec sys_admin_toolbox python manage.py createsuperuser
```
Then follow the prompts.

## API Endpoints
Below is a short overview of the main endpoints exposed by the monitoring app (assuming your URLs are prefixed with `/api/` in `urls.py`):

1. Servers
- `GET /api/servers/` – List all servers
- `POST /api/servers/` – Create a new server
- `GET /api/servers/{id}/` – Retrieve, update, or delete a specific server
2. Categories
- `GET /api/categories/` – List all categories
- `POST /api/categories/` – Create a new category
3. Tools
- `GET /api/tools/`
- `POST /api/tools/`
4. Logs
- `GET /api/logs/`
- `POST /api/logs/`
5. System Metrics (if implemented)
- `GET /api/system-metrics/`
You can also add custom endpoints for uptime checks or Docker logs as needed.

## Next Steps
- Security & Authentication: Add authentication (Token Auth, JWT, or Session Auth) to secure these endpoints.
- Monitoring Scheduler: Use Celery or cron jobs to regularly poll CPU usage, uptime, or logs from remote servers.
- Production: Replace `runserver` with a production WSGI server (e.g., Gunicorn) behind a reverse proxy like NGINX.

## License
This project is licensed under the MIT License (or whichever license you prefer). See the LICENSE file for details.

## Happy Monitoring!
You now have a fully functioning Django-based server monitor that can run standalone or as part of a Docker multi-service environment. For any questions or improvements, please feel free to open an issue or submit a pull request.