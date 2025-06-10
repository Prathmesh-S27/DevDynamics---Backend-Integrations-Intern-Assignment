#!/bin/bash

# Validate and set PORT variable
if [ -z "$PORT" ]; then
    PORT=8000
elif ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "Invalid PORT value: $PORT. Using default port 8000"
    PORT=8000
fi

echo "Starting uvicorn on port $PORT"
echo "Environment: ${NODE_ENV:-production}"
echo "Database URL configured: ${DATABASE_URL:+yes}"

# Wait a moment for database to be ready if in production
if [[ "${DATABASE_URL}" == *"postgresql"* ]]; then
    echo "Waiting for database to be ready..."
    sleep 5
fi

# Start the application
exec uvicorn src.main:app --host 0.0.0.0 --port "$PORT" --workers 1
