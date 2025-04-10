from peewee import *
from .database import BaseModel

class Coletor(BaseModel):
    id = AutoField()
    modelo = CharField(unique=True)
    disponibilidade = BooleanField(default=True)

    def __str__(self):
        return f"Coletor {self.id} ({self.modelo})"