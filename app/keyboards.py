from app.config import WEB_APP_URL
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Последние записи")],
            [KeyboardButton(text="📣 Предупредить об опоздании")],
            [KeyboardButton(text="📅 Расписание на завтра")]
        ],
        resize_keyboard=True
    )

webapp_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть мини-апп 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

admin_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✏️ Добавить запись")],
            [KeyboardButton(text="📖 Посмотреть записи")],
            [KeyboardButton(text="🗑 Удалить запись")],
            [KeyboardButton(text="📄 Последние записи")],
            [KeyboardButton(text="📅 Расписание на завтра")],
            [KeyboardButton(text="Изменить расписание")]
        ],
        resize_keyboard=True
    )