from ultils import gerar_nif_valido, validar_data, log_servidor
import json
import os
_pacientes = {}
paciente_ficheiro = "paciente_ficheiro.json"
def guardar_paciente1():
    with open(paciente_ficheiro,"w", encoding="utf-8") as paciente:
        json.dump(_pacientes, paciente, indent=4, ensure_ascii=False)
def carregar_paciente():
    global _pacientes
    if os.path.exists(paciente_ficheiro):
        with open(paciente_ficheiro,"r", encoding="utf-8") as paciente:
            _pacientes = json.load(paciente)
    else:
        _pacientes = {}

def criar_paciente(nome, data_nascimento, nacionalidade, tipo_sanguineo,
                   alergias, doencas_cronicas, cirurgias_anteriores, id_medico):
    carregar_paciente()
    if not nome or not nome.strip():
        log_servidor(400, "Nome nao pode estar vazio.")
        return 400, "Nome nao pode estar vazio."

    if not validar_data(data_nascimento):
        log_servidor(400, "Data de nascimento invalida. Use YYYY-MM-DD.")
        return 400, "Data de nascimento invalida."

    if not validar_data(data_nascimento):
        log_servidor(400, "Data de nascimento invalida. Use YYYY-MM-DD.")
        return 400, "Data de nascimento invalida."

    if not isinstance(id_medico, str) or not id_medico.strip():
        log_servidor(400, "ID do medico deve ser uma string (Ex: M001).")
        return 400, "ID do medico invalido."

    while True:
        nif = gerar_nif_valido()
        if nif not in _pacientes:
            break

    _pacientes[nif] = {
        "nome": nome.strip().title(),
        "nif": nif,
        "data_nascimento": data_nascimento,
        "nacionalidade": nacionalidade,
        "tipo_sanguineo": tipo_sanguineo,
        "alergias": alergias,
        "doencas_cronicas": doencas_cronicas,
        "cirurgias_anteriores": cirurgias_anteriores,
        "id_medico": id_medico.strip(),
    }

    log_servidor(201, f"Paciente '{nome}' criado com sucesso. NIF: {nif}")
    guardar_paciente1()
    return 201, dict(_pacientes[nif])
   


def listar_pacientes():
    carregar_paciente()
    if not _pacientes:
        log_servidor(404, "Nenhum paciente registado.")
        return 404, "Nenhum paciente registado."
    log_servidor(200, "Lista de pacientes recuperada.")
    return 200, dict(_pacientes)


def consultar_paciente(nif):
    carregar_paciente()
    if nif not in _pacientes:
        log_servidor(404, f"Paciente NIF '{nif}' nao encontrado.")
        return 404, f"Paciente NIF '{nif}' nao encontrado."
    log_servidor(200, f"Paciente NIF '{nif}' encontrado.")
    return 200, dict(_pacientes[nif])


def atualizar_paciente(nif, nome=None, data_nascimento=None, nacionalidade=None,
                       tipo_sanguineo=None, alergias=None, doencas_cronicas=None,
                       cirurgias_anteriores=None, id_medico=None):
    carregar_paciente()
    if nif not in _pacientes:
        log_servidor(404, f"Paciente NIF '{nif}' nao encontrado.")
        return 404, f"Paciente NIF '{nif}' nao encontrado."

    pac = _pacientes[nif]

    if nome is not None and nome.strip():
        pac["nome"] = nome.strip().title()

    if data_nascimento is not None:
        if not validar_data(data_nascimento):
            log_servidor(400, "Data de nascimento invalida.")
            return 400, "Data de nascimento invalida."
        pac["data_nascimento"] = data_nascimento
    if nacionalidade is not None: pac["nacionalidade"] = nacionalidade
    if tipo_sanguineo is not None: pac["tipo_sanguineo"] = tipo_sanguineo
    if alergias is not None: pac["alergias"] = alergias
    if doencas_cronicas is not None: pac["doencas_cronicas"] = doencas_cronicas
    if cirurgias_anteriores is not None: pac["cirurgias_anteriores"] = cirurgias_anteriores
    if id_medico is not None: pac["id_medico"] = id_medico.strip()

    log_servidor(200, f"Paciente NIF '{nif}' atualizado com sucesso.")
    guardar_paciente1()
    return 200, dict(pac)
    


def remover_paciente(nif):
    carregar_paciente()
    if nif not in _pacientes:
        log_servidor(404, f"Paciente NIF '{nif}' nao encontrado.")
        return 404, f"Paciente NIF '{nif}' nao encontrado."
    nome = _pacientes.pop(nif)["nome"]
    log_servidor(200, f"Paciente '{nome}' (NIF: {nif}) removido.")
    guardar_paciente1()
    return 200, nome
   
