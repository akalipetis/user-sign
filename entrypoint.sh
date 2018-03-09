#!/bin/bash

set -xe

# Wait for the database to be available if needed
# Run migrate if needed
if [[ ${CHECK_POSTGRES} == "1" ]]; then
    dockerize -wait tcp://${POSTGRES_HOST:-postgres}:${POSTGRES_PORT:-5432}
fi

# Run migrate if needed
if [[ ${RUN_MIGRATE} == "1" ]]; then
    ./manage.py migrate --noinput
fi

# Run collectstatic if needed
if [[ ${RUN_COLLECTSTATIC} == "1" ]]; then
    ./manage.py collectstatic --noinput
fi

# Execute subcommand, wrapping
exec "$@"
