.PHONY: help setup dev build test deploy clean

help:
	@echo "KrishiAI - AI Agriculture Assistant"
	@echo ""
	@echo "Commands:"
	@echo "  make setup      - Initial setup (install deps, create dirs)"
	@echo "  make dev        - Start development environment"
	@echo "  make build      - Build production images"
	@echo "  make test       - Run tests"
	@echo "  make deploy     - Deploy to production"
	@echo "  make clean      - Clean up"

setup:
	@echo "Setting up KrishiAI..."
	cp -n .env.example .env 2>/dev/null || true
	pip install -r backend/requirements.txt
	cd frontend && npm install 2>/dev/null || true
	mkdir -p backend/uploads/diseases backend/uploads/audio
	docker compose up -d db redis
	@echo "Setup complete! Start with: make dev"

dev:
	docker compose up -d
	@echo "Access API at http://localhost:8000"
	@echo "Access Docs at http://localhost:8000/docs"

build:
	docker compose build

test:
	cd backend && python -m pytest tests/ -v

deploy:
	@echo "Deploying to production..."
	docker compose -f docker-compose.yml build
	docker compose -f docker-compose.yml up -d

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python -m app.db.seed_data

logs:
	docker compose logs -f backend

clean:
	docker compose down -v
	@echo "Cleaned up all containers and volumes"
