from aiogram import Router, F # type: ignore
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo # type: ignore

router = Router()

WEB_APP_URL = "https://vercel-gray-gamma.vercel.app/"

@router.message(F.text == "/start")
async def start_handler(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть мини-апп 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Привет! Жми на кнопку и открой мини-апп.", reply_markup=kb)

@router.message(F.web_app_data)
async def webapp_data_handler(message: Message, db):
    data = message.web_app_data.data
    await db.execute("INSERT INTO webapp_data (user_id, data) VALUES ($1, $2);", message.from_user.id, data)
    await message.answer(f"✅ Сохранил: <code>{data}</code>")
