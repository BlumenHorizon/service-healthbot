from telegram import InlineKeyboardButton


def add_back_button(keyboard: list[list[InlineKeyboardButton]]) -> None:
    keyboard.append([InlineKeyboardButton(f"Back", callback_data=f"start")])
