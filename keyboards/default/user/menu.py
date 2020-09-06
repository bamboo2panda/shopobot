from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пригласить друга и получить $10"),
        ],
    ],
    resize_keyboard=True
)