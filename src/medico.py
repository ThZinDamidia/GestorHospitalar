from ultils import gerar_id_medico, validar_data, log_servidor

medicos = {}


def adicionar_medico():
    print("\n--- Cadastro de Medico ---")
    id_do_medico = gerar_id_medico()

    # Nome
    while True:
        nome = input("Informe o nome do medico: ").title().strip()
        if nome: break
        log_servidor(400, "Erro: O nome nao pode estar vazio.")

    # Data de Nascimento
    while True:
        data_de_nascimento = input("Informe a data de nascimento (YYYY-MM-DD): ")
        if validar_data(data_de_nascimento):
            break
        log_servidor(400, "Formato de data invalida! Use YYYY-MM-DD.")

    nacionalidade = input("Informe a nacionalidade: ")
    area_de_especialidade = input("Informe a area de especialidade: ")

    # Data de Registro
    while True:
        data_de_registo = input("Informe a data de registro (YYYY-MM-DD): ")
        if validar_data(data_de_registo):
            break
        log_servidor(400, "Formato de data invalida! Use YYYY-MM-DD.")

    idiomas = input("Informe os idiomas: ")
    ponto_forte = input("Informe o ponto forte: ")
    ponto_fraco = input("Informe o ponto fraco: ")

    # ID Unidade de Saude
    while True:
        try:
            id_da_unidade_de_saude = int(input("Informe o ID da unidade de saude (numero): "))
            break
        except ValueError:
            log_servidor(400, "Erro: Digite apenas numeros para o ID da unidade.")

    horario_turno = input("Informe o horario do turno: ")
    cargo = input("Informe o cargo: ")

    # Salvando no dicionario
    medicos[id_do_medico] = {
        "nome": nome,
        "data_de_nascimento": data_de_nascimento,
        "nacionalidade": nacionalidade,
        "area_de_especialidade": area_de_especialidade,
        "data_de_registo": data_de_registo,
        "idiomas": idiomas,
        "ponto_forte": ponto_forte,
        "ponto_fraco": ponto_fraco,
        "id_da_unidade_de_saude": id_da_unidade_de_saude,
        "horario_turno": horario_turno,
        "cargo": cargo,
    }

    log_servidor(201, f"Medico {nome} cadastrado com sucesso! ID: {id_do_medico}")


def listar_nomes__dos_medicos():
    if not medicos:
        log_servidor(404, "Nao ha medicos no registro.")
        return

    log_servidor(200, "Lista de medicos recuperada.")
    print("\n--- Lista de Medicos ---")
    for id_medico, dados in medicos.items():
        print(f"ID: {id_medico} | Nome: {dados['nome']}")


def consultar_medicos():
    if not medicos:
        log_servidor(404, "O sistema esta vazio.")
        return

    try:
        escolha = int(input("\nIntroduza o ID do medico: "))
        medico_encontrado = medicos.get(escolha)

        if medico_encontrado:
            log_servidor(200, "Recurso encontrado.")
            print(f"\n--- Ficha do Medico (ID: {escolha}) ---")
            for chave, valor in medico_encontrado.items():
                titulo = chave.replace("_", " ").capitalize()
                print(f"{titulo}: {valor}")
        else:
            log_servidor(404, f"ID {escolha} nao encontrado.")
    except ValueError:
        log_servidor(400, "Entrada invalida: Digite um ID numerico.")


def atualizar_medico():
    if not medicos:
        log_servidor(404, "Nenhum medico registrado para atualizar.")
        return

    try:
        id_escolhido = int(input("\nDigite o ID do medico que deseja alterar: "))

        if id_escolhido in medicos:
            medico = medicos[id_escolhido]
            log_servidor(200, "Acesso aos campos permitido.")

            print("\nO que deseja alterar?")
            opcoes = list(medico.keys())

            for i, chave in enumerate(opcoes):
                print(f"{i + 1}. {chave.replace('_', ' ').capitalize()}")

            escolha = int(input("\nEscolha o numero do campo: ")) - 1

            if 0 <= escolha < len(opcoes):
                campo_para_alterar = opcoes[escolha]
                novo_valor = input(f"Novo valor para {campo_para_alterar}: ")

                if campo_para_alterar == "id_da_unidade_de_saude":
                    try:
                        novo_valor = int(novo_valor)
                    except ValueError:
                        log_servidor(400, "Erro: Este campo exige um numero.")
                        return

                medico[campo_para_alterar] = novo_valor
                log_servidor(200, f"Campo {campo_para_alterar} atualizado com sucesso.")
            else:
                log_servidor(400, "Opcao invalida selecionada.")
        else:
            log_servidor(404, "ID nao encontrado.")
    except ValueError:
        log_servidor(400, "Erro de digitacao: Entrada numerica esperada.")


def deletar_medico():
    if not medicos:
        log_servidor(404, "Nao ha medicos para deletar.")
        return
    try:
        id_para_deletar = int(input("\nQual ID do medico para ser deletado? "))
        if id_para_deletar in medicos:
            nome_medico = medicos[id_para_deletar]['nome']
            medicos.pop(id_para_deletar)
            log_servidor(200, f"Medico {nome_medico} (ID {id_para_deletar}) removido com sucesso.")
        else:
            log_servidor(404, "ID nao localizado.")
    except ValueError:
        log_servidor(400, "Erro: ID deve ser numerico.")
