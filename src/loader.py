from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from peewee import PostgresqlDatabase
from playhouse.migrate import PostgresqlMigrator

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = PostgresqlDatabase(config.POSTGRES_DB, user=config.POSTGRES_USER, password=config.POSTGRES_PASSWORD, host="db")
db_migrator = PostgresqlMigrator(db)

