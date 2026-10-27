#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Create the superuser automatically (fails silently if it already exists)
python manage.py createsuperuser --no-input || true