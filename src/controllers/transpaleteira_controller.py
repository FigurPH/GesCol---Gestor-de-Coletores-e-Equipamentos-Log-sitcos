from peewee import IntegrityError

from models.transpaleteira import Transpaleteira


def adicionar_transpaleteira(id, modelo, disponibilidade):
    """
    Adiciona uma nova transpaleteira ao sistema.
    Args:
        id (int): Número de identificação da transpaleteira
        modelo (str): Modelo/nome da transpaleteira
        disponibilidade (bool): Status de disponibilidade da transpaleteira
    Returns:
        Transpaleteira: Objeto Transpaleteira criado com sucesso
        None: Em caso de erro na criação ou dados inválidos
    Raises:
        IntegrityError: Quando já existe uma transpaleteira com o mesmo ID
    """

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


def buscar_transpaleteira(transpaleteira_id):
    """
    Busca uma transpaleteira específica pelo ID no banco de dados.
    Args:
        transpaleteira_id: ID da transpaleteira a ser buscada.
    Returns:
        Transpaleteira: Objeto Transpaleteira se encontrado
        None: Se a transpaleteira não for encontrada
    Raises:
        Transpaleteira.DoesNotExist: Quando a transpaleteira não é encontrada no banco de dados
    """

    try:
        transpaleteira = Transpaleteira.get(
            Transpaleteira.id == transpaleteira_id
        )
        return transpaleteira
    except Transpaleteira.DoesNotExist as e:
        print(f'Erro: Transpaleteira com ID {transpaleteira_id} não encontrada. {e}')
        return None


def excluir_transpaleteira(transpaleteira_id):
    """
    Exclui uma transpaleteira do banco de dados pelo ID.
    Args:
        transpaleteira_id: ID da transpaleteira a ser excluída.
    Returns:
        bool: True se a transpaleteira foi excluída com sucesso, False se não foi encontrada.
    Raises:
        Transpaleteira.DoesNotExist: Se a transpaleteira com o ID especificado não existir no banco de dados.
    Example:
        >>> excluir_transpaleteira(1)
        Transpaleteira com ID 1 excluída com sucesso.
        True
    """

    try:
        transpaleteira = Transpaleteira.get(Transpaleteira.id == transpaleteira_id)
        transpaleteira.delete_instance()
        print(f'Transpaleteira com ID {transpaleteira_id} excluída com sucesso.')
        return True
    except Transpaleteira.DoesNotExist:
        print(f'Erro: Transpaleteira com ID {transpaleteira_id} não encontrada.')
        return False
