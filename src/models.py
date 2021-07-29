from enum import unique
import peewee

from loader import db


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Group(BaseModel):
    chat_id = peewee.CharField(unique=True)


class ForbiddenWord(BaseModel):
    text = peewee.CharField(unique=True)


class AllowedWord(BaseModel):
    text = peewee.CharField(unique=True)


class Message(BaseModel):
    message_id = peewee.CharField(unique=True)
    group = peewee.ForeignKeyField(Group, on_delete='cascade')
    text = peewee.TextField()
    user_id = peewee.CharField()
    username = peewee.CharField(null=True)
    first_name = peewee.CharField(null=True)
    last_name = peewee.CharField(null=True)