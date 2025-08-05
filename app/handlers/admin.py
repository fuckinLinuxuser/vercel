from aiogram import Router, F
from aiogram.types import Message
from app.config import ADMINS
from aiogram.filters import Command

router = Router()

@router.message(Command("add"))
async def add_post(message: Message, db):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 У тебя нет доступа.")
    
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("⚠️ Используй: /add Текст записи")
    
    text = parts[1]
    await db.execute(
        "INSERT INTO webapp_data (user_id, data) VALUES ($1, $2);",
        message.from_user.id,
        text
    )
    await message.answer("✅ Запись добавлена!")


@router.message(Command("delete"))
async def delete_record(message: Message, db):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 У тебя нет доступа.")

    parts = message.text.strip().split()
    if len(parts) < 2 or not parts[1].isdigit():
        return await message.answer("⚠️ Используй: /delete ID")

    post_id = int(parts[1])
    result = await db.execute("DELETE FROM webapp_data WHERE id = $1", post_id)

    if result == "DELETE 1":
        await message.answer(f"🗑 Запись #{post_id} удалена.")
    else:
        await message.answer("❌ Запись не найдена.")


@router.message(Command("list"))
async def list_posts(message: Message, db):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 У тебя нет доступа.")

    rows = await db.fetch("SELECT id, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 10")
    if not rows:
        return await message.answer("📭 Нет записей.")

    text = "\n\n".join([
        f"#{r['id']} | {r['created_at']:%d-%m}\n<code>{r['data']}</code>"
        for r in rows
    ])
    await message.answer(f"🗂 Последние записи:\n\n{text}")



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

    text = "\n\n".join([f"<b>{r['user_id']}</b> | {r['created_at']:%d-%m}:\n<code>{r['data']}</code>" for r in rows])
    await message.answer(f"🗂 Последние записи:\n\n{text}")
