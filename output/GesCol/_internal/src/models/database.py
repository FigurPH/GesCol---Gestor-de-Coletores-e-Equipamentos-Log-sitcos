# src/models/database.py
'''from peewee import *

DATABASE_NAME = 'src/data/gescol.db'
db = SqliteDatabase(DATABASE_NAME)


class BaseModel(Model):
    class Meta:
        database = db'''
import os
import sys

from peewee import *


def get_database_path():
    """Retorna o caminho correto do banco de dados dependendo do ambiente."""
    if hasattr(sys, '_MEIPASS'):
        # Executável gerado pelo PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # Ambiente de desenvolvimento (VSCode, Python direto)
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Caminho do banco de dados
    return os.path.join(base_path, '..', 'data', 'gescol.db')


# Configuração do banco de dados
DATABASE_NAME = get_database_path()
print(f"Banco de dados em: {DATABASE_NAME}")  # Para depuração
db = SqliteDatabase(DATABASE_NAME)


class BaseModel(Model):
    class Meta:
        database = db
