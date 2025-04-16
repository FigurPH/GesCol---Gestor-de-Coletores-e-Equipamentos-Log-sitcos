from peewee import *

from .database import BaseModel


class Coletor(BaseModel):
    id = IntegerField(primary_key=True)
    modelo = CharField(null=False)
    disponibilidade = BooleanField(default=True)

    def __str__(self):
        return f'Coletor {self.id} ({self.modelo})'
