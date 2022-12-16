from prefect import get_run_logger, flow
from typing import Any


@flow
def parametrized(
    user: str = "Marvin", question: str = "Ultimate", answer: Any = 42
) -> None:
    logger = get_run_logger()
    logger.info("Hello from Prefect, %s! 👋", user)
    logger.info("The answer to the %s question is %s! 🤖", question, answer)


if __name__ == "__main__":
    parametrized(user="World")
