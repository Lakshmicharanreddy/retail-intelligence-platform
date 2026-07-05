"""
Sales Transaction Generator

Loads all prerequisite master data required to generate
realistic retail sales transactions.

This module forms the foundation for sales generation and
validates that all required datasets are available before
transaction creation begins.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd

from config.settings import settings
from database.connection import DatabaseConnection
from utils.logger import get_logger


logger = get_logger(__name__)


class SalesGenerator:
    """
    Sales Transaction Generator.

    Responsible for loading all master datasets required for
    realistic sales generation.
    """

    def __init__(self) -> None:
        self.db = DatabaseConnection()

        self.customers = pd.DataFrame()
        self.products = pd.DataFrame()
        self.stores = pd.DataFrame()
        self.promotions = pd.DataFrame()
        self.inventory = pd.DataFrame()

    def _load_table(self, table_name: str) -> pd.DataFrame:
        """
        Load a table into a pandas DataFrame.

        Parameters
        ----------
        table_name : str
            Database table name.

        Returns
        -------
        pd.DataFrame
        """

        query = f"SELECT * FROM {table_name};"

        df = pd.read_sql(
            query,
            self.db.engine
        )

        logger.info(
            "Loaded %s (%d rows)",
            table_name,
            len(df)
        )

        return df

    def load_master_data(self) -> None:
        """
        Load all required master tables.
        """

        logger.info("Loading master datasets...")

        self.customers = self._load_table(
            settings.CUSTOMER_TABLE
        )

        self.products = self._load_table(
            settings.PRODUCT_TABLE
        )

        self.stores = self._load_table(
            settings.STORE_TABLE
        )

        self.promotions = self._load_table(
            settings.PROMOTION_TABLE
        )

        self.inventory = self._load_table(
            settings.INVENTORY_TABLE
        )

        logger.info("Master data loaded successfully.")

    def validate_master_data(self) -> None:
        """
        Ensure required datasets are not empty.
        """

        datasets: Dict[str, pd.DataFrame] = {
            "Customers": self.customers,
            "Products": self.products,
            "Stores": self.stores,
            "Promotions": self.promotions,
            "Inventory": self.inventory,
        }

        for name, dataset in datasets.items():

            if dataset.empty:

                raise ValueError(
                    f"{name} dataset is empty."
                )

        logger.info(
            "Master data validation successful."
        )


if __name__ == "__main__":

    generator = SalesGenerator()

    generator.load_master_data()

    generator.validate_master_data()

    print(generator.customers.head())

    print(generator.products.head())

    print(generator.stores.head())

    print(generator.promotions.head())

    print(generator.inventory.head())