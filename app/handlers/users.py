from aiogram import Router, F # type: ignore
from app import db
from app.config import ADMINS, WEB_APP_URL
from app.keyboards import reply_kb, webapp_kb, users_inline_schedule_kb
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
    
    # Собираем полное имя
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = (first_name + " " + last_name).strip()

    # Проверяем: есть ли запись о пользователе
    row = await db.fetchrow("SELECT * FROM users WHERE telegram_id = $1", user_id)
    
    if row:
        # Уже был запуск
        return await message.answer("👋 Ты уже запускал бота.", reply_markup=reply_kb)
    
    # Первый запуск → записываем в БД
    await db.execute(
        "INSERT INTO users (telegram_id, full_name) VALUES ($1, $2);",
        user_id,
        full_name
    )
    
    await message.answer(f"Привет, {full_name}!", reply_markup=reply_kb)
    await message.answer("Открой мини-приложение:", reply_markup=webapp_kb)



@router.message(F.text == "📄 Последние записи")
async def show_posts(message: Message, db):
    rows = await db.fetch(
        "SELECT user_id, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 5"
    )
    if not rows:
        return await message.answer("📭 Нет записей.")

    text = "\n\n".join([
        f"<b>{r['created_at']:%d.%m}</b>\n<code>{r['data']}</code>"
        for r in rows
    ])
    await message.answer(f"📄 Последние 5 записей:\n\n{text}")



@router.message(F.text == "📣 Предупредить об опоздании")
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

@router.message(F.text == "📅 Расписание")
async def schedule(message: Message, db):
    await message.answer("Выберите действие:", reply_markup=users_inline_schedule_kb)


@router.callback_query(F.data == "schedule_tomorrow")
async def schedule_tomorrow(callback: CallbackQuery, db):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday()  # Понедельник = 0, Воскресенье = 6
        
    rows = await db.fetch(
        "SELECT id, pair_number, subject FROM schedules WHERE day_of_week = $1 ORDER BY pair_number",
        tomorrow_weekday
    )

    if not rows:
        return await callback.message.answer("Расписание на завтра отсутствует.")

    schedule_text = f"📅 Расписание на {tomorrow.strftime('%d.%m.%Y')}:\n"
    for row in rows:
        schedule_text += f"{row['pair_number']} пара — {row['subject']}\n"

    await callback.message.answer(schedule_text)

@router.callback_query(F.data == "schedule_week")
async def schedule_week(message: Message, db):
    today = datetime.now()
    week_type = today.isocalendar()[1] % 2 + 1
    
    
