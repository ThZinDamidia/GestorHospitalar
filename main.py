
from medico import adicionar_medico
from medico import listar_nomes__dos_medicos
from medico import consultar_medicos
from medico import atualizar_medico
from paciente import adicionar_paciente
from medico import deletar_medico


def main():
    while True:
        try:
            print("1 - Deletar Medico")
            print("2 - Adicionar medico")
            print("3 - Listar Medicos")
            print("4 -Consultar medicos")
            print("5 - Atualizar medicos")
            print("6 - Entra menu do paciente")
            print("7 - Sair")


            escolha_menu_medico = int(input("Escolha uma das opções acima: "))

            if escolha_menu_medico == 1:
                deletar_medico()

            elif escolha_menu_medico == 2:
                adicionar_medico()

            elif escolha_menu_medico == 3:
                listar_nomes__dos_medicos()

            elif escolha_menu_medico == 4:
                consultar_medicos()

            elif escolha_menu_medico == 5:
                atualizar_medico()

            elif escolha_menu_medico == 6:
                print("---Menu do paciente---")
                print("2 - Adicionar Paciente")
                print("3 - Listar Pacientes")
                print("4 -Consultar Paciente")
                print("5 - Atualizar Paciente")
                print("Deletar Paciente")
                escolha_menu_paciente = int(input("Escolha uma das opções acima: "))
                if escolha_menu_paciente ==  1:
                    adicionar_paciente()

            elif escolha_menu_medico == 7:
                print("Sair")

            else:
                print("opção invalida")
        except ValueError:
            print("Erro esolha apenas umas das opções")






if __name__ == "__main__":
        main()
