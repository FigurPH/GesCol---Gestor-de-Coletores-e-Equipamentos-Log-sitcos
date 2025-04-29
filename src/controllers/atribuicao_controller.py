# src/controllers/atribuicao_controller.py


from datetime import datetime

from models.atribuicao import Atribuicao
from models.colaborador import Colaborador
from src.controllers import coletor_controller


def buscar_atribuicao_por_matricula(matricula):
    """
    Busca a atribuição ativa de um colaborador com base na matrícula.

    Esta função consulta o banco de dados para encontrar a atribuição mais recente
    de um colaborador cuja matrícula corresponda ao valor fornecido. Apenas atribuições
    que ainda estão ativas (ou seja, cuja data de término é nula) são consideradas.

    Args:
        matricula (str): A matrícula do colaborador para o qual a atribuição será buscada.

    Returns:
        Atribuicao or None: Retorna a atribuição ativa mais recente do colaborador, 
        ou None se nenhuma atribuição ativa for encontrada.
    """

    atribuicao = (
        Atribuicao.select()
        .join(Colaborador)
        .where((Colaborador.matricula == matricula) & (Atribuicao.data_fim.is_null()))
        .order_by(Atribuicao.data_inicio.desc())
    ) if Colaborador.get(Colaborador.matricula == matricula) else None
    return atribuicao if atribuicao else None


def carregar_informacoes_colaborador(matricula):
    """
    Carrega as informações de atribuição de um colaborador com base na matrícula.
    Este método tenta buscar as atribuições associadas a um colaborador pela matrícula.
    Caso não encontre atribuições, ele cria e retorna um objeto "falso" de atribuição
    com os dados do colaborador injetados.
    Args:
        matricula (str): A matrícula do colaborador.
    Returns:
        Atribuicao: Um objeto de atribuição associado ao colaborador, ou um objeto
        "falso" de atribuição com os dados do colaborador.
    Raises:
        Exception: Caso ocorra algum erro durante a execução.
    """
    try:
        atribuicao = buscar_atribuicao_por_matricula(matricula)
        # atr_id = buscar_atribuicao_por_id([atr.id for atr in atribuicao])
        if atribuicao:
            # return atr_id
            return atribuicao[0]
        else:
            colaborador = Colaborador.get(Colaborador.matricula == matricula)

            # Mocka um objeto "falso" de Atribuições com os dados de Colborador injetados
            return Atribuicao(
                colaborador=colaborador,
                coletor=None,
                empilhadeira=None,
                transpaleteira=None,
                data_inicio=None,
                data_fim=None
            )
    except Exception as e:
        print(f'Erro: {e}')


def buscar_atribuicao_por_chave(chave, valor):
    """
    Busca uma atribuição no banco de dados com base em uma chave e valor fornecidos.

    Args:
        chave (str): O nome do campo da classe `Atribuicao` a ser utilizado na busca.
        valor (Any): O valor correspondente ao campo especificado para filtrar os resultados.

    Returns:
        Atribuicao: A primeira instância de `Atribuicao` encontrada que corresponde aos critérios
        de busca, com `data_fim` nulo e ordenada pela data de início em ordem decrescente.
        Retorna `None` se nenhuma atribuição for encontrada.
    """
    campo = getattr(Atribuicao, chave)
    atribuido = (
            Atribuicao.select()
            .where((campo == valor) & (Atribuicao.data_fim.is_null()))
            .order_by(Atribuicao.data_inicio.desc())
            .first()
        )
    return atribuido


def bool_coletor_atribuído(coletor_id) -> bool:
    """
    Verifica se o coletor informado está atribuído a alguém.

    Args:
        coletor_id (int): ID do coletor a ser verificado.

    Returns:
        bool: True se o coletor está atribuído, False caso contrário.
    """
    try:
        if buscar_atribuicao_por_chave(chave='coletor', valor=coletor_id):
            return True
        else:
            return False
    except Exception:
        print('deu exceção no bool atrib controller')
        return True


def atribuir_coletor(matricula, coletor_id):
    """
    Atribui um coletor a um colaborador com base na matrícula e no ID do coletor.

    Esta função verifica se o coletor especificado existe e não está atribuído a outro colaborador.
    Caso o coletor esteja disponível, ela cria um registro de atribuição no banco de dados.

    Args:
        matricula (str): A matrícula (identificador) do colaborador.
        coletor_id (int): O ID do coletor a ser atribuído.

    Returns:
        bool: True se a atribuição foi bem-sucedida, False caso contrário.

    Raises:
        Exception: Caso ocorra um erro durante o processo de criação da atribuição.

    Observações:
        - Se o coletor não existir, uma mensagem será exibida indicando isso.
        - Se o coletor já estiver atribuído, a função não prossegue com a atribuição.
    """
    coletor = coletor_controller.buscar_coletor(int(coletor_id))
    if coletor and coletor.disponibilidade == True:
        if not bool_coletor_atribuído(coletor_id):
            try:
                Atribuicao.create(
                    colaborador=matricula,
                    coletor=coletor_id
                )
                return True
            except Exception as e:
                print(f'Deu um erro >> {e} atrib_controll')
                return False
    else:
        print('Mensagem dizendo que coletor não existe')


def devolver_coletor(coletor_id):
    """
    Devolve o coletor informado, atualizando a atribuição correspondente com a data de término.

    Args:
        coletor_id (int): ID do coletor a ser devolvido.

    Returns:
        bool: True se a devolução foi bem-sucedida, False caso contrário.
    """
    try:
        atribuicao = buscar_atribuicao_por_chave(chave='coletor', valor=coletor_id)
        if atribuicao:
            atribuicao.data_fim = datetime.now()
            atribuicao.save()
            return True
        else:
            print("Nenhuma atribuição ativa encontrada para o coletor informado.")
            return False
    except Exception as e:
        print(f"Erro ao devolver coletor: {e}")
        return False
