from medico import (
    criar_medico, listar_medicos, consultar_medico,
    atualizar_medico, remover_medico, medico_existe
)
from paciente import (
    criar_paciente, listar_pacientes, consultar_paciente,
    atualizar_paciente, remover_paciente
)

def menu_principal():
    print("\n===== SISTEMA DE GESTÃO HOSPITALAR =====")
    print("1 - Menu Médico")
    print("2 - Menu Paciente")
    print("0 - Sair")

def menu_medico():
    print("\n===== MENU MÉDICO =====")
    print("1 - Criar médico")
    print("2 - Listar médicos")
    print("3 - Consultar médico")
    print("4 - Atualizar médico")
    print("5 - Remover médico")
    print("0 - Voltar")

def menu_paciente():
    print("\n===== MENU PACIENTE =====")
    print("1 - Criar paciente")
    print("2 - Listar pacientes")
    print("3 - Consultar paciente")
    print("4 - Atualizar paciente")
    print("5 - Remover paciente")
    print("0 - Voltar")

def submenu_medico():
    while True:
        menu_medico()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome        = input("Nome: ")
            dt_nasc     = input("Data de nascimento (YYYY-MM-DD): ")
            nacional    = input("Nacionalidade: ")
            especial    = input("Especialidade: ")
            dt_registo  = input("Data de registo (YYYY-MM-DD): ")
            idiomas     = input("Idiomas: ")
            p_forte     = input("Ponto forte: ")
            p_fraco     = input("Ponto fraco: ")
            
            try:
                id_unidade = int(input("ID da unidade de saúde: "))
            except ValueError:
                print("\n❌ Erro: ID da unidade deve ser um número inteiro.")
                continue
                
            horario     = input("Horário do turno: ")
            cargo       = input("Cargo: ")

            code, obj = criar_medico(nome, dt_nasc, nacional, especial,
                                     dt_registo, idiomas, p_forte, p_fraco,
                                     id_unidade, horario, cargo)
            if code == 201:
                print("\n✅ Sucesso: " + str(obj))
            else:
                print("\n❌ Falha: " + str(obj))

        elif opcao == "2":
            code, obj = listar_medicos()
            if code == 200:
                print("\nLista de médicos:")
                for id_med, dados in obj.items():
                    print(f"  ID: {id_med} | Nome: {dados['nome']} | "
                          f"Especialidade: {dados['especialidade']} | Cargo: {dados['cargo']}")
            else:
                print("\n❌ " + str(obj))

        elif opcao == "3":
            id_medico = input("ID do médico: ")
            code, obj = consultar_medico(id_medico)
            if code == 200:
                print(f"\nFicha do Médico {id_medico}:")
                for chave, valor in obj.items():
                    print(f"  {chave.replace('_', ' ').capitalize()}: {valor}")
            else:
                print("\n❌ " + str(obj))

        elif opcao == "4":
            id_medico   = input("ID do médico: ")
            nome        = input("Novo nome (enter para manter): ")
            dt_nasc     = input("Nova data nascimento YYYY-MM-DD (enter para manter): ")
            nacional    = input("Nova nacionalidade (enter para manter): ")
            especial    = input("Nova especialidade (enter para manter): ")
            dt_registo  = input("Nova data de registo YYYY-MM-DD (enter para manter): ")
            idiomas     = input("Novos idiomas (enter para manter): ")
            p_forte     = input("Novo ponto forte (enter para manter): ")
            p_fraco     = input("Novo ponto fraco (enter para manter): ")
            id_unidade_str = input("Novo ID da unidade (enter para manter): ")
            horario     = input("Novo horário do turno (enter para manter): ")
            cargo       = input("Novo cargo (enter para manter): ")

            id_unidade = None
            if id_unidade_str.strip():
                try:
                    id_unidade = int(id_unidade_str)
                except ValueError:
                    print("\n❌ Erro: ID da unidade deve ser um número inteiro.")
                    continue

            code, obj = atualizar_medico(
                id_medico,
                nome        if nome.strip() else None,
                dt_nasc     if dt_nasc.strip() else None,
                nacional    if nacional.strip() else None,
                especial    if especial.strip() else None,
                dt_registo  if dt_registo.strip() else None,
                idiomas     if idiomas.strip() else None,
                p_forte     if p_forte.strip() else None,
                p_fraco     if p_fraco.strip() else None,
                id_unidade,
                horario     if horario.strip() else None,
                cargo       if cargo.strip() else None,
            )
            if code == 200:
                print("\n✅ Atualizado:\n" + str(obj))
            else:
                print("\n❌ Falha: " + str(obj))

        elif opcao == "5":
            id_medico = input("ID do médico: ")
            code, obj = remover_medico(id_medico)
            if code == 200:
                print("\n✅ Removido: " + str(obj))
            else:
                print("\n❌ Falha: " + str(obj))

        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")

