from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import super_admins
from loader import dp
from states.shop_administration.referrals import CheckReferral
from utils.db_api.commands import user_db_commands as commands
from utils.misc.check_user import check_referral, is_registered_user


# Перехватываем все команды /start
@dp.message_handler(
    lambda message: True if is_registered_user(int(message.from_user.id)) else False,
    CommandStart()
    )
# @dp.message_handler(func= lambda message: is_registered_user(int(message.from_user.id)),
#    CommandStart()
#     )
async def bot_start_registered_user(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    await hello_answer(message)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    referral = message.get_args()
    await message.answer(f'Привет, {message.from_user.full_name}!')
    await message.answer(f'Нужно зарегистрироваться.')
    await manage_new_visitor(message, referral)


async def manage_new_visitor(message, referral):
    if referral:
        referral_is_valid = await check_referral(message=message, referral=referral)
        if referral_is_valid:
            await add_new_user(message, referral)
        else:
            await get_referral_id(message, referral)
    else:
        await get_referral_id(message, referral)


async def get_referral_id(message: types.Message, state: FSMContext = None, referral: int = None, ):
    await message.answer("Введите код приглашения")
    if state is None:
        await CheckReferral.Get.set()
    await state.update_data(
        dict(referral=referral)
    )


@dp.message_handler(state=CheckReferral.Get)
async def check_referral_message(message: types.Message, state: FSMContext):
    check = await check_referral(message)
    if check:
        await add_new_user(message, state.get_data("referral"))
        await state.finish()
    else:
        await message.answer("Неверный код, попробуйте ещё раз.")
        await get_referral_id(message)


async def add_new_user(message, referral):
    id = int(message.from_user.id)
    name = message.from_user.full_name
    await commands.add_user(id=id, name=name, referral=referral)
    await hello_answer(message)


async def hello_answer(message):
    await message.answer("Добро пожаловать!")
    await message.answer("Введите /help чтобы узнать все комадны\n"
                         "Ввудите /menu чтобы посмотреть все товары\n"
                         "Приятных покупок!")
