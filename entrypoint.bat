@echo off
setlocal enabledelayedexpansion

REM Run database migrations
python manage.py migrate --noinput

REM Seed airports and routes
python manage.py seed_routes

REM Create superuser if not existing
python -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')"

REM Start the Django development server
python manage.py runserver 0.0.0.
