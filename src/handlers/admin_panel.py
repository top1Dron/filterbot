import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import MessageToDeleteNotFound
import peewee

from data.config import ADMINS
from keyboards import words_cb, create_admin_start_menu, get_manage_words_kb, get_back_menu
from loader import dp, bot
from models import ForbiddenWord, Group
from states.manage_words import WordsStates, UserMessagesDeleteStates
from utils import db_utils, misc
from utils.notify_admins import send_message_to_admins


@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    chat_id = message.chat.id
    try:
        group: Group = db_utils.get_group(chat_id=chat_id)
    except:
        db_utils.create_group(chat_id)
    message_text = 'Привет!\nЯ бот - "антиспам", фильтрую всю ненормативную лексику в чате.\n' \
        'Надеюсь на ваше понимание, уважайте друг друга'
    is_private = False
    try:
        chat_administrators = [admin.user.id for admin in await message.chat.get_administrators() if not admin.user.is_bot]
    except:
        is_private = True
    if is_private or message.from_user.id in chat_administrators:
        if message.from_user.id not in ADMINS:
            await message.reply(message_text)
        else:
            await message.reply(message_text, reply_markup=create_admin_start_menu())


@dp.message_handler(lambda message: message.chat.id in db_utils.get_bot_groups(), commands=['stop'])
async def stop_command(message: types.Message):
    try:
        chat_administrators = [admin.user.id for admin in await message.chat.get_administrators() if not admin.user.is_bot]
    except:
        is_private = True
    if is_private or message.from_user.id in chat_administrators:
        db_utils.delete_group(chat_id=message.chat.id)


@dp.message_handler(lambda message: message.from_user.id in ADMINS and 
    message.chat.id in db_utils.get_bot_groups(), commands=['rm'])
async def process_rm_keyboard(message):
    await message.reply('remove keyboard', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.from_user.id in ADMINS and
    message.text == 'Управление словами' and message.chat.id in db_utils.get_bot_groups())
async def get_forbidden_words(message: types.Message):
    forbidden_words = db_utils.get_forbidden_words()
    await message.reply(f'Запрещённые слова: {forbidden_words}', reply_markup=get_manage_words_kb())


@dp.message_handler(lambda message: message.from_user.id in ADMINS and 
    message.text == 'Удаление по ключевым словам' and message.chat.id in db_utils.get_bot_groups())
async def delete_messages_with_forbidden_words_command(message: types.Message):
    await misc.delete_old_messages_with_forbidden_words()


@dp.callback_query_handler(lambda callback_query: callback_query.from_user.id in ADMINS, 
    words_cb.filter(action=['back']), state=[WordsStates.ADD_WORD, WordsStates.REMOVE_WORD])
async def process_go_back(callback_query: types.CallbackQuery, state: FSMContext):
    '''
    callback for "Отмена" inline button
    '''
    forbidden_words = db_utils.get_forbidden_words()
    await state.finish()
    try:
        await bot.delete_message(chat_id=callback_query.message.chat.id, 
            message_id=callback_query.message.message_id)
    except MessageToDeleteNotFound:
        pass
    await bot.send_message(chat_id=callback_query.message.chat.id, 
        text=f'Запрещённые слова: {forbidden_words}', 
        reply_markup=get_manage_words_kb())


@dp.callback_query_handler(lambda callback_query: callback_query.from_user.id in ADMINS and
    callback_query.message.chat.id in db_utils.get_bot_groups(), 
    words_cb.filter(action=['add']), state='*')
async def process_add_forbidden_word(callback_query: types.CallbackQuery):
    '''
    callback for "Добавить слово" inline button
    '''

    await WordsStates.ADD_WORD.set()
    await bot.edit_message_text(message_id=callback_query.message.message_id, 
        chat_id=callback_query.message.chat.id, 
        text=f'Напишите слово, которое хотите добавить в список', 
        reply_markup=get_back_menu())


