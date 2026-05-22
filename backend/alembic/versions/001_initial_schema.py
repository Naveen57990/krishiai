"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-01-01
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("phone", sa.String(20), unique=True, nullable=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("farmer", "admin", "extension_officer", name="userrole"), nullable=False, server_default="farmer"),
        sa.Column("preferred_language", sa.String(10), server_default="en"),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("farm_size", sa.Float(), nullable=True),
        sa.Column("soil_type", sa.String(100), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("is_verified", sa.Boolean(), server_default="false"),
        sa.Column("profile_image_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "crops",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("name_te", sa.String(255), nullable=True),
        sa.Column("name_hi", sa.String(255), nullable=True),
        sa.Column("scientific_name", sa.String(255), nullable=True),
        sa.Column("crop_type", sa.String(100), nullable=True),
        sa.Column("season", sa.String(100), nullable=True),
        sa.Column("soil_type", sa.String(100), nullable=True),
        sa.Column("min_ph", sa.Float(), nullable=True),
        sa.Column("max_ph", sa.Float(), nullable=True),
        sa.Column("min_rainfall", sa.Float(), nullable=True),
        sa.Column("max_rainfall", sa.Float(), nullable=True),
        sa.Column("min_temperature", sa.Float(), nullable=True),
        sa.Column("max_temperature", sa.Float(), nullable=True),
        sa.Column("growing_period_days", sa.Integer(), nullable=True),
        sa.Column("water_requirement", sa.String(100), nullable=True),
        sa.Column("nutrition_info", sa.JSON(), nullable=True),
        sa.Column("common_pests", sa.JSON(), nullable=True),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "crop_diseases",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("crop_id", sa.Integer(), nullable=False),
        sa.Column("disease_name", sa.String(255), nullable=False),
        sa.Column("disease_name_te", sa.String(255), nullable=True),
        sa.Column("disease_name_hi", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("symptoms", sa.JSON(), nullable=True),
        sa.Column("causes", sa.Text(), nullable=True),
        sa.Column("treatment", sa.Text(), nullable=True),
        sa.Column("treatment_te", sa.Text(), nullable=True),
        sa.Column("treatment_hi", sa.Text(), nullable=True),
        sa.Column("prevention", sa.Text(), nullable=True),
        sa.Column("organic_treatment", sa.Text(), nullable=True),
        sa.Column("chemical_treatment", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(50), server_default="medium"),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("confidence_threshold", sa.Float(), server_default="0.5"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "disease_reports",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("farmer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("crop_id", sa.Integer(), nullable=True),
        sa.Column("crop_name", sa.String(255), nullable=True),
        sa.Column("disease_name", sa.String(255), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("image_thumbnail_url", sa.String(500), nullable=True),
        sa.Column("treatment_recommended", sa.Text(), nullable=True),
        sa.Column("organic_treatment", sa.Text(), nullable=True),
        sa.Column("chemical_treatment", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(50), nullable=True),
        sa.Column("is_resolved", sa.Boolean(), server_default="false"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("location_lat", sa.Float(), nullable=True),
        sa.Column("location_lng", sa.Float(), nullable=True),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "chatbot_history",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("session_id", sa.String(100), index=True, nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column("language", sa.String(10), server_default="en"),
        sa.Column("message_type", sa.String(50), server_default="text"),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("tokens_used", sa.Integer(), nullable=True),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "weather_logs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("location", sa.String(255), index=True, nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("feels_like", sa.Float(), nullable=True),
        sa.Column("temp_min", sa.Float(), nullable=True),
        sa.Column("temp_max", sa.Float(), nullable=True),
        sa.Column("humidity", sa.Float(), nullable=True),
        sa.Column("pressure", sa.Float(), nullable=True),
        sa.Column("wind_speed", sa.Float(), nullable=True),
        sa.Column("wind_direction", sa.Float(), nullable=True),
        sa.Column("weather_condition", sa.String(100), nullable=True),
        sa.Column("weather_description", sa.String(255), nullable=True),
        sa.Column("weather_icon", sa.String(50), nullable=True),
        sa.Column("rainfall_mm", sa.Float(), nullable=True),
        sa.Column("cloud_cover", sa.Float(), nullable=True),
        sa.Column("uv_index", sa.Float(), nullable=True),
        sa.Column("visibility", sa.Float(), nullable=True),
        sa.Column("forecast", sa.JSON(), nullable=True),
        sa.Column("raw_data", sa.JSON(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("crop_name", sa.String(255), nullable=False),
        sa.Column("crop_name_te", sa.String(255), nullable=True),
        sa.Column("crop_name_hi", sa.String(255), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("soil_type", sa.String(100), nullable=True),
        sa.Column("ph_level", sa.Float(), nullable=True),
        sa.Column("rainfall_mm", sa.Float(), nullable=True),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("season", sa.String(50), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("profitability_estimate", sa.Float(), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=True),
        sa.Column("risk_factors", sa.JSON(), nullable=True),
        sa.Column("farming_tips", sa.JSON(), nullable=True),
        sa.Column("is_adopted", sa.Boolean(), server_default="false"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "yield_predictions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("crop_name", sa.String(255), nullable=False),
        sa.Column("area_hectares", sa.Float(), nullable=False),
        sa.Column("predicted_yield_kg", sa.Float(), nullable=True),
        sa.Column("predicted_yield_per_hectare", sa.Float(), nullable=True),
        sa.Column("confidence_interval_lower", sa.Float(), nullable=True),
        sa.Column("confidence_interval_upper", sa.Float(), nullable=True),
        sa.Column("soil_type", sa.String(100), nullable=True),
        sa.Column("ph_level", sa.Float(), nullable=True),
        sa.Column("rainfall_mm", sa.Float(), nullable=True),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("fertilizer_usage", sa.String(255), nullable=True),
        sa.Column("irrigation_method", sa.String(100), nullable=True),
        sa.Column("seed_variety", sa.String(255), nullable=True),
        sa.Column("planting_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("harvest_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("historical_yield", sa.Float(), nullable=True),
        sa.Column("weather_impact_score", sa.Float(), nullable=True),
        sa.Column("model_used", sa.String(100), nullable=True),
        sa.Column("model_version", sa.String(50), nullable=True),
        sa.Column("features_used", sa.JSON(), nullable=True),
        sa.Column("recommendations", sa.JSON(), nullable=True),
        sa.Column("actual_yield_kg", sa.Float(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "voice_logs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("session_id", sa.String(100), index=True, nullable=False),
        sa.Column("audio_url", sa.String(500), nullable=True),
        sa.Column("audio_duration_seconds", sa.Float(), nullable=True),
        sa.Column("transcript", sa.Text(), nullable=True),
        sa.Column("translated_text", sa.Text(), nullable=True),
        sa.Column("source_language", sa.String(10), nullable=True),
        sa.Column("target_language", sa.String(10), server_default="en"),
        sa.Column("response_text", sa.Text(), nullable=True),
        sa.Column("response_audio_url", sa.String(500), nullable=True),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "farmer_memories",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("memory_type", sa.String(50), nullable=False),
        sa.Column("key", sa.String(255), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("embedding_id", sa.String(100), nullable=True),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("importance_score", sa.Float(), server_default="0.5"),
        sa.Column("access_count", sa.Integer(), server_default="0"),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index("idx_disease_reports_farmer", "disease_reports", ["farmer_id", "created_at"])
    op.create_index("idx_chatbot_session", "chatbot_history", ["user_id", "session_id"])
    op.create_index("idx_weather_location_time", "weather_logs", ["location", "recorded_at"])
    op.create_index("idx_recommendations_user", "recommendations", ["user_id", "created_at"])
    op.create_index("idx_yield_user", "yield_predictions", ["user_id", "created_at"])
    op.create_index("idx_voice_user_session", "voice_logs", ["user_id", "session_id"])
    op.create_index("idx_memories_user", "farmer_memories", ["user_id", "memory_type"])


def downgrade() -> None:
    op.drop_table("farmer_memories")
    op.drop_table("voice_logs")
    op.drop_table("yield_predictions")
    op.drop_table("recommendations")
    op.drop_table("weather_logs")
    op.drop_table("chatbot_history")
    op.drop_table("disease_reports")
    op.drop_table("crop_diseases")
    op.drop_table("crops")
    op.drop_table("users")
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=False)
