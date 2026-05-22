#!/bin/bash
set -e

echo "========================================"
echo "  KrishiAI - AI Agriculture Assistant"
echo "  Setup Script"
echo "========================================"

echo ""
echo "1. Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
echo "   ✓ Docker found"
echo "   ✓ Python found"

echo ""
echo "2. Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   ✓ Created .env from .env.example"
    echo "   ⚠  Edit .env to add your API keys before running"
else
    echo "   ✓ .env already exists"
fi

echo ""
echo "3. Creating directories..."
mkdir -p backend/uploads/{diseases,audio}
mkdir -p ai-services/{disease_detection,recommendation,yield_prediction}/models
mkdir -p data/{chroma,memory}
mkdir -p nginx/ssl
echo "   ✓ Directories created"

echo ""
echo "4. Installing backend dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..
echo "   ✓ Backend dependencies installed"

echo ""
echo "5. Installing frontend dependencies..."
cd frontend
npm install 2>/dev/null || echo "   ⚠ npm not available, skip frontend setup"
cd ..
echo "   ✓ Frontend dependencies installed"

echo ""
echo "6. Starting Docker services..."
docker compose up -d db redis
echo "   ✓ Database and Redis started"
echo "   Waiting for database to be ready..."
sleep 5

echo ""
echo "7. Running database migrations..."
docker compose run --rm backend alembic upgrade head 2>/dev/null || \
    echo "   ⚠ Migrations skipped (run manually: docker compose exec backend alembic upgrade head)"

echo ""
echo "8. Seeding database..."
docker compose run --rm backend python -m app.db.seed_data 2>/dev/null || \
    echo "   ⚠ Seeding skipped (run manually: docker compose exec backend python -m app.db.seed_data)"

echo ""
echo "========================================"
echo "  ✅ KrishiAI setup complete!"
echo "========================================"
echo ""
echo "  Start all services:  docker compose up -d"
echo "  View API docs:       http://localhost:8000/docs"
echo "  Run frontend:        cd frontend && npx expo start"
echo ""
echo "  Default credentials:"
echo "    PgAdmin: admin@krishiai.com / admin"
echo "    MinIO:   minioadmin / minioadmin"
echo ""
echo "  Don't forget to:"
echo "  1. Edit .env with your API keys"
echo "  2. Generate SSL certs for production"
echo "  3. Change default passwords"
echo "========================================"
