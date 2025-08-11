from aiogram import Router, F # type: ignore
from app import db
from app.config import ADMINS, WEB_APP_URL
from app.keyboards import reply_kb, webapp_kb
from datetime import datetime, timedelta
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    CallbackQuery,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)


router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, db):
    user_id = message.from_user.id

    # Проверяем: есть ли запись о пользователе
    row = await db.fetchrow("SELECT * FROM users WHERE telegram_id = $1", user_id)
    
    if row:
        # Уже был запуск
        return await message.answer("👋 Ты уже запускал бота.", reply_markup=reply_kb)
    
    # Первый запуск → записываем в БД
    await db.execute(
        "INSERT INTO users (telegram_id) VALUES ($1);",
        user_id
    )


    await message.answer("Привет! Добро пожаловать 👋", reply_markup=reply_kb)
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



@router.message(F.text == "Предупредить об опоздании")
async def delay(message: Message, bot):
    user = message.from_user

    for admin_id in ADMINS:
        await bot.send_message(
            chat_id=admin_id,
            text=(
                f"📬 Пользователь <b>{user.full_name}</b> "
                f" \"📢 Задержится \""
            )
        )

    await message.answer ("Бот передал сообщение")

@router.message(F.text == "📅 Расписание на завтра")
async def schedule_tomorrow(message: Message, db):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday()  # Понедельник = 0, Воскресенье = 6

    rows = await db.fetch(
        "SELECT pair_number, subject FROM schedules WHERE day_of_week = $1 ORDER BY pair_number",
        tomorrow_weekday
    )

    if not rows:
        return await message.answer("Расписание на завтра отсутствует.")

    schedule_text = f"📅 Расписание на {tomorrow.strftime('%d.%m.%Y')}:\n"
    for row in rows:
        schedule_text += f"{row['pair_number']} пара — {row['subject']}\n"

    await message.answer(schedule_text)
