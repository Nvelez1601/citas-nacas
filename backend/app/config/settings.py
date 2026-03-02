from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    smtp_email: str | None = None
    smtp_password: str | None = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    # smtp (local) or mailersend
    email_provider: str = "smtp"

    bookings_path: str = "app/data/bookings.json"

    timezone: str = "America/Caracas"
    cors_origins: str = "http://localhost:5173"
    mailersend_api_key: str | None = None
    mailersend_from_email: str | None = None
    mailersend_from_name: str | None = None

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
