from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from filters import type_chat_filter, check_admins
from keyboards.kb_admin import kb_admin

router = Router()
router.message.filter(type_chat_filter.ChatTypeFilter(['private']), check_admins.CheckAdmin())


class AddProductState(StatesGroup):
    title = State()
    description = State()
    price = State()
    photo = State()


@router.message(Command('admin'))
async def admin_cmd(message: Message):
    await message.answer('При этой команде будет выводиться список админов группы и допускаться к этим командам только им',
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
async def add_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer_photo(photo=data['photo'], caption=f'{data["title"]}\n{data["description"]}\n{data["price"]}', reply_markup=kb_admin(['Добавить пиццу', 'Меню админа']))
    await state.clear()


@router.message(AddProductState.photo)
async def no_photo(message: Message):
    await message.answer('Нужно отправить фото')


#---------------------------------------------------------------------------------------------------


@router.message(F.text.lower() == 'меню админа')
@router.message(Command('menu_admin'))
async def menu_admin_cmd(message: Message):
    await message.answer('Меню админа')
    await message.delete()


