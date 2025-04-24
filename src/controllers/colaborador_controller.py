from peewee import IntegrityError

from models.colaborador import Colaborador


def adicionar_colaborador(
    matricula,
    nome,
    cargo,
    autorizado_transpaleteira=False,
    autorizado_empilhadeira=False,
):
    """
        Adiciona um novo colaborador ao sistema.
        Args:
            matricula (str): Matrícula única do colaborador.
            nome (str): Nome completo do colaborador.
            cargo (str): Cargo ou função do colaborador.
            autorizado_transpaleteira (bool, opcional): Indica se o colaborador está autorizado a operar transpaleteira. 
                Padrão é False.
            autorizado_empilhadeira (bool, opcional): Indica se o colaborador está autorizado a operar empilhadeira. 
                Padrão é False.
        Returns:
            Colaborador: Objeto do colaborador criado com sucesso.
            None: Retorna None se ocorrer um erro de integridade, como uma matrícula duplicada.
        Raises:
            IntegrityError: Caso ocorra um erro ao tentar criar o colaborador no banco de dados.
    """
   
    try:
        colaborador = Colaborador.create(
            matricula=matricula,
            nome=nome,
            cargo=cargo,
            autorizado_transpaleteira=autorizado_transpaleteira,
            autorizado_empilhadeira=autorizado_empilhadeira,
        )
        print(
            f'Colaborador {colaborador.nome} (Matrícula: {colaborador.matricula}) adicionado com sucesso.'
        )
        return colaborador
    except IntegrityError:
        print(f'Erro: Colaborador com matrícula {matricula} já existe.')
        return None


def listar_colaboradores():
    """
    Lista todos os colaboradores cadastrados no sistema.
    Esta função recupera todos os registros de colaboradores utilizando o método `select` 
    da classe `Colaborador`. Caso existam colaboradores cadastrados, exibe uma lista com 
    informações detalhadas de cada colaborador, incluindo nome, matrícula, cargo e 
    autorizações para operar transpaleteira e empilhadeira. Caso contrário, informa que 
    não há colaboradores cadastrados.
    Retorna:
        None
    """

    colaboradores = Colaborador.select()
    if colaboradores:
        print('\nLista de Colaboradores:')
        for colaborador in colaboradores:
            print(
                f'- {colaborador.nome} (Matrícula: {colaborador.matricula}), Cargo: {colaborador.cargo}, Transp.: {colaborador.autorizado_transpaleteira}, Empilh.: {colaborador.autorizado_empilhadeira}'
            )
    else:
        print('Nenhum colaborador cadastrado.')


def editar_colaborador(
    matricula,
    nome,
    cargo,
    autorizado_transpaleteira,
    autorizado_empilhadeira,
):
    """
    Edita as informações de um colaborador existente.

    Args:
        matricula (int): Matrícula do colaborador a ser editado.
        nome (str): Novo nome do colaborador.
        cargo (str): Novo cargo do colaborador.
        autorizado_transpaleteira (bool): Indica se o colaborador está autorizado a operar transpaleteira.
        autorizado_empilhadeira (bool): Indica se o colaborador está autorizado a operar empilhadeira.

    Returns:
        bool: Retorna True se a edição for bem-sucedida, False caso contrário.

    Raises:
        Colaborador.DoesNotExist: Caso o colaborador com a matrícula fornecida não seja encontrado.
        Exception: Para outros erros inesperados durante a edição.
    """
    
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        colaborador.nome = nome
        colaborador.cargo = cargo
        colaborador.autorizado_transpaleteira = autorizado_transpaleteira
        colaborador.autorizado_empilhadeira = autorizado_empilhadeira
        colaborador.save()
        return True
    except Colaborador.DoesNotExist:
        print(
            f'Erro ao editar: Colaborador com matrícula {matricula} não encontrado.'
        )
        return False
    except Exception as e:
        print(f'Erro ao editar colaborador: {e}')
        return False


def excluir_colaborador(matricula):
    """
    Exclui as informações de um colaborador existente com base na matrícula fornecida.
    Args:
        matricula (int): A matrícula do colaborador que será excluído.
    Returns:
        bool: Retorna True se a exclusão for bem-sucedida, caso contrário, retorna False.
    Raises:
        Exception: Caso ocorra algum erro durante a exclusão, uma mensagem de erro será exibida.
    """
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        colaborador.delete_instance()
        return True
    except Exception:
        print('algo errado')
        return False


def buscar_colaborador(matricula):
    """
    Busca as informações de um colaborador com base na matrícula fornecida.
    Args:
        matricula (int): Número de matrícula do colaborador a ser buscado.
    Returns:
        Colaborador: Objeto do colaborador encontrado, contendo suas informações.
        None: Caso nenhum colaborador com a matrícula fornecida seja encontrado.
    Exceções:
        Colaborador.DoesNotExist: Lançada quando nenhum colaborador com a matrícula fornecida é encontrado.
    Exemplo:
        >>> buscar_colaborador(12345)
        Informações do Colaborador 12345:
        - Nome: João Silva
        - Cargo: Operador
        - Autorizado Transpaleteira: Sim
        - Autorizado Empilhadeira: Não
    """

    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        print(f'\nInformações do Colaborador {matricula}:')
        print(f'- Nome: {colaborador.nome}')
        print(f'- Cargo: {colaborador.cargo}')
        print(
            f'- Autorizado Transpaleteira: {colaborador.autorizado_transpaleteira}'
        )
        print(
            f'- Autorizado Empilhadeira: {colaborador.autorizado_empilhadeira}'
        )
        return colaborador
    except Colaborador.DoesNotExist:
        print(f'Erro: Colaborador com matrícula {matricula} não encontrado.')
        return None


def listar_colaboradores_para_exibicao():
    """
    Retorna uma lista de dicionários contendo informações dos colaboradores para exibição.
    A função busca todos os colaboradores no banco de dados e organiza as informações
    em uma lista de dicionários, onde cada dicionário representa um colaborador com os
    seguintes campos:
    - 'matricula': Matrícula do colaborador.
    - 'nome': Nome do colaborador.
    - 'cargo': Cargo do colaborador.
    - 'autorizado_transpaleteira': Indica se o colaborador está autorizado a operar transpaleteira.
    - 'autorizado_empilhadeira': Indica se o colaborador está autorizado a operar empilhadeira.
    Returns:
        list[dict]: Lista de dicionários contendo os dados dos colaboradores.
    """

    colaboradores = Colaborador.select()
    lista_exibicao = []
    for colaborador in colaboradores:
        lista_exibicao.append({
            'matricula': colaborador.matricula,
            'nome': colaborador.nome,
            'cargo': colaborador.cargo,
            'autorizado_transpaleteira': colaborador.autorizado_transpaleteira,
            'autorizado_empilhadeira': colaborador.autorizado_empilhadeira,
        })
    return lista_exibicao
