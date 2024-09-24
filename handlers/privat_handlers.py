from aiogram import Router, F

from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from filters.type_chat_filter import ChatTypeFilter
from keyboards.kb_users import kb_users


router = Router()
router.message.filter(ChatTypeFilter(['private']))


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
async def menu_cmd(message: Message):
    await message.answer('Список пицц')
    await message.bot.delete_message(message.chat.id, message_id=message.message_id)


@router.message(F.text.lower() == 'помощь')
@router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer('help text')
    await message.delete()


