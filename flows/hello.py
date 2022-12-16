from prefect import flow, get_run_logger
from platform import node, platform


@flow
def hello(user_input: str = "World"):
    logger = get_run_logger()
    logger.info("Network: %s. Instance: %s. Agent is healthy ✅️", node(), platform())
    logger.info("Hello, %s! This confirms a new GH Action workflow run 🚀", user_input)


if __name__ == "__main__":
    hello()
