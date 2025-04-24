# src/controllers/atribuicao_controller.py


from models.atribuicao import Atribuicao
from models.colaborador import Colaborador
from src.controllers import coletor_controller



def listar_atribuicoes_ativas():
    """
    Lista todas as atribuições que ainda não foram finalizadas (data_fim é nula).

    Returns:
        list: Uma lista de objetos Atribuicao ativos.
    """
    atribuicoes = (
        Atribuicao.select()
        .where(Atribuicao.data_fim == None)
        .order_by(Atribuicao.data_inicio.desc())
    )
    if atribuicoes:
        '''print('\n--- Atribuições Ativas ---')
        for atribuicao in atribuicoes:
            equipamentos = []
            if atribuicao.coletor:
                equipamentos.append(
                    f'Coletor: {atribuicao.coletor.modelo} (ID: {atribuicao.coletor.id})'
                )
            if atribuicao.empilhadeira:
                equipamentos.append(
                    f'Empilhadeira: {atribuicao.empilhadeira.modelo} (ID: {atribuicao.empilhadeira.id})'
                )
            if atribuicao.transpaleteira:
                equipamentos.append(
                    f'Transpaleteira: {atribuicao.transpaleteira.modelo} (ID: {atribuicao.transpaleteira.id})'
                )
            print(
                f'- ID: {atribuicao.id}, Colaborador: {atribuicao.colaborador.nome} (Matrícula: {atribuicao.colaborador.matricula}), Equipamentos: {", ".join(equipamentos)}, Início: {atribuicao.data_inicio.strftime("%Y-%m-%d %H:%M:%S")}'
            )'''
        return list(atribuicoes)
    else:
        print('Não há atribuições ativas no momento.')
        return []


def buscar_atribuicao_por_id(atribuicao_id):
    """
    Busca uma atribuição pelo seu ID.

    Args:
        atribuicao_id (int): ID da atribuição a ser buscada.

    Returns:
        Atribuicao or None: O objeto Atribuicao se encontrado, None caso contrário.
    """
    try:
        atribuicao = Atribuicao.get(Atribuicao.id == atribuicao_id)
        equipamentos = []
        if atribuicao.data_fim:
            print('')
        return atribuicao
    except Atribuicao.DoesNotExist:
        print(f'Erro: Atribuição com ID {atribuicao_id} não encontrada.')
        return None


def buscar_atribuicao_por_matricula(matricula):
    atribuicao = (
        Atribuicao.select()
        .join(Colaborador)
        .where((Colaborador.matricula == matricula) & (Atribuicao.data_fim.is_null()))
        .order_by(Atribuicao.data_inicio.desc())
    )
    '''print(atribuicao)
    for atr in atribuicao:
        print(f'ID: {atr.id}, Colaborador: {atr.colaborador.nome}, \
            Matrícula: {atr.colaborador.matricula}, Início: {atr.data_inicio}, Fim: {atr.data_fim}')'''

    return atribuicao if atribuicao else None


def carregar_informacoes_colaborador(matricula):
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


def atribuir_coletor(matricula, coletor_id):
    coletor = coletor_controller.buscar_coletor(int(coletor_id))
    if coletor is not None:
        try:
            Atribuicao.create(
                colaborador = matricula,
                coletor = coletor_id
            )
            return True
        except Exception as e:
            print(f'Deu um erro >> {e}')
            return False
    else: return False