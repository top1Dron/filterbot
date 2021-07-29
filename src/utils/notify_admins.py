import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
        except Exception as err:
            logging.exception(err)


async def send_message_to_admins(message: str, dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, message)
        except Exception as err:
            logging.exception(err)
