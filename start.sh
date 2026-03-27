#!/usr/bin/env bash
set -e

cd /app/frontend
npm run start -- --hostname 0.0.0.0 --port 3000 &

cd /app
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
