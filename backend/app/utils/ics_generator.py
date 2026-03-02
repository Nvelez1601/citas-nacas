from datetime import datetime, timedelta, timezone
import uuid

from app.models.date_model import DateModel


def _format_dt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def build_ics(date_obj: DateModel, start_dt: datetime) -> str:
    end_dt = start_dt + timedelta(hours=2)
    uid = f"{uuid.uuid4()}@citas-nacas"

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Citas Nacas//Booking//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:REQUEST",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{_format_dt(datetime.now(timezone.utc))}Z",
        f"DTSTART:{_format_dt(start_dt)}",
        f"DTEND:{_format_dt(end_dt)}",
        f"SUMMARY:{date_obj.name}",
        f"DESCRIPTION:{date_obj.challenge}",
        "END:VEVENT",
        "END:VCALENDAR",
    ]

    return "\r\n".join(lines)
