import logging

from app.config.settings import settings
from app.models.date_model import DateModel
from app.services.calendar_service import create_event
from app.services.email_service import send_booking_email
from app.utils.date_parser import parse_date


def create_booking(email: str, comments: str | None, date_obj: DateModel) -> str | None:
    try:
        start_dt = parse_date(date_obj.date, settings.timezone)
        event_id = create_event(email, comments, date_obj, start_dt)
        send_booking_email(email, comments, date_obj)
        return event_id
    except Exception:
        logging.exception("Booking service failed")
        raise
