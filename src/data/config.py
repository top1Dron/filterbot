from configparser import ConfigParser
import logging


#instantiate
config = ConfigParser()

#parse config.ini file
config.read('config.ini')

#read values from config.ini
ADMINS = config.get('bot_section', 'ADMINS').split(',')
ADMINS = [int(id) for id in ADMINS]
logging.info(ADMINS)
BOT_TOKEN = config.get('bot_section', 'BOT_TOKEN')
ip = config.get('bot_section', 'ip')
POSTGRES_USER = config.get('db_section', 'POSTGRES_USER')
POSTGRES_PASSWORD = config.get('db_section', 'POSTGRES_PASSWORD')
POSTGRES_DB = config.get('db_section', 'POSTGRES_DB')
