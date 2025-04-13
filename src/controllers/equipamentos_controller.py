from src.models import Equipamento
from peewee import IntegrityError


def adicionar_coletor(modelo):
	try:
		equipamento = Equipamento.create(modelo=modelo)
		print(
			f'Coletor {equipamento.modelo} (ID: {equipamento.id}) adicionado com sucesso.'
		)
		return equipamento
	except IntegrityError:
		print(f'Erro: Coletor com modelo {modelo} já existe.')
		return None


def listar_coletores():
	equipamento = Equipamento.select()
	if equipamento:
		print('\nLista de Coletores:')
		for coletor in equipamento:
			print(
				f'- ID: {coletor.id}, Modelo: {coletor.modelo}, Disponível: {coletor.disponibilidade}'
			)
	else:
		print('Nenhum coletor cadastrado.')


def buscar_coletor(empilhadeira_id):
	try:
		equipamento = Equipamento.get(Equipamento.id == empilhadeira_id)
		print(f'\nInformações do Coletor {empilhadeira_id}:')
		print(f'- Modelo: {equipamento.modelo}')
		print(f'- Disponibilidade: {equipamento.disponibilidade}')
		return equipamento
	except Equipamento.DoesNotExist:
		print(f'Erro: Coletor com ID {empilhadeira_id} não encontrado.')
		return None
