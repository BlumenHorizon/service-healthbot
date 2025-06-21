import sys

from loguru import logger as base_logger

from src.services.env_utils import get_env_var


def configure_logger() -> None:
    base_logger.remove()

    base_logger.add(
        "src/logs/bot.log",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | " "{level:<8} | " "{extra} | " "{message}"
        ),
        level=get_env_var("LOGURU_LOGS_LEVEL", "INFO"),
        rotation="10 MB",
        compression="lzma",
    )
    if get_env_var("MODE") == "DEV":
        base_logger.add(
            sys.stdout,
            level=get_env_var("LOGURU_LOGS_LEVEL", "DEBUG"),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan> | <magenta>{extra}</magenta>",
        )
