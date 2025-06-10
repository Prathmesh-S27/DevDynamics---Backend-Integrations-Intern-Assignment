#!/bin/bash

echo "🧪 Running Smart Event Planner Tests..."

# Check if containers are running
if ! docker-compose ps | grep -q "web.*Up"; then
    echo "Starting containers..."
    docker-compose up -d
    echo "Waiting for services to be ready..."
    sleep 10
fi

# Run tests
echo "Running pytest..."
docker-compose exec web pytest tests/ -v --tb=short

echo "✅ Tests completed!"
