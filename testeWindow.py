# test_console.py
import sys
import os

# Adiciona o diretório 'src' ao sys.path para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.controllers import colaborador_controller, coletor_controller
from src.models import db

def menu():
    print("\n--- Menu de Teste Console ---")
    print("1. Adicionar Colaborador")
    print("2. Listar Colaboradores")
    print("3. Buscar Colaborador")
    print("4. Adicionar Coletor")
    print("5. Listar Coletores")
    print("6. Buscar Coletor")
    print("0. Sair")

def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            matricula = input("Matrícula: ")
            nome = input("Nome: ")
            cargo = input("Cargo: ")
            autorizado_transp = input("Autorizado Transpaleteira (s/n): ").lower() == 's'
            autorizado_emp = input("Autorizado Empilhadeira (s/n): ").lower() == 's'
            colaborador_controller.adicionar_colaborador(matricula, nome, cargo, autorizado_transp, autorizado_emp)
        elif opcao == '2':
            colaborador_controller.listar_colaboradores()
        elif opcao == '3':
            matricula = input("Digite a matrícula do colaborador: ")
            colaborador_controller.buscar_colaborador(matricula)
        elif opcao == '4':
            modelo = input("Modelo do Coletor: ")
            coletor_controller.adicionar_coletor(modelo)
        elif opcao == '5':
            coletor_controller.listar_coletores()
        elif opcao == '6':
            coletor_id = input("Digite o ID do coletor: ")
            try:
                coletor_id = int(coletor_id)
                coletor_controller.buscar_coletor(coletor_id)
            except ValueError:
                print("ID inválido.")
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    # Conecta ao banco de dados antes de iniciar
    db.connect()
    main()
    # Fecha a conexão ao sair
    db.close()