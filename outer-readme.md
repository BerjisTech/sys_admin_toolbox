# Server Monitoring and Multi-Service Application
This repository contains a Django-based server monitoring service alongside additional services (Rails, Angular, Node.js, and Postgres) managed with Docker Compose.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#Prerequisites)
3. [Project Structure](#Project%20Structure)
3. [Environment Variables](#Environment%20Variables)
5. [Docker Build & Run](#Docker%20Build%20&%20Run)
6. [Managing the Django Monitor](#Managing%20the%20Django%20Monitor)
7. [Additional Services](#Additional%20Services)
8. [Useful Commands](#Useful%20Commands)
9. [License](#License)
## Overview
This setup includes the following containers/services:

- caller-angular: Angular front-end.
- caller-rails: Rails back-end.
- caller-node: Node.js service (e.g., WebSockets, WebRTC).
- caller-db: PostgreSQL database.
- caller-nginx: NGINX reverse proxy.
caller-flask: Flask-based service for handling lightweight web requests and APIs. Used as a server monitoring tool
- caller-django: Django server monitoring tool (replacing or extending the Flask-based monitor).

The Django server-monitor service connects to the same PostgreSQL instance used by the Rails container. You can then use Django REST Framework (or any other Django-based approach) to monitor and manage servers, categories, logs, and more.

## Prerequisites
- Docker: Make sure Docker is installed and running.
- Docker Compose: At least v1.29+ (or Docker Desktop which bundles an equivalent).

### Project Structure
A simplified view of the relevant files and directories:

```perl

.
├── caller-sim1/              # Angular code
├── caller-sim2/              # Rails code
├── caller-server/            # Node.js code
├── server_monitor/
│   ├── manage.py
│   ├── requirements.txt
│   ├── dev-Dockerfile.django  # The Dockerfile for Django dev
│   ├── server_monitor/
│   │   ├── settings.py
│   │   └── ...
│   └── ...
├── dev-Dockerfile.angular
├── dev-Dockerfile.rails
├── dev-Dockerfile.nodejs
├── dev-Dockerfile.python      # (If previously used for Flask)
├── docker-compose.yml
├── dev-nginx.conf
└── README.md                  # (You are here!)
```
## Environment Variables
In your .env file (or directly in your environment), define at least the following:

```bash
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=myrailsdb       # DB used by Rails
PYTHON_POSTGRES_DB=mydjdb   # DB used by the Django server monitor
SECRET_KEY=mysecretkey
GOOGLE_CLIENT_ID=<optional_for_rails_oauth>
GOOGLE_CLIENT_SECRET=<optional_for_rails_oauth>
GITHUB_CLIENT_ID=<optional_for_rails_oauth>
GITHUB_CLIENT_SECRET=<optional_for_rails_oauth>
```
- POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB: Credentials for the primary Postgres DB used by Rails.
- PYTHON_POSTGRES_DB: The name of the separate Postgres DB that Django will use (you can reuse `POSTGRES_DB`, but many prefer a different database).
- SECRET_KEY: Django’s secret key (used for cryptographic signing).

## Docker Build & Run
1. Build all services:

```bash
docker-compose build
```
Or just run `build` or `sh build.sh`

2. Start containers in the background:

```bash
docker-compose up -d
```
3. Check container statuses:

```bash
docker-compose ps
```
4. View logs for a specific container, for example the Django server-monitor:

```bash
docker-compose logs -f server-monitor
```
After a short time, each service should be up and healthy.

## Managing the Django Monitor
1. Migrations
To create all database tables for the Django server monitor, run:

```bash
docker-compose exec server-monitor python manage.py migrate
```
2. Create a Superuser
If you want to use Django’s admin panel (/admin):

```bash
docker-compose exec server-monitor python manage.py createsuperuser
```
3. Access the Django Service
- By default, Django runs on port 8000 inside the container.
- In your `docker-compose.yml`, it’s mapped to the host’s port 8000.
- Visit http://localhost:8000 in your browser to confirm it’s working.
- Admin panel: http://localhost:8000/admin.

## Additional Services
1. caller-angular
- Runs on port 8085 (mapped to `localhost:8085`).
- You can access your Angular front-end in a browser at `http://localhost:8085`.

2. caller-rails
- Exposed on port 3008.
- Rails environment runs in `development` by default.
- Healthcheck script verifies Postgres connectivity.

3. caller-node
- Runs on port 3006 by default.
- Use this service for real-time or custom Node.js tasks.

4. caller-db (Postgres)
Exposes no external port outside Docker by default.
The Django and Rails containers connect using the internal Docker network alias `caller-db`.

5. caller-nginx
- Reverse proxy for the Angular, Rails, and Node services.
- You can configure additional routes to proxy to the Django service if desired.

## Useful Commands
- Stop all containers:
```bash
docker-compose down
```

- Stop and remove containers, networks, images, and volumes:
```bash
docker-compose down --rmi all -v
```
(Use with caution if you don’t want to lose volumes/data.)

- Rebuild an individual service (e.g. the Django server):
```bash
docker-compose build server-monitor
```

- Shell into a running container:
```bash
docker-compose exec server-monitor bash
```

Then you can run additional Django management commands or debug as needed.

## License
This project is licensed under the MIT License (or whichever you prefer). See LICENSE for more details.

## Enjoy Monitoring!
You now have a Django-based server monitor alongside other microservices (Rails, Angular, Node) in a single Docker Compose environment. For any questions or improvements, feel free to open an issue or submit a pull request.