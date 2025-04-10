from models import (
    atribuicao, colaborador, coletor,
    database, empilhadeira, transpaleteira
)

db = database.db
Atribuicao = atribuicao.Atribuicao()
Colaborador = colaborador.Colaborador()
Coletor = coletor.Coletor()
Empilhadeira = empilhadeira.Empilhadeira()
Transpaleteira = transpaleteira.Transpaleteira()
