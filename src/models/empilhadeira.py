from peewee import *
from .database import BaseModel

class Empilhadeira(BaseModel):
    id = AutoField()
    modelo = CharField(unique=True)
    disponibilidade = BooleanField(default=True)

    def __str__(self):
        return f"Empilhadeira {self.id} ({self.modelo})"