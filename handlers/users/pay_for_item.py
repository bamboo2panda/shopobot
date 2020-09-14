from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hcode, hlink

from data import config
from keyboards.inline.purchases import  paid_keyboard
from loader import dp
from utils.db_api.commands.item_db_commands import select_item
from utils.db_api.schemas.item import Item
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


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
        await call.message.answer("Успешно оплачено")
    await call.message.edit_reply_markup()
    await state.finish()


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
        await call.message.answer("Успешно оплачено")
    await call.message.edit_reply_markup()
    await state.finish()
