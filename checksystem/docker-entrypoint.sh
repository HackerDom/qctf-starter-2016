#!/bin/bash
set -e

case "$1" in
"manage.py")
    exec python "$@"
    ;;
*)
    python manage.py collectstatic --noinput
    python manage.py migrate --noinput

    exec gunicorn qctf_checksystem.wsgi --config gunicorn.conf.py
    ;;
esac
