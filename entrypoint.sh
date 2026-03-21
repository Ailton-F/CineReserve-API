#!/bin/sh

set -e

# Run migrations
echo "Running migrations..."
python src/manage.py migrate --noinput

if [ "$DJANGO_DEBUG" = "True" ]; then
    echo "Environment is in DEBUG mode. Checking if seeding is needed..."
    python src/manage.py seed_data
fi

exec "$@"