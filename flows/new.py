from faker import Faker
from prefect import flow


@flow(log_prints=True)
def new():
    fake = Faker()
    print(f"Let's {fake.bs()} 🚀")


if __name__ == "__main__":
    new()
