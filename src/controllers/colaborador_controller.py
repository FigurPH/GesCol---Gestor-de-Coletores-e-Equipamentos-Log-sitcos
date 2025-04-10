from models.colaborador import Colaborador
from peewee import IntegrityError


def adicionar_colaborador(matricula, nome, cargo, autorizado_transpaleteira=False, autorizado_empilhadeira=False):
    try:
        colaborador = Colaborador.create(
            matricula=matricula,
            nome=nome,
            cargo=cargo,
            autorizado_transpaleteira=autorizado_transpaleteira,
            autorizado_empilhadeira=autorizado_empilhadeira
        )
        print(f"Colaborador {colaborador.nome} (Matrícula: {colaborador.matricula}) adicionado com sucesso.")
        return colaborador
    except IntegrityError:
        print(f"Erro: Colaborador com matrícula {matricula} já existe.")
        return None

def listar_colaboradores():
    colaboradores = Colaborador.select()
    if colaboradores:
        print("\nLista de Colaboradores:")
        for colaborador in colaboradores:
            print(f"- {colaborador.nome} (Matrícula: {colaborador.matricula}), Cargo: {colaborador.cargo}, Transp.: {colaborador.autorizado_transpaleteira}, Empilh.: {colaborador.autorizado_empilhadeira}")
    else:
        print("Nenhum colaborador cadastrado.")

def editar_colaborador(matricula, nome, cargo, autorizado_transpaleteira, autorizado_empilhadeira):
    """Edita as informações de um colaborador existente."""
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        colaborador.nome = nome
        colaborador.cargo = cargo
        colaborador.autorizado_transpaleteira = autorizado_transpaleteira
        colaborador.autorizado_empilhadeira = autorizado_empilhadeira
        colaborador.save()
        return True
    except Colaborador.DoesNotExist:
        print(f"Erro ao editar: Colaborador com matrícula {matricula} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao editar colaborador: {e}")
        return False
    

def excluir_colaborador(matricula):
    """Exclui as informações de um colaborador existente"""
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        colaborador.delete_instance()
        return True
    except Exception:
        print('algo errado')
        return False


def buscar_colaborador(matricula):
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        print(f"\nInformações do Colaborador {matricula}:")
        print(f"- Nome: {colaborador.nome}")
        print(f"- Cargo: {colaborador.cargo}")
        print(f"- Autorizado Transpaleteira: {colaborador.autorizado_transpaleteira}")
        print(f"- Autorizado Empilhadeira: {colaborador.autorizado_empilhadeira}")
        return colaborador
    except Colaborador.DoesNotExist:
        print(f"Erro: Colaborador com matrícula {matricula} não encontrado.")
        return None
    
def listar_colaboradores_para_exibicao():
    """Retorna uma lista de dicionários de colaboradores para exibição na lista."""
    colaboradores = Colaborador.select()
    lista_exibicao = []
    for colaborador in colaboradores:
        lista_exibicao.append({
            'matricula': colaborador.matricula,
            'nome': colaborador.nome,
            'cargo': colaborador.cargo,
            'autorizado_transpaleteira': colaborador.autorizado_transpaleteira,
            'autorizado_empilhadeira': colaborador.autorizado_empilhadeira
        })
    return lista_exibicao