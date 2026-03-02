import logging

from app.config.settings import settings
from app.models.date_model import DateModel
from app.services.booking_store import save_booking
from app.services.email_service import send_booking_email
from app.utils.date_parser import parse_date


def create_booking(email: str, comments: str | None, date_obj: DateModel) -> str | None:
    try:
        start_dt = parse_date(date_obj.date, settings.timezone)
        send_booking_email(email, comments, date_obj, start_dt)
        save_booking(email, comments, date_obj, start_dt)
        return None
    except Exception:
        logging.exception("Booking service failed")
        raise
