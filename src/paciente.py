
paciente = {}

def adicionar_paciente():
    while True:
        try:
            print("Insira os dados a seguir ")
            nome = input("Digite o nome do paciente: ").title()
            nif = int(input("Digite o nif: "))
            nif = int(input("Digite o nif: "))
            data_de_nascimento = input("Digite o data de nascimento: ")
            nacionalidade = input("Digite o nacionalidade: ")
            tipo_sanguinio = input("Digite o tipo de sanguinio: ")
            alergias = input("Digite as alergias: ")
            doencas_cronicas = input("Digite as doencas cronicas: ")
            cirurgias_anteriores = input("Digite as cirurgias anteriores: ")
            medico_atual = int(input("Digite o ID do medio atual: "))

            paciente[paciente] = {
                "nome": nome,
                "nif": nif,
                "data_de_nascimento": data_de_nascimento,
                "nacionalidade": nacionalidade,
                "tipo_sanguinio": tipo_sanguinio,
                "alergias": alergias,
                "doencas_cronicas": doencas_cronicas,
                "cirurgias_anteriores": cirurgias_anteriores,
                "medico_atual": medico_atual,
            }
            print(f'Paciente {nome} adicionado com sucesso')
            break
        except ValueError:
            print("Errado")


def listar_pacientes():
    if not paciente:
        print("Não ha paciente ainda no registro")
        return
    for valor in paciente.keys():
        print(valor)



def atualizar_paciente():
    if not paciente:
        print("Não ha pacientes no registro")
        return
    while True:
        try:
            nif_escolha = int(input("Digite o nif do paciente: "))

            if nif_escolha in paciente:
                paciente_nif = paciente[nif_escolha]

                print("O que deseja alterar? ")
                opcao_p = list(paciente.keys())
                for i,chave in enumerate(opcao_p):
                    print(f"{i + 1}. {chave.replace('_', ' ').capitalize()}")

                escolha = int(input("\nEscolha o número do campo a alterar: ")) - 1
                if 0 <= escolha < len(opcao_p):
                    campo_para_alterar = opcao_p[escolha]
                    novo_valor = input(f"Novo valor para {campo_para_alterar}: ")

                    paciente[campo_para_alterar] = novo_valor
                    print(f"Sucesso! {campo_para_alterar.replace('_', ' ')} atualizado.")
                else:
                    print("Opção inválida.")
            else:
                print("ID não encontrado.")

        except ValueError:
            print("Erro: Introduza apenas números para IDs e opções.")



def deletar_paciente():
    if not paciente:
        print("Não ha paciente no registro")
        return
    deletar_pacient = int(input("Digite o NIF do paciente: "))
    if deletar_pacient in paciente:
        remover1 = paciente.pop(deletar_pacient)
        print(f"Paciente{remover1} deletado com sucesso!")



def consultar_paciente():
    if not paciente:
        print("O sistema está vazio. Adicione um médico primeiro.")
        return
    try:
        # 1. Pedimos o ID (a chave) ao utilizador
        escolha = int(input("Introduza o ID do médico que deseja consultar: "))

        # 2. Acedemos ao dicionário interno usando a chave 'escolha'
        # Usamos .get() para evitar que o programa pare se o ID não existir
        paciente_encontrado = paciente.get(escolha)

        if paciente_encontrado:
            print(f"\n--- Ficha do Médico (ID: {escolha}) ---")

            # 3. Complexidade Dinâmica: Iteramos sobre as sub-chaves
            # Assim, não precisas de escrever "print(nome)", "print(cargo)", etc.
            for chave, valor in paciente_encontrado.items():
                # Formatamos a chave para ficar bonita (ex: ponto_forte -> Ponto Forte)
                titulo = chave.replace("_", " ").capitalize()
                print(f"{titulo}: {valor}")
        else:
            print(f"Erro: O ID {escolha} não foi encontrado no sistema.")

    except ValueError:
        print("Erro: Por favor, digite um número de ID válido.")







