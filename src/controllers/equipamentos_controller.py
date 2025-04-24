
from models import Empilhadeira, Transpaleteira


def listar_equipamentos():
    """
    Lista todos os equipamentos cadastrados no sistema.
    Esta função recupera todas as empilhadeiras e transpaleteiras do banco de dados
    e retorna uma lista unificada contendo as informações básicas de cada equipamento.
    Returns:
        list: Uma lista de dicionários onde cada dicionário contém:
            - id (int): Identificador único do equipamento
            - modelo (str): Modelo do equipamento
            - disponibilidade (bool): Status de disponibilidade do equipamento
            - tipo (str): Tipo do equipamento ('Empilhadeira' ou 'Transpaleteira')
    Exemplo de retorno:
        [
            {
                'id': 1,
                'modelo': 'BT RRE160H',
                'disponibilidade': True,
            },
            {
                'id': 2, 
                'modelo': 'BT LWE130',
                'disponibilidade': False,
            }
        ]
    """

    empilhadeiras = Empilhadeira.select()
    transpaleteiras = Transpaleteira.select()
    lista_exibicao = []

    for empilhadeira in empilhadeiras:
        lista_exibicao.append({
            'id': empilhadeira.id,
            'modelo': empilhadeira.modelo,
            'disponibilidade': empilhadeira.disponibilidade,
            'tipo': 'Empilhadeira'
        })

    for transpaleteira in transpaleteiras:
        lista_exibicao.append({
            'id': transpaleteira.id,
            'modelo': transpaleteira.modelo,
            'disponibilidade': transpaleteira.disponibilidade,
            'tipo': 'Transpaleteira'
        })

    return lista_exibicao
