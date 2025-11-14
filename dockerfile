# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Prevent Python from writing .pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# Install system dependencies needed for psycopg2 + build tools
RUN apt-get update \
    && apt-get install -y gcc libpq-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy FastAPI project files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Optional: HEALTHCHECK for container orchestration
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
