from telegram import InlineKeyboardButton

from src.labels import MenuLabel

START_KEYBOARD = [
    [InlineKeyboardButton(MenuLabel.CHECK_STATUS, callback_data="check_status")],
    [InlineKeyboardButton(MenuLabel.SITE_LIST, callback_data="site_list")],
]
