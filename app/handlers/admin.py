from aiogram import Router, F
from aiogram.types import Message
from app.config import ADMINS
from aiogram.filters import Command
from app.keyboards import admin_inline_posts_kb, admin_inline_schedule_kb, admin_kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

class PostForm(StatesGroup):
    waiting_for_post = State()

@router.message(F.text == "✏️ Записи")
async def cmd_posts(message: Message):
    await message.answer("Выберите действие:", reply_markup=admin_inline_posts_kb)


@router.callback_query(F.data == "add_post")
async def cmd_add_post(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✍️ Введите текст записи:")
    await state.set_state(PostForm.waiting_for_post)

@router.callback_query(PostForm.waiting_for_post)
async def process_post(callback: CallbackQuery, state: FSMContext, db):
    text = message.text.strip()
    full_name = from_user.full_name or from_user.username or "Неизвестный"
    data = message.text
    if not text:
        return await callback.message.answer("⚠️ Текст не может быть пустым. Попробуйте ещё раз.")

    await db.execute(
        "INSERT INTO webapp_data (full_name, data) VALUES ($1, $2);",
        full_name,
        text
    )
    await callback.message.answer("✅ Запись добавлена!")
    await state.clear()


class DeleteRecord(StatesGroup):
    waiting_for_record_id = State()

@router.callback_query(F.data == "delete_post")
async def delete_record_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🗑 Введи ID записи, которую хочешь удалить:")
    await state.set_state(DeleteRecord.waiting_for_record_id)

@router.callback_query(DeleteRecord.waiting_for_record_id)
async def delete_record_confirm(callback: CallbackQuery, state: FSMContext, db):
    if not callback.message.text.isdigit():
        return await callback.message.answer("⚠️ ID должен быть числом. Попробуй ещё раз.")
    
    post_id = int(callback.message.text)
    result = await db.execute("DELETE FROM webapp_data WHERE id = $1", post_id)
    
    if result == "DELETE 1":
        await callback.message.answer(f"✅ Запись #{post_id} успешно удалена.")
    else:
        await callback.message.answer("❌ Запись с таким ID не найдена.")
    
    await state.clear()


# Функция просмотра последних 10 записей (только для админов)
@router.callback_query(F.data == "list_posts")
async def list_posts(callback: CallbackQuery, db):
    rows = await db.fetch("SELECT id, full_name, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 10")
    if not rows:
        return await callback.message.answer("📭 Нет записей.")

    text = "\n\n".join([
        f"#{r['id']} | {r['full_name']} | {r['created_at'].strftime('%d.%m')}\n {r['data']}"
        for r in rows
    ])
    await callback.message.answer(f"🗂 Последние записи:\n\n{text}")

class ScheduleForm(StatesGroup):
    waiting_for_data = State()


@router.message(F.text == "📆 Расписание")
async def cmd_schedule(message: Message):
    await message.answer("Выберите действие:", reply_markup=admin_inline_schedule_kb)


@router.callback_query(F.data == "change_schedule")
async def change_schedule(message: Message, state: FSMContext):
    await message.answer("Введите данные в формате:\n\"Номер недели, Номер дня недели, Номер пары, Название предмета\"\nПример: 1, 3, 2, Алгебра")
    await state.set_state(ScheduleForm.waiting_for_data)
    
@router.message(ScheduleForm.waiting_for_data)
async def process_data(message: Message, state: FSMContext, db):
    text = message.text.strip()
    parts = [p.strip() for p in text.split(",")]

    # Проверка на количество аргументов
    if len(parts) != 4:
        return await message.answer("⚠️ Неверный формат данных. Попробуйте ещё раз.")

    week_type_str, day_of_week_str, pair_number_str, subject = parts

    # Проверка, что первые три — числа
    if not (week_type_str.isdigit() and day_of_week_str.isdigit() and pair_number_str.isdigit()):
        return await message.answer("⚠️ Неверный формат данных. Попробуйте ещё раз.")

    # Преобразуем в int
    week_type = int(week_type_str)
    day_of_week = int(day_of_week_str)
    pair_number = int(pair_number_str)

    # Отладка
    print("DEBUG types:",
          type(week_type), week_type,
          type(day_of_week), day_of_week,
          type(pair_number), pair_number,
          type(subject), subject)

    # Вставка в базу
    await db.execute(
        "INSERT INTO schedules (week_type, day_of_week, pair_number, subject) VALUES ($1, $2, $3, $4);",
        week_type,
        day_of_week,
        pair_number,
        subject
    )

    await message.answer("✅ Расписание успешно изменено!")
    await state.clear()


@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 У тебя нет доступа.")
    
    await message.answer("👑 Админ-панель:\n- /list — посмотреть все записи", reply_markup=admin_kb)    
