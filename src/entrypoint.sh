#!/bin/bash

wait_for () {
    for _ in `seq 0 100`; do
        (echo > /dev/tcp/$1/$2) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$1:$2 accepts connections"
            break
        fi
        sleep 1
    done
}

case "$PROCESS" in
"LINT")
    mypy . && flake8 . && bandit -r . && safety check
    ;;
"DEV_DJANGO")
    wait_for "${POSTGRES_HOST}" "${POSTGRES_PORT}"
    python manage.py collectstatic --noinput &&
    python manage.py makemigrations &&
    python manage.py migrate &&
    python manage.py create_standard_admin_setting &&
    python manage.py runserver 0.0.0.0:8000
#    uvicorn config.asgi:application --reload-dir apps --debug --host 0.0.0.0 --port 8080 --log-level info --use-colors
#    gunicorn config.asgi:application --workers 4 --reload --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker --capture-output --log-level info --access-logfile -
    ;;
esac