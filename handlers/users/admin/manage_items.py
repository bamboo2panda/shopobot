from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.misc.check_user_status import is_product_admin
from utils.db_api.commands.item_db_commands import add_item
from states.shop_administration.add_item import AddItem


@dp.message_handler(Command("add_item"), state=None)
async def add_item_start(message: types.Message, state: FSMContext):
    is_admin: bool = await is_product_admin(message.from_user.id)
    print(is_admin)
    if is_admin:
        await message.answer("Добавляю новый товар.\n"
                             "Сначала отправьте мне его фото.")

    else:
        await message.answer("Только админы могут добавлять товары.")

    await AddItem.Photo.set()


# @dp.message_handler(state=AddItem.Photo)
@dp.message_handler(content_types=types.ContentType.PHOTO, state=AddItem.Photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    photo_uri = message.photo[-1].file_unique_id
    print(photo_uri)
    path = await message.photo[-1].download('data/images/')
    path = path.name
    await state.update_data(
        {
            "photo_uri": path
        }
    )
    await message.answer("Введите название товара:")
    await AddItem.next()


@dp.message_handler(state=AddItem.Name)
async def add_item_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {
            "name": name
        }
    )
    await message.answer("Добавьте описание:")
    await AddItem.next()


@dp.message_handler(state=AddItem.Description)
async def add_item_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {
            "description": description
        }
    )
    await message.answer("Введите цену товара:")
    await AddItem.next()


@dp.message_handler(state=AddItem.Price)
async def add_item_price(message: types.Message, state: FSMContext):
    price = message.text
    data = await state.get_data()
    print(data["photo_uri"])
    await add_item(name=str(data["name"]),
                   description=str(data["description"]),
                   photo=str(data["photo_uri"]),
                   price=int(price))
    await message.answer("Товар добавлен")
    await state.finish()

