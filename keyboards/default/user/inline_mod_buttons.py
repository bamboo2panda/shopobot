from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_to_registration = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пройдите регистрацию"),
        ],
    ],
    resize_keyboard=True
)