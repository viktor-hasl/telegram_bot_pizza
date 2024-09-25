from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from filters import type_chat_filter, check_admins
from keyboards.kb_admin import kb_admin
from middlewares.db import SessionMiddleware
from database.engine import session_maker
from orm_query import orm_add_product, orm_get_products

router = Router()
router.message.filter(type_chat_filter.ChatTypeFilter(['private']), check_admins.CheckAdmin())
router.message.middleware(SessionMiddleware(session_pool=session_maker))


class AddProductState(StatesGroup):
    title = State()
    description = State()
    price = State()
    photo = State()


@router.message(Command('admin'))
async def admin_cmd(message: Message):
    await message.answer('Что вас интересует?',
                         reply_markup=kb_admin(['Добавить пиццу', 'Меню админа']))
    await message.delete()


# Добавление пиццы---------------------------------------------------------------------------------------------------
@router.message(StateFilter(None), F.text.lower() == 'добавить пиццу')
@router.message(StateFilter(None), Command('add_pizza'))
async def add_pizza_cmd(message: Message, state: FSMContext):
    await message.answer('Введите название пиццы, ', reply_markup=kb_admin(['Отмена']))
    await state.set_state(AddProductState.title)
    await message.delete()


@router.message(StateFilter('*'), F.text.lower() == 'отмена')
async def cancel_game(message: Message, state: FSMContext):
    now_state = await state.get_state()
    if now_state is None:
        return
    else:
        await state.clear()
        await message.answer('Процесс остановлен', reply_markup=kb_admin(['Добавить пиццу', 'Меню админа']))


@router.message(AddProductState.title, F.text)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddProductState.description)
    await message.answer('Введите описание пиццы')


@router.message(AddProductState.title)
async def no_title(message: Message):
    await message.answer('Нужно ввести текст ')


@router.message(AddProductState.description, F.text)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProductState.price)
    await message.answer("Теперь введите цену")


@router.message(AddProductState.description)
async def no_description(message: Message):
    await message.answer('Нужно ввести текст ')


@router.message(AddProductState.price, F.text)
async def add_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AddProductState.photo)
    await message.answer('Теперь отправьте фото пиццы')


@router.message(AddProductState.price)
async def no_price(message: Message):
    await message.answer('Нужно ввести цену ')


@router.message(AddProductState.photo, F.photo)
async def add_photo(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer_photo(photo=data['photo'], caption=f'{data["title"]}\n{data["description"]}\n{data["price"]}',
                               reply_markup=kb_admin(['Добавить пиццу', 'Меню админа']))

    # Добавление продукта в бд
    try:
        await orm_add_product(session, data)
        await message.answer('Товар добавлен')
        # Очистка машинного состояния
        await state.clear()
    except Exception as e:
        str_er = str(e)
        await message.answer(f'Ошибка: {str_er}, обратитесь к программисту')
        await state.clear()


@router.message(AddProductState.photo)
async def no_photo(message: Message):
    await message.answer('Нужно отправить фото')


# ---------------------------------------------------------------------------------------------------

@router.message(F.text.lower() == 'меню админа')
@router.message(Command('menu_admin'))
async def menu_admin_cmd(message: Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(photo=product.photo,
                                   caption=f'{product.title}\n{product.description}\n{round(product.price, 2)}',
                                   reply_markup=kb_admin(['Добавить пиццу', 'Меню админа']))

    await message.answer('Меню админа')
    await message.delete()
