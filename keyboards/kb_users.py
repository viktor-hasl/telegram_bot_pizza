from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_users = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='О нас'), KeyboardButton(text='Помощь')], [KeyboardButton(text='Меню'), ]],
    resize_keyboard=True
)