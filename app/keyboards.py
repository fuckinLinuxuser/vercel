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
            [KeyboardButton(text="📅 Расписание")]
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
        [
            KeyboardButton(text="✏️ Записи"),
        ],
        [
            KeyboardButton(text="📅 Расписание"),
        ]
    ],
    resize_keyboard=True
)

users_inline_schedule_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Расписание на завтра", callback_data="schedule_tomorrow")
        ]
    ],
    resize_keyboard=True
)

admin_inline_schedule_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Расписание на завтра", callback_data="schedule_tomorrow"),
            InlineKeyboardButton(text="📆 Изменить расписание", callback_data="change_schedule")
        ]
    ],
    resize_keyboard=True
)

admin_inline_posts_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Добавить запись", callback_data="add_post"),
            InlineKeyboardButton(text="📖 Посмотреть записи", callback_data="list_posts")
        ],
        [
            InlineKeyboardButton(text="🗑 Удалить запись", callback_data="delete_post"),
            InlineKeyboardButton(text="📄 Последние записи", callback_data="list_posts")
        ]
    ],
    resize_keyboard=True
)    