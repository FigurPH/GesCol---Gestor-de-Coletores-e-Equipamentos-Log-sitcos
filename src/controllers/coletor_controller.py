from models.coletor import Coletor
from peewee import IntegrityError


def adicionar_coletor(id, modelo, disponibilidade):
	try:
		coletor = Coletor.create(
			id=id, modelo=modelo, disponibilidade=disponibilidade
		)
		# print(f"Coletor {coletor.modelo} (ID: {coletor.id}) adicionado com sucesso.")
		return coletor
	except IntegrityError:
		print(f'Erro: Coletor com modelo {modelo} já existe.')
		return None


def listar_coletores():
	coletores = Coletor.select()
	lista_exibicao = []
	for coletor in coletores:
		lista_exibicao.append(
			{
				'id': coletor.id,
				'modelo': coletor.modelo,
				'disponibilidade': coletor.disponibilidade,
			}
		)
	return lista_exibicao


def buscar_coletor(coletor_id):
	try:
		coletor = Coletor.get(Coletor.id == coletor_id)
		print(f'Encontrado o coletor {coletor_id}')
		"""print(f"\nInformações do Coletor {coletor_id}:")
        print(f"- Modelo: {coletor.modelo}")
        print(f"- Disponibilidade: {coletor.disponibilidade}")"""
		return coletor
	except Coletor.DoesNotExist:
		print(f'Erro: Coletor com ID {type(coletor_id)} não encontrado.')
		return None


def editar_coletor(coletor_id, modelo, disponibilidade):
	try:
		coletor = Coletor.get(Coletor.id == coletor_id)
		print(f'Coletor {coletor_id} encontrado.')
		coletor.id = coletor_id
		coletor.modelo = modelo
		coletor.disponibilidade = disponibilidade
		try:
			coletor.save()
			return True
		except Exception as e:
			print(f'ERRO NA HORA DE SALVAR A EDIÇÂO > {e}')

	except Coletor.DoesNotExist:
		print(f'Coletor {coletor_id} não encontrado.')
		return False
	except Exception as e:
		print(f'Ocorreu uma exceção. {e}')
		return False


def excluir_coletor(coletor_id):
	try:
		coletor = Coletor.get(Coletor.id == coletor_id)
		coletor.delete_instance()
		return True
	except Exception:
		print('Algo errado na exclusão do coletor')
		return False
