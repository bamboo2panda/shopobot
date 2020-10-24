from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hcode, hlink

from data import config
from keyboards.inline.purchases import paid_keyboard
from loader import dp
from states.shop_administration.Order import OrderItems
from states.shop_administration.referrals import CheckReferral
from utils.db_api.commands.item_db_commands import select_item, get_item_price
from utils.db_api.commands.purcahse_db_commands import add_purchase
from utils.db_api.commands.user_db_commands import get_user_points
from utils.db_api.schemas.item import Item
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(text_contains="order")
async def order_items(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    item_id = call.data.split(":")[-1]
    item_id = int(item_id)
    item: Item = await select_item(item_id)
    # await state.set_state("number_of_items"
    await call.answer("Введите количество")
    await OrderItems.Count.set()
    await state.update_data(item_id=item.id)


@dp.message_handler(state=OrderItems.Count)
async def set_number_of_items(message: types.Message, state: FSMContext):
    if int(message.text):
        number_of_items = int(message.text)
        await state.update_data(count=number_of_items)
        await OrderItems.next()
        await message.answer("Введите адрес доставки")
    else:
        await message.answer("Нужно ввести целое число. Попроуйте ещё раз.")


@dp.message_handler(state=OrderItems.Address)
async def set_delivery_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await use_points(message, state)


async def use_points(message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    available_points = int(await get_user_points(user_id))
    item_price = int(await get_item_price(data["item_id"]))
    count_of_items = data["count"]
    cart_price = item_price * count_of_items
    await state.update_data(cart_price=cart_price)
    if available_points == 0:
        await state.update_data(points_used=0)
        await state.update_data(ammount=cart_price)
        await send_invoice(message, state)
    elif cart_price <= available_points:
        await state.update_data(points_used=cart_price)
        await state.update_data(ammount=0)
    else:
        await state.update_data(points_used=available_points)
        await state.update_data(ammount=cart_price - available_points)
        await send_invoice(message, state)




#
# async def apply_points(message: types.Message, state: FSMContext):
#     await state.update_data(apply_points=True)
#     data = await state.get_data()
#     amount = data['cart_price'] - data['available_points']
#     await send_invoice(message, ammount, state)


async def send_invoice(message, state: FSMContext):
    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        "\n".join([
            f"Оплатите не менее {amount:.2f} по номеру телефона или по адресу",
            "",
            hlink(config.WALLET_QIWI, url=payment.invoice),
            "И обязательно укажите ID платежа:",
            hcode(payment.id)
        ]),
        reply_markup=paid_keyboard)

    await state.set_state("qiwi")
    await state.update_data(payment=payment)


@dp.callback_query_handler(text_contains="buy")
async def create_invoice(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    item_id = call.data.split(":")[-1]
    item_id = int(item_id)
    item: Item = await select_item(item_id)

    amount = item.price
    payment = Payment(amount=amount)
    payment.create()

    await call.message.answer(
        "\n".join([
            f"Оплатите не менее {amount:.2f} по номеру телефона или по адресу",
            "",
            hlink(config.WALLET_QIWI, url=payment.invoice),
            "И обязательно укажите ID платежа:",
            hcode(payment.id)
        ]),
        reply_markup=paid_keyboard)

    await state.set_state("qiwi")
    await state.update_data(payment=payment)


@dp.callback_query_handler(text="cancel", state="qiwi")
async def cancel_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отменено")
    await state.finish()


@dp.callback_query_handler(text="paid", state="qiwi")
async def approve_payment(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get("payment")
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена.")
        return
    except NotEnoughMoney:
        await call.message.answer("Оплаченная сума меньше необходимой.")
        return

    else:
        await success_payment(call.message, state)
    await call.message.edit_reply_markup()
    await state.finish()


async def success_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await cut_pionts(user_id, ammount)
    await add_purchase(user_id=message.from_user.id,
                       item_id=data['item_id'],
                       transaction_id=data['payment'].id,
                       count=data['count'],
                       address=data['address'],
                       points_used=data['points_used'],
                       amount=data['amount'])
    await message.answer("Успешно оплачено")
