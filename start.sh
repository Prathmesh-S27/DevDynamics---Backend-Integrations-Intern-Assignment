#!/bin/bash

# Validate and set PORT variable
if [ -z "$PORT" ]; then
    PORT=8000
elif ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "Invalid PORT value: $PORT. Using default port 8000"
    PORT=8000
fi

echo "🚀 Starting Smart Event Planner API"
echo "Port: $PORT"
echo "Environment: ${NODE_ENV:-production}"
echo "Database URL configured: ${DATABASE_URL:+yes}"

# Create SQLite database directory if needed
mkdir -p /app/data

# Start the application with better error handling
exec uvicorn src.main:app --host 0.0.0.0 --port "$PORT" --workers 1 --access-log
