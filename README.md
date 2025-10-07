
# AeroRoute-System

A Django-based flight route management system that allows users to add airport routes, search specific nodes, and analyze the longest and shortest routes based on duration.

This README explains how to build and run the project (Docker and local), describes what the Docker entrypoint does, and includes troubleshooting tips.

## What the Docker entrypoint does

When the container starts it runs `entrypoint.sh`, which performs these steps in order:

1. `python manage.py makemigrations --noinput` (safe to run; will no-op if no model changes)
2. `python manage.py migrate --noinput`
3. Create a Django superuser if one doesn't already exist (using environment variables below)
4. Run the custom management command `seed_routes` (if present)
5. Start the Django development server with `debugpy` listening on port `5678`

Files changed to support this flow:

- `entrypoint.sh` — new entrypoint script
- `Dockerfile` — copies `entrypoint.sh` and sets it as the container entrypoint
- `docker-compose.yml` — environment variables for admin creation and restart policy

## Default superuser credentials

The entrypoint will create a superuser using these defaults unless overridden via environment variables:

- Username: `admin`
- Email: `admin@gmail.com`
- Password: `admin`

You can override these by setting the environment variables:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

Example (in `docker-compose.yml`):

```yaml
environment:
	- DJANGO_SUPERUSER_USERNAME=myadmin
	- DJANGO_SUPERUSER_EMAIL=myadmin@example.com
	- DJANGO_SUPERUSER_PASSWORD=securepassword
```

## Running with Docker (recommended)

1. Build the image (PowerShell):

```powershell
docker-compose build --no-cache
```

2. Start the services:

```powershell
docker-compose up --force-recreate
```

3. Visit the app at `http://localhost:8000`.

Logs will show migration, superuser creation (or "superuser exists"), seed command output, and then the Django server starting.

## Running locally without Docker

1. Create and activate a virtual environment (example using venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run migrations and create superuser (interactive):

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

3. Optionally run the seed command:

```powershell
python manage.py seed_routes
```

4. Run the dev server:

```powershell
python manage.py runserver
```

## Troubleshooting

- Container keeps restarting with an error about `settings not configured`:
	- Ensure `entrypoint.sh` sets `DJANGO_SETTINGS_MODULE` (it defaults to `flight_routes.settings`). If you override settings, export `DJANGO_SETTINGS_MODULE` in `docker-compose.yml`.
- DB connection errors on startup:
	- If using an external DB (Postgres/MySQL), the container may start before the DB is ready. Consider adding a DB readiness/wait loop in `entrypoint.sh` or using `depends_on` and healthchecks in `docker-compose.yml`.
- Seed command errors:
	- The seed command (`seed_routes`) is executed but intentionally wrapped so it won't stop the container on failure. Check its output in the logs; if it fails, run it manually inside the container to debug:

```powershell
docker-compose run --rm web python manage.py seed_routes
```

## Next improvements (optional)

- Add a retry/wait loop in `entrypoint.sh` to wait for the DB host/port before running migrations.
- Add a `db` service (Postgres) in `docker-compose.yml` with a proper healthcheck.
- Use gunicorn/uvicorn in production instead of Django's dev server.

---
If you'd like, I can add the DB wait/retry loop and an example `db` service to `docker-compose.yml`. Tell me which DB you'd prefer (Postgres or MySQL) and whether you want volumes created for persistence.
