from email.message import EmailMessage
from pathlib import Path
import logging
import smtplib

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config.settings import settings
from app.models.date_model import DateModel
from app.utils.ics_generator import build_ics

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"


def send_booking_email(email: str, comments: str | None, date_obj: DateModel, start_dt):
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("email_template.html")
    html_body = template.render(
        name=date_obj.name,
        date=date_obj.date,
        challenge=date_obj.challenge,
        dress_code=date_obj.dress_code,
        comments=comments or "No comments",
    )

    text_body = (
        f"Your booking is confirmed for {date_obj.name} on {date_obj.date}.\n"
        f"Challenge: {date_obj.challenge}\n"
        f"Comments: {comments or 'No comments'}"
    )

    message = EmailMessage()
    message["Subject"] = f"Booking confirmed: {date_obj.name}"
    message["From"] = settings.smtp_email
    message["To"] = ", ".join([email, "nvelezcuauro@gmail.com"])
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    ics_content = build_ics(date_obj, start_dt)
    message.add_attachment(
        ics_content,
        subtype="calendar",
        filename="invite.ics",
    )

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(settings.smtp_email, settings.smtp_password)
            smtp.send_message(message)
    except Exception:
        logging.exception("Failed to send booking email")
        raise
