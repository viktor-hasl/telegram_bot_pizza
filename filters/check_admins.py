from aiogram.types import Message
from aiogram.filters import BaseFilter

from config.config import list_admins


class Checkadmin(BaseFilter):
    async def __call__(self, message: Message):
        if message.from_user.id in list_admins:
            return True
        else:
            return False
