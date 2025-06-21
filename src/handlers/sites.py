from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.db.database import async_session
from src.formatters.sites import compose_dropped_sites_message
from src.labels import InlineLabel, MenuLabel
from src.repos.sites import SiteRepo
from src.services.keyboards import add_back_button
from src.services.sites_use_cases import delete_site, get_sites


async def handle_check_site_status(
    query: CallbackQuery,
    keyboard: list[list[InlineKeyboardButton]],
) -> None:
    """
    Handle a callback query to check and display the status of monitored sites.

    Fetches site statuses from the database and composes a message listing
    sites that are down. Edits the original message with the status info and
    provided inline keyboard.

    Args:
        query (CallbackQuery): Telegram callback query object.
        keyboard (list[list[InlineKeyboardButton]]): Keyboard buttons to include in the message.

    Returns:
        None
    """
    async with async_session() as db:
        sites_history_list = await SiteRepo(db=db).fetch_statuses()

    if not sites_history_list:
        add_back_button(keyboard)
        await query.edit_message_text(
            text=InlineLabel.SITES_NOT_FROUD,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return
    status_message = compose_dropped_sites_message(
        [site for site in sites_history_list]
    )

    add_back_button(keyboard)
    await query.edit_message_text(
        text=status_message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_site_list(query: CallbackQuery) -> None:
    """
    Handle a callback query to display the list of all monitored sites.

    Retrieves all sites from the database, builds a message listing the sites,
    and generates a keyboard with buttons to remove each site.
    Edits the original message with this information.

    Args:
        query (CallbackQuery): Telegram callback query object.

    Returns:
        None
    """
    async with async_session() as db:
        site_list = await SiteRepo(db=db).get_all()

    site_message = InlineLabel.SITE_LIST
    keyboard = []

    for site in site_list:
        site_url = site.url
        site_id = site.id
        site_message += f"{site_url}\n"
        keyboard.append(
            [
                InlineKeyboardButton(
                    MenuLabel.remove_site(site_url),
                    callback_data=f"remove_{site_id}",
                )
            ]
        )

    if not site_list:
        site_message = InlineLabel.NO_SITES_FOUND

    add_back_button(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=site_message, reply_markup=reply_markup)


async def handle_delete_site(query: CallbackQuery, site_id: int) -> None:
    """
    Handle a callback query to delete a monitored site by its ID.

    Attempts to delete the site from the database, then fetches the updated
    site list and updates the message accordingly.
    If deletion fails, sends an error message.

    Args:
        query (CallbackQuery): Telegram callback query object.
        site_id (int): ID of the site to be deleted.

    Returns:
        None
    """
    if await delete_site(site_id):
        site_list = await get_sites()
        keyboard = []

        if not site_list:
            site_message = InlineLabel.SITES_NOT_FOUND
        else:
            site_message = InlineLabel.UPDATED_SITES
            for site in site_list:
                site_url = site.url
                site_id = site.id
                site_message += f"{site_url}\n"
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            MenuLabel.remove_site(site_url),
                            callback_data=f"remove_{site_id}",
                        )
                    ]
                )

        add_back_button(keyboard)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=site_message, reply_markup=reply_markup)
    else:
        await query.edit_message_text(text="Error removing the site. Try again later.")
