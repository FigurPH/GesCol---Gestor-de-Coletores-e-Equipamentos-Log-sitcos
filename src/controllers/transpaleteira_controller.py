from peewee import IntegrityError

from src.models import Transpaleteira


def adicionar_coletor(modelo):
    try:
        transpaleteira = Transpaleteira.create(modelo=modelo)
        print(
            f'Coletor {transpaleteira.modelo} (ID: {transpaleteira.id}) adicionado com sucesso.'
        )
        return transpaleteira
    except IntegrityError:
        print(f'Erro: Coletor com modelo {modelo} já existe.')
        return None


def listar_coletores():
    transpaleteira = Transpaleteira.select()
    if transpaleteira:
        print('\nLista de Coletores:')
        for coletor in transpaleteira:
            print(
                f'- ID: {coletor.id}, Modelo: {coletor.modelo}, Disponível: {coletor.disponibilidade}'
            )
    else:
        print('Nenhum coletor cadastrado.')


def buscar_coletor(transpaleteira_id):
    try:
        transpaleteira = Transpaleteira.get(
            Transpaleteira.id == transpaleteira_id
        )
        print(f'\nInformações do Coletor {transpaleteira_id}:')
        print(f'- Modelo: {transpaleteira.modelo}')
        print(f'- Disponibilidade: {transpaleteira.disponibilidade}')
        return transpaleteira
    except Transpaleteira.DoesNotExist:
        print(f'Erro: Coletor com ID {transpaleteira_id} não encontrado.')
        return None
