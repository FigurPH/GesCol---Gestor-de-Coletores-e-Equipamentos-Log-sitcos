from src.models import Empilhadeira
from peewee import IntegrityError


def adicionar_coletor(modelo):
	try:
		empilhadeira = Empilhadeira.create(modelo=modelo)
		print(
			f'Coletor {empilhadeira.modelo} (ID: {empilhadeira.id}) adicionado com sucesso.'
		)
		return empilhadeira
	except IntegrityError:
		print(f'Erro: Coletor com modelo {modelo} já existe.')
		return None


def listar_coletores():
	empilhadeira = Empilhadeira.select()
	if empilhadeira:
		print('\nLista de Coletores:')
		for coletor in empilhadeira:
			print(
				f'- ID: {coletor.id}, Modelo: {coletor.modelo}, Disponível: {coletor.disponibilidade}'
			)
	else:
		print('Nenhum coletor cadastrado.')


def buscar_coletor(empilhadeira_id):
	try:
		empilhadeira = Empilhadeira.get(Empilhadeira.id == empilhadeira_id)
		print(f'\nInformações do Coletor {empilhadeira_id}:')
		print(f'- Modelo: {empilhadeira.modelo}')
		print(f'- Disponibilidade: {empilhadeira.disponibilidade}')
		return empilhadeira
	except Empilhadeira.DoesNotExist:
		print(f'Erro: Coletor com ID {empilhadeira_id} não encontrado.')
		return None
