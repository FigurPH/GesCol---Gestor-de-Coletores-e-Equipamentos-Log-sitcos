from src.models import Coletor
from peewee import IntegrityError

def adicionar_coletor(modelo):
    try:
        coletor = Coletor.create(modelo=modelo)
        print(f"Coletor {coletor.modelo} (ID: {coletor.id}) adicionado com sucesso.")
        return coletor
    except IntegrityError:
        print(f"Erro: Coletor com modelo {modelo} já existe.")
        return None

def listar_coletores():
    coletores = Coletor.select()
    if coletores:
        print("\nLista de Coletores:")
        for coletor in coletores:
            print(f"- ID: {coletor.id}, Modelo: {coletor.modelo}, Disponível: {coletor.disponibilidade}")
    else:
        print("Nenhum coletor cadastrado.")

def buscar_coletor(coletor_id):
    try:
        coletor = Coletor.get(Coletor.id == coletor_id)
        print(f"\nInformações do Coletor {coletor_id}:")
        print(f"- Modelo: {coletor.modelo}")
        print(f"- Disponibilidade: {coletor.disponibilidade}")
        return coletor
    except Coletor.DoesNotExist:
        print(f"Erro: Coletor com ID {coletor_id} não encontrado.")
        return None