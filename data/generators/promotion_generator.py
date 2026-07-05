"""
Generate promotion master data.
"""

import random

import pandas as pd

from config.settings import settings
from utils.logger import get_logger

random.seed(settings.RANDOM_SEED)

logger = get_logger(__name__)


PROMOTION_NAMES = [
    "Diwali Sale",
    "Summer Sale",
    "Winter Sale",
    "Weekend Offer",
    "Mega Discount",
    "Clearance Sale",
    "Back to School",
    "Festival Bonanza",
    "New Year Sale",
    "Flash Sale"
]


PROMOTION_TYPES = [
    "Percentage Discount",
    "Flat Discount",
    "Buy One Get One",
    "Cashback"
]


DISCOUNT_PERCENTAGES = [
    5,
    10,
    15,
    20,
    25,
    30,
    40,
    50
]


PROMOTION_STATUS = [
    "Active",
    "Expired",
    "Upcoming"
]


def generate_promotions() -> pd.DataFrame:
    """
    Generate promotion master data.
    """

    promotions = []

    for promotion_id in range(settings.PROMOTION_COUNT):

        start_date = pd.Timestamp.today() - pd.Timedelta(
            days=random.randint(0, 365)
        )

        end_date = start_date + pd.Timedelta(
            days=random.randint(7, 45)
        )

        promotions.append({

            "promotion_name": random.choice(PROMOTION_NAMES),

            "promotion_type": random.choice(PROMOTION_TYPES),

            "discount_percentage": random.choice(
                DISCOUNT_PERCENTAGES
            ),

            "start_date": start_date.date(),

            "end_date": end_date.date(),
            "is_active": random.choice([True, False])

        })

    df = pd.DataFrame(promotions)

    logger.info(
        "Generated %s promotions.",
        len(df)
    )

    return df


if __name__ == "__main__":

    promotions = generate_promotions()

    print(promotions.head())