# src/controllers/atribuicao_controller.py
from src.models import Atribuicao
from src.models import Colaborador
from src.models import Coletor
from src.models import Empilhadeira
from src.models import Transpaleteira
from datetime import datetime

def iniciar_turno(colaborador_matricula, coletor_id, empilhadeira_id=None, transpaleteira_id=None):
    """
    Inicia o turno de um colaborador, atribuindo um coletor e, opcionalmente,
    uma empilhadeira e/ou transpaleteira, verificando as autorizações e disponibilidades.

    Args:
        colaborador_matricula (str): Matrícula do colaborador.
        coletor_id (int): ID do coletor a ser atribuído.
        empilhadeira_id (int, opcional): ID da empilhadeira a ser atribuída. Defaults to None.
        transpaleteira_id (int, opcional): ID da transpaleteira a ser atribuída. Defaults to None.

    Returns:
        Atribuicao or None: O objeto Atribuicao criado em caso de sucesso, None em caso de erro.
    """
    try:
        colaborador = Colaborador.get(Colaborador.matricula == colaborador_matricula)
    except Colaborador.DoesNotExist:
        print(f"Erro: Colaborador com matrícula {colaborador_matricula} não encontrado.")
        return None

    try:
        coletor = Coletor.get(Coletor.id == coletor_id, Coletor.disponibilidade == True)
    except Coletor.DoesNotExist:
        print(f"Erro: Coletor com ID {coletor_id} não encontrado ou indisponível.")
        return None

    empilhadeira = None
    if empilhadeira_id is not None:
        if not colaborador.autorizado_empilhadeira:
            print(f"Erro: Colaborador {colaborador_matricula} não autorizado a usar empilhadeira.")
            return None
        try:
            empilhadeira = Empilhadeira.get(Empilhadeira.id == empilhadeira_id, Empilhadeira.disponibilidade == True)
        except Empilhadeira.DoesNotExist:
            print(f"Erro: Empilhadeira com ID {empilhadeira_id} não encontrada ou indisponível.")
            return None

    transpaleteira = None
    if transpaleteira_id is not None:
        if not colaborador.autorizado_transpaleteira:
            print(f"Erro: Colaborador {colaborador_matricula} não autorizado a usar transpaleteira.")
            return None
        try:
            transpaleteira = Transpaleteira.get(Transpaleteira.id == transpaleteira_id, Transpaleteira.disponibilidade == True)
        except Transpaleteira.DoesNotExist:
            print(f"Erro: Transpaleteira com ID {transpaleteira_id} não encontrada ou indisponível.")
            return None

    try:
        atribuicao = Atribuicao.create(
            colaborador=colaborador,
            coletor=coletor,
            empilhadeira=empilhadeira,
            transpaleteira=transpaleteira,
            data_inicio=datetime.now()
        )

        coletor.disponibilidade = False
        coletor.save()
        if empilhadeira:
            empilhadeira.disponibilidade = False
            empilhadeira.save()
        if transpaleteira:
            transpaleteira.disponibilidade = False
            transpaleteira.save()

        print(f"Turno iniciado para {colaborador.nome} (Matrícula: {colaborador.matricula}) com Coletor ID: {coletor.id}.")
        if empilhadeira:
            print(f"Empilhadeira ID: {empilhadeira.id} atribuída.")
        if transpaleteira:
            print(f"Transpaleteira ID: {transpaleteira.id} atribuída.")
        return atribuicao
    except Exception as e:
        print(f"Erro ao iniciar turno: {e}")
        return None

def finalizar_turno(atribuicao_id):
    """
    Finaliza o turno de um colaborador, marcando a data de fim da atribuição
    e tornando os equipamentos atribuídos novamente disponíveis.

    Args:
        atribuicao_id (int): ID da atribuição a ser finalizada.

    Returns:
        bool: True se a finalização foi bem-sucedida, False caso contrário.
    """
    try:
        atribuicao = Atribuicao.get(Atribuicao.id == atribuicao_id, Atribuicao.data_fim == None)
    except Atribuicao.DoesNotExist:
        print(f"Erro: Atribuição com ID {atribuicao_id} não encontrada ou já finalizada.")
        return False

    try:
        atribuicao.data_fim = datetime.now()
        atribuicao.save()

        # Tornar os equipamentos disponíveis novamente
        coletor = atribuicao.coletor
        coletor.disponibilidade = True
        coletor.save()

        if atribuicao.empilhadeira:
            empilhadeira = atribuicao.empilhadeira
            empilhadeira.disponibilidade = True
            empilhadeira.save()

        if atribuicao.transpaleteira:
            transpaleteira = atribuicao.transpaleteira
            transpaleteira.disponibilidade = True
            transpaleteira.save()

        print(f"Turno finalizado para a atribuição ID: {atribuicao_id} do colaborador {atribuicao.colaborador.nome}.")
        return True
    except Exception as e:
        print(f"Erro ao finalizar turno: {e}")
        return False

def listar_atribuicoes_ativas():
    """
    Lista todas as atribuições que ainda não foram finalizadas (data_fim é nula).

    Returns:
        list: Uma lista de objetos Atribuicao ativos.
    """
    atribuicoes = Atribuicao.select().where(Atribuicao.data_fim == None).order_by(Atribuicao.data_inicio.desc())
    if atribuicoes:
        print("\n--- Atribuições Ativas ---")
        for atribuicao in atribuicoes:
            equipamentos = []
            if atribuicao.coletor:
                equipamentos.append(f"Coletor: {atribuicao.coletor.modelo} (ID: {atribuicao.coletor.id})")
            if atribuicao.empilhadeira:
                equipamentos.append(f"Empilhadeira: {atribuicao.empilhadeira.modelo} (ID: {atribuicao.empilhadeira.id})")
            if atribuicao.transpaleteira:
                equipamentos.append(f"Transpaleteira: {atribuicao.transpaleteira.modelo} (ID: {atribuicao.transpaleteira.id})")
            print(f"- ID: {atribuicao.id}, Colaborador: {atribuicao.colaborador.nome} (Matrícula: {atribuicao.colaborador.matricula}), Equipamentos: {', '.join(equipamentos)}, Início: {atribuicao.data_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        return list(atribuicoes)
    else:
        print("Não há atribuições ativas no momento.")
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
        if atribuicao.coletor:
            equipamentos.append(f"Coletor: {atribuicao.coletor.modelo} (ID: {atribuicao.coletor.id})")
        if atribuicao.empilhadeira:
            equipamentos.append(f"Empilhadeira: {atribuicao.empilhadeira.modelo} (ID: {atribuicao.empilhadeira.id})")
        if atribuicao.transpaleteira:
            equipamentos.append(f"Transpaleteira: {atribuicao.transpaleteira.modelo} (ID: {atribuicao.transpaleteira.id})")
        print(f"\n--- Atribuição ID: {atribuicao.id} ---")
        print(f"- Colaborador: {atribuicao.colaborador.nome} (Matrícula: {atribuicao.colaborador.matricula})")
        print(f"- Equipamentos: {', '.join(equipamentos)}")
        print(f"- Início: {atribuicao.data_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        if atribuicao.data_fim:
            print(f"- Fim: {atribuicao.data_fim.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("- Fim: Ainda não finalizada")
        return atribuicao
    except Atribuicao.DoesNotExist:
        print(f"Erro: Atribuição com ID {atribuicao_id} não encontrada.")
        return None