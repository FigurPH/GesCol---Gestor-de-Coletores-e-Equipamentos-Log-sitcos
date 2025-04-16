from peewee import IntegrityError

from controllers import empilhadeira_controller, transpaleteira_controller
from models import Empilhadeira, Transpaleteira



def listar_equipamentos():
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