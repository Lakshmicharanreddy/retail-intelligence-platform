"""
Generate product master data.
"""

from faker import Faker
import pandas as pd
import random

from config.settings import settings
from utils.logger import get_logger

fake = Faker()
fake.seed_instance(settings.RANDOM_SEED)
random.seed(settings.RANDOM_SEED)

logger = get_logger(__name__)


PRODUCT_CATALOG = {

    "Electronics": {
        "Mobile": [
            "Samsung",
            "Apple",
            "OnePlus",
            "Xiaomi"
        ],

        "Laptop": [
            "Dell",
            "HP",
            "Lenovo",
            "Asus"
        ]
    },

    "Groceries": {

        "Beverages": [
            "Coca-Cola",
            "Pepsi",
            "Sprite"
        ],

        "Snacks": [
            "Lays",
            "Kurkure",
            "Bingo"
        ]
    },

    "Fashion": {

        "Men": [
            "Levis",
            "Puma",
            "Nike"
        ],

        "Women": [
            "Zara",
            "H&M",
            "Biba"
        ]
    }

}


def generate_products() -> pd.DataFrame():

    products = []

    for _ in range(settings.PRODUCT_COUNT):

        category = random.choice(list(PRODUCT_CATALOG.keys()))

        subcategory = random.choice(
            list(PRODUCT_CATALOG[category].keys())
        )

        brand = random.choice(
            PRODUCT_CATALOG[category][subcategory]
        )

        product_name = f"{brand} {fake.word().title()}"

        unit_cost = round(
            random.uniform(100, 3000),
            2
        )

        unit_price = round(
            unit_cost * random.uniform(1.15, 1.60),
            2
        )

        products.append({

            "product_name": product_name,

            "category": category,

            "subcategory": subcategory,

            "brand": brand,

            "supplier": fake.company(),

            "cost_price": unit_cost,

            "selling_price": unit_price,

            "is_active": random.choice(
                [True, True, True, False]
            )

        })

    df = pd.DataFrame(products)

    logger.info(
        "Generated %s products.",
        len(df)
    )

    return df


if __name__ == "__main__":

    df = generate_products()

    print(df.head())