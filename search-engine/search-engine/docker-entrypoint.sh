#!/bin/bash
set -e

case "$1" in
"gunicorn")
    exec gunicorn --config gunicorn.conf.py "$2"
    ;;
*)
    exec "$@"
	;;
esac
