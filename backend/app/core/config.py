"""
Dispatch OS application configuration.

Centralized configuration will be expanded as authentication,
multi-tenancy, billing, integrations, and production deployment
are added.
"""

import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Dispatch OS")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()
