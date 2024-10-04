from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_users = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отмена')]], resize_keyboard=True
)

ikb_main_page = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наше меню', callback_data='menu')],
    [InlineKeyboardButton(text='Корзина', callback_data='cart'), InlineKeyboardButton(text='О нас', callback_data='about')]])

def ikb_menu_page(page: int, id_product):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👈", callback_data=f'back_{page}'), InlineKeyboardButton(text='Добавить в корзину', callback_data=f'addInCart_{id_product}'),
         InlineKeyboardButton(text='👉', callback_data=f'next_{page}')],
        [InlineKeyboardButton(text='Корзина', callback_data='cart'), InlineKeyboardButton(text='Главное меню', callback_data='about')]

])


def ikb_cart_page(page, id_cart, id_product):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👈", callback_data=f'back_cart_{page}'), InlineKeyboardButton(text='👉', callback_data=f'next_cart_{page}')],
        [InlineKeyboardButton(text='Добавить ещё', callback_data=f'addInCart_cart_{id_product}'),
         InlineKeyboardButton(text='Удалить из корзины', callback_data=f'delInCart_{id_cart}')],
        [InlineKeyboardButton(text='Очистить корзину', callback_data='clear_cart'), InlineKeyboardButton(text='Главное меню', callback_data='about')],
        [InlineKeyboardButton(text="Оформить заказа", callback_data='order')],

    ])