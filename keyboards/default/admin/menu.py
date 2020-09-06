from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.user import menu

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить товар"),
        ],
    ],
    resize_keyboard=True
)