from fastapi import APIRouter
from app.api.v1 import auth, disease, chatbot, voice, weather, recommendation, yield_prediction, memory, health

router = APIRouter(prefix="/api/v1")
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(disease.router, prefix="/disease", tags=["Disease Detection"])
router.include_router(chatbot.router, prefix="/chatbot", tags=["AI Chatbot"])
router.include_router(voice.router, prefix="/voice", tags=["Voice Assistant"])
router.include_router(weather.router, prefix="/weather", tags=["Weather Intelligence"])
router.include_router(recommendation.router, prefix="/recommendations", tags=["Crop Recommendations"])
router.include_router(yield_prediction.router, prefix="/yield", tags=["Yield Prediction"])
router.include_router(memory.router, prefix="/memory", tags=["Farmer Memory"])
