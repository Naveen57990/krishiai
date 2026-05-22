from app.celery_app import celery_app
from app.core.config import settings
from loguru import logger


@celery_app.task
def process_disease_image(image_path: str):
    logger.info(f"Processing disease image: {image_path}")
    try:
        from ai_services.disease_detection.inference import DiseaseDetector
        detector = DiseaseDetector()
        result = detector.predict(image_path)
        return result
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        return {"error": str(e)}


@celery_app.task
def update_weather_cache(location: str):
    logger.info(f"Updating weather cache for: {location}")
    import httpx
    import json
    try:
        response = httpx.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={"q": location, "appid": settings.WEATHER_API_KEY, "units": "metric"},
            timeout=10,
        )
        data = response.json()
        logger.info(f"Weather cache updated for {location}")
        return data
    except Exception as e:
        logger.error(f"Weather update failed: {e}")
        return {"error": str(e)}


@celery_app.task
def cleanup_old_records():
    logger.info("Running cleanup of old records")
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import create_engine, text

    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    engine = create_engine(settings.DATABASE_URL_SYNC)

    with engine.connect() as conn:
        conn.execute(text(f"DELETE FROM voice_logs WHERE created_at < '{cutoff.isoformat()}'"))
        conn.execute(text(f"DELETE FROM chatbot_history WHERE created_at < '{cutoff.isoformat()}'"))
        conn.commit()

    logger.info("Cleanup completed")
    return {"cleaned_up_to": cutoff.isoformat()}
