from datetime import datetime

from peewee import *

from .colaborador import Colaborador
from .coletor import Coletor
from .database import BaseModel
from .empilhadeira import Empilhadeira
from .transpaleteira import Transpaleteira


class Atribuicao(BaseModel):
    """
    Classe que representa a atribuição de equipamentos a um colaborador.
    Esta classe mantém o registro de quais equipamentos (coletor, empilhadeira e/ou transpaleteira)
    estão atribuídos a qual colaborador, incluindo o período de início e fim da atribuição.
    Atributos:
        id (AutoField): Identificador único da atribuição
        colaborador (ForeignKeyField): Referência ao colaborador que recebeu a atribuição
        coletor (ForeignKeyField): Referência ao coletor atribuído
        empilhadeira (ForeignKeyField): Referência à empilhadeira atribuída (opcional)
        transpaleteira (ForeignKeyField): Referência à transpaleteira atribuída (opcional)
        data_inicio (DateTimeField): Data e hora do início da atribuição
        data_fim (DateTimeField): Data e hora do fim da atribuição (opcional)
    Métodos:
        __str__(): Retorna uma representação em string da atribuição, incluindo o nome do colaborador,
                  data de início e equipamentos atribuídos
    """

    id = AutoField()
    colaborador = ForeignKeyField(Colaborador, backref='atribuicoes')
    coletor = ForeignKeyField(Coletor, backref='atribuicoes')
    empilhadeira = ForeignKeyField(
        Empilhadeira, backref='atribuicoes', null=True
    )
    transpaleteira = ForeignKeyField(
        Transpaleteira, backref='atribuicoes', null=True
    )
    data_inicio = DateTimeField(default=datetime.now)
    data_fim = DateTimeField(null=True)

    def __str__(self):
        equipamentos = []
        if self.coletor:
            equipamentos.append(f'Coletor: {self.coletor}')
        if self.empilhadeira:
            equipamentos.append(f'Empilhadeira: {self.empilhadeira}')
        if self.transpaleteira:
            equipamentos.append(f'Transpaleteira: {self.transpaleteira}')
        return f'Model: Atribuição para {self.colaborador.nome} em \
            {self.data_inicio.strftime("%Y-%m-%d %H:%M:%S")}. Equipamentos: \
            {", ".join(equipamentos)}'
