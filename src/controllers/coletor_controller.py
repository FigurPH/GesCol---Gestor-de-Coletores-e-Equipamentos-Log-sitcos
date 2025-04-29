import csv

from peewee import IntegrityError

from models.coletor import Coletor


def adicionar_coletor(id, modelo, disponibilidade):
    """
    Adiciona um novo coletor ao sistema.
    Esta função cria um novo registro de coletor no banco de dados com os parâmetros fornecidos.
    Args:
        id (int): Número de identificação único do coletor
        modelo (str): Modelo/nome do coletor
        disponibilidade (bool): Estado de disponibilidade do coletor (True para disponível, False para indisponível)
    Returns:
        Coletor: Objeto Coletor criado com sucesso
        None: Se houver erro na criação (ID duplicado ou campos faltantes)
    Raises:
        IntegrityError: Quando há violação de integridade do banco de dados (ID duplicado ou tipo de dado incorreto)
    Exemplo:
        >>> adicionar_coletor(1, "MC92", True)
        <Coletor: id=1, modelo='MC92', disponibilidade=True>
    """

    if id and modelo and disponibilidade is not None:
        try:
            coletor = Coletor.create(
                id=id, modelo=modelo, disponibilidade=disponibilidade
            )
            # print(f"Coletor {coletor.modelo} (ID: {coletor.id}) adicionado com sucesso.")
            return coletor
        except IntegrityError as e:
            if "datatype mismatch" in str(e):
                print(f'Erro: ID deve ser um inteiro. {type(e)} > {e}')
            else:
                print(f'Erro: Coletor com número {id} já existe. {type(e)} > {e}')
                return None
    else:
        print('Erro: ID, modelo e disponibilidade são obrigatórios.')
        return None


def listar_coletores():
    coletores = Coletor.select()
    lista_exibicao = []
    for coletor in coletores:
        lista_exibicao.append({
            'id': coletor.id,
            'modelo': coletor.modelo,
            'disponibilidade': coletor.disponibilidade,
        })
    return lista_exibicao


def buscar_coletor(coletor_id):
    try:
        coletor = Coletor.get(Coletor.id == coletor_id)
        print(f'Coletor_Controller encontrou o coletor {coletor_id}')
        return coletor
    except Coletor.DoesNotExist:
        return None


def editar_coletor(coletor_id, modelo, disponibilidade):
    try:
        coletor = Coletor.get(Coletor.id == coletor_id)
        print(f'Coletor {coletor_id} encontrado.')
        coletor.id = coletor_id
        coletor.modelo = modelo
        coletor.disponibilidade = disponibilidade
        try:
            coletor.save()
            return True
        except Exception as e:
            print(f'ERRO NA HORA DE SALVAR A EDIÇÂO > {e}')

    except Coletor.DoesNotExist:
        print(f'Coletor {coletor_id} não encontrado.')
        return False
    except Exception as e:
        print(f'Ocorreu uma exceção. {e}')
        return False


def excluir_coletor(coletor_id):
    try:
        coletor = Coletor.get(Coletor.id == coletor_id)
        coletor.delete_instance()
        return True
    except Exception:
        print('Algo errado na exclusão do coletor')
        return False


def carregar_coletores_csv(path):
    """
    Carrega coletores a partir de um arquivo CSV e os adiciona ao banco de dados.
    Args:
        path (str): Caminho para o arquivo CSV.
    Returns:
        dict: Um dicionário contendo o número de registros adicionados e erros encontrados.
    """
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            try:
                Coletor.create(
                    id=row['id'],
                    modelo=row['modelo'],
                    disponibilidade=True
                )
            except Exception as e:
                print(e)
