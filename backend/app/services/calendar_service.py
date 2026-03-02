from datetime import timedelta
import logging

from gcsa.attendee import Attendee
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar

from app.config.settings import settings
from app.models.date_model import DateModel


def create_event(email: str, comments: str | None, date_obj: DateModel, start_dt):
    description_lines = [date_obj.challenge]
    if comments:
        description_lines.append("")
        description_lines.append(f"Comments: {comments}")
    description = "\n".join(description_lines)

    event = Event(
        summary=date_obj.name,
        start=start_dt,
        end=start_dt + timedelta(hours=2),
        description=description,
        attendees=[Attendee(email)],
    )

    try:
        calendar = GoogleCalendar(
            calendar=settings.calendar_id,
            credentials_path=settings.calendar_credentials_path,
        )
        created = calendar.add_event(event)
        return getattr(created, "id", None)
    except Exception:
        logging.exception("Failed to create calendar event")
        raise
