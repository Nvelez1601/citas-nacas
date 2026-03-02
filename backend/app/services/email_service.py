from email.message import EmailMessage
from pathlib import Path
import logging
import smtplib
import ssl

from jinja2 import Environment, FileSystemLoader, select_autoescape
from mailersend import MailerSendClient, EmailBuilder

from app.config.settings import settings
from app.models.date_model import DateModel
from app.utils.ics_generator import build_ics

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"


def _send_via_smtp(message: EmailMessage):
    if not settings.smtp_email or not settings.smtp_password:
        raise RuntimeError("SMTP_EMAIL or SMTP_PASSWORD not configured")

    host = settings.smtp_host
    port = settings.smtp_port
    context = ssl.create_default_context()

    with smtplib.SMTP(host, port) as server:
        server.starttls(context=context)
        server.login(settings.smtp_email, settings.smtp_password)
        server.send_message(message)


def _send_via_mailersend(message: EmailMessage):
    api_key = settings.mailersend_api_key
    if not api_key:
        raise RuntimeError("MAILERSEND_API_KEY not configured")

    from_email = settings.mailersend_from_email
    if not from_email:
        raise RuntimeError("MAILERSEND_FROM_EMAIL not configured")
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
    from_addr = (
        settings.smtp_email
        or settings.mailersend_from_email
        or "no-reply@example.com"
    )
    message["From"] = from_addr
    # Un solo destinatario principal
    message["To"] = email
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    ics_content = build_ics(date_obj, start_dt)
    message.add_attachment(ics_content, subtype="calendar", filename="invite.ics")

    provider = getattr(settings, "email_provider", "smtp").lower()
    if provider == "smtp":
        _send_via_smtp(message)
    else:
        _send_via_mailersend(message)