@dp.message_handler(lambda message: message.from_user.id in ADMINS and 
    message.chat.id in db_utils.get_bot_groups(), state=WordsStates.ADD_WORD)
async def enter_new_word(message: types.Message, state: FSMContext):
    '''
    adding new forbidden word to database
    '''
    
    word = message.text
    try:
        fw = db_utils.get_forbidden_word(word)
        await message.reply(f'Это слово уже в списке запрещённых!\n'
                f'Список не поменялся: {[word.text for word in ForbiddenWord.select()]}',
                reply_markup=get_manage_words_kb())
    except peewee.DoesNotExist:
        if word.lower() in db_utils.get_allowed_words():
            await message.reply('Введённое слово находится в списке разрешённых!\n'
                f'Список не поменялся: {[word.text for word in ForbiddenWord.select()]}',
                reply_markup=get_manage_words_kb())
        else:
            new_word = ForbiddenWord(text=word.lower().strip())
            new_word.save()
            await message.reply('Введённое слово добавлено в список запрещённых успешно!\n'
                f'Новый список: {[word.text for word in ForbiddenWord.select()]}',
                reply_markup=get_manage_words_kb())
            await misc.delete_old_messages_with_forbidden_words()
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.from_user.id in ADMINS and
    callback_query.message.chat.id in db_utils.get_bot_groups(), 
    words_cb.filter(action=['remove']), state='*')
async def process_remove_forbidden_word(callback_query: types.CallbackQuery):
    '''
    callback for "Удалить слово" inline button
    '''

    await WordsStates.REMOVE_WORD.set()
    await bot.edit_message_text(message_id=callback_query.message.message_id, 
        chat_id=callback_query.message.chat.id, 
        text=f'Напишите слово, которое хотите удалить из списка',
        reply_markup=get_back_menu())


@dp.message_handler(lambda message: message.from_user.id in ADMINS 
    and message.chat.id in db_utils.get_bot_groups(), state=WordsStates.REMOVE_WORD)
async def delete_word(message: types.Message, state: FSMContext):
    '''
    remove forbidden word from database
    '''
    
    word = message.text
    try:
        fw: ForbiddenWord = db_utils.get_forbidden_word(word)
        fw.delete_instance()
        await message.reply(f'Это слово удалено из списка запрещённых!\n' \
            f'Новый список: {[word.text for word in ForbiddenWord.select()]}',
            reply_markup=get_manage_words_kb())
    except peewee.DoesNotExist:
        await message.reply('Введённого слова нету в списке запрещённых!\n' \
            f'Текущий список: {[word.text for word in ForbiddenWord.select()]}',
            reply_markup=get_manage_words_kb())
    await state.finish()


@dp.message_handler(lambda message: message.from_user.id in ADMINS and 
    message.text == 'Удаление сообщений пользователя' and 
    message.chat.id in db_utils.get_bot_groups(), state=None)
async def enter_user(message: types.Message):
    await message.answer("Введите любые, на выбор, данные о пользователе, сообщения которого нужно удалить.\n" \
        '(user_id, username или имя + фамилия)')
    await UserMessagesDeleteStates.DELETE_STATE.set()


@dp.message_handler(lambda message: message.chat.id in db_utils.get_bot_groups(), 
    state=UserMessagesDeleteStates.DELETE_STATE)
async def delete_messages_by_user(message: types.Message, state: FSMContext):
    '''
    delete messages by founded user
    '''
    messages = db_utils.get_user_messages(message.text)
    logging.info(messages)
    deleted_messages = 0
    for mes in messages:
        try:
            await bot.delete_message(mes.group.chat_id, mes.message_id)
            mes.delete_instance()
            deleted_messages += 1
        except MessageToDeleteNotFound:
            continue
    if deleted_messages == 0:
        await message.answer("Сообщений пользователя не найдено")
    else:
        await message.answer('Сообщения этого пользователя успешно удалены!')
    await state.finish()