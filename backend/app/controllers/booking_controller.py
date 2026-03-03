from pathlib import Path
import json
import logging

from fastapi import APIRouter, HTTPException, Request

from app.models.booking_model import BookingRequest, BookingResponse
from app.models.date_model import DateModel
from app.services.booking_service import create_booking
from app.utils.validators import is_valid_email

router = APIRouter(tags=["booking"])
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "dates.json"


def load_dates() -> list[DateModel]:
    with DATA_PATH.open("r", encoding="utf-8") as file_handle:
        raw = json.load(file_handle)
    return [DateModel(**item) for item in raw]


@router.get("/dates", response_model=list[DateModel])
def list_dates(request: Request):
    logger = logging.getLogger("citasnacas")
    from app.utils.logging import js

    js(
        logger,
        logging.INFO,
        event="list_dates",
        request_id=getattr(request.state, "request_id", None),
        client=request.client.host if request.client else None,
        origin=request.headers.get("origin"),
        user_agent=(request.headers.get("user-agent") or "")[:200],
    )
    return load_dates()


@router.post("/book", response_model=BookingResponse)
def book_date(payload: BookingRequest, request: Request):
    if not is_valid_email(payload.email):
        raise HTTPException(status_code=400, detail="Invalid email")

    dates = load_dates()
    selected = next((item for item in dates if item.id == payload.date_id), None)
    if not selected:
        raise HTTPException(status_code=404, detail="Date not found")

    logger = logging.getLogger("citasnacas")
    from app.utils.logging import js

    js(
        logger,
        logging.INFO,
        event="booking_attempt",
        request_id=getattr(request.state, "request_id", None),
        email=payload.email,
        date_id=payload.date_id,
        client=request.client.host if request.client else None,
        origin=request.headers.get("origin"),
        user_agent=(request.headers.get("user-agent") or "")[:200],
    )

    try:
        event_id = create_booking(payload.email, payload.comments, selected)
    except Exception as exc:
        logger.exception("Failed to complete booking request_id=%s", getattr(request.state, "request_id", None))
        raise HTTPException(status_code=500, detail="Booking failed") from exc

    return BookingResponse(success=True, message="Booking created", event_id=event_id)
