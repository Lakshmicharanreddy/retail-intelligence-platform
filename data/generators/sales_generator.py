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
import uuid
from datetime import timedelta
from typing import Dict

import pandas as pd
from sqlalchemy import text

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

        # ------------------------------------------------------------------
    # Sales Calculation Engine
    # ------------------------------------------------------------------

    def get_product_details(
        self,
        product_id: int
    ) -> pd.Series:
        """
        Return product details for a given product.

        Parameters
        ----------
        product_id : int
            Product identifier.

        Returns
        -------
        pd.Series
            Product details.

        Raises
        ------
        ValueError
            If the product does not exist.
        """

        product = self.products[
            self.products["product_id"] == product_id
        ]

        if product.empty:
            raise ValueError(
                f"Product {product_id} not found."
            )

        return product.iloc[0]

    def find_applicable_promotion(
        self
    ) -> pd.Series | None:
        """
        Randomly select an active promotion based on the
        configured promotion probability.

        Returns
        -------
        pd.Series | None
            Selected promotion or None.
        """

        active_promotions = self.promotions[
            self.promotions["is_active"]
        ]

        if active_promotions.empty:
            return None

        if (
            random.random()
            > settings.PROMOTION_PROBABILITY
        ):
            return None

        return active_promotions.sample(n=1).iloc[0]

    def calculate_subtotal(
        self,
        unit_price: float,
        quantity: int
    ) -> float:
        """
        Calculate subtotal.

        Returns
        -------
        float
        """

        return round(
            unit_price * quantity,
            settings.ROUND_DECIMALS
        )

    def calculate_discount(
        self,
        subtotal: float,
        promotion: pd.Series | None
    ) -> tuple[int | None, float]:
        """
        Calculate promotion discount.

        Returns
        -------
        tuple[int | None, float]
            Promotion ID and discount amount.
        """

        if promotion is None:
            return None, 0.0

        discount = subtotal * (
            promotion["discount_percentage"] / 100
        )

        return (
            int(promotion["promotion_id"]),
            round(
                discount,
                settings.ROUND_DECIMALS
            )
        )

    def calculate_tax(
        self,
        taxable_amount: float
    ) -> float:
        """
        Calculate GST.

        Returns
        -------
        float
        """

        tax = (
            taxable_amount
            * settings.GST_RATE
        )

        return round(
            tax,
            settings.ROUND_DECIMALS
        )

    def calculate_profit(
        self,
        product: pd.Series,
        quantity: int,
        discount: float
    ) -> float:
        """
        Calculate gross profit.

        Returns
        -------
        float
        """

        gross_profit = (
            (
                product["selling_price"]
                - product["cost_price"]
            )
            * quantity
        )

        return round(
            gross_profit - discount,
            settings.ROUND_DECIMALS
        )

    def enrich_sale_candidate(
        self,
        candidate: dict
    ) -> dict:
        """
        Enrich a sale candidate with financial details.

        Parameters
        ----------
        candidate : dict
            Draft sale transaction.

        Returns
        -------
        dict
            Financially enriched sale.
        """

        product = self.get_product_details(
            candidate["product_id"]
        )

        unit_price = float(
            product["selling_price"]
        )

        subtotal = self.calculate_subtotal(
            unit_price,
            candidate["quantity"]
        )

        promotion = self.find_applicable_promotion()

        promotion_id, discount = (
            self.calculate_discount(
                subtotal,
                promotion
            )
        )

        taxable_amount = subtotal - discount

        tax = self.calculate_tax(
            taxable_amount
        )

        total = round(
            taxable_amount + tax,
            settings.ROUND_DECIMALS
        )

        profit = self.calculate_profit(
            product,
            candidate["quantity"],
            discount
        )

        candidate.update(
            {
                "unit_price": unit_price,
                "subtotal": subtotal,
                "promotion_id": promotion_id,
                "discount_amount": discount,
                "tax_amount": tax,
                "total_amount": total,
                "profit": profit,
            }
        )

        logger.info(
            "Financial details calculated."
        )

        return candidate


        # ------------------------------------------------------------------
    # Transaction Finalization Engine
    # ------------------------------------------------------------------

    def weighted_choice(
        self,
        options: dict[str, float]
    ) -> str:
        """
        Return a weighted random choice from a dictionary.

        Parameters
        ----------
        options : dict[str, float]
            Mapping of option names to probabilities.

        Returns
        -------
        str
            Selected option.
        """

        return random.choices(
            population=list(options.keys()),
            weights=list(options.values()),
            k=1
        )[0]

    def generate_payment_method(self) -> str:
        """
        Generate a payment method.

        Returns
        -------
        str
            Payment method.
        """

        return self.weighted_choice(
            settings.PAYMENT_METHODS
        )

    def generate_sales_channel(self) -> str:
        """
        Generate a sales channel.

        Returns
        -------
        str
            Sales channel.
        """

        return self.weighted_choice(
            settings.SALES_CHANNELS
        )

    def generate_order_status(self) -> str:
        """
        Generate an order status.

        Returns
        -------
        str
            Order status.
        """

        return self.weighted_choice(
            settings.ORDER_STATUSES
        )

    def generate_order_timestamp(
        self
    ) -> pd.Timestamp:
        """
        Generate a random order timestamp within the
        configured sales period.

        Returns
        -------
        pd.Timestamp
            Random timestamp.
        """

        start = pd.to_datetime(
            settings.SALES_START_DATE
        )

        end = pd.to_datetime(
            settings.SALES_END_DATE
        )

        total_seconds = int(
            (end - start).total_seconds()
        )

        random_seconds = random.randint(
            0,
            total_seconds
        )

        return start + timedelta(
            seconds=random_seconds
        )

    def generate_invoice_number(self) -> str:
        """
        Generate a unique invoice number.

        Returns
        -------
        str
            Invoice number.
        """

        return (
            f"{settings.INVOICE_PREFIX}-"
            f"{uuid.uuid4().hex[:10].upper()}"
        )

    def reduce_inventory(
        self,
        inventory_id: int,
        quantity: int
    ) -> None:
        """
        Reduce inventory in memory after a completed sale.

        Parameters
        ----------
        inventory_id : int
            Inventory identifier.

        quantity : int
            Quantity sold.
        """

        mask = (
            self.inventory["inventory_id"]
            == inventory_id
        )

        self.inventory.loc[
            mask,
            "stock_quantity"
        ] -= quantity

        logger.info(
            "Inventory %d reduced by %d units.",
            inventory_id,
            quantity
        )

    def finalize_sale(
        self,
        sale: dict
    ) -> dict:
        """
        Finalize a sale by adding operational metadata.

        Parameters
        ----------
        sale : dict
            Financially enriched sale.

        Returns
        -------
        dict
            Complete sale ready for database insertion.
        """

        metadata = {
            "payment_method": (
                self.generate_payment_method()
            ),
            "sales_channel": (
                self.generate_sales_channel()
            ),
            "order_status": (
                self.generate_order_status()
            ),
            "order_timestamp": (
                self.generate_order_timestamp()
            ),
            "invoice_number": (
                self.generate_invoice_number()
            ),
        }

        sale.update(metadata)

        if sale["order_status"] == "Completed":

            self.reduce_inventory(
                sale["inventory_id"],
                sale["quantity"]
            )

        logger.info(
            "Sale finalized successfully."
        )

        return sale


        # ------------------------------------------------------------------
    # Batch Generation Engine
    # ------------------------------------------------------------------

    def generate_sale(self) -> dict:
        """
        Generate one complete retail transaction.

        Returns
        -------
        dict
            Complete sale transaction.
        """

        candidate = self.create_sale_candidate()

        sale = self.enrich_sale_candidate(
            candidate
        )

        sale = self.finalize_sale(
            sale
        )

        return sale

    def generate_sales_batch(
        self,
        number_of_sales: int
    ) -> pd.DataFrame:
        """
        Generate multiple sales transactions.

        Parameters
        ----------
        number_of_sales : int
            Number of sales to generate.

        Returns
        -------
        pd.DataFrame
            Generated sales.
        """

        if number_of_sales <= 0:
            raise ValueError(
                "number_of_sales must be greater than zero."
            )

        logger.info(
            "Generating %d sales...",
            number_of_sales
        )

        sales = []

        for index in range(number_of_sales):

            sale = self.generate_sale()

            sales.append(sale)

            if (
                (index + 1)
                % settings.GENERATION_PROGRESS_INTERVAL
                == 0
            ):
                logger.info(
                    "Generated %d/%d sales",
                    index + 1,
                    number_of_sales
                )

        sales_df = pd.DataFrame(sales)

        logger.info(
            "Sales generation completed."
        )

        return sales_df

    def get_generation_summary(
        self,
        sales_df: pd.DataFrame
    ) -> None:
        """
        Display summary statistics.

        Parameters
        ----------
        sales_df : pd.DataFrame
            Generated sales.
        """

        logger.info(
            "Sales Generated : %d",
            len(sales_df)
        )

        logger.info(
            "Revenue : %.2f",
            sales_df["total_amount"].sum()
        )

        logger.info(
            "Profit : %.2f",
            sales_df["profit"].sum()
        )

        logger.info(
            "Average Order Value : %.2f",
            sales_df["total_amount"].mean()
        )

    
    

    def validate_sales_data(
        self,
        sales_df: pd.DataFrame
    ) -> dict:
        """
        Validate generated sales data.

        Returns
        -------
        dict
            Validation statistics.
        """

        validation = {
            "total_sales": len(sales_df),

            "negative_revenue": (
                sales_df["total_amount"] <= 0
            ).sum(),

            "negative_profit": (
                sales_df["profit"] < 0
            ).sum(),

            "invalid_quantity": (
                sales_df["quantity"] <= 0
            ).sum(),

            "invalid_unit_price": (
                sales_df["unit_price"] <= 0
            ).sum(),

            "negative_tax": (
                sales_df["tax_amount"] < 0
            ).sum(),

            "negative_discount": (
                sales_df["discount_amount"] < 0
            ).sum(),

            "missing_customer_id": (
                sales_df["customer_id"].isna()
            ).sum(),

            "missing_product_id": (
                sales_df["product_id"].isna()
            ).sum(),

            "missing_store_id": (
                sales_df["store_id"].isna()
            ).sum(),

            "missing_timestamp": (
                sales_df["order_timestamp"].isna()
            ).sum(),

            "missing_invoice": (
                sales_df["invoice_number"].isna()
            ).sum(),

            "duplicate_invoices": (
                sales_df["invoice_number"]
                .duplicated()
                .sum()
            ),
        }

        return validation
    

    def validate_inventory(
        self
    ) -> int:
        """
        Count inventory rows having negative stock.

        Returns
        -------
        int
        """

        return (
            self.inventory["stock_quantity"] < 0
        ).sum()




    def validate_financials(
        self,
        sales_df: pd.DataFrame
    ) -> int:
        """
        Verify financial calculations.

        Returns
        -------
        int
            Number of invalid rows.
        """

        subtotal = (
            sales_df["unit_price"]
            * sales_df["quantity"]
        ).round(
            settings.ROUND_DECIMALS
        )

        total = (
            subtotal
            - sales_df["discount_amount"]
            + sales_df["tax_amount"]
        ).round(
            settings.ROUND_DECIMALS
        )

        invalid = (
            (
                subtotal
                != sales_df["subtotal"]
            )
            |
            (
                total
                != sales_df["total_amount"]
            )
        )

        return invalid.sum()

    
    

    def generate_quality_report(
        self,
        sales_df: pd.DataFrame
    ) -> None:
        """
        Generate and display data quality report.
        """

        validation = self.validate_sales_data(
            sales_df
        )

        inventory_errors = (
            self.validate_inventory()
        )

        financial_errors = (
            self.validate_financials(
                sales_df
            )
        )

        failed_records = (
        validation["negative_revenue"]
        + validation["invalid_quantity"]
        + validation["invalid_unit_price"]
        + validation["negative_tax"]
        + validation["negative_discount"]
        + validation["missing_customer_id"]
        + validation["missing_product_id"]
        + validation["missing_store_id"]
        + validation["missing_timestamp"]
        + validation["missing_invoice"]
        + validation["duplicate_invoices"]
        + inventory_errors
        + financial_errors
    )

        passed_records = (
            validation["total_sales"]
            - failed_records
        )

        logger.info("")

        logger.info(
            "=" * 40
        )

        logger.info(
            "Sales Data Quality Report"
        )

        logger.info(
            "=" * 40
        )

        logger.info(
            "Total Sales            : %d",
            validation["total_sales"]
        )

        logger.info(
            "Passed Records         : %d",
            passed_records
        )

        logger.info(
            "Failed Records         : %d",
            failed_records
        )

        logger.info(
            "Duplicate Invoices     : %d",
            validation["duplicate_invoices"]
        )

        logger.info(
            "Negative Revenue       : %d",
            validation["negative_revenue"]
        )

        logger.info(
            "Negative Profit        : %d",
            validation["negative_profit"]
        )

        logger.info(
            "Missing Customer IDs   : %d",
            validation["missing_customer_id"]
        )

        logger.info(
            "Missing Product IDs    : %d",
            validation["missing_product_id"]
        )

        logger.info(
            "Missing Store IDs      : %d",
            validation["missing_store_id"]
        )

        logger.info(
            "Inventory Errors       : %d",
            inventory_errors
        )

        logger.info(
            "Financial Errors       : %d",
            financial_errors
        )

        logger.info(
            "Overall Status         : %s",
            "PASSED"
            if failed_records == 0
            else "FAILED"
        )

        logger.info(
            "=" * 40
        )

        return failed_records == 0


    def load_sales_to_database(
        self,
        sales_df: pd.DataFrame
    ) -> None:
        """
        Load generated sales into PostgreSQL
        in configurable batches.
        """

        logger.info(
            "Loading sales into database..."
        )

        total_rows = len(sales_df)

        with self.db.engine.begin() as connection:

            for start in range(
                0,
                total_rows,
                settings.DB_BATCH_SIZE
            ):

                end = min(
                    start + settings.DB_BATCH_SIZE,
                    total_rows
                )

                batch = sales_df.iloc[start:end]

                self.insert_sales_batch(
                    connection,
                    batch
                )

                logger.info(
                    "Inserted Batch %d (%d rows)",
                    (start // settings.DB_BATCH_SIZE) + 1,
                    len(batch)
                )

        logger.info(
            "Database Load Completed."
        )


    def insert_sales_batch(
        self,
        connection,
        batch_df: pd.DataFrame
    ) -> None:
        """
        Insert one batch into PostgreSQL.
        """

        sql = text(
            """
            INSERT INTO sale (

                invoice_number,
                order_timestamp,
                customer_id,
                product_id,
                store_id,
                inventory_id,
                promotion_id,
                quantity,
                unit_price,
                subtotal,
                discount_amount,
                tax_amount,
                total_amount,
                profit,
                payment_method,
                sales_channel,
                order_status

            )

            VALUES (

                :invoice_number,
                :order_timestamp,
                :customer_id,
                :product_id,
                :store_id,
                :inventory_id,
                :promotion_id,
                :quantity,
                :unit_price,
                :subtotal,
                :discount_amount,
                :tax_amount,
                :total_amount,
                :profit,
                :payment_method,
                :sales_channel,
                :order_status

            )
            """
        )

        records = batch_df.to_dict(
            orient="records"
        )

        connection.execute(
            sql,
            records
        )


    def generate_validate_and_load(
        self,
        number_of_sales: int
    ) -> None:
        """
        Complete sales generation pipeline.
        """

        sales_df = self.generate_sales_batch(
            number_of_sales
        )

        self.get_generation_summary(
            sales_df
        )

        passed = self.generate_quality_report(
            sales_df
        )

        if not passed:
            raise ValueError(
                "Sales validation failed. Database loading aborted."
            )

        self.load_sales_to_database(
            sales_df
        )


if __name__ == "__main__":

    generator = SalesGenerator()

    generator.load_master_data()

    generator.validate_master_data()

    generator.generate_validate_and_load(
        settings.DEFAULT_SALES_COUNT
    )