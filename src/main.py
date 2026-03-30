from medico import adicionar_medico, listar_nomes__dos_medicos, consultar_medicos, atualizar_medico, deletar_medico
from paciente import adicionar_paciente, listar_pacientes, consultar_paciente, atualizar_paciente, deletar_paciente


def menu_paciente():
    """Sub-menu dedicado apenas aos pacientes"""
    while True:
        try:
            print("\n--- MENU DO PACIENTE ---")
            print("1 - Adicionar Paciente")
            print("2 - Listar Pacientes")
            print("3 - Consultar Paciente")
            print("4 - Atualizar Paciente")
            print("5 - Deletar Paciente")
            print("6 - Voltar ao Menu Principal")

            escolha = int(input("\nEscolha uma opção: "))

            if escolha == 1:
                adicionar_paciente()
            elif escolha == 2:
                listar_pacientes()
            elif escolha == 3:
                consultar_paciente()
            elif escolha == 4:
                atualizar_paciente()
            elif escolha == 5:
                deletar_paciente()
            elif escolha == 6:
                break  # Sai do loop do paciente e volta pro main
            else:
                print("Opção inválida!")
        except ValueError:
            print("Erro: Digite apenas números.")


def main():
    while True:
        try:
            print("\n=== SISTEMA DE GESTÃO HOSPITALAR ===")
            print("1 - Adicionar Médico")
            print("2 - Listar Médicos")
            print("3 - Consultar Médico")
            print("4 - Atualizar Médico")
            print("5 - Deletar Médico")
            print("6 - Menu do Paciente >")
            print("7 - Sair")

            escolha_menu_medico = int(input("\nEscolha uma opção: "))

            if escolha_menu_medico == 1:
                adicionar_medico()
            elif escolha_menu_medico == 2:
                listar_nomes__dos_medicos()
            elif escolha_menu_medico == 3:
                consultar_medicos()
            elif escolha_menu_medico == 4:
                atualizar_medico()
            elif escolha_menu_medico == 5:
                deletar_medico()
            elif escolha_menu_medico == 6:
                menu_paciente()  # Chama a função do sub-menu
            elif escolha_menu_medico == 7:
                print("Encerrando o sistema... Até logo!")
                break
            else:
                print("Opção inválida!")
        except ValueError:
            print("Erro: Escolha apenas os números das opções acima.")


if __name__ == "__main__":
    main()
