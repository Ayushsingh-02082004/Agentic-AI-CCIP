FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make startup scripts executable
RUN chmod +x start_backend.sh start_frontend.sh

# Default: start FastAPI backend
# Override with: sh start_frontend.sh for Streamlit service on Railway
CMD ["sh", "start_backend.sh"]
