import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@(gmail\.com|hotmail\.com)$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.fullmatch(email))
