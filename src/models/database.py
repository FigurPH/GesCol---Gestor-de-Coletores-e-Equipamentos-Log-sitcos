# src/models/database.py
from peewee import *

from resources.settings import Settings

DATABASE_NAME = Settings().DATABASE_URL
db = SqliteDatabase(DATABASE_NAME)


class BaseModel(Model):
    class Meta:
        database = db
