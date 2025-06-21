from typing import Awaitable, Callable

from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from src import commands
from src.auth.decorators import admin_only
from src.handlers.sites import (
    handle_check_site_status,
    handle_delete_site,
    handle_site_list,
)


@admin_only
async def monolith_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles callback queries from inline keyboard buttons.

    This asynchronous function processes the incoming callback query from an update,
    determines the appropriate handler based on the callback data, and invokes it.
    It supports several predefined commands like checking site status, listing sites.
    It also handles dynamic actions such as deleting
    a site.

    Parameters:
        update (Update): The incoming Telegram update containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context provided by the Telegram bot framework.

    Returns:
        None
    """
    query = update.callback_query
    if not query or not query.data:
        return

    if query.data == "start":
        await commands.start(update, context)
        return

    await query.answer()

    keyboard: list[list[InlineKeyboardButton]] = []
    handlers: dict[str, Callable[[], Awaitable[None]]] = {
        "check_status": lambda: handle_check_site_status(
            query=query, keyboard=keyboard
        ),
        "site_list": lambda: handle_site_list(query=query),
    }

    handler = handlers.get(query.data)
    if handler:
        await handler()
        return

    if query.data.startswith("remove_"):
        site_id = int(query.data.split("_")[1])
        await handle_delete_site(query=query, site_id=site_id)
