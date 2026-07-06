"""
Central configuration for the Retail Intelligence Platform.
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application configuration."""

    # ------------------------------------------------------------------
    # Database Configuration
    # ------------------------------------------------------------------
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # ------------------------------------------------------------------
    # General Configuration
    # ------------------------------------------------------------------
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))

    # ------------------------------------------------------------------
    # Dataset Sizes
    # ------------------------------------------------------------------
    CUSTOMER_COUNT = 500
    PRODUCT_COUNT = 200
    STORE_COUNT = 20
    PROMOTION_COUNT = 25

    # ------------------------------------------------------------------
    # Inventory Configuration
    # ------------------------------------------------------------------
    MIN_STOCK = 10
    MAX_STOCK = 500

    MIN_REORDER_LEVEL = 20
    MAX_REORDER_LEVEL = 80

    # ------------------------------------------------------------------
    # Sales Calculation Configuration
    # ------------------------------------------------------------------
    GST_RATE = 0.18

    PROMOTION_PROBABILITY = 0.35

    ROUND_DECIMALS = 2

    # ------------------------------------------------------------------
    # Database Table Names
    # ------------------------------------------------------------------
    CUSTOMER_TABLE = "customer"
    PRODUCT_TABLE = "product"
    STORE_TABLE = "store"
    PROMOTION_TABLE = "promotion"
    INVENTORY_TABLE = "inventory"
    SALES_TABLE = "sale"


settings = Settings()