from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import super_admins
from handlers.users.item import show_item_from_message
from loader import dp
from states.shop_administration.referrals import CheckReferral
from utils.db_api.commands import user_db_commands as commands
from utils.misc.check_user import check_referral, is_registered_user


# Перехватываем все команды /start


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = int(message.from_user.id)
    param = message.get_args()

    if await is_registered_user(user_id):
        await show_item_from_message(message)
    elif await has_referral(param):
        referral = int(param.split("referral_", 1)[1])
        await manage_new_visitor(message, referral)
    else:
        await get_referral_id(message)


async def manage_new_visitor(message, referral):
    if await check_referral(referral):
        await add_new_user(message, referral)
    else:
        await get_referral_id(message, referral)


async def get_referral_id(message: types.Message, state: FSMContext = None, referral: int = None, ):
    await message.answer("Вы ещё не зарегистрировались.\n"
                         "Введите код приглашения")
    if state is None:
        await CheckReferral.Get.set()
    else:
        await state.update_data(
            {
                "referral": referral
            }
        )


@dp.message_handler(state=CheckReferral.Get)
async def check_referral_message(message: types.Message, state: FSMContext):
    referral = int(message.text)
    if await check_referral(referral):
        await add_new_user(message, referral)
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
    await message.answer(text="Введите /help чтобы узнать все комадны\n"
                         "Ввудите /menu чтобы посмотреть все товары\n"
                         "Приятных покупок!",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(
                                         text="Перейти в инлайн режим для покупки",
                                         switch_inline_query_current_chat=""
                                     )
                                 ]
                             ]
                         )),


async def has_referral(param):
    if "referral_" in param:
        return True
    return False
