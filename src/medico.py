from ultils import gerar_id_medico, validar_data, log_servidor

_medicos = {}


def criar_medico(nome, data_nascimento, nacionalidade, especialidade,
                 data_registo, idiomas, ponto_forte, ponto_fraco,
                 id_unidade, horario_turno, cargo):
    # Validações
    if not nome or not nome.strip():
        log_servidor(400, "Nome nao pode estar vazio.")
        return 400, "Nome nao pode estar vazio."

    if not validar_data(data_nascimento):
        log_servidor(400, "Data de nascimento invalida. Use YYYY-MM-DD.")
        return 400, "Data de nascimento invalida."

    if not validar_data(data_registo):
        log_servidor(400, "Data de registo invalida. Use YYYY-MM-DD.")
        return 400, "Data de registo invalida."

    if not isinstance(id_unidade, int):
        log_servidor(400, "ID da unidade deve ser um numero inteiro.")
        return 400, "ID da unidade invalido."

    id_medico = gerar_id_medico()

    _medicos[id_medico] = {
        "nome": nome.strip().title(),
        "data_nascimento": data_nascimento,
        "nacionalidade": nacionalidade,
        "especialidade": especialidade,
        "data_registo": data_registo,
        "idiomas": idiomas,
        "ponto_forte": ponto_forte,
        "ponto_fraco": ponto_fraco,
        "id_unidade": id_unidade,
        "horario_turno": horario_turno,
        "cargo": cargo,
    }

    log_servidor(201, f"Medico '{nome}' criado com sucesso. ID: {id_medico}")
    return 201, _medicos[id_medico]


def listar_medicos():
    if not _medicos:
        log_servidor(404, "Nenhum medico registado.")
        return 404, "Nenhum medico registado."

    log_servidor(200, "Lista de medicos recuperada.")
    return 200, dict(_medicos)


def consultar_medico(id_medico):
    if id_medico not in _medicos:
        log_servidor(404, f"Medico ID '{id_medico}' nao encontrado.")
        return 404, f"Medico '{id_medico}' nao encontrado."

    log_servidor(200, f"Medico ID '{id_medico}' encontrado.")
    return 200, dict(_medicos[id_medico])


def atualizar_medico(id_medico, nome=None, data_nascimento=None, nacionalidade=None,
                     especialidade=None, data_registo=None, idiomas=None,
                     ponto_forte=None, ponto_fraco=None, id_unidade=None,
                     horario_turno=None, cargo=None):
    if id_medico not in _medicos:
        log_servidor(404, f"Medico ID '{id_medico}' nao encontrado.")
        return 404, f"Medico '{id_medico}' nao encontrado."

    medico = _medicos[id_medico]

    if nome is not None:
        medico["nome"] = nome.strip().title()
    if data_nascimento is not None:
        if not validar_data(data_nascimento):
            log_servidor(400, "Data de nascimento invalida.")
            return 400, "Data de nascimento invalida."
        medico["data_nascimento"] = data_nascimento
    if nacionalidade is not None:
        medico["nacionalidade"] = nacionalidade
    if especialidade is not None:
        medico["especialidade"] = especialidade
    if data_registo is not None:
        if not validar_data(data_registo):
            log_servidor(400, "Data de registo invalida.")
            return 400, "Data de registo invalida."
        medico["data_registo"] = data_registo
    if idiomas is not None:
        medico["idiomas"] = idiomas
    if ponto_forte is not None:
        medico["ponto_forte"] = ponto_forte
    if ponto_fraco is not None:
        medico["ponto_fraco"] = ponto_fraco
    if id_unidade is not None:
        medico["id_unidade"] = id_unidade
    if horario_turno is not None:
        medico["horario_turno"] = horario_turno
    if cargo is not None:
        medico["cargo"] = cargo

    log_servidor(200, f"Medico ID '{id_medico}' atualizado com sucesso.")
    return 200, dict(medico)


def remover_medico(id_medico):
    if id_medico not in _medicos:
        log_servidor(404, f"Medico ID '{id_medico}' nao encontrado.")
        return 404, f"Medico '{id_medico}' nao encontrado."

    nome = _medicos.pop(id_medico)["nome"]
    log_servidor(200, f"Medico '{nome}' (ID: {id_medico}) removido.")
    return 200, nome


def medico_existe(id_medico):
    """Utilitário para outros módulos verificarem sem acoplar lógica."""
    return id_medico in _medicos
