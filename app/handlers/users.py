from aiogram import Router, F # type: ignore
from app import db
from app.config import ADMINS, WEB_APP_URL
from app.keyboards import users_kb, webapp_kb, users_inline_schedule_kb, admin_inline_schedule_kb, admin_kb, back_kb
from datetime import datetime, timedelta
from aiogram.types import (
    Message,
    CallbackQuery,
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
        if message.from_user.id in ADMINS:
            return await message.answer("👋 Ты уже запускал бота.", reply_markup=admin_kb)
        else:
            return await message.answer("👋 Ты уже запускал бота.", reply_markup=users_kb)
    
    # Первый запуск → записываем в БД
    await db.execute(
        "INSERT INTO users (telegram_id, full_name) VALUES ($1, $2);",
        user_id,
        full_name
    )
    
    if message.from_user.id in ADMINS:
        await message.answer(f"Привет, {full_name}!", reply_markup=admin_kb)
    else:
        await message.answer(f"Привет, {full_name}!", reply_markup=users_kb)
    await message.answer("Открой мини-приложение:", reply_markup=webapp_kb)



@router.callback_query(F.data == "show_posts")
async def show_posts(message: Message, db):
    rows = await db.fetch(
        "SELECT user_id, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 5"
    )
    if not rows:
        return await message.answer("📭 Нет записей.", reply_markup=back_kb)

    text = "\n\n".join([
        f"<b>{r['created_at']:%d.%m}</b>\n<code>{r['data']}</code>"
        for r in rows
    ])
    await message.answer(f"📄 Последние 5 записей:\n\n{text}", reply_markup=back_kb)



@router.callback_query(F.data == "delay")
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

@router.callback_query(F.data == "schedule")
async def schedule(callback: CallbackQuery, db):
    if callback.from_user.id in ADMINS:
        await callback.message.answer("Выберите действие:", reply_markup=admin_inline_schedule_kb)
    else:
        await callback.message.answer("Выберите действие:", reply_markup=users_inline_schedule_kb)


@router.callback_query(F.data == "schedule_tomorrow")
async def schedule_tomorrow(callback: CallbackQuery, db):
    week_type = datetime.now().isocalendar()[1] % 2 + 1
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday()  # Понедельник = 0, Воскресенье = 6
        
    rows = await db.fetch(
        "SELECT id, pair_number, subject FROM schedules WHERE week_type = $1 AND day_of_week = $2 ORDER BY pair_number",
        week_type,
        tomorrow_weekday
    )

    if not rows:
        return await callback.message.answer("Расписание на завтра отсутствует.", reply_markup=back_kb)

    schedule_text = f"📅 Расписание на {tomorrow.strftime('%d.%m.%Y')}:\n"
    for row in rows:
        schedule_text += f"{row['pair_number']} пара — {row['subject']}\n"

    await callback.message.answer(schedule_text, reply_markup=back_kb)
    await callback.answer()

@router.callback_query(F.data == "schedule_week")
async def schedule_week(callback: CallbackQuery, db):
    today = datetime.now()
    week_type = today.isocalendar()[1] % 2 + 1
    
    rows = await db.fetch(
        "SELECT id, pair_number, subject FROM schedules WHERE week_type = $1 ORDER BY day_of_week, pair_number",
        week_type
    )
    
    if not rows:
        return await callback.message.answer("Расписание на неделю отсутствует.", reply_markup=back_kb)

    schedule_text = "\n\n".join([
        f"{row['pair_number']} пара — {row['subject']}"
        for row in rows
    ])
    await callback.message.answer(schedule_text, reply_markup=back_kb)
    await callback.answer()
    
@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=reply_kb)
