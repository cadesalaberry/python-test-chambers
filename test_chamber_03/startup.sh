#!/usr/bin/env bash

set -e

EXTRA_GUNICORN_FLAGS=

if [ "${DEVELOPMENT:=no}" = "yes" ]; then
    echo 'DEVELOPMENT'
    EXTRA_GUNICORN_FLAGS=--reload
else
    echo 'PRODUCTION'
fi

./manage.py migrate
exec /usr/local/bin/gunicorn test_chamber.wsgi:application -w ${WORKERS:=4} -b :8000 ${EXTRA_GUNICORN_FLAGS}
