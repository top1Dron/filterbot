from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp
from utils import db_utils, misc


@dp.message_handler(lambda message: message.chat.id in db_utils.get_bot_groups(), state=None)
@dp.throttled(misc.anti_flood, rate=1/1.5)
async def filter_messages(message: types.Message):
    db_utils.create_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        text=message.text
    )
    forbidden_words = db_utils.get_forbidden_words()
    for word in forbidden_words:
        if word.lower() in message.text.lower().split():
            await message.delete()
            db_utils.delete_message(message_id=message.message_id, chat_id=message.chat.id)
            await message.answer('Сообщение было удалено из-за наличия ненормативной лексики!')
            break


@dp.message_handler(lambda message: message.chat.id in db_utils.get_bot_groups(), CommandHelp())
async def help_command(message: types.Message):
    help_message = 'Я бот-антиспам, фильтрую спам и ненормативную лексику.' \
        'Надеюсь на ваше понимание, уважайте друг друга.'
    if message.from_user.id in ADMINS:
        help_message += '\nУ меня есть следующие команды:\n' \
            '/rm - удалить все текстовые кнопки\n' \
            '/forbidden_words - просмотр/добавление/удаление ключевых слов,\n' \
            'по которым фильтруются сообщения\n' \
            '/cancel - отменяет действие при вводе на удаление/добавление слова в базу данных'
    await message.reply(help_message)
    await misc.delete_old_messages_with_forbidden_words()