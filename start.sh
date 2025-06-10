#!/bin/bash

# Set default port if PORT is not set or is empty
if [ -z "$PORT" ]; then
    export PORT=8000
fi

echo "Starting uvicorn on port $PORT"

# Start the application
exec uvicorn src.main:app --host 0.0.0.0 --port $PORT --reload
