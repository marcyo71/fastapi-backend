#!/bin/bash
set -e

echo "⏳ Attendo che il database sia pronto..."
sleep 3

echo "🚀 Applico migrazioni Alembic..."
alembic upgrade head

echo "🔥 Avvio FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
