from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    smtp_email: str
    smtp_password: str
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    calendar_id: str = "primary"
    calendar_credentials_path: str = "app/config/calendar_credentials.json"

    timezone: str = "America/Caracas"
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
