from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default.user.menu import user_menu as menu
from loader import dp, bot


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer(text="Выберите из меню", reply_markup=menu)
    a = ReplyKeyboardRemove


@dp.message_handler(Text(equals=["Ссылка"]))
async def make_referral_link(message: Message):
    bot_id = (await bot.get_me()).username
    referral_id = message.from_user.id
    await message.answer(f"https://t.me/{bot_id}/?start={referral_id}")
