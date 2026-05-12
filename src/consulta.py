from ultils import validar_data, log_servidor
from datetime import datetime
import json
import os

consultas_ficheiro = "consultas.json"
def guardar_consulta1():
    with open(consultas_ficheiro,"w",encoding="utf-8") as consutas:
        json.dump(_consultas, consultas, indent=4, ensure_ascii=False)

def carregar_consulta():
    global _consultas
    if os.path.exists(consultas_ficheiro):
        with open(consultas_ficheiro,"r") as consultas:
            _consultas = json.load(consultas)
    else:
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
     guardar_consulta1()
    return 201, dict(_consultas[id_consulta]) | {"id_consulta": id_consulta}



def listar_consultas(filtro_medico=None, filtro_paciente=None, filtro_estado=None):
    """
    Lista consultas com filtros opcionais por médico, paciente (NIF) ou estado.
    """
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
        return 404, "Nenhuma consulta encontrada com os filtros fornecidos."

    log_servidor(200, f"{len(resultado)} consulta(s) recuperada(s).")
    return 200, resultado


def consultar_consulta(id_consulta):
     carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        return 404, f"Consulta '{id_consulta}' nao encontrada."

    log_servidor(200, f"Consulta '{id_consulta}' encontrada.")
    return 200, dict(_consultas[id_consulta]) | {"id_consulta": id_consulta}
   

def atualizar_consulta(id_consulta, data_hora=None, sintomas=None,
                       observacoes=None, estado=None):
    carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        return 404, f"Consulta '{id_consulta}' nao encontrada."

    consulta = _consultas[id_consulta]

    if consulta["estado"] == "Cancelada":
        log_servidor(409, f"Consulta '{id_consulta}' esta cancelada e nao pode ser editada.")
        return 409, "Nao e possivel editar uma consulta cancelada."

    if data_hora is not None:
        if not _validar_datetime(data_hora):
            log_servidor(400, "Data/hora invalida.")
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
            return 400, f"Estado invalido. Use: {', '.join(estados_validos)}"
        consulta["estado"] = estado

    log_servidor(200, f"Consulta '{id_consulta}' atualizada.")
     guardar_consulta1()
    return 200, dict(consulta) | {"id_consulta": id_consulta}
    


def cancelar_consulta(id_consulta):
     carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        return 404, f"Consulta '{id_consulta}' nao encontrada."

    if _consultas[id_consulta]["estado"] == "Cancelada":
        log_servidor(409, f"Consulta '{id_consulta}' ja esta cancelada.")
        return 409, "Consulta ja se encontra cancelada."

    _consultas[id_consulta]["estado"] = "Cancelada"
    log_servidor(200, f"Consulta '{id_consulta}' cancelada.")
    guardar_consulta1()
    return 200, dict(_consultas[id_consulta]) | {"id_consulta": id_consulta}
   


def remover_consulta(id_consulta):
    carregar_consulta()
    if id_consulta not in _consultas:
        log_servidor(404, f"Consulta '{id_consulta}' nao encontrada.")
        return 404, f"Consulta '{id_consulta}' nao encontrada."
    _consultas.pop(id_consulta)
    log_servidor(200, f"Consulta '{id_consulta}' removida.")
     guardar_consulta1()
    return 200, f"Consulta '{id_consulta}' removida com sucesso."
    

def consulta_existe(id_consulta):
    guardar_consulta1()
    return id_consulta in _consultas
