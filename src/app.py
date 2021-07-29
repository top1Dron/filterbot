from aiogram import executor

from loader import dp, db
# import middlewares, filters, handlers
from handlers import admin_panel
from models import Group, ForbiddenWord, Message, AllowedWord
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    db.connect()
    Group.create_table()
    ForbiddenWord.create_table()
    Message.create_table()
    AllowedWord.create_table()
    
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

