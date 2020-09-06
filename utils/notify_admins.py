import logging

from aiogram import Dispatcher

from data.config import super_admins


async def on_startup_notify(dp: Dispatcher):
    for admin in super_admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
