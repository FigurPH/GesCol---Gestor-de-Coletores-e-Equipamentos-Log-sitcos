from peewee import IntegrityError

from models.transpaleteira import Transpaleteira


def adicionar_transpaleteira(id, modelo, disponibilidade):
    if id and modelo and disponibilidade is not None:
        try:
            transpaleteira = Transpaleteira.create(
                id=id, modelo=modelo, disponibilidade=disponibilidade
            )
            # print(f"Coletor {coletor.modelo} (ID: {coletor.id}) adicionado com sucesso.")
            return transpaleteira
        except IntegrityError as e:
            print(f'Erro: Transpaleteira com número {id} já existe. {e}')
            return None
    else:
        print('Erro: ID, modelo e disponibilidade são obrigatórios.')
        return None


def editar_transpaleteira(transpaleteira_id, modelo, disponibilidade):
    ...


def buscar_transpaleteira(transpaleteira_id):
    try:
        transpaleteira = Transpaleteira.get(
            Transpaleteira.id == transpaleteira_id
        )
        return transpaleteira
    except Transpaleteira.DoesNotExist as e:
        print(f'Erro: Transpaleteira com ID {transpaleteira_id} não encontrada. {e}')
        return None


def excluir_transpaleteira(transpaleteira_id):
    try:
        transpaleteira = Transpaleteira.get(Transpaleteira.id == transpaleteira_id)
        transpaleteira.delete_instance()
        print(f'Transpaleteira com ID {transpaleteira_id} excluída com sucesso.')
        return True
    except Transpaleteira.DoesNotExist:
        print(f'Erro: Transpaleteira com ID {transpaleteira_id} não encontrada.')
        return False
