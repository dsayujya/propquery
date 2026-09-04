"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration using pydantic-settings.

    Values are loaded from environment variables or a .env file.
    """

    # Database
    database_url: str = "postgresql://propquery_user:propquery_pass@localhost:5432/propquery"

    # Application
    app_name: str = "PropQuery"
    app_version: str = "1.0.0"
    debug: bool = False

    # CORS
    cors_origins: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
