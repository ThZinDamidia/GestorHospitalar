from ultils import gerar_nif_valido, validar_data, log_servidor
import json
import os
import logging

logger = logging.getLogger('gestor')

_pacientes = {}
paciente_ficheiro = "paciente_ficheiro.json"

def guardar_paciente1():
    logger.debug("A guardar pacientes no ficheiro '%s'.", paciente_ficheiro)
    with open(paciente_ficheiro, "w", encoding="utf-8") as paciente:
        json.dump(_pacientes, paciente, indent=4, ensure_ascii=False)
    logger.debug("Pacientes guardados com sucesso.")

def carregar_paciente():
    global _pacientes
    if os.path.exists(paciente_ficheiro):
        logger.debug("A carregar pacientes do ficheiro '%s'.", paciente_ficheiro)
        with open(paciente_ficheiro, "r", encoding="utf-8") as paciente:
            _pacientes = json.load(paciente)
        logger.debug("Pacientes carregados: %d registo(s).", len(_pacientes))
    else:
        logger.debug("Ficheiro '%s' nao encontrado. A iniciar dicionario vazio.", paciente_ficheiro)
        _pacientes = {}

def criar_paciente(nome, data_nascimento, nacionalidade, tipo_sanguineo,
                   alergias, doencas_cronicas, cirurgias_anteriores, id_medico):
    logger.info("Tentativa de criacao de paciente: nome='%s', medico='%s'.", nome, id_medico)
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

    logger.debug("NIF gerado para o paciente '%s': %s.", nome, nif)

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
    logger.info("Paciente criado com sucesso: NIF=%s, nome='%s', medico='%s'.",
                nif, nome, id_medico)
    guardar_paciente1()
    return 201, dict(_pacientes[nif])


def listar_pacientes():
    logger.info("Pedido de listagem de pacientes.")
    carregar_paciente()
    if not _pacientes:
        log_servidor(404, "Nenhum paciente registado.")
        return 404, "Nenhum paciente registado."
    log_servidor(200, "Lista de pacientes recuperada.")
    logger.info("Listagem de pacientes concluida: %d paciente(s) retornado(s).", len(_pacientes))
    return 200, dict(_pacientes)


def consultar_paciente(nif):
    logger.info("Pedido de consulta do paciente NIF='%s'.", nif)
    carregar_paciente()
    if nif not in _pacientes:
        log_servidor(404, f"Paciente NIF '{nif}' nao encontrado.")
        logger.warning("Paciente NIF='%s' nao encontrado.", nif)
        return 404, f"Paciente NIF '{nif}' nao encontrado."
    log_servidor(200, f"Paciente NIF '{nif}' encontrado.")
    logger.info("Paciente NIF='%s' encontrado e retornado.", nif)
    return 200, dict(_pacientes[nif])


def atualizar_paciente(nif, nome=None, data_nascimento=None, nacionalidade=None,
                       tipo_sanguineo=None, alergias=None, doencas_cronicas=None,
                       cirurgias_anteriores=None, id_medico=None):
    logger.info("Pedido de atualizacao do paciente NIF='%s'.", nif)
    carregar_paciente()
    if nif not in _pacientes:
        log_servidor(404, f"Paciente NIF '{nif}' nao encontrado.")
        logger.warning("Atualizacao falhada: paciente NIF='%s' nao encontrado.", nif)
        return 404, f"Paciente NIF '{nif}' nao encontrado."

    pac = _pacientes[nif]

    if nome is not None and nome.strip():
        logger.debug("Paciente NIF='%s': nome alterado de '%s' para '%s'.",
                     nif, pac["nome"], nome.strip().title())
        pac["nome"] = nome.strip().title()

    if data_nascimento is not None:
        if not validar_data(data_nascimento):
            log_servidor(400, "Data de nascimento invalida.")
            logger.warning("Data de nascimento invalida na atualizacao do paciente NIF='%s'.", nif)
            return 400, "Data de nascimento invalida."
        logger.debug("Paciente NIF='%s': data_nascimento alterada para '%s'.", nif, data_nascimento)
        pac["data_nascimento"] = data_nascimento

    if nacionalidade is not None:
        logger.debug("Paciente NIF='%s': nacionalidade alterada.", nif)
        pac["nacionalidade"] = nacionalidade
    if tipo_sanguineo is not None:
        logger.debug("Paciente NIF='%s': tipo_sanguineo alterado para '%s'.", nif, tipo_sanguineo)
        pac["tipo_sanguineo"] = tipo_sanguineo
    if alergias is not None:
        logger.debug("Paciente NIF='%s': alergias atualizadas.", nif)
        pac["alergias"] = alergias
    if doencas_cronicas is not None:
        logger.debug("Paciente NIF='%s': doencas_cronicas atualizadas.", nif)
        pac["doencas_cronicas"] = doencas_cronicas
    if cirurgias_anteriores is not None:
        logger.debug("Paciente NIF='%s': cirurgias_anteriores atualizadas.", nif)
        pac["cirurgias_anteriores"] = cirurgias_anteriores
    if id_medico is not None:
        logger.debug("Paciente NIF='%s': id_medico alterado para '%s'.", nif, id_medico.strip())
        pac["id_medico"] = id_medico.strip()

    log_servidor(200, f"Paciente NIF '{nif}' atualizado com sucesso.")
    logger.info("Paciente NIF='%s' atualizado com sucesso.", nif)
    guardar_paciente1()
    return 200, dict(pac)


def remover_paciente(nif):
    logger.info("Pedido de remocao do paciente NIF='%s'.", nif)
    carregar_paciente()
    if nif not in _pacientes:
        log_servidor(404, f"Paciente NIF '{nif}' nao encontrado.")
        logger.warning("Remocao falhada: paciente NIF='%s' nao encontrado.", nif)
        return 404, f"Paciente NIF '{nif}' nao encontrado."
    nome = _pacientes.pop(nif)["nome"]
    log_servidor(200, f"Paciente '{nome}' (NIF: {nif}) removido.")
    logger.info("Paciente NIF='%s' (nome='%s') removido com sucesso.", nif, nome)
    guardar_paciente1()
    return 200, nome
