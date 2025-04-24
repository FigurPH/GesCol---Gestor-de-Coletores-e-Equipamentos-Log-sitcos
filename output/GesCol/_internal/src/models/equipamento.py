from peewee import *

from .database import BaseModel


class Equipamento(BaseModel):
    id = AutoField()
    modelo = CharField(unique=True)
    tipo = CharField(
        not_null=True,
    )  # Emp. > Empilhadeira | Tra. > Transpaleteira
    disponibilidade = BooleanField(default=True)

    def __str__(self):
        return f'Equipamento {self.id} ({self.modelo})'
