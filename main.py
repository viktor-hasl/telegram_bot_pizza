import os
import asyncio

from aiogram import Bot, Dispatcher

from handlers import privat_handlers, admin_handlers

from dotenv import load_dotenv

load_dotenv()

async def main():
    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(privat_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.set_my_commands()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



