"""
Master Data ETL Pipeline.

Generates and loads all master datasets into PostgreSQL.
"""
print(">>> Running pipeline.py from:", __file__)
from sqlalchemy import text

from database.connection import get_database_engine
from config.settings import settings

from etl.load import load_dataframe

from data.generators.customer_generator import generate_customers
from data.generators.product_generator import generate_products
from data.generators.store_generator import generate_stores
from data.generators.promotion_generator import generate_promotions
from data.generators.inventory_generator import generate_inventory


def reset_database() -> None:
    print(">>> reset_database() called")

    engine = get_database_engine()

    with engine.begin() as connection:
        print(">>> Executing TRUNCATE...")
        connection.execute(
            text("""
                TRUNCATE TABLE
                    sale,
                    inventory,
                    promotion,
                    product,
                    store,
                    customer
                RESTART IDENTITY CASCADE;
            """)
        )

    print("✓ Database cleared")


def main() -> None:

    print("=" * 60)
    print("Retail Intelligence ETL Pipeline")
    print("=" * 60)

    reset_database()

    print("\nGenerating Customers...")
    customers = generate_customers()
    load_dataframe(customers, settings.CUSTOMER_TABLE)
    print("✓ Customers Loaded")

    print("\nGenerating Products...")
    products = generate_products()
    load_dataframe(products, settings.PRODUCT_TABLE)
    print("✓ Products Loaded")

    print("\nGenerating Stores...")
    stores = generate_stores()
    load_dataframe(stores, settings.STORE_TABLE)
    print("✓ Stores Loaded")

    print("\nGenerating Promotions...")
    promotions = generate_promotions()
    load_dataframe(promotions, settings.PROMOTION_TABLE)
    print("✓ Promotions Loaded")

    print("\nGenerating Inventory...")
    inventory = generate_inventory(products, stores)
    load_dataframe(inventory, settings.INVENTORY_TABLE)
    print("✓ Inventory Loaded")

    print("\n" + "=" * 60)
    print("✓ Master Data Pipeline Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()