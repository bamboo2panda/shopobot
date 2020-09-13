from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp, bot
from utils.db_api.commands import item_db_commands as item_commands
from utils.db_api.commands.item_db_commands import search_item_by_name
from utils.misc.check_user import is_registered_user


@dp.inline_handler(lambda query: True if is_registered_user(int(query.from_user.id)) else False)
@dp.inline_handler(text="")
async def handle_empty_query(query: types.InlineQuery):
    user_id = query.from_user.id
    user_is_registered = await is_registered_user(user_id)
    print(user_is_registered)
    if user_is_registered:
        await show_all_items(query)
    else:
        await send_to_registration(query)


@dp.inline_handler()
async def handle_item_search_query(query: types.InlineQuery):
    query_text = query.query
    items = await search_item_by_name(query_text)
    await show_inline_list_of_items(items, query)


async def send_to_registration(query):
    await query.answer(
        results=[],
        switch_pm_text="Бот недоступен. Подключить бота",
        switch_pm_parameter="connect_user",
        cache_time=0)
    return


async def show_all_items(query):
    items = await item_commands.select_all_items()
    await show_inline_list_of_items(items, query)


async def show_inline_list_of_items(items, query):
    bot_url = "https://t.me/udemy_shopobot/"
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=item.id,
                title=item.name,
                description=item.description,
                thumb_url=item.photo,
                url=bot_url + "?item=" + str(item.id),
                input_message_content=types.InputTextMessageContent(
                    message_text=f"<a href=\"{item.photo}\">&#8205;</a>\n"
                                 f"<b>{item.name}</b>\n"
                                 f"{item.description}\n"
                                 f"<a href=\"{bot_url}?start&item={item.id}\">Купить</a>\n\n",
                    parse_mode="HTML"
                )
            )
            for item in items
        ],
        cache_time=0,
    )

@dp.message_handler(CommandStart(deep_link="connect_user"))
async def connect_user(message: types.Message):
    allowed_users.append(message.from_user.id)
    await message.answer("Вы подключены")
