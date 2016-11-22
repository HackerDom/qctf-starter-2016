#!/bin/bash
set -e

case "$1" in
"manage.py")
    exec python "$@"
    ;;
*)
    python manage.py collectstatic --noinput
    python manage.py makemigrations
    python manage.py migrate

    exec gunicorn qctf_checksystem.wsgi --config gunicorn.conf.py
    ;;
esac
