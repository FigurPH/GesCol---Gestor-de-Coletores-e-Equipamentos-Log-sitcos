from peewee import *
from .database import BaseModel

class Equipamento(BaseModel):
    id = AutoField()
    modelo = CharField(unique=True)
    tipo = CharField(unique=True) # Emp. > Empilhadeira | Tra. > Transpaleteira
    disponibilidade = BooleanField(default=True)

    def __str__(self):
        return f"Equipamento {self.id} ({self.modelo})"