# src/models/database.py
from peewee import *

DATABASE_NAME = 'data/db/gescol.db'
db = SqliteDatabase(DATABASE_NAME)

class BaseModel(Model):
    class Meta:
        database = db
