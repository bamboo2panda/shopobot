from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def order_keyboard(item_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Купить", callback_data=f"order:{item_id}")
            ]
        ]
    )
    return keyboard


def buy_keyboard(item_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оплатить", callback_data=f"buy:{item_id}")
            ]
        ]
    )
    return keyboard


paid_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оплатил",
                callback_data="paid")
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel")
        ],
    ]
)
