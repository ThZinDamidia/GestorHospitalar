from ultils import gerar_id_medico, validar_data, log_servidor
from unidade import unidade_existe, verificar_capacidade, incrementar_medicos, decrementar_medicos
import os
import json
_medicos = {}

medico_ficheiro = "medico_ficheiro.json"
def carregar_medico():
    with open(medico_ficheiro, "w", encoding="utf-8") as consultas:
        json.dump(_medicos,medico_ficheiro, indent=4, ensure_ascii=False)

def guardar_medico():
    global _medicos
    if os.path.exists():
        with open(medico_ficheiro, "r", encoding="utf-8") as medico:
            ficheiro = json.load(medicos)
    else:
        medicos = {}



def criar_medico(nome, data_nascimento, nacionalidade, especialidade,
                 data_registo, idiomas, ponto_forte, ponto_fraco,
                 id_unidade, horario_turno, cargo):
    carregar_medico()
    if not nome or not nome.strip():
        log_servidor(400, "Nome nao pode estar vazio.")
        return 400, "Nome nao pode estar vazio."

    if not validar_data(data_nascimento):
        log_servidor(400, "Data de nascimento invalida. Use YYYY-MM-DD.")
        return 400, "Data de nascimento invalida."

    if not validar_data(data_registo):
        log_servidor(400, "Data de registo invalida. Use YYYY-MM-DD.")
        return 400, "Data de registo invalida."

    if not isinstance(id_unidade, str) or not id_unidade.strip():
        log_servidor(400, "ID da unidade deve ser uma string (Ex: U001).")
        return 400, "ID da unidade invalido."

    id_unidade = id_unidade.strip().upper()

    if not unidade_existe(id_unidade):
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        return 404, f"Unidade '{id_unidade}' nao encontrada. Registe a unidade primeiro."

    if not verificar_capacidade(id_unidade):
        log_servidor(403, f"Unidade '{id_unidade}' atingiu a capacidade maxima.")
        return 403, f"Erro 403: Capacidade maxima da unidade '{id_unidade}' atingida."

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

    incrementar_medicos(id_unidade)

    log_servidor(201, f"Medico '{nome}' criado com sucesso. ID: {id_medico}")
    return 201, dict(_medicos[id_medico]) | {"id_medico": id_medico}
    guardar_medico()

def listar_medicos():
    carregar_medico()
    if not _medicos:
        log_servidor(404, "Nenhum medico registado.")
        return 404, "Nenhum medico registado."

    log_servidor(200, "Lista de medicos recuperada.")
    return 200, dict(_medicos)

def consultar_medico(id_medico):
    carregar_medico()
    if id_medico not in _medicos:
        log_servidor(404, f"Medico ID '{id_medico}' nao encontrado.")
        return 404, f"Medico '{id_medico}' nao encontrado."

    log_servidor(200, f"Medico ID '{id_medico}' encontrado.")
    return 200, dict(_medicos[id_medico])

def atualizar_medico(id_medico, nome=None, data_nascimento=None, nacionalidade=None,
                     especialidade=None, data_registo=None, idiomas=None,
                     ponto_forte=None, ponto_fraco=None, id_unidade=None,
                     horario_turno=None, cargo=None):
    carregar_medico()
    if id_medico not in _medicos:
        log_servidor(404, f"Medico ID '{id_medico}' nao encontrado.")
        return 404, f"Medico '{id_medico}' nao encontrado."

    medico = _medicos[id_medico]

    if nome is not None and nome.strip():
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
        id_unidade_novo = id_unidade.strip().upper()
        if not unidade_existe(id_unidade_novo):
            log_servidor(404, f"Unidade '{id_unidade_novo}' nao encontrada.")
            return 404, f"Unidade '{id_unidade_novo}' nao encontrada."
        if not verificar_capacidade(id_unidade_novo):
            log_servidor(403, f"Unidade '{id_unidade_novo}' atingiu a capacidade maxima.")
            return 403, f"Erro 403: Capacidade maxima da unidade '{id_unidade_novo}' atingida."
        # Atualizar contadores
        decrementar_medicos(medico["id_unidade"])
        incrementar_medicos(id_unidade_novo)
        medico["id_unidade"] = id_unidade_novo

    if horario_turno is not None:
        medico["horario_turno"] = horario_turno
    if cargo is not None:
        medico["cargo"] = cargo

    log_servidor(200, f"Medico ID '{id_medico}' atualizado com sucesso.")
    return 200, dict(medico)
    guardar_medico()

def remover_medico(id_medico):
    carregar_medico()
    if id_medico not in _medicos:
        log_servidor(404, f"Medico ID '{id_medico}' nao encontrado.")
        return 404, f"Medico '{id_medico}' nao encontrado."

    id_unidade = _medicos[id_medico]["id_unidade"]
    nome = _medicos.pop(id_medico)["nome"]
    decrementar_medicos(id_unidade)

    log_servidor(200, f"Medico '{nome}' (ID: {id_medico}) removido.")
    return 200, nome
    guardar_medico()

def medico_existe(id_medico):
    carregar_medico()
    return id_medico in _medicos