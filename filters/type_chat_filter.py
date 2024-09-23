from aiogram.filters import BaseFilter
from aiogram.types import Message

# Фильтр на тип чата ____________________________________________________________


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: list):
        self.chat_type = chat_type

    async def __call__(self, message: Message):
        if message.chat.type in self.chat_type:
            return True
        else:
            return False