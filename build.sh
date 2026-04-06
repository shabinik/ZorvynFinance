#!/usr/bin/env bash
set -o errexit
cd finance_dashboard
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_admin