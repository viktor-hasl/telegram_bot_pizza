from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def kb_admin(buttons: list):
    list_buttons = [KeyboardButton(text=name) for name in buttons]
    kb = ReplyKeyboardMarkup(keyboard=[list_buttons], resize_keyboard=True)
    return kb