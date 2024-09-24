import os
import asyncio

from aiogram import Bot, Dispatcher, types, F

from handlers import privat_handlers, admin_handlers
from filters.type_chat_filter import ChatTypeFilter


from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()
    bot.list_admins = set()

    # С помощью этой команды будем обновлять список админов в нашей группе, которые могут пользоваться админ возможностями бота
    @dp.message(ChatTypeFilter(['group', 'supergroup']), F.text == 'admin')
    async def check_admin(message: types.Message):
        admins = await message.bot.get_chat_administrators(message.chat.id)
        for admin in admins:
            bot.list_admins.add(admin.user.id)
        await message.delete()

    dp.include_router(admin_handlers.router)
    dp.include_router(privat_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



