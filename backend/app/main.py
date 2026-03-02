from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.controllers.booking_controller import router as booking_router

app = FastAPI(title="Citas Nacas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(booking_router, prefix="/api")


@app.get("/")
async def health_check():
    return {"status": "ok"}
