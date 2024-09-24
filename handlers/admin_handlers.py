from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from filters import type_chat_filter, check_admins
from keyboards.kb_admin import kb_admin

router = Router()
router.message.filter(type_chat_filter.ChatTypeFilter(['private']), check_admins.Checkadmin())


@router.message(Command('admin'))
async def admin_cmd(message: Message):
    await message.answer('При этой команде будет выводиться список админов группы и допускаться к этим командам только им',
                         reply_markup=kb_admin(['Добавить пиццу', 'Меню админа']))
    await message.delete()


@router.message(F.text.lower() == 'добавить пиццу')
@router.message(Command('add_pizza'))
async def add_pizza_cmd(message: Message):
    await message.answer('Добавление пиццы')
    await message.delete()


@router.message(F.text.lower() == 'меню админа')
@router.message(Command('menu_admin'))
async def menu_admin_cmd(message: Message):
    await message.answer('Меню админа')
    await message.delete()


