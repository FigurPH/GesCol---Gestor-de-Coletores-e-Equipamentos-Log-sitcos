from peewee import *
import os
from models import *

def create_tables():
    with db:
        db.create_tables([
            Colaborador,
            Coletor,
            Empilhadeira,
            Transpaleteira,
            Atribuicao
        ])

if not os.path.exists('data'):
    os.makedirs('data')

db.connect()
create_tables()
db.close()