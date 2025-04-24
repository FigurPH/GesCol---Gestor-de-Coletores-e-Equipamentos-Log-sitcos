from peewee import IntegrityError

from models.empilhadeira import Empilhadeira


def adicionar_empilhadeira(id, modelo, disponibilidade):
    """
    Adiciona uma nova empilhadeira ao sistema.
    Args:
        id (int): Identificador único da empilhadeira.
        modelo (str): Modelo da empilhadeira.
        disponibilidade (bool): Disponibilidade da empilhadeira (True para disponível, False para indisponível).
    Returns:
        Empilhadeira: Objeto da empilhadeira criada, se a operação for bem-sucedida.
        None: Retorna None se ocorrer um erro, como ID duplicado ou dados obrigatórios ausentes.
    Raises:
        IntegrityError: Caso o ID da empilhadeira já exista no banco de dados.
    """

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
    """
    Lista todas as empilhadeiras cadastradas no sistema.
    Esta função recupera os registros de empilhadeiras do banco de dados
    e exibe uma lista com o ID, modelo e disponibilidade de cada empilhadeira.
    Caso não existam empilhadeiras cadastradas, uma mensagem informativa será exibida.
    Retorna:
        None
    """

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
    """
    Busca uma empilhadeira no banco de dados pelo seu ID.
    Args:
        empilhadeira_id (int): O ID da empilhadeira a ser buscada.
    Returns:
        Empilhadeira: Objeto da empilhadeira encontrada, se existir.
        None: Caso a empilhadeira com o ID fornecido não seja encontrada.
    Exceções Tratadas:
        Empilhadeira.DoesNotExist: Lançada quando nenhuma empilhadeira com o ID fornecido é encontrada no banco de dados.
    """

    try:
        empilhadeira = Empilhadeira.get(
            Empilhadeira.id == empilhadeira_id
        )
        return empilhadeira
    except Empilhadeira.DoesNotExist as e:
        print(f'Erro: Empilhadeira com ID {empilhadeira_id} não encontrada. {e}')
        return None


def excluir_empilhadeira(empilhadeira_id):
    """
    Exclui uma empilhadeira do banco de dados pelo seu ID.
    Args:
        empilhadeira_id: ID da empilhadeira a ser excluída.
    Returns:
        bool: True se a empilhadeira foi excluída com sucesso, False se não foi encontrada.
    Raises:
        Empilhadeira.DoesNotExist: Quando a empilhadeira com o ID especificado não é encontrada.
    """

    try:
        empilhadeira = Empilhadeira.get(Empilhadeira.id == empilhadeira_id)
        empilhadeira.delete_instance()
        print(f'Empilhadeira com ID {empilhadeira_id} excluída com sucesso.')
        return True
    except Empilhadeira.DoesNotExist:
        print(f'Erro: Empilhadeira com ID {empilhadeira_id} não encontrada.')
        return False


def editar_empilhadeira(empilhadeira_id, modelo, disponibilidade):
    """
    Edita os dados de uma empilhadeira existente no banco de dados.
    Args:
        empilhadeira_id: ID da empilhadeira a ser editada
        modelo: Novo modelo da empilhadeira
        disponibilidade: Nova disponibilidade da empilhadeira
    Returns:
        bool: True se a edição foi bem sucedida, False caso contrário
    Raises:
        Empilhadeira.DoesNotExist: Se a empilhadeira com o ID fornecido não for encontrada
        Exception: Para outros erros que possam ocorrer durante a edição
    """
    
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
