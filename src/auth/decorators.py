from functools import wraps
from typing import Any, cast

from telegram import Update
from telegram.ext import ContextTypes

from src import config
from src.labels import MenuLabel
from src.responses import CallableCommand, R


def admin_only(func: CallableCommand[R]) -> CallableCommand[R]:
    @wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args: int, **kwargs: Any
    ) -> R | None:
        user = update.effective_user
        chat_id = update.effective_chat.id if update.effective_chat else None

        if update.callback_query:
            await update.callback_query.answer()
        if not user or user.id not in config.ADMIN_USERS:
            if chat_id:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=MenuLabel.UNAUTHORIZED,
                )
            return None
        return await func(update, context, *args, **kwargs)

    return cast(CallableCommand[R], wrapper)
