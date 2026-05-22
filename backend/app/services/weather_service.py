from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.weather_log import WeatherLog
from app.core.config import settings
import httpx
import json
from datetime import datetime, timezone


class WeatherService:
    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.api_key = settings.WEATHER_API_KEY

    async def get_current_weather(self, location: str) -> dict:
        if not self.api_key:
            return self._get_fallback_weather(location)

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/weather",
                    params={"q": location, "appid": self.api_key, "units": "metric"},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()

                weather = {
                    "location": location,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "temp_min": data["main"]["temp_min"],
                    "temp_max": data["main"]["temp_max"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_direction": data.get("wind", {}).get("deg"),
                    "weather_condition": data["weather"][0]["main"],
                    "weather_description": data["weather"][0]["description"],
                    "weather_icon": data["weather"][0]["icon"],
                    "rainfall_mm": data.get("rain", {}).get("1h"),
                    "cloud_cover": data.get("clouds", {}).get("all"),
                    "visibility": data.get("visibility"),
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                }

                if self.db:
                    repo = BaseRepository(self.db, WeatherLog)
                    await repo.create(location=location, **{k: v for k, v in weather.items() if k != "location"})

                return weather
            except Exception:
                return self._get_fallback_weather(location)

    async def get_forecast(self, location: str, days: int = 5) -> dict:
        if not self.api_key:
            return {"location": location, "forecast": [], "generated_at": datetime.now(timezone.utc).isoformat()}

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{self.base_url}/forecast",
                    params={"q": location, "appid": self.api_key, "units": "metric", "cnt": days * 8},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()

                daily_forecast = {}
                for item in data["list"]:
                    date = item["dt_txt"].split()[0]
                    if date not in daily_forecast:
                        daily_forecast[date] = {
                            "date": date,
                            "temp_min": item["main"]["temp_min"],
                            "temp_max": item["main"]["temp_max"],
                            "humidity": item["main"]["humidity"],
                            "condition": item["weather"][0]["description"],
                            "icon": item["weather"][0]["icon"],
                            "wind_speed": item["wind"]["speed"],
                            "rainfall": item.get("rain", {}).get("3h", 0),
                        }

                return {
                    "location": location,
                    "forecast": list(daily_forecast.values())[:days],
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                }
            except Exception:
                return {"location": location, "forecast": [], "generated_at": datetime.now(timezone.utc).isoformat()}

    async def get_farming_recommendations(self, location: str) -> dict:
        weather = await self.get_current_weather(location)
        forecast = await self.get_forecast(location)

        temp = weather.get("temperature", 25)
        humidity = weather.get("humidity", 60)
        condition = weather.get("weather_condition", "Clear")
        rainfall = weather.get("rainfall_mm", 0)

        advice_parts = []
        pesticide_advice = None
        irrigation_advice = None
        harvest_advice = None
        alerts = []

        if temp > 35:
            advice_parts.append("High temperature stress. Ensure adequate irrigation and consider shade nets for sensitive crops.")
            alerts.append("Heat wave warning: temperatures above 35°C")
        elif temp < 15:
            advice_parts.append("Low temperature. Protect crops with mulch or row covers. Delay sowing if possible.")

        if humidity > 80:
            advice_parts.append("High humidity. Monitor for fungal diseases. Consider preventive fungicide application.")
            pesticide_advice = "High humidity increases disease risk. Apply preventive fungicide within 2-3 days."
            alerts.append("High humidity alert: increased risk of fungal diseases")
        elif humidity < 30:
            advice_parts.append("Low humidity. Increase irrigation frequency. Monitor for pest infestations.")

        if condition in ["Rain", "Drizzle", "Thunderstorm"]:
            advice_parts.append("Rain expected. Avoid spraying pesticides. Ensure proper drainage in fields.")
            irrigation_advice = "Rain expected, skip irrigation for 1-2 days."
        elif condition == "Clear" and temp > 30:
            irrigation_advice = "High evaporation expected. Irrigate early morning or late evening."

        advice_parts.append("Regularly monitor crop health. Maintain proper nutrient management.")

        return {
            "location": location,
            "current_weather": weather,
            "farming_advice": " ".join(advice_parts),
            "pesticide_advice": pesticide_advice,
            "irrigation_advice": irrigation_advice,
            "harvest_advice": harvest_advice,
            "alerts": alerts,
        }

    def _get_fallback_weather(self, location: str) -> dict:
        return {
            "location": location,
            "temperature": 28.0,
            "feels_like": 30.0,
            "temp_min": 25.0,
            "temp_max": 32.0,
            "humidity": 65.0,
            "pressure": 1013.0,
            "wind_speed": 3.5,
            "wind_direction": 180.0,
            "weather_condition": "Clear",
            "weather_description": "clear sky",
            "weather_icon": "01d",
            "rainfall_mm": 0.0,
            "cloud_cover": 10.0,
            "visibility": 10000.0,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
