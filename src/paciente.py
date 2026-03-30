from ultils import gerar_nif_valido, log_servidor

paciente = {}


def adicionar_paciente():
    print("\n--- Cadastro de Paciente ---")

    # 1. Nome
    while True:
        nome = input("Digite o nome do paciente: ").title().strip()
        if nome: break
        log_servidor(400, "Erro: O nome nao pode estar vazio.")

    # 2. NIF (Gerado automaticamente)
    while True:
        nif = gerar_nif_valido()
        if nif not in paciente:
            break

    print(f"NIF gerado automaticamente pelo sistema: {nif}")

    # 3. Data de Nascimento
    data_de_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")

    # 4. Dados Complementares
    nacionalidade = input("Digite a nacionalidade: ")
    tipo_sanguinio = input("Digite o tipo sanguineo: ")
    alergias = input("Digite as alergias: ")
    doencas_cronicas = input("Digite as doencas cronicas: ")
    cirurgias_anteriores = input("Digite as cirurgias anteriores: ")

    # 5. Medico Atual
    while True:
        try:
            medico_atual = int(input("Digite o ID do medico atual: "))
            break
        except ValueError:
            log_servidor(400, "Erro: O ID do medico deve ser um numero.")

    # Salvando no dicionario
    paciente[nif] = {
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
    log_servidor(201, f"Paciente {nome} criado com sucesso no servidor.")


def listar_pacientes():
    if not paciente:
        log_servidor(404, "Nao ha pacientes no registro.")
        return

    log_servidor(200, "Lista de pacientes recuperada.")
    print("\n--- Lista de Pacientes (NIFs) ---")
    for nif, dados in paciente.items():
        print(f"NIF: {nif} | Nome: {dados['nome']}")


def consultar_paciente():
    if not paciente:
        log_servidor(404, "O sistema esta vazio.")
        return
    try:
        escolha = int(input("\nIntroduza o NIF do paciente que deseja consultar: "))
        paciente_encontrado = paciente.get(escolha)

        if paciente_encontrado:
            log_servidor(200, "Recurso encontrado.")
            print(f"\n--- Ficha do Paciente (NIF: {escolha}) ---")
            for chave, valor in paciente_encontrado.items():
                titulo = chave.replace("_", " ").capitalize()
                print(f"{titulo}: {valor}")
        else:
            log_servidor(404, f"O NIF {escolha} nao foi encontrado.")
    except ValueError:
        log_servidor(400, "Bad Request: Digite um NIF numerico valido.")


def atualizar_paciente():
    if not paciente:
        log_servidor(404, "Nao ha pacientes para atualizar.")
        return

    try:
        nif_escolha = int(input("\nDigite o NIF do paciente que deseja alterar: "))

        if nif_escolha in paciente:
            dados_paciente = paciente[nif_escolha]
            log_servidor(200, "Acesso aos dados permitido.")

            opcoes = list(dados_paciente.keys())
            for i, chave in enumerate(opcoes):
                print(f"{i + 1}. {chave.replace('_', ' ').capitalize()}")

            escolha = int(input("\nEscolha o numero do campo: ")) - 1

            if 0 <= escolha < len(opcoes):
                campo_para_alterar = opcoes[escolha]
                novo_valor = input(f"Novo valor para {campo_para_alterar}: ")

                if campo_para_alterar in ["nif", "medico_atual"]:
                    try:
                        novo_valor = int(novo_valor)
                    except ValueError:
                        log_servidor(400, "Erro: Este campo exige um formato numerico.")
                        return

                dados_paciente[campo_para_alterar] = novo_valor
                log_servidor(200, f"Sucesso: {campo_para_alterar} atualizado.")
            else:
                log_servidor(400, "Opcao invalida.")
        else:
            log_servidor(404, "NIF nao encontrado.")
    except ValueError:
        log_servidor(400, "Erro de digitacao: Entrada numerica esperada.")


def deletar_paciente():
    if not paciente:
        log_servidor(404, "Base de dados vazia.")
        return
    try:
        nif_deletar = int(input("\nDigite o NIF do paciente para deletar: "))
        if nif_deletar in paciente:
            nome_p = paciente[nif_deletar]['nome']
            paciente.pop(nif_deletar)
            log_servidor(200, f"Paciente {nome_p} removido do sistema.")
        else:
            log_servidor(404, "NIF nao localizado.")
    except ValueError:
        log_servidor(400, "Bad Request: NIF deve ser numerico.")
