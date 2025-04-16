from peewee import *

from .database import BaseModel


class Colaborador(BaseModel):
    matricula = CharField(primary_key=True)
    nome = CharField(null=False)
    cargo = CharField(null=False)
    autorizado_transpaleteira = BooleanField(default=False)
    autorizado_empilhadeira = BooleanField(default=False)

    def __str__(self):
        return f'{self.nome} ({self.matricula})'
