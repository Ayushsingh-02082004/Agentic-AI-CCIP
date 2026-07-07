#!/bin/sh
# Startup script for FastAPI backend
# Resolves $PORT from Railway, falls back to 8000 locally
exec uvicorn backend.api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
