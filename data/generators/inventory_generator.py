"""
Generate inventory master data.
"""

import random

import pandas as pd

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

random.seed(settings.RANDOM_SEED)


def generate_inventory(
    products: pd.DataFrame,
    stores: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate inventory records.
    """

    inventory = []

    for store_id in range(1, len(stores) + 1):

        available_products = random.sample(
            range(1, len(products) + 1),
            k=random.randint(
                int(len(products) * 0.6),
                int(len(products) * 0.9)
            )
        )

        for product_id in available_products:

            current_stock = random.randint(
                settings.MIN_STOCK,
                settings.MAX_STOCK
            )

            reorder_level = random.randint(
                settings.MIN_REORDER_LEVEL,
                settings.MAX_REORDER_LEVEL
            )

            max_stock_level = random.randint(
                current_stock,
                settings.MAX_STOCK + 200
            )

            inventory.append({

                "product_id": product_id,

                "store_id": store_id,

                "stock_quantity": current_stock,

                "reorder_level": reorder_level,

                "last_stock_update":
                    pd.Timestamp.today().date()
                    - pd.Timedelta(
                        days=random.randint(1, 60)
                    )

            })

    df = pd.DataFrame(inventory)

    logger.info(
        "Generated %s inventory records.",
        len(df)
    )

    return df


if __name__ == "__main__":

    from data.generators.product_generator import generate_products
    from data.generators.store_generator import generate_stores

    products = generate_products()

    stores = generate_stores()

    inventory = generate_inventory(
        products,
        stores
    )

    print(inventory.head())