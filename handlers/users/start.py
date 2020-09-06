from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.shop_administration.referrals import CheckReferral
from utils.db_api.commands.user_db_commands import select_users_ids


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    referral = message.get_args()
    await message.answer(f'Привет, {message.from_user.full_name}!')
    if referral:
        await message.answer(f"Тебя пригласил: {referral}")
    else:
        await message.answer("Ты пришел сам")
        await get_referral_id(message)


async def get_referral_id(message: types.Message):
    await message.answer("Введите код приглашения")
    CheckReferral.Get.set()


@dp.message_handler(state=CheckReferral.Get)
async def check_referral(message: types.Message, state=FSMContext):
    referral = message.text
    user_ids = select_users_ids()
    if referral not in user_ids:
        await message.answer("Неверный код, попробуй ещё раз.")
    else:
        await message.answer("Добро пожаловать!")
        await state.finish()


