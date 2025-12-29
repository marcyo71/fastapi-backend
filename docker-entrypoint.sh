#!/bin/sh
set -e

# Default locale se Railway non passa PORT
PORT=${PORT:-8000}

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Uvicorn on port $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
