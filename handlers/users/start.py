from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.shop_administration.referrals import CheckReferral
from utils.db_api.commands import user_db_commands as commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = int(message.from_user.id)
    referral = message.get_args()
    await message.answer(f'Привет, {message.from_user.full_name}!')
    user_ids = await commands.select_users_ids()
    if user_id in user_ids:
        await hello_answer(message)
        return True
    if referral:
        await check_referral(message=message, referral=referral)
    else:
        await get_referral_id(message)


async def get_referral_id(message: types.Message):
    await message.answer("Введите код приглашения")
    await CheckReferral.Get.set()


@dp.message_handler(state=CheckReferral.Get)
async def check_referral_message(message: types.Message, state=FSMContext):
    check = await check_referral(message)
    if check:
        await state.finish()
    else:
        await get_referral_id(message)


async def check_referral(message: types.Message, **kwargs):
    referral = int(kwargs.get('referral') if kwargs.get('referral') else int(message.text))
    user_ids = await commands.select_users_ids()
    if referral in user_ids:
        id = int(message.from_user.id)
        name = message.from_user.full_name
        await commands.add_user(id=id, name=name, referral=referral)
        await hello_answer(message)
        return True
    else:
        await message.answer("Неверный код, попробуйте ещё раз.")
        return False


async def hello_answer(message):
    await message.answer("Добро пожаловать!")
    await message.answer("Введите /help чтобы узнать все комадны\n"
                         "Ввудите /menu чтобы посмотреть все товары\n"
                         "Приятных покупок!")