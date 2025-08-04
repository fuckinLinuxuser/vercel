from aiogram import Router, F
from aiogram.types import Message
from app.config import ADMINS

router = Router()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 У тебя нет доступа.")
    
    await message.answer("👑 Админ-панель:\n- /list — посмотреть все записи")

@router.message(F.text == "/list")
async def list_entries(message: Message, db):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 Доступ запрещён.")

    rows = await db.fetch("SELECT user_id, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 10;")
    if not rows:
        return await message.answer("📭 Нет данных.")

    text = "\n\n".join([f"<b>{r['user_id']}</b> | {r['created_at']:%Y-%m-%d}:\n<code>{r['data']}</code>" for r in rows])
    await message.answer(f"🗂 Последние записи:\n\n{text}")
