from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.type_chat_filter import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(Command('admin'))
async def admin_cmd(message: Message):
    await message.answer('При этой команде будет выводиться список админов группы и допускаться к этим командам только им')
    await message.delete()


@router.message(Command('add_pizza'))
async def add_pizza_cmd(message: Message):
    await message.answer('Добавление пиццы')
    await message.delete()

