#!/bin/sh
# Entrypoint for Docker container: run migrations, create admin, seed data, then start server
set -e

echo "Waiting for DB (brief sleep)..."
sleep 1

echo "Running makemigrations"
python manage.py makemigrations --noinput || true

echo "Running migrate"
python manage.py migrate --noinput

# Ensure settings module is defined for non-management python invocations
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-flight_routes.settings}

# Create superuser non-interactively if it doesn't exist using manage.py shell
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@gmail.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin}

echo "Creating superuser if not exists: $DJANGO_SUPERUSER_USERNAME"
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
u = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
e = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@gmail.com')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

print('checking user', u)
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(username=u, email=e, password=p)
    print('created superuser', u)
else:
    print('superuser exists', u)
PY

echo "Running seed_routes command"
python manage.py seed_routes || true

echo "Starting Django development server"
exec python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
