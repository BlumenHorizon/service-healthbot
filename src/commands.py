from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.auth.decorators import admin_only
from src.keyboards import START_KEYBOARD
from src.labels import MenuLabel
from src.schemas.sites import SiteCreateSchema
from src.services.commands_validation import (
    send_args_error,
    send_validation_errors,
    validate_args_count,
    validate_site_data,
)
from src.services.sites_use_cases import create_site


@admin_only
async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    if not context.args or not validate_args_count(context.args, SiteCreateSchema):
        await send_args_error(update.message, SiteCreateSchema)
        return

    site, errors = validate_site_data(context.args)
    if not site:
        if errors:
            await send_validation_errors(update.message, errors)
            return
        else:
            raise RuntimeError()

    await create_site(
        site_url=site.url.encoded_string(),
        expected_status_code=site.expected_status_code,
    )
    await update.message.reply_text(f"{site.url} успішно створено")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send a help message with usage instructions to the user.

    Args:
        update (Update): Incoming update from Telegram.
        context (CallbackContext): Telegram context.

    Returns:
        None
    """
    if update.message:
        await update.message.reply_text(MenuLabel.START)


@admin_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup(START_KEYBOARD)

    if update.callback_query:
        await update.callback_query.answer()
        if update.callback_query.message:
            await update.callback_query.edit_message_text(
                MenuLabel.CHOOSE_OPTION, reply_markup=reply_markup
            )
    elif update.message:
        await update.message.reply_text(
            MenuLabel.CHOOSE_OPTION, reply_markup=reply_markup
        )
