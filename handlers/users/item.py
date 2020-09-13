from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import super_admins
from loader import dp
from utils.db_api.commands.item_db_commands import select_item


async def show_item_from_message(message: types.Message):
    param = message.get_args()
    if "item_" in param:
        print("YESS!!")
        id = int(param.split("item_", 1)[1])
        await show_item(message, id)
        return True
    else:
        print(f"NOOOO!  {param}")


async def show_item(message: types.Message, id: int):
    item = await select_item(id)
    await message.answer_photo(
        photo=item.photo,
    )
    await message.answer(
        text=f"<b>{item.name}</b>\n"
             f"{item.description}\n"
             f"Цена: {item.price}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Купить через Киви",
                        url="https://ya.ru"
                    )
                ]
            ]
        )
    )
    return
