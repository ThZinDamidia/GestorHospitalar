from ultils import validar_data, log_servidor
from datetime import datetime
import json
import os
import logging

logger = logging.getLogger('gestor')

consultas_ficheiro = "consultas.json"

def guardar_consulta1():
    logger.debug("A guardar ficheiro de consultas.")
    with open(consultas_ficheiro, "w", encoding="utf-8") as consutas:
        json.dump(_consultas, consultas, indent=4, ensure_ascii=False)
    logger.debug("Ficheiro de consultas guardado.")

def carregar_consulta():
    global _consultas
    if os.path.exists(consultas_ficheiro):
        logger.debug("A carregar ficheiro de consultas.")
        with open(consultas_ficheiro, "r") as consultas:
            _consultas = json.load(consultas)
        logger.debug("Ficheiro de consultas carregado: %d registo(s).", len(_consultas))
    else:
        logger.debug("Ficheiro de consultas inexistente. A iniciar vazio.")
        consultas = {}

_consultas = {}
_contador_consultas = 1


def _gerar_id_consulta():
    global _contador_consultas
    novo_id = f"C{_contador_consultas:03d}"
    _contador_consultas += 1
    return novo_id


def _validar_datetime(dt_texto):
    """Valida formato YYYY-MM-DD HH:MM"""
    if not dt_texto:
        return False
    try:
        datetime.strptime(dt_texto, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def criar_consulta(id_medico, id_paciente, data_hora, sintomas, observacoes=""):
    """
    Cria uma nova consulta.
    data_hora: formato 'YYYY-MM-DD HH:MM'
    """
    logger.info("Tentativa de criacao de consulta: medico='%s'.", id_medico)
    carregar_consulta()
    if not id_medico or not id_medico.strip():
        log_servidor(400, "ID do medico nao pode estar vazio.")
        return 400, "ID do medico invalido."

    if not isinstance(id_paciente, int):
        log_servidor(400, "ID do paciente (NIF) deve ser um inteiro.")
        return 400, "NIF do paciente invalido."

    if not _validar_datetime(data_hora):
        log_servidor(400, "Data/hora invalida. Use YYYY-MM-DD HH:MM.")
        return 400, "Data/hora invalida. Use o formato YYYY-MM-DD HH:MM."

    if not sintomas or not sintomas.strip():
        log_servidor(400, "Sintomas nao podem estar vazios.")
        return 400, "Sintomas nao podem estar vazios."

    id_consulta = _gerar_id_consulta()

    _consultas[id_consulta] = {
        "id_medico": id_medico.strip().upper(),
        "id_paciente": id_paciente,
        "data_hora": data_hora.strip(),
        "sintomas": sintomas.strip(),
        "observacoes": observacoes.strip() if observacoes else "",
        "estado": "Agendada",   # Agendada | Realizada | Cancelada
    }

    log_servidor(201, f"Consulta '{id_consulta}' criada: medico={id_medico}, paciente NIF={id_paciente}.")
    logger.info("Consulta criada com sucesso: ID='%s', medico='%s'.", id_consulta, id_medico)
    guardar_consulta1()
    return 201, dict(_consultas[id_consulta]) | {"id_consulta": id_consulta}


def listar_consultas(filtro_medico=None, filtro_paciente=None, filtro_estado=None):
    """
    Lista consultas com filtros opcionais por médico, paciente (NIF) ou estado.
    """
    logger.info("Pedido de listagem de consultas.")
    carregar_consulta()
    if not _consultas:
        log_servidor(404, "Nenhuma consulta registada.")
        return 404, "Nenhuma consulta registada."

    resultado = {}
    for cid, dados in _consultas.items():
        if filtro_medico and dados["id_medico"] != filtro_medico.upper():
            continue
        if filtro_paciente and dados["id_paciente"] != filtro_paciente:
            continue
        if filtro_estado and dados["estado"].lower() != filtro_estado.lower():
            continue
        resultado[cid] = dict(dados)

    if not resultado:
        log_servidor(404, "Nenhuma consulta corresponde aos filtros.")
        logger.warning("Listagem sem resultados para os filtros aplicados.")
        return 404, "Nenhuma consulta encontrada com os filtros fornecidos."

    log_servidor(200, f"{len(resultado)} consulta(s) recuperada(s).")
    logger.info("Listagem concluida: %d consulta(s).", len(resultado))
    return 200, resultado


def consultar_consulta(id_consulta):
    logger.info("Pedido de detalhe da consulta ID='%s'.", id_consulta)
    carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        logger.warning("Consulta ID='%s' nao encontrada.", id_consulta)
        return 404, f"Consulta '{id_consulta}' nao encontrada."

    log_servidor(200, f"Consulta '{id_consulta}' encontrada.")
    logger.info("Consulta ID='%s' retornada.", id_consulta)
    return 200, dict(_consultas[id_consulta]) | {"id_consulta": id_consulta}


def atualizar_consulta(id_consulta, data_hora=None, sintomas=None,
                       observacoes=None, estado=None):
    logger.info("Pedido de atualizacao da consulta ID='%s'.", id_consulta)
    carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        logger.warning("Atualizacao falhada: consulta ID='%s' nao encontrada.", id_consulta)
        return 404, f"Consulta '{id_consulta}' nao encontrada."

    consulta = _consultas[id_consulta]

    if consulta["estado"] == "Cancelada":
        log_servidor(409, f"Consulta '{id_consulta}' esta cancelada e nao pode ser editada.")
        logger.warning("Atualizacao bloqueada: consulta ID='%s' ja cancelada.", id_consulta)
        return 409, "Nao e possivel editar uma consulta cancelada."

    if data_hora is not None:
        if not _validar_datetime(data_hora):
            log_servidor(400, "Data/hora invalida.")
            logger.warning("Data/hora invalida na atualizacao da consulta ID='%s'.", id_consulta)
            return 400, "Data/hora invalida. Use o formato YYYY-MM-DD HH:MM."
        consulta["data_hora"] = data_hora.strip()

    if sintomas is not None and sintomas.strip():
        consulta["sintomas"] = sintomas.strip()

    if observacoes is not None:
        consulta["observacoes"] = observacoes.strip()

    if estado is not None:
        estados_validos = ["Agendada", "Realizada", "Cancelada"]
        if estado not in estados_validos:
            log_servidor(400, f"Estado invalido. Opcoes: {estados_validos}")
            logger.warning("Estado invalido na atualizacao da consulta ID='%s'.", id_consulta)
            return 400, f"Estado invalido. Use: {', '.join(estados_validos)}"
        logger.info("Consulta ID='%s': estado alterado para '%s'.", id_consulta, estado)
        consulta["estado"] = estado

    log_servidor(200, f"Consulta '{id_consulta}' atualizada.")
    logger.info("Consulta ID='%s' atualizada com sucesso.", id_consulta)
    guardar_consulta1()
    return 200, dict(consulta) | {"id_consulta": id_consulta}


def cancelar_consulta(id_consulta):
    logger.info("Pedido de cancelamento da consulta ID='%s'.", id_consulta)
    carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        logger.warning("Cancelamento falhado: consulta ID='%s' nao encontrada.", id_consulta)
        return 404, f"Consulta '{id_consulta}' nao encontrada."

    if _consultas[id_consulta]["estado"] == "Cancelada":
        log_servidor(409, f"Consulta '{id_consulta}' ja esta cancelada.")
        logger.warning("Cancelamento ignorado: consulta ID='%s' ja estava cancelada.", id_consulta)
        return 409, "Consulta ja se encontra cancelada."

    _consultas[id_consulta]["estado"] = "Cancelada"
    log_servidor(200, f"Consulta '{id_consulta}' cancelada.")
    logger.info("Consulta ID='%s' cancelada com sucesso.", id_consulta)
    guardar_consulta1()
    return 200, dict(_consultas[id_consulta]) | {"id_consulta": id_consulta}


def remover_consulta(id_consulta):
    logger.info("Pedido de remocao da consulta ID='%s'.", id_consulta)
    carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        logger.warning("Remocao falhada: consulta ID='%s' nao encontrada.", id_consulta)
        return 404, f"Consulta '{id_consulta}' nao encontrada."
    _consultas.pop(id_consulta)
    log_servidor(200, f"Consulta '{id_consulta}' removida.")
    logger.info("Consulta ID='%s' removida com sucesso.", id_consulta)
    guardar_consulta1()
    return 200, f"Consulta '{id_consulta}' removida com sucesso."


def consulta_existe(id_consulta):
    carregar_consulta()
    logger.debug("Verificacao de existencia: consulta ID='%s'.", id_consulta)
    return id_consulta in _consultas
