from peewee import IntegrityError

from models.empilhadeira import Empilhadeira


def adicionar_empilhadeira(id, modelo, disponibilidade):
    if id and modelo and disponibilidade is not None:
        try:
            empilhadeira = Empilhadeira.create(
                id=id, modelo=modelo, disponibilidade=disponibilidade
            )
            # print(f"Coletor {coletor.modelo} (ID: {coletor.id}) adicionado com sucesso.")
            return empilhadeira
        except IntegrityError as e:
            print(f'Erro: Empilhadeira com número {id} já existe. {e}')
            return None
    else:
        print('Erro: ID, modelo e disponibilidade são obrigatórios.')
        return None


def listar_empilhadeira():
    empilhadeira = Empilhadeira.select()
    if empilhadeira:
        print('\nLista de Coletores:')
        for coletor in empilhadeira:
            print(
                f'- ID: {coletor.id}, Modelo: {coletor.modelo}, Disponível: {coletor.disponibilidade}'
            )
    else:
        print('Nenhum coletor cadastrado.')


def buscar_empilhadeira(empilhadeira_id):
    try:
        empilhadeira = Empilhadeira.get(
            Empilhadeira.id == empilhadeira_id
        )
        return empilhadeira
    except Empilhadeira.DoesNotExist as e:
        print(f'Erro: Empilhadeira com ID {empilhadeira_id} não encontrada. {e}')
        return None


def excluir_empilhadeira(empilhadeira_id):
    try:
        empilhadeira = Empilhadeira.get(Empilhadeira.id == empilhadeira_id)
        empilhadeira.delete_instance()
        print(f'Empilhadeira com ID {empilhadeira_id} excluída com sucesso.')
        return True
    except Empilhadeira.DoesNotExist:
        print(f'Erro: Empilhadeira com ID {empilhadeira_id} não encontrada.')
        return False

def editar_empilhadeira(empilhadeira_id, modelo, disponibilidade):
    try:
        empilhadeira = Empilhadeira.get(Empilhadeira.id == empilhadeira_id)
        empilhadeira.modelo = modelo
        empilhadeira.disponibilidade = disponibilidade
        empilhadeira.save()
        return True
    except Empilhadeira.DoesNotExist:
        print(
            f'Erro ao editar: Empilhadeira com ID {empilhadeira_id} não encontrada.'
        )
        return False
    except Exception as e:
        print(f'Erro ao editar empilhadeira: {e}')
        return False
