from app.config import WEB_APP_URL
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

users_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📄 Последние записи", callback_data="show_posts")],
            [InlineKeyboardButton(text="📣 Предупредить об опоздании", callback_data="delay")],
            [InlineKeyboardButton(text="📅 Расписание", callback_data="schedule")]
        ],
        resize_keyboard=True
    )

webapp_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть мини-апп 🚀", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Записи", callback_data="posts"),
        ],
        [
            InlineKeyboardButton(text="📅 Расписание", callback_data="schedule"),
        ]
    ],
    resize_keyboard=True
)

users_inline_schedule_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Расписание на завтра", callback_data="schedule_tomorrow"),
            InlineKeyboardButton(text="📅 Расписание на неделю", callback_data="schedule_week")
        ]
    ],
    resize_keyboard=True
)

admin_inline_schedule_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Расписание на завтра", callback_data="schedule_tomorrow"),
            InlineKeyboardButton(text="📅 Расписание на неделю", callback_data="schedule_week"),
            InlineKeyboardButton(text="Добавить", callback_data="change_schedule"),
            InlineKeyboardButton(text="Удалить", callback_data="delete_schedule")
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
            InlineKeyboardButton(text="🗑 Удалить запись", callback_data="delete_post")
        ]
    ],
    resize_keyboard=True
)    

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back")
        ]
    ]
)