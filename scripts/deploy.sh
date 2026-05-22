#!/bin/bash
set -e

ENV=${1:-production}
echo "Deploying KrishiAI to $ENV environment..."

if [ "$ENV" = "production" ]; then
    echo "Building production images..."
    docker compose -f docker-compose.yml build --no-cache

    echo "Running migrations..."
    docker compose run --rm backend alembic upgrade head

    echo "Starting production services..."
    docker compose -f docker-compose.yml up -d

    echo "Running health check..."
    sleep 5
    curl -f http://localhost:8000/api/v1/health || echo "Health check pending..."

elif [ "$ENV" = "staging" ]; then
    docker compose -f docker-compose.yml up -d --build

elif [ "$ENV" = "rollback" ]; then
    echo "Rolling back to previous version..."
    docker compose pull backend
    docker compose up -d --no-deps backend

else
    echo "Usage: ./scripts/deploy.sh [production|staging|rollback]"
    exit 1
fi

echo "Deployment to $ENV completed!"
