from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ссылка"),
        ],
    ],
    resize_keyboard=True
)