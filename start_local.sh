#!/usr/bin/env bash
set -e
export $(grep -v '^#' .env | xargs)
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..
uvicorn app.main:app --reload --host 0.0.0.0 --port 10000
kill $FRONTEND_PID
