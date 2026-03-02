from datetime import datetime
from pathlib import Path
import json
import logging

from app.config.settings import settings
from app.models.date_model import DateModel


def save_booking(email: str, comments: str | None, date_obj: DateModel, start_dt: datetime) -> None:
    path = Path(settings.bookings_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "email": email,
        "comments": comments,
        "date_id": date_obj.id,
        "date_name": date_obj.name,
        "date": date_obj.date,
        "scheduled_start": start_dt.isoformat(),
    }

    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as file_handle:
                data = json.load(file_handle)
        else:
            data = []

        data.append(entry)
        with path.open("w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle, ensure_ascii=False, indent=2)
    except Exception:
        logging.exception("Failed to save booking")
        raise
