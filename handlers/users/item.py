from aiogram import types

from keyboards.inline.purchases import buy_keyboard
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
    caption = """
    Название продукта: {title}
    <i>Описание:</i>
    {description}

    <u>Цена:</u> {price:.2f} <b>RUB</b>
    """
    await message.answer_photo(
        photo=item.photo,
        caption=caption.format(
            title=item.name,
            description=item.description,
            price=item.price,
        ),
        reply_markup=buy_keyboard(item_id=item.id)
    )
    # await message.answer_photo(
    #     photo=item.photo,
    # )
    # await message.answer(
    #     text=f"<b>{item.name}</b>\n"
    #          f"{item.description}\n"
    #          f"Цена: {item.price}",
    #     reply_markup=InlineKeyboardMarkup(
    #         inline_keyboard=[
    #             [
    #                 InlineKeyboardButton(
    #                     text="Купить через Киви",
    #                     url="https://ya.ru"
    #                 )
    #             ]
    #         ]
    #     )
    # )
    return

