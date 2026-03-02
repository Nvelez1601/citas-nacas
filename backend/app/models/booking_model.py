from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    email: str = Field(..., description="User email")
    comments: str | None = Field(default=None, description="Optional comments")
    date_id: int = Field(..., description="Selected date id")


class BookingResponse(BaseModel):
    success: bool
    message: str
    event_id: str | None = None
