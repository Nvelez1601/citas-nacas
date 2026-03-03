from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

import logging
import uuid
from time import time

from app.config.settings import settings
from app.controllers.booking_controller import router as booking_router
from app.utils.logging import setup_structured_logging, js

# configure structured logging
root_logger = setup_structured_logging()
logger = logging.getLogger("citasnacas")

app = FastAPI(title="Citas Nacas API")


@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start = time()
    js(
        logger,
        logging.INFO,
        event="request_start",
        method=request.method,
        path=request.url.path,
        request_id=request_id,
        client=request.client.host if request.client else None,
        origin=request.headers.get("origin"),
        user_agent=(request.headers.get("user-agent") or "")[:200],
    )
    try:
        response: Response = await call_next(request)
    except Exception as exc:
        js(
            logger,
            logging.ERROR,
            event="request_error",
            request_id=request_id,
            path=request.url.path,
            error=str(exc),
        )
        raise
        raise
    duration = (time() - start) * 1000
    response.headers["X-Request-Id"] = request_id
    js(
        logger,
        logging.INFO,
        event="request_end",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None,
        request_id=request_id,
        duration_ms=round(duration, 2),
        status=response.status_code,
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(booking_router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok"}
