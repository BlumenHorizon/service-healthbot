import traceback

from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles exceptions raised during update processing.

    This function serves as a centralized error handler for the bot,
    following the recommended pattern by the python-telegram-bot library.
    It captures exceptions raised in any update handler, logs the full traceback,
    and attempts to notify the user about the internal server error.

    Having a single, unified error handler simplifies debugging and ensures
    consistent user feedback across all commands and callbacks.

    Args:
        update (object): The update that caused the error.
        context (ContextTypes.DEFAULT_TYPE): The context of the callback,
            containing error information and bot instance.

    Returns:
        None
    """
    error = context.error
    error_type = type(error) if error is not None else None

    tb_str = "".join(
        traceback.format_exception(
            error_type,
            error,
            error.__traceback__ if error is not None else None,
        )
    )
    logger.error(f"Exception while handling an update:\n{tb_str}")

    try:
        if isinstance(update, Update) and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🚨 Сталася внутрішня помилка сервера. Будь ласка, спробуйте пізніше.",
            )
    except Exception as send_err:
        logger.error(f"Failed to send error message to user: {send_err}")
