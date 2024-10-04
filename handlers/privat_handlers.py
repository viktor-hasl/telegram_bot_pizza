from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession

from filters.type_chat_filter import ChatTypeFilter
from keyboards.kb_users import ikb_main_page, ikb_menu_page, ikb_cart_page, kb_users
from database.engine import session_maker
from middlewares.db import SessionMiddleware
from orm_query import (orm_get_products, orm_get_banner, orm_add_product_in_cart,
                       orm_get_all_products_in_cart, orm_get_one, orm_del_product_in_cart, orm_del_all_products_in_cart)

router = Router()
router.message.filter(ChatTypeFilter(['private']))
router.message.middleware(SessionMiddleware(session_pool=session_maker))
router.callback_query.middleware(SessionMiddleware(session_pool=session_maker))


@router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):

    if await orm_get_banner(session) is None:
        await message.answer_photo(photo='AgACAgIAAxkBAAITu2b1nyGGnw0_OdThBJXvXpcJv6cZAAIc4TEbhT6xS-RiOETEXy_0AQADAgADeQADNgQ',
                                   caption='Добро пожаловать в нашу пиццерию.\nМы очень рады вас видеть!\nTут вы можете заказать себе вкусную пиццу',
                                   reply_markup=ikb_main_page)
    else:
        banner = await orm_get_banner(session)
        await message.answer_photo(photo=banner.photo,
                                   caption='Добро пожаловать в нашу пиццерию.\nМы очень рады вас видеть!\n'
                                           'Tут вы можете заказать себе вкусную пиццу', reply_markup=ikb_main_page)


@router.callback_query(F.data == 'menu')
async def menu_cmd(callback: CallbackQuery, session: AsyncSession):
    products = await orm_get_products(session)
    await callback.message.edit_media(media=InputMediaPhoto(media=products[0].photo,
                                                            caption=f'<b>{products[0].title}</b>\n{products[0].description}\n'
                                                                    f'{round(products[0].price, 2)}\nстраница 1 из {len(products)}', parse_mode=ParseMode.HTML ),
                                      reply_markup=ikb_menu_page(products[0].page, products[0].id))


@router.callback_query(F.data.startswith('next'))
async def next_product_callback(callback: CallbackQuery, session: AsyncSession):
    # Переходы в корзине
    if callback.data.split('_')[1] == 'cart':
        products_cart = await orm_get_all_products_in_cart(session, callback.message.from_user.id)
        page = int(callback.data.split('_')[-1])
        if page < len(products_cart) - 1:
            page += 1
            product = await orm_get_one(session, products_cart[page].id_product)
            all_price = round(0, 2)
            for cart in products_cart:
                prod = await orm_get_one(session, cart.id_product)
                all_price += round(prod.price, 2)
            await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                                    caption=f'<b>{product.title}</b>\n{product.description}\n'
                                                                            f'{round(product.price, 2)}\n'
                                                                            f'товар {page + 1} из {len(products_cart)}\n'
                                                                            f'Общая сумма: {all_price}',
                                                                    parse_mode=ParseMode.HTML),
                                              reply_markup=ikb_cart_page(products_cart[page].page, products_cart[page].id, id_product=product.id))
            return None
        else:
            return None

    # Переходы товаров в меню
    products = await orm_get_products(session)
    page = int(callback.data.split('_')[-1])
    max_page = len(products)
    if page < max_page-1:
        page += 1
    else:
        await callback.answer('Закончились (((', show_alert=True)
        return None
    await callback.message.edit_media(media=InputMediaPhoto(media=products[page].photo,
                                                            caption=f'<b>{products[page].title}</b>\n{products[page].description}\n'
                                                                    f'{round(products[page].price, 2)}\nстраница {page+1} из {len(products)}',
                                                            parse_mode=ParseMode.HTML),
                                      reply_markup=ikb_menu_page(products[page].page, products[page].id))


@router.callback_query(F.data.startswith('back'))
async def next_product_callback(callback: CallbackQuery, session: AsyncSession):
    # Переходы в корзине
    if callback.data.split('_')[1] == 'cart':
        products_cart = await orm_get_all_products_in_cart(session, callback.message.from_user.id)
        page = int(callback.data.split('_')[-1])
        if page > 0:
            page -= 1
            product = await orm_get_one(session, products_cart[page].id_product)
            all_price = round(0, 2)
            for cart in products_cart:
                prod = await orm_get_one(session, cart.id_product)
                all_price += round(prod.price, 2)
            await callback.answer()
            await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                                    caption=f'<b>{product.title}</b>\n{product.description}\n'
                                                                            f'{round(product.price, 2)}\n'
                                                                            f'товар {page + 1} из {len(products_cart)}\n'
                                                                            f'Общая сумма: {all_price}',
                                                                    parse_mode=ParseMode.HTML),
                                              reply_markup=ikb_cart_page(products_cart[page].page, products_cart[page].id, id_product=product.id))
            return None
        else:
            await callback.answer()
            return None

    # Переходы товаров в меню

    products = await orm_get_products(session)
    page = int(callback.data.split('_')[-1])
    if page > 0:
        page -= 1
    else:
        await callback.answer('Вы уже вначале =))', show_alert=True)
        return None
    await callback.message.edit_media(media=InputMediaPhoto(media=products[page].photo,
                                                            caption=f'<b>{products[page].title}</b>\n{products[page].description}\n'
                                                                    f'{round(products[page].price, 2)}\nстраница {page + 1} из {len(products)}',
                                                            parse_mode=ParseMode.HTML),
                                      reply_markup=ikb_menu_page(products[page].page, products[page].id))


############################################################ Корзина ########################################################
@router.callback_query(F.data == 'cart')
async def cart(callback: CallbackQuery, session: AsyncSession):
    products_cart = await orm_get_all_products_in_cart(session, callback.message.from_user.id)
    if len(products_cart) == 0:
        await callback.answer('Корзина пуста', show_alert=True)
        return None
    all_price = round(0, 2)
    for cart in products_cart:
        prod = await orm_get_one(session, cart.id_product)
        all_price += round(prod.price, 2)
    product = await orm_get_one(session, products_cart[0].id_product)
    await callback.answer()
    await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                            caption=f'<b>{product.title}</b>\n{product.description}\n'
                                                                    f'{round(product.price, 2)}\nстраница {1} из {len(products_cart)}\n'
                                                                    f'Общая сумма:{all_price}',
                                                            parse_mode=ParseMode.HTML),
                                      reply_markup=ikb_cart_page(products_cart[0].page, products_cart[0].id, id_product=product.id))


@router.callback_query(F.data.startswith('addInCart'))
async def add_product_in_cart(callback: CallbackQuery, session: AsyncSession,):
    id_product = int(callback.data.split('_')[-1])
    await orm_add_product_in_cart(session, id_product=id_product, id_user=callback.message.from_user.id)
    await callback.answer('Товар добавлен', show_alert=True)
    if callback.data.split('_')[1] == 'cart':
        products_cart = await orm_get_all_products_in_cart(session, callback.message.from_user.id)
        product = await orm_get_one(session, products_cart[0].id_product)
        all_price = round(0, 2)
        for cart in products_cart:
            prod = await orm_get_one(session, cart.id_product)
            all_price += round(prod.price, 2)
        await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                                caption=f'<b>{product.title}</b>\n{product.description}\n'
                                                                        f'{round(product.price, 2)}\nстраница {1} из {len(products_cart)}\n'
                                                                        f'Общая сумма: {all_price}',
                                                                parse_mode=ParseMode.HTML),
                                          reply_markup=ikb_cart_page(products_cart[0].page, products_cart[0].id, id_product=product.id))
    await callback.answer()


@router.callback_query(F.data.startswith('delInCart'))
async def del_product_in_cart(callback: CallbackQuery, session: AsyncSession):
    id_product = int(callback.data.split('_')[-1])
    await orm_del_product_in_cart(session, id_product)
    products_cart = await orm_get_all_products_in_cart(session, callback.message.from_user.id)
    product = await orm_get_one(session, products_cart[0].id_product)
    all_price = round(0, 2)
    for cart in products_cart:
        prod = await orm_get_one(session, cart.id_product)
        all_price += round(prod.price, 2)
    await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                            caption=f'<b>{product.title}</b>\n{product.description}\n'
                                                                    f'{round(product.price, 2)}\nстраница {1} из {len(products_cart)}\n'
                                                                    f'Общая сумма: {all_price}',
                                                            parse_mode=ParseMode.HTML),
                                      reply_markup=ikb_cart_page(products_cart[0].page, products_cart[0].id, id_product=product.id))
    await callback.answer()


@router.callback_query(F.data == 'clear_cart')
async def clear_cart(callback: CallbackQuery, session):
    await orm_del_all_products_in_cart(session, callback.message.from_user.id)
    await callback.message.edit_caption(caption='Наша пиццерия такая-то, мы находимся там-то, готовим очень вкусную пиццу, рады что вы к нам заглянули'
                                                'можете заказать пиццу в тг боте,а можете тут выбрать, а затем позвонить нам, приятного'
                                                'аппетита, хорошего дня НАШИ НОМЕРА', reply_markup=ikb_main_page)
    await callback.answer('Корзина очищена', show_alert=True)


############################### Оформление заказа ########################################################

class OrderState(StatesGroup):
    name = State()
    phone = State()
    address = State()


@router.message(StateFilter('*'), F.text.lower() == 'отмена')
async def cancel_game(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено, для открытия меню нажмите /start', reply_markup=ReplyKeyboardRemove())


@router.callback_query(StateFilter(None), F.data == 'order')
async def order(callback: CallbackQuery, state: FSMContext, session):
    user_id = callback.message.from_user.id
    carts = await orm_get_all_products_in_cart(session, user_id)
    all_price = round(0, 2)
    products_str = ''
    for cart in carts:
        product = await orm_get_one(session, cart.id_product)
        all_price += round(product.price, 2)
        products_str += f'{product.title} - {round(product.price, 2)}\n'
    await state.update_data(all_price=all_price, products_str=products_str)
    await orm_del_all_products_in_cart(session, user_id)
    await state.set_state(OrderState.name)
    await callback.message.delete()
    await callback.message.answer('Введите ваше имя', reply_markup=kb_users)


@router.message(OrderState.name)
async def order_name(message: Message, state: FSMContext):
    await state.set_state(OrderState.phone)
    await state.update_data(name=message.text)
    await message.answer('Напишите ваш номер телефона', reply_markup=kb_users)


@router.message(OrderState.phone)
async def order_phone(message: Message, state: FSMContext):
    await state.set_state(OrderState.address)
    await state.update_data(phone=message.text)
    await message.answer('Укажите адрес доставки', reply_markup=kb_users)


@router.message(OrderState.address)
async def order_address(message: Message, state: FSMContext, session):
    from config import config
    data = await state.get_data()
    await message.bot.send_message(chat_id=config.group,
                                   text=f'Заказ:\n'
                                        f'{data["products_str"]}\n'
                                        f'Общая сумма: {data["all_price"]}\n'
                                        f'Имя: {data["name"]}\n'
                                        f'Адрес: {message.text}\n'
                                        f'Номер телефона: {data["phone"]}\n'
                                   )

    await message.answer('Заказ оформлен', reply_markup=ReplyKeyboardRemove())
    # очищаем стате
    await state.clear()

    if await orm_get_banner(session) is None:
        await message.answer_photo(photo='AgACAgIAAxkBAAITu2b1nyGGnw0_OdThBJXvXpcJv6cZAAIc4TEbhT6xS-RiOETEXy_0AQADAgADeQADNgQ',
                                   caption='Добро пожаловать в нашу пиццерию.\nМы очень рады вас видеть!\nTут вы можете заказать себе вкусную пиццу',
                                   reply_markup=ikb_main_page)
    else:
        banner = await orm_get_banner(session)
        await message.answer_photo(photo=banner.photo,
                                   caption='Добро пожаловать в нашу пиццерию.\nМы очень рады вас видеть!\n'
                                           'Tут вы можете заказать себе вкусную пиццу', reply_markup=ikb_main_page)


@router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer('Если пошло что-то не так введите команду /start и должно появиться главное меню')
    await message.delete()


@router.callback_query(F.data == 'about')
async def about_cmd(callback: CallbackQuery):
    await callback.message.edit_caption(caption='Наша пиццерия такая-то, мы находимся там-то, готовим очень вкусную пиццу, рады что вы к нам заглянули'
                                                'можете заказать пиццу в тг боте,а можете тут выбрать, а затем позвонить нам, приятного'
                                                'аппетита, хорошего дня НАШИ НОМЕРА', reply_markup=ikb_main_page)
    await callback.answer()
