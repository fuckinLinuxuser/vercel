from aiogram import Router, F
from aiogram.types import Message
from app.config import ADMINS
from aiogram.filters import Command
from app.keyboards import admin_kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


router = Router()

class Form(StatesGroup):
    waiting_for_post = State()

@router.message(F.text == "✏️ Добавить запись")
async def cmd_add_post(message: Message, state: FSMContext):
    await message.answer("✍️ Введите текст записи:")
    await state.set_state(Form.waiting_for_post)

@router.message(Form.waiting_for_post)
async def process_post(message: Message, state: FSMContext, db):
    text = message.text.strip()
    full_name = message.from_user.full_name or message.from_user.username or "Неизвестный"
    data = message.text
    if not text:
        return await message.answer("⚠️ Текст не может быть пустым. Попробуйте ещё раз.")

    await db.execute(
        "INSERT INTO webapp_data (full_name, data) VALUES ($1, $2);",
        full_name,
        text
    )
    await message.answer("✅ Запись добавлена!")
    await state.clear()


class DeleteRecord(StatesGroup):
    waiting_for_id = State()

@router.message(F.text == "🗑 Удалить запись")
async def delete_record_start(message: Message, state: FSMContext):
    await message.answer("🗑 Введи ID записи, которую хочешь удалить:")
    await state.set_state(DeleteRecord.waiting_for_id)

@router.message(DeleteRecord.waiting_for_id)
async def delete_record_confirm(message: Message, state: FSMContext, db):
    if not message.text.isdigit():
        return await message.answer("⚠️ ID должен быть числом. Попробуй ещё раз.")
    
    post_id = int(message.text)
    result = await db.execute("DELETE FROM webapp_data WHERE id = $1", post_id)
    
    if result == "DELETE 1":
        await message.answer(f"✅ Запись #{post_id} успешно удалена.")
    else:
        await message.answer("❌ Запись с таким ID не найдена.")
    
    await state.clear()




# Функция просмотра последних 10 записей (только для админов)
@router.message(F.text == "📖 Посмотреть записи")
async def list_posts(message: Message, db):
    rows = await db.fetch("SELECT id, full_name, data, created_at FROM webapp_data ORDER BY id DESC LIMIT 10")
    if not rows:
        return await message.answer("📭 Нет записей.")

    text = "\n\n".join([
        f"#{r['id']} | {r['full_name']} | {r['created_at'].strftime('%d.%m')}\n {r['data']}"
        for r in rows
    ])
    await message.answer(f"🗂 Последние записи:\n\n{text}")


@router.message(F.text == "Изменить расписание")
async def change_schedule(message: Message, state: FSMContext, db):
    await message.answer("Введите данные в формате: \"Номер недели, Номер дня недели, Номер пары, Название предмета\"")
    await state.set_state(Form.waiting_for_post)

@router.message(Form.waiting_for_post)
async def process_post(message: Message, state: FSMContext, db):
    await db.execute("INSERT INTO schedules (week_type, day_of_week, pair_number, subject) VALUES ($1, $2, $3, $4);", message.text)
    await message.answer("✅ Расписание изменено!")
    await state.clear()
    

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("🚫 У тебя нет доступа.")
    
    await message.answer("👑 Админ-панель:\n- /list — посмотреть все записи", reply_markup=admin_kb)    
