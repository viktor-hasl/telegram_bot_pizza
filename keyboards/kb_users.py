from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_users = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='О нас'), KeyboardButton(text='Помощь')], [KeyboardButton(text='Меню'), ]],
    resize_keyboard=True
)

ikb_main_page = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наше меню', callback_data='menu')],
    [InlineKeyboardButton(text='Корзина', callback_data='cart'), InlineKeyboardButton(text='О нас', callback_data='about')]])