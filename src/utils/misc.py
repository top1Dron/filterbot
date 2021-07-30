import functools
import logging
from os import lockf
import re
from typing import Union

from aiogram.utils.exceptions import MessageToDeleteNotFound

from . import db_utils
from loader import bot
from models import Group


async def delete_old_messages_with_forbidden_words():
    forbidden_words = db_utils.get_forbidden_words()
    groups = db_utils.get_groups()
    for group in groups:
        any_changes = False
        group_messages = db_utils.get_group_messages(group.chat_id)
        for message in group_messages:
            for word in forbidden_words:
                if word in message.text.lower().split():
                    try:
                        await bot.delete_message(
                            chat_id=int(message.group.chat_id),
                            message_id=int(message.message_id)
                        )
                    except MessageToDeleteNotFound:
                        logging.info('Message was deleted before!')
                    except Exception as e:
                        logging.error(e)
                    db_utils.delete_message(message_id=message.message_id, chat_id=message.group.chat_id)
                    any_changes = True

        if any_changes:
            await bot.send_message(chat_id=int(group.chat_id),
                text=f'Произведена очистка чата от ненормативной лексики!')
        else:
            await bot.send_message(chat_id=int(group.chat_id),
                text=f'На текущий момент чат чист от ненормативной лексики!')


async def anti_flood(*args, **kwargs):
    m = args[0]
    username = m['from']['username']
    if m.chat.title is not None:
        await bot.send_message(m.chat.id, f"Пользователь {username} флудит в чате {m.chat.title}")
    else:
        await bot.send_message(m.chat.id, f"Пользователь {username} флудит в приватном чате")
    try:
        await bot.delete_message(m.chat.id, m.message_id)
    except MessageToDeleteNotFound:
        pass


def is_message_in_active_chat():
    def decorator(message_handler):
        @functools.wraps(message_handler)
        async def wrapper(*args):
            logging.info(args)
            try:
                db_utils.get_group(chat_id=args[0].chat.id)
                return await message_handler(*args)
            except:
                pass
        return wrapper
    return decorator


def is_callback_query_in_active_chat():
    def decorator(message_handler):
        @functools.wraps(message_handler)
        async def wrapper(*args):
            try:
                db_utils.get_group(chat_id=args[0].message.chat.id)
                return await message_handler(*args)
            except:
                pass
        return wrapper
    return decorator    