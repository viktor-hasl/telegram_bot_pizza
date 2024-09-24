from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import BaseFilter


class CheckAdmin(BaseFilter):
    async def __call__(self, message: Message, bot: Bot):
        if message.from_user.id in bot.list_admins:
            return True
        else:
            return False
