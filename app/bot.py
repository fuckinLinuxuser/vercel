import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# URL на твой мини-апп, размещённый на Vercel или GitHub Pages
WEB_APP_URL = "https://vercel-gray-gamma.vercel.app/"

# Инициализация бота
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Стартовая команда с кнопкой
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть мини-апп 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Привет! Жми на кнопку и открой мини-апп.", reply_markup=keyboard)

# Обработка данных из мини-аппа
@dp.message(F.web_app_data)
async def webapp_data_handler(message: Message):
    data = message.web_app_data.data
    await message.answer(f"📬 Получено из мини-аппа:\n<code>{data}</code>")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

