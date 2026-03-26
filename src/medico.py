medicos = {}


def adicionar_medico():
    while True:
        try:

            id_do_medico = int(input("ID do medico: "))
            if id_do_medico in medicos:
                print("ID já existe não e possivel adicionar ID's iguais no sistema")
                continue
            if id_do_medico == 0:
                print("Não e possivel adicionar ID 0 no sistema")
                continue
            nome = input("Informe o nome do medico: ").title()
            data_de_nascimento = (input("Informe a data de nascimento do medico: "))
            nacionalidade = input("Informe o nacionalidade do medico: ")
            area_de_especialidade = input("Informe o area do medico: ")
            data_de_regsito = (input("Informe a data de resgito do medico: "))
            idiomas = input("Informe os idiomas do medico: ")
            ponto_forte = input("Informe o ponto forte do medico: ")
            ponto_fraco = input("Informe o ponto fraco do medico: ")
            id_da_unidade_de_saude = int(input("Informe o id da unidade de saude: "))
            horario_turno = input("Informe o horario do turno: ")
            cargo = input("Informe o cargo do medico: ")
            medicos[id_do_medico] = {
                        "nome": nome,
                        "data_de_nascimento": data_de_nascimento,
                        "nacionalidade": nacionalidade,
                        "area_de_especialidade": area_de_especialidade,
                        "data_de_regsito": data_de_regsito,
                        "idiomas": idiomas,
                        "ponto_forte": ponto_forte,
                        "ponto_fraco": ponto_fraco,
                        "id_da_unidade_de_saude": id_da_unidade_de_saude,
                        "horario_turno": horario_turno,
                        "cargo": cargo,

                    }
            print(f'ID {id_do_medico} adicionado com sucesso!')
            break
        except ValueError:
                print("Erro de digitação")


def listar_nomes__dos_medicos():
    if not medicos:
        print("Não ha medicos no registro")
    for chaves in medicos.keys():
        print(chaves)





def consultar_medicos():
        if not medicos:
            print("O sistema está vazio. Adicione um médico primeiro.")
            return

        try:
            # 1. Pedimos o ID (a chave) ao utilizador
            escolha = int(input("Introduza o ID do médico que deseja consultar: "))

            # 2. Acedemos ao dicionário interno usando a chave 'escolha'
            # Usamos .get() para evitar que o programa pare se o ID não existir
            medico_encontrado = medicos.get(escolha)

            if medico_encontrado:
                print(f"\n--- Ficha do Médico (ID: {escolha}) ---")

                # 3. Complexidade Dinâmica: Iteramos sobre as sub-chaves
                # Assim, não precisas de escrever "print(nome)", "print(cargo)", etc.
                for chave, valor in medico_encontrado.items():
                    # Formatamos a chave para ficar bonita (ex: ponto_forte -> Ponto Forte)
                    titulo = chave.replace("_", " ").capitalize()
                    print(f"{titulo}: {valor}")
            else:
                print(f"Erro: O ID {escolha} não foi encontrado no sistema.")

        except ValueError:
            print("Erro: Por favor, digite um número de ID válido.")





def atualizar_medico():

        if not medicos:
            print("Nenhum médico registado.")
            return

        try:
            id_escolhido = int(input("Digite o ID do médico que deseja alterar: "))

            # 1. Verificamos se o médico existe
            if id_escolhido in medicos:
                medico = medicos[id_escolhido]

                # 2. Mostramos as opções disponíveis dinamicamente usando .keys()
                print("\nO que deseja alterar?")
                opcoes = list(medico.keys())
                for i, chave in enumerate(opcoes):
                    print(f"{i + 1}. {chave.replace('_', ' ').capitalize()}")

                # 3. Escolha da característica
                escolha = int(input("\nEscolha o número do campo a alterar: ")) - 1

                if 0 <= escolha < len(opcoes):
                    campo_para_alterar = opcoes[escolha]
                    novo_valor = input(f"Novo valor para {campo_para_alterar}: ")

                    # 4. A Altração propriamente dita (Update)
                    medico[campo_para_alterar] = novo_valor
                    print(f"Sucesso! {campo_para_alterar.replace('_', ' ')} atualizado.")
                else:
                    print("Opção inválida.")
            else:
                print("ID não encontrado.")

        except ValueError:
            print("Erro: Introduza apenas números para IDs e opções.")



def deletar_medico():
    if not medicos:
        print("Não ha medicos no registro ainda")
        return
    id_para_deletar = int(input("Qual ID do medico para ser deletado? "))
    if id_para_deletar in medicos:
        removido = medicos.pop(id_para_deletar)
        print(f"Medico {removido}deletado com sucesso!")












