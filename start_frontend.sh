#!/bin/sh
# Startup script for Streamlit frontend
# Resolves $PORT from Railway, falls back to 8501 locally
exec streamlit run frontend/app.py \
    --server.port "${PORT:-8501}" \
    --server.address 0.0.0.0 \
    --server.headless true
