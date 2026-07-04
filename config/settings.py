"""
Central configuration for the Retail Intelligence Platform.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration."""

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))


settings = Settings()