from aiogram import Router, F # type: ignore
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
router = Router()

WEB_APP_URL = "https://vercel-gray-gamma.vercel.app/"

@router.message(F.text == "/start")
async def start_handler(message: Message):
    # Обычные кнопки внизу
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Последние записи")]
        ],
        resize_keyboard=True
    )

    # Inline-кнопка для Mini App (это нельзя сделать через обычную кнопку)
    webapp_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть мини-апп 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    await message.answer("Привет! Жми на мини-апп или посмотри записи 👇", reply_markup=reply_kb)
    await message.answer("Открой мини-приложение:", reply_markup=webapp_kb)

@router.message(F.text == "📄 Последние записи")
async def show_posts(message: Message, db):
    rows = await db.fetch(
        "SELECT user_id, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 3"
    )
    if not rows:
        return await message.answer("📭 Нет записей.")

    text = "\n\n".join([
        f"<b>{r['created_at']:%d-%m}</b>\n<code>{r['data']}</code>"
        for r in rows
    ])
    await message.answer(f"📄 Последние 3 записи:\n\n{text}")
