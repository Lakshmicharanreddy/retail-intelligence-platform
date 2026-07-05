"""
Database connection module.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config.settings import settings


def get_database_engine() -> Engine:
    """
    Create and return a SQLAlchemy Engine.
    """

    database_url = (
        f"postgresql+psycopg2://"
        f"{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:"
        f"{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )

    engine = create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        future=True,
    )

    return engine


class DatabaseConnection:
    """
    Database connection wrapper.

    Provides a reusable SQLAlchemy engine across the project.
    """

    def __init__(self) -> None:
        self.engine = get_database_engine()


if __name__ == "__main__":

    db = DatabaseConnection()

    try:
        with db.engine.connect():
            print("✅ Database connection successful.")
    except Exception as error:
        print(f"❌ Connection failed: {error}")