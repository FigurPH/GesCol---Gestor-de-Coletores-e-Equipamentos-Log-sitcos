from datetime import datetime

from models.atribuicao import Atribuicao
from src.controllers import atribuicao_controller


def contar_colaboradores_ativos():
    """
    Conta o número de colaboradores ativos no sistema.

    Esta função consulta o banco de dados para contar o número total de
    colaboradores que estão atualmente ativos (ou seja, aqueles que têm
    atribuições com data de término nula).

    Returns:
        int: O número total de colaboradores ativos.
    """
    colaboradores_ativos = Atribuicao.select().where(
        Atribuicao.data_fim.is_null()
    ).count()
    return colaboradores_ativos

def contar_coletores_atribuidos():
    """
    Conta o número de coletores atribuídos no sistema.

    Esta função consulta o banco de dados para contar o número total de
    coletores que estão atualmente atribuídos a colaboradores (ou seja, aqueles
    que têm atribuições com data de término nula).

    Returns:
        int: O número total de coletores atribuídos.
    """
    coletores_atribuidos = Atribuicao.select().where(
        Atribuicao.data_fim.is_null() & Atribuicao.coletor.is_null(False)
    ).count()
    return coletores_atribuidos

def contar_transpaleteiras_atribuidas():
    """
    Conta o número de transpaleteiras atribuídas no sistema.

    Esta função consulta o banco de dados para contar o número total de
    transpaleteiras que estão atualmente atribuídas a colaboradores (ou seja, aqueles
    que têm atribuições com data de término nula).

    Returns:
        int: O número total de transpaleteiras atribuídas.
    """
    transpaleteiras_atribuidas = Atribuicao.select().where(
        Atribuicao.data_fim.is_null() & Atribuicao.transpaleteira.is_null(False)
    ).count()
    return transpaleteiras_atribuidas

def contar_empilhadeiras_atribuidas():
    """
    Conta o número de empilhadeiras atribuídas no sistema.

    Esta função consulta o banco de dados para contar o número total de
    empilhadeiras que estão atualmente atribuídas a colaboradores (ou seja, aqueles
    que têm atribuições com data de término nula).

    Returns:
        int: O número total de empilhadeiras atribuídas.
    """
    empilhadeiras_atribuidas = Atribuicao.select().where(
        Atribuicao.data_fim.is_null() & Atribuicao.empilhadeira.is_null(False)
    ).count()
    return empilhadeiras_atribuidas

def buscar_atribuicoes():
    """
    Busca todas as atribuições que não possuem data de término.

    Retorna:
        list: Uma lista contendo todas as instâncias de atribuições 
        cuja data_fim é nula.
    """

    atribuicoes = Atribuicao.select().where(Atribuicao.data_fim.is_null())
    return list(atribuicoes)

def filtrar_atribuicoes(matricula=None, coletor=None):
    """
    Filtra as atribuições com base em um critério fornecido.

    Args:
        filtro (dict, optional): Um dicionário contendo os critérios de filtro.
            As chaves podem ser os nomes dos campos e os valores são os valores
            a serem filtrados. Exemplo: {'colaborador_id': 1, 'coletor': True}

    Returns:
        list: Uma lista contendo as instâncias de atribuições que correspondem
        aos critérios de filtro.
    """
    if matricula:
        atribuicao = atribuicao_controller.buscar_atribuicao_por_matricula(matricula)
        return atribuicao if atribuicao else None
    if coletor:
        atribuicao = atribuicao_controller.buscar_atribuicao_por_chave(chave='coletor', valor=coletor)
        return atribuicao if atribuicao else None