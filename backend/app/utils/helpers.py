import uuid
import os
from datetime import datetime, timezone
from typing import Optional


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_filename(ext: str = ".jpg") -> str:
    return f"{uuid.uuid4()}{ext}"


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def format_datetime(dt: Optional[datetime] = None) -> str:
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()
