from datetime import datetime
from zoneinfo import ZoneInfo


def parse_date(date_str: str, tz_name: str) -> datetime:
    parsed = datetime.strptime(date_str, "%d-%m-%Y")
    return parsed.replace(tzinfo=ZoneInfo(tz_name))