def submenu_paciente():
    while True:
        menu_paciente()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome        = input("Nome: ")
            dt_nasc     = input("Data de nascimento (YYYY-MM-DD): ")
            nacional    = input("Nacionalidade: ")
            tipo_sang   = input("Tipo sanguíneo: ")
            alergias    = input("Alergias: ")
            doencas     = input("Doenças crónicas: ")
            cirurgias   = input("Cirurgias anteriores: ")

            id_medico_str = input("ID do médico responsável (ex: M001): ")
            if not medico_existe(id_medico_str):
                print(f"\n❌ Erro 404: Médico '{id_medico_str}' não encontrado. Registe o médico primeiro.")
                continue

            code, obj = criar_paciente(nome, dt_nasc, nacional, tipo_sang,
                                       alergias, doencas, cirurgias, id_medico_str)
            if code == 201:
                print("\n✅ Sucesso: " + str(obj))
            else:
                print("\n❌ Falha: " + str(obj))

        elif opcao == "2":
            code, obj = listar_pacientes()
            if code == 200:
                print("\nLista de pacientes:")
                for nif, dados in obj.items():
                    print(f"  NIF: {nif} | Nome: {dados['nome']} | "
                          f"Tipo sanguíneo: {dados['tipo_sanguineo']} | Médico: {dados['id_medico']}")
            else:
                print("\n❌ " + str(obj))

        elif opcao == "3":
            try:
                nif = int(input("NIF do paciente: "))
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue
            code, obj = consultar_paciente(nif)
            if code == 200:
                print(f"\nFicha do Paciente (NIF: {nif}):")
                for chave, valor in obj.items():
                    print(f"  {chave.replace('_', ' ').capitalize()}: {valor}")
            else:
                print("\n❌ " + str(obj))

        elif opcao == "4":
            try:
                nif = int(input("NIF do paciente: "))
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue

            nome        = input("Novo nome (enter para manter): ")
            dt_nasc     = input("Nova data nascimento YYYY-MM-DD (enter para manter): ")
            nacional    = input("Nova nacionalidade (enter para manter): ")
            tipo_sang   = input("Novo tipo sanguíneo (enter para manter): ")
            alergias    = input("Novas alergias (enter para manter): ")
            doencas     = input("Novas doenças crónicas (enter para manter): ")
            cirurgias   = input("Novas cirurgias anteriores (enter para manter): ")
            id_medico   = input("Novo ID do médico (enter para manter): ")

            if id_medico.strip() and not medico_existe(id_medico.strip()):
                print(f"\n❌ Erro: Médico '{id_medico.strip()}' não encontrado.")
                continue

            code, obj = atualizar_paciente(
                nif,
                nome        if nome.strip() else None,
                dt_nasc     if dt_nasc.strip() else None,
                nacional    if nacional.strip() else None,
                tipo_sang   if tipo_sang.strip() else None,
                alergias    if alergias.strip() else None,
                doencas     if doencas.strip() else None,
                cirurgias   if cirurgias.strip() else None,
                id_medico   if id_medico.strip() else None,
            )
            if code == 200:
                print("\n✅ Atualizado:\n" + str(obj))
            else:
                print("\n❌ Falha: " + str(obj))

        elif opcao == "5":
            try:
                nif = int(input("NIF do paciente: "))
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue
            code, obj = remover_paciente(nif)
            if code == 200:
                print("\n✅ Removido: " + str(obj))
            else:
                print("\n❌ Falha: " + str(obj))

        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")

def main():
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            submenu_medico()
        elif opcao == "2":
            submenu_paciente()
        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!\n")
            break
        else:
            print("\n❌ Opção inválida.")

if __name__ == "__main__":
    main()
