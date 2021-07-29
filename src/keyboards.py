from aiogram import types
from aiogram.utils.callback_data import CallbackData

words_cb: CallbackData = CallbackData('word', 'id', 'action')


def create_admin_start_menu() -> types.ReplyKeyboardMarkup:
    menu = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Управление словами"),
            ],
            [
                types.KeyboardButton(text="Удаление по ключевым словам"),
            ],
            [
                types.KeyboardButton(text="Удаление сообщений пользователя"),
            ],
        ],
        resize_keyboard=True
    )
    return menu


def get_manage_words_kb() -> types.InlineKeyboardMarkup:
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)
    add_word_btn = types.InlineKeyboardButton(text="Добавить слово", callback_data=words_cb.new(id=hash('add'), action='add'))
    remove_word_btn = types.InlineKeyboardButton(text='Удалить слово', callback_data=words_cb.new(id=hash('remove'), action='remove'))
    inline_kb_full.add(add_word_btn, remove_word_btn)
    return inline_kb_full


def get_back_menu() -> types.InlineKeyboardMarkup:
    menu = types.InlineKeyboardMarkup(row_width=1)
    back_btn = types.InlineKeyboardButton(text="Отмена", callback_data=words_cb.new(id=hash('back'), action='back'))
    menu.add(back_btn)
    return menu