import asyncio
from aiogram.types import Message, chat

from config import admin_id
from main import bot, dp


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler()
async def echo(message: Message):
    text = f'Привет, ты написал: {message.text}'
    # await bot.send_message(chat_id=message.from_user.id, text=text)
    await message.answer(text=text)