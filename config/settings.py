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
    # Sales Generation Configuration
    # ------------------------------------------------------------------
    PAYMENT_METHODS = {
        "UPI": 0.35,
        "Credit Card": 0.25,
        "Debit Card": 0.20,
        "Cash": 0.15,
        "Wallet": 0.05,
    }

    SALES_CHANNELS = {
        "In-Store": 0.80,
        "Online": 0.20,
    }

    ORDER_STATUSES = {
        "Completed": 0.94,
        "Cancelled": 0.03,
        "Returned": 0.02,
        "Pending": 0.01,
    }

    SALES_START_DATE = "2025-01-01"

    SALES_END_DATE = "2025-12-31"

    INVOICE_PREFIX = "INV"

    # ------------------------------------------------------------------
# Sales Generation Configuration
# ------------------------------------------------------------------
    DEFAULT_SALES_COUNT = 1000

    GENERATION_PROGRESS_INTERVAL = 100

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