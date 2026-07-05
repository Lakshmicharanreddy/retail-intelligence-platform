"""
Load DataFrames into PostgreSQL.
"""

from database.connection import get_database_engine
from utils.logger import get_logger

logger = get_logger(__name__)

engine = get_database_engine()


def load_dataframe(dataframe, table_name: str) -> None:
    """
    Load a DataFrame into PostgreSQL.
    """

    dataframe.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    logger.info(
        "Loaded %d rows into '%s'.",
        len(dataframe),
        table_name,
    )