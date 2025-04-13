from peewee import *
from .database import BaseModel
from .colaborador import Colaborador
from .coletor import Coletor
from .empilhadeira import Empilhadeira
from .transpaleteira import Transpaleteira
from datetime import datetime


class Atribuicao(BaseModel):
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
		return f'Atribuição para {self.colaborador.nome} em \
            {self.data_inicio.strftime("%Y-%m-%d %H:%M:%S")}. Equipamentos: \
            {", ".join(equipamentos)}'
