from faker import Faker
from prefect import flow, get_run_logger
from platform import node, platform


@flow
def bs():
    logger = get_run_logger()
    fake = Faker()
    logger.info("We should %s 🚀", fake.bs())
    logger.info("Network: %s. Instance: %s. Agent is healthy ✅️", node(), platform())


if __name__ == "__main__":
    bs()
