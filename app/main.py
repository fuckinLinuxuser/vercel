import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app import config, db
from app.middleware import DBMiddleware
from app.handlers import users, admin

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    db_pool = await db.create_db_pool()
    dp.message.middleware.register(DBMiddleware(db_pool))
    dp.callback_query.middleware.register(DBMiddleware(db_pool))

    dp.include_router(users.router)
    dp.include_router(admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
