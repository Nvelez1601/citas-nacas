from email.message import EmailMessage
from pathlib import Path
import logging
import smtplib

from jinja2 import Environment, FileSystemLoader, select_autoescape
from mailersend import MailerSendClient, EmailBuilder

from app.config.settings import settings
from app.models.date_model import DateModel
from app.utils.ics_generator import build_ics

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"


def _send_via_mailersend(message: EmailMessage):
    api_key = settings.mailersend_api_key
    if not api_key:
        raise RuntimeError("MAILERSEND_API_KEY not configured")

    from_email = settings.mailersend_from_email or settings.smtp_email
    from_name = settings.mailersend_from_name
    to_addrs = [a.strip() for a in message.get("To", "").split(",") if a.strip()]

    builder = EmailBuilder().from_email(from_email, from_name).to_many(
        [{"email": addr} for addr in to_addrs]
    ).subject(message.get("Subject"))

    plain = message.get_body(preferencelist=("plain",))
    html = message.get_body(preferencelist=("html",))
    if plain:
        builder = builder.text(plain.get_content())
    if html:
        builder = builder.html(html.get_content())

    for part in message.iter_attachments():
        content = part.get_content()
        if isinstance(content, str):
            content = content.encode("utf-8")
        builder = builder.attach_content(
            content,
            filename=part.get_filename() or "attachment",
            disposition="attachment",
        )

    client = MailerSendClient(api_key=api_key)
    email = builder.build()
    response = client.emails.send(email)
    if not getattr(response, "message_id", None):
        logging.warning("MailerSend response missing message_id: %s", response)


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
    # include owner as second recipient if configured
    to_list = [email]
    if getattr(settings, "owner_email", None):
        to_list.append(settings.owner_email)
    message["To"] = ", ".join(to_list)
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    ics_content = build_ics(date_obj, start_dt)
    message.add_attachment(ics_content, subtype="calendar", filename="invite.ics")

    # Try MailerSend first (SDK)
    if settings.mailersend_api_key:
        try:
            _send_via_mailersend(message)
            return
        except Exception:
            logging.exception("Failed to send booking email via MailerSend, falling back to SMTP")

    # Fallback to SMTP
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(settings.smtp_email, settings.smtp_password)
            smtp.send_message(message)
    except Exception:
        logging.exception("Failed to send booking email via SMTP")
        raise
