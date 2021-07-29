from aiogram.dispatcher.filters.state import StatesGroup, State


class WordsStates(StatesGroup):
    ADD_WORD = State()
    REMOVE_WORD = State()


class UserMessagesDeleteStates(StatesGroup):
    DELETE_STATE = State()
