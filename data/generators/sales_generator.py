"""
Sales Transaction Generator

Loads all prerequisite master data required to generate
realistic retail sales transactions.

This module forms the foundation for sales generation and
validates that all required datasets are available before
transaction creation begins.
"""

from __future__ import annotations

import random
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

    # ------------------------------------------------------------------
    # Selection Engine
    # ------------------------------------------------------------------

    def get_active_customers(self) -> pd.DataFrame:
        """
        Return only active customers.

        Returns
        -------
        pd.DataFrame
            Active customers.
        """

        return self.customers[
            self.customers["customer_status"] == "Active"
        ]

    def get_active_products(self) -> pd.DataFrame:
        """
        Return only active products.

        Returns
        -------
        pd.DataFrame
            Active products.
        """

        return self.products[
            self.products["is_active"]
        ]

    def get_store_inventory(self, store_id: int) -> pd.DataFrame:
        """
        Return inventory available for a specific store.

        Parameters
        ----------
        store_id : int
            Store identifier.

        Returns
        -------
        pd.DataFrame
            Inventory records with stock available.
        """

        return self.inventory[
            (self.inventory["store_id"] == store_id)
            &
            (self.inventory["stock_quantity"] > 0)
        ]

    def select_customer(self) -> pd.Series:
        """
        Randomly select one active customer.

        Returns
        -------
        pd.Series
            Selected customer.
        """

        customers = self.get_active_customers()

        return customers.sample(n=1).iloc[0]

    def select_store(self) -> pd.Series:
        """
        Randomly select one store.

        Returns
        -------
        pd.Series
            Selected store.
        """

        return self.stores.sample(n=1).iloc[0]

    def select_inventory_item(
        self,
        store_id: int
    ) -> pd.Series:
        """
        Select one active inventory item for a store.

        Parameters
        ----------
        store_id : int
            Store identifier.

        Returns
        -------
        pd.Series
            Selected inventory item.

        Raises
        ------
        ValueError
            If no active inventory exists.
        """

        inventory = self.get_store_inventory(store_id)

        active_products = self.get_active_products()

        inventory = inventory.merge(
            active_products,
            on="product_id",
            how="inner"
        )

        if inventory.empty:
            raise ValueError(
                f"No active inventory available for store {store_id}."
            )

        return inventory.sample(n=1).iloc[0]

    def generate_quantity(
        self,
        stock_quantity: int
    ) -> int:
        """
        Generate a realistic purchase quantity.

        Parameters
        ----------
        stock_quantity : int
            Available stock.

        Returns
        -------
        int
            Purchase quantity.
        """

        max_quantity = min(stock_quantity, 5)

        return random.randint(1, max_quantity)

    def create_sale_candidate(self) -> dict:
        """
        Create one valid sale candidate.

        Returns
        -------
        dict
            Draft sale transaction.
        """

        customer = self.select_customer()

        store = self.select_store()

        inventory = self.select_inventory_item(
            int(store["store_id"])
        )

        quantity = self.generate_quantity(
            int(inventory["stock_quantity"])
        )

        candidate = {
            "customer_id": int(customer["customer_id"]),
            "store_id": int(store["store_id"]),
            "product_id": int(inventory["product_id"]),
            "inventory_id": int(inventory["inventory_id"]),
            "quantity": quantity,
        }

        logger.info(
            "Sale candidate created: %s",
            candidate
        )

        return candidate


if __name__ == "__main__":

    generator = SalesGenerator()

    generator.load_master_data()

    generator.validate_master_data()

    candidate = generator.create_sale_candidate()

    print("\nSale Candidate\n")

    print(candidate)