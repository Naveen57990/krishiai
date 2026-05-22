# 🌾 KrishiAI — AI Agriculture Assistant

> AI-powered agriculture platform for Indian farmers with multilingual support (English, Telugu, Hindi)

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔬 **Disease Detection** | Upload plant photos, AI detects diseases & recommends treatments |
| 🤖 **AI Chatbot** | Multilingual farming assistant with weather-aware responses |
| 🎤 **Voice Assistant** | Voice queries in Telugu/Hindi/English with STT & TTS |
| 🌤️ **Weather Intelligence** | Real-time weather, forecasts & farming recommendations |
| 🌱 **Crop Recommendation** | ML-based crop suggestions based on soil, climate & season |
| 📊 **Yield Prediction** | AI predicts crop yield based on farm parameters |
| 🧠 **Farmer Memory** | Long-term memory system for personalized recommendations |
| 🔐 **Authentication** | Secure JWT-based auth with role-based access |
| 🚀 **Production Ready** | Docker, CI/CD, monitoring, auto-scaling |

## 🏗️ Architecture

```
krishiai/
├── frontend/          # React Native (Expo) mobile app
├── backend/           # FastAPI async REST API
├── ai-services/       # ML inference services
├── ml-training/       # Model training pipelines
├── docker/           # Docker configurations
├── nginx/            # Reverse proxy configs
├── monitoring/       # Prometheus & Grafana
├── .github/          # CI/CD workflows
└── infrastructure/   # Terraform & K8s configs
```

## 🛠️ Tech Stack

**Frontend:** React Native, Expo, TypeScript, React Navigation  
**Backend:** FastAPI, Python 3.11, SQLAlchemy, PostgreSQL, Redis, Celery  
**AI/ML:** PyTorch, Google Gemini, OpenAI, Whisper, YOLOv8, scikit-learn, ChromaDB  
**Infrastructure:** Docker, Docker Compose, Nginx, GitHub Actions, Prometheus, Grafana  

## 📋 Prerequisites

- Docker & Docker Compose v2+
- Python 3.11+
- Node.js 20+
- Expo CLI (`npm install -g expo-cli`)
- OpenAI / Gemini API keys

## 🚦 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/your-org/krishiai.git
cd krishiai
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run with Docker

```bash
docker compose up -d
```

### 3. Seed Database

```bash
docker compose exec backend python -m app.db.seed_data
```

### 4. Access Services

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PgAdmin | http://localhost:5050 |
| MinIO | http://localhost:9001 |

### 5. Run Frontend (Development)

```bash
cd frontend
npm install
npx expo start
```

## 📚 API Documentation

Full API documentation available at `/docs` when running.

### Authentication

```
POST /api/v1/auth/signup    - Create account
POST /api/v1/auth/login     - Login
POST /api/v1/auth/refresh   - Refresh token
GET  /api/v1/auth/me        - Get profile
PUT  /api/v1/auth/me        - Update profile
```

### Disease Detection

```
POST /api/v1/disease/detect      - Upload & detect disease
GET  /api/v1/disease/reports     - Get detection history
GET  /api/v1/disease/reports/:id - Get single report
```

### AI Chatbot

```
POST /api/v1/chatbot/chat        - Chat with AI
POST /api/v1/chatbot/anonymous   - Anonymous chat
GET  /api/v1/chatbot/history/:id - Conversation history
```

### Voice Assistant

```
POST /api/v1/voice/process  - Process voice input
POST /api/v1/voice/tts      - Text to speech
GET  /api/v1/voice/history  - Voice interaction history
```

### Weather

```
GET  /api/v1/weather/current       - Current weather
GET  /api/v1/weather/forecast      - Weather forecast
GET  /api/v1/weather/farming-advice - Farming recommendations
```

### Crop Recommendations

```
POST /api/v1/recommendations/crop  - Get crop suggestions
GET  /api/v1/recommendations/history - History
```

### Yield Prediction

```
POST /api/v1/yield/predict  - Predict crop yield
GET  /api/v1/yield/history  - Prediction history
```

## 🌐 Supported Languages

- English (en)
- తెలుగు - Telugu (te)
- हिन्दी - Hindi (hi)

## 🐳 Docker Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend

# Restart a service
docker compose restart backend

# Run migrations
docker compose exec backend alembic upgrade head

# Seed data
docker compose exec backend python -m app.db.seed_data

# Run tests
docker compose exec backend pytest

# Stop everything
docker compose down

# Full clean restart
docker compose down -v && docker compose up -d
```

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests
cd frontend && npm test

# Run specific test
pytest tests/test_auth.py -v
```

## 🚀 Deployment

### Railway

```bash
railway login
railway init
railway up
```

### AWS ECS

```bash
cd infrastructure/terraform
terraform init
terraform apply
```

### Render

Connect GitHub repo → Select service → Deploy

## 📊 Monitoring

- **Prometheus** metrics at `/metrics`
- **Grafana** dashboards for visualization
- Pre-configured PostgreSQL & Redis monitoring

## 🔒 Security

- JWT authentication with refresh tokens
- Password hashing (bcrypt)
- Rate limiting (100 req/hour default)
- CORS protection
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy)
- HTTPS-ready Nginx config
- Secure secrets management (.env)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- PlantVillage dataset for disease detection training
- OpenWeatherMap for weather data
- Google Gemini & OpenAI for AI capabilities

---

Built with ❤️ for Indian farmers
