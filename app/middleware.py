from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class DBMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def __call__(self, handler, event: TelegramObject, data: dict = None):
        if data is None:
            data = {}

        # Безопасно пробуем добавить соединение с БД
        async with self.pool.acquire() as conn:
            data["db"] = conn
            return await handler(event, data)
