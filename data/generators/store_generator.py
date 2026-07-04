"""
Generate store master data.
"""

from faker import Faker
import pandas as pd
import random

from config.settings import settings
from utils.logger import get_logger

fake = Faker("en_IN")
fake.seed_instance(settings.RANDOM_SEED)
random.seed(settings.RANDOM_SEED)

logger = get_logger(__name__)


STORE_LOCATIONS = {

    "North": [
        ("Delhi", "Delhi"),
        ("Chandigarh", "Chandigarh"),
        ("Jaipur", "Rajasthan"),
        ("Lucknow", "Uttar Pradesh")
    ],

    "South": [
        ("Hyderabad", "Telangana"),
        ("Bengaluru", "Karnataka"),
        ("Chennai", "Tamil Nadu"),
        ("Kochi", "Kerala")
    ],

    "East": [
        ("Kolkata", "West Bengal"),
        ("Bhubaneswar", "Odisha"),
        ("Patna", "Bihar"),
        ("Ranchi", "Jharkhand")
    ],

    "West": [
        ("Mumbai", "Maharashtra"),
        ("Pune", "Maharashtra"),
        ("Ahmedabad", "Gujarat"),
        ("Surat", "Gujarat")
    ]

}


STORE_TYPES = [
    "Hypermarket",
    "Supermarket",
    "Express"
]


STORE_STATUS = [
    "Open",
    "Open",
    "Open",
    "Closed"
]


def generate_stores() -> pd.DataFrame:
    """
    Generate store master data.
    """

    stores = []

    for store_number in range(1, settings.STORE_COUNT + 1):

        region = random.choice(list(STORE_LOCATIONS.keys()))

        city, state = random.choice(
            STORE_LOCATIONS[region]
        )

        stores.append({

            "store_name": f"{city} Store {store_number}",

            "city": city,

            "state": state,

            "region": region,

            "store_type": random.choice(STORE_TYPES),

            "manager_name": fake.name(),

            "opening_date": fake.date_between(
                start_date="-15y",
                end_date="-1y"
            ),

            "store_status": random.choice(STORE_STATUS)

        })

    df = pd.DataFrame(stores)

    logger.info(
        "Generated %s stores.",
        len(df)
    )

    return df


if __name__ == "__main__":

    stores = generate_stores()

    print(stores.head())