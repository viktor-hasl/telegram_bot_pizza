from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from filters.type_chat_filter import ChatTypeFilter
from keyboards.kb_admin import ikb_admin
from keyboards.kb_users import kb_users
from database.engine import session_maker
from middlewares.db import SessionMiddleware
from orm_query import orm_get_products, orm_get_one

router = Router()
router.message.filter(ChatTypeFilter(['private']))
router.message.middleware(SessionMiddleware(session_pool=session_maker))
router.callback_query.middleware(SessionMiddleware(session_pool=session_maker))


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer('Добро пожаловать текст, начало использования бота', reply_markup=kb_users)
    await message.bot.delete_message(message.chat.id, message_id=message.message_id)


@router.message(F.text.lower() == 'о нас')
@router.message(Command('about'))
async def about_cmd(message: Message):
    await message.answer('Текст о нас')
    await message.bot.delete_message(message.chat.id, message_id=message.message_id)


@router.message(F.text.lower() == 'меню')
@router.message(Command('menu'))
async def menu_cmd(message: Message, session: AsyncSession, state: FSMContext):
    products = await orm_get_products(session)
    list_id_product = []
    index = 0
    for product in products:
        list_id_product.append(product.id)
    await state.update_data(list_id_product=list_id_product, index=index)
    await message.answer_photo(photo=products[index].photo,
                               caption=f'{products[index].title}\n{products[index].description}\n{round(products[index].price, 2)}',
                               reply_markup=ikb_admin({'👈': 'back',  '❌': 'end', '👉': 'next'}))

    await message.bot.delete_message(message.chat.id, message_id=message.message_id)


@router.callback_query(F.data.startswith('next'))
async def next_product_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    if not data:
        await callback.message.delete()
        return
    products_id = data['list_id_product']
    index = data['index']
    if index < len(products_id)-1:
        index += 1
        product = await orm_get_one(session, products_id[index])
        await state.update_data(index=index)
        await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                                caption=f'{product.title}\n{product.description}\n{round(product.price, 2)}', ),
                                          reply_markup=ikb_admin({'👈': 'back', '❌': 'end', '👉': f'next'}))
        await callback.answer()
    else:
        await callback.answer('Закончились =((( \nПопробуйте ещё раз вызвать меню, может что-то добавили =)))', show_alert=True)


@router.callback_query(F.data.startswith('back'))
async def next_product_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    if not data:
        await callback.message.delete()
        return
    products_id = data['list_id_product']
    index = data['index']
    if index > 0:
        index -= 1
        product = await orm_get_one(session, products_id[index])
        await state.update_data(index=index)
        await callback.message.edit_media(media=InputMediaPhoto(media=product.photo,
                                                                caption=f'{product.title}\n{product.description}\n{round(product.price, 2)}', ),
                                          reply_markup=ikb_admin({'👈': 'back', '❌': 'end', '👉': f'next'}))
        await callback.answer()
    else:
        await callback.answer('Ты уже в начале 😉😉', show_alert=True)

@router.callback_query(F.data == 'end')
async def end_check_products(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

@router.message(F.text.lower() == 'помощь')
@router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer('help text')
    await message.delete()
