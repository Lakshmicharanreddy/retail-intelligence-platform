"""
Generate customer master data.
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


def generate_customers() -> pd.DataFrame:
    """
    Generate customer data.
    """

    customers = []

    loyalty_levels = [
        "Bronze",
        "Silver",
        "Gold",
        "Platinum"
    ]

    statuses = [
        "Active",
        "Inactive"
    ]

    for _ in range(settings.CUSTOMER_COUNT):

        customers.append({

            "first_name": fake.first_name(),

            "last_name": fake.last_name(),

            "gender": random.choice(
                ["Male", "Female"]
            ),

            "date_of_birth": fake.date_of_birth(
                minimum_age=18,
                maximum_age=70
            ),

            "email": fake.unique.email(),

            "phone": fake.phone_number(),

            "city": fake.city(),

            "state": fake.state(),

            "join_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            ),

            "loyalty_level": random.choice(
                loyalty_levels
            ),

            "customer_status": random.choice(
                statuses
            )

        })

    df = pd.DataFrame(customers)

    logger.info(
        "Generated %s customers.",
        len(df)
    )

    return df


if __name__ == "__main__":

    customers = generate_customers()

    print(customers.head())