from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def kb_admin(buttons: list):
    list_buttons = [KeyboardButton(text=name) for name in buttons]
    kb = ReplyKeyboardMarkup(keyboard=[list_buttons], resize_keyboard=True)
    return kb


def ikb_admin(buttons: dict):
    inline_button = [InlineKeyboardButton(text=key, callback_data=buttons[key]) for key in buttons.keys()]
    ikb = InlineKeyboardMarkup(inline_keyboard=[inline_button])
    return ikb

