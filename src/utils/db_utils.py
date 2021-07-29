from typing import Iterable, Union

from aiogram.types import user

from models import ForbiddenWord, Group, Message, AllowedWord


def get_group(chat_id: int) -> Group:
    return Group.get(Group.chat_id == str(chat_id))


def get_bot_groups() -> Iterable[Group]:
    return Group.select()


def create_group(chat_id: int) -> Group:
    new_group = Group(chat_id=str(chat_id))
    new_group.save()
    return new_group


def create_message(chat_id: int, message_id: int, user_id: int, 
    username: str, first_name: str, last_name: str, text: str) -> Message:
    message = Message(
        group=get_group(chat_id),
        message_id=str(message_id),
        user_id=str(user_id),
        username=username,
        first_name=first_name,
        last_name=last_name,
        text=text
    )
    message.save()


def delete_message(message_id: Union[int, str], chat_id: Union[int, str]):
    message: Message = Message.get(Message.message_id == str(message_id), Message.group == get_group(chat_id))
    message.delete_instance()


def get_group_messages(chat_id: Union[int, str]) -> Iterable[Message]:
    return Message.filter(group=get_group(chat_id))


def get_user_messages(user_data: str) -> Iterable[Message]:
    messages = {}
    messages['messages_by_user_id'] = Message.filter(Message.user_id == user_data)
    messages['messages_by_username'] = Message.filter(Message.username == user_data)
    messages['messages_by_name'] = []
    user_data = user_data.split()
    if len(user_data) > 1:
        messages['messages_by_name'] = Message.filter(Message.first_name == user_data[0], Message.last_name == user_data[1])
    messages = [v for k, v in messages.items() if len(messages[k]) > 0]
    return messages[0] if len(messages) > 0 else []


def get_forbidden_words() -> list[str]:
    return [i.text for i in ForbiddenWord.select()]


def get_forbidden_word(text: str) -> ForbiddenWord:
    return ForbiddenWord.get(ForbiddenWord.text == text.lower().strip())


def get_allowed_words() -> list[str]:
    return [i.text.lower() for i in AllowedWord.select()]