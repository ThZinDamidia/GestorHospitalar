# ==============================
# consulta.py
# CRUD de Consultas com regras de negócio
# ==============================

from utils import (
    gerar_id_consulta,
    validar_data, validar_hora, validar_data_futura,
    combinar_data_hora, parsear_data_hora,
    STATUS_CONSULTA, log_servidor,
)
from medico import medico_existe, obter_especialidade_medico, obter_departamento_medico
from paciente import paciente_existe
from departamento import obter_especialidades_departamento

_consultas: dict = {}


# ─── HELPERS PÚBLICOS ────────────────────────

def consulta_existe(id_con: str) -> bool:
    return id_con in _consultas


def paciente_tem_consulta_no_horario(id_pac: str, data: str, hora: str,
                                      excluir_id: str = None) -> bool:
    """Verifica se o paciente já tem consulta marcada nesse exato dia e hora."""
    dh = combinar_data_hora(data, hora)
    return any(
        c["paciente_id"] == id_pac
        and c["data_hora"] == dh
        and c["status"] == "Agendada"
        and c["id"] != excluir_id
        for c in _consultas.values()
    )


def medico_tem_consulta_no_horario(id_med: str, data: str, hora: str,
                                    excluir_id: str = None) -> bool:
    """Verifica se o médico já tem outra consulta nesse exato horário."""
    dh = combinar_data_hora(data, hora)
    return any(
        c["medico_id"] == id_med
        and c["data_hora"] == dh
        and c["status"] == "Agendada"
        and c["id"] != excluir_id
        for c in _consultas.values()
    )


# ─── CRIAR ────────────────────────────────────

def agendar_consulta(id_paciente: str, id_medico: str, id_departamento: str,
                     data: str, hora: str, motivo: str) -> tuple:
    """
    Agenda uma consulta com validações completas.

    Regras de negócio:
      - Paciente e médico devem existir.
      - O médico deve pertencer ao departamento indicado.
      - A especialidade do médico deve estar nas especialidades do departamento.
      - A data deve ser hoje ou futura.
      - Nem o paciente nem o médico podem ter outra consulta agendada no mesmo horário.
      - Um paciente internado não pode marcar consulta no mesmo horário do internamento
        (verificado pelo status do internamento).
      - O motivo é obrigatório.
    """
    # — Existência —
    if not paciente_existe(id_paciente):
        msg = f"Paciente '{id_paciente}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    if not medico_existe(id_medico):
        msg = f"Médico '{id_medico}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    # — Data e hora —
    if not validar_data_futura(data):
        msg = "Data inválida ou no passado. Use YYYY-MM-DD e uma data atual ou futura."
        log_servidor(400, msg)
        return 400, msg

    if not validar_hora(hora):
        msg = "Hora inválida. Use formato HH:MM."
        log_servidor(400, msg)
        return 400, msg

    # — Motivo —
    if not motivo or not motivo.strip():
        msg = "Motivo da consulta é obrigatório."
        log_servidor(400, msg)
        return 400, msg

    # — Relação médico ↔ departamento —
    dep_medico = obter_departamento_medico(id_medico)
    if dep_medico != id_departamento:
        msg = (f"O médico '{id_medico}' pertence ao departamento '{dep_medico}', "
               f"não a '{id_departamento}'.")
        log_servidor(400, msg)
        return 400, msg

    # — Especialidade do médico no departamento —
    esp_medico = obter_especialidade_medico(id_medico)
    especialidades_dep = obter_especialidades_departamento(id_departamento)
    if esp_medico not in especialidades_dep:
        msg = (f"A especialidade '{esp_medico}' do médico não está disponível "
               f"no departamento '{id_departamento}'.")
        log_servidor(400, msg)
        return 400, msg

    # — Conflito de horário: paciente —
    if paciente_tem_consulta_no_horario(id_paciente, data, hora):
        msg = f"O paciente '{id_paciente}' já tem uma consulta agendada para {data} às {hora}."
        log_servidor(409, msg)
        return 409, msg

    # — Conflito de horário: médico —
    if medico_tem_consulta_no_horario(id_medico, data, hora):
        msg = f"O médico '{id_medico}' já tem uma consulta agendada para {data} às {hora}."
        log_servidor(409, msg)
        return 409, msg

    # — Paciente internado no mesmo horário —
    _verificar_conflito_internamento(id_paciente, data, hora)

    id_con = gerar_id_consulta()
    _consultas[id_con] = {
        "id": id_con,
        "paciente_id": id_paciente,
        "medico_id": id_medico,
        "departamento_id": id_departamento,
        "data_hora": combinar_data_hora(data, hora),
        "motivo": motivo.strip(),
        "status": "Agendada",
        "notas_clinicas": "",
        "criado_em": _agora(),
        "atualizado_em": _agora(),
    }

    log_servidor(201, f"Consulta {id_con} agendada para {data} às {hora}.")
    return 201, dict(_consultas[id_con])


def _verificar_conflito_internamento(id_pac: str, data: str, hora: str) -> None:
    """Aviso (não bloqueante) se o paciente estiver internado nessa data."""
    try:
        from internamento import _internamentos
        for i in _internamentos.values():
            if i["paciente_id"] == id_pac and i["status"] == "Ativo":
                print(f"  ⚠️  AVISO: Paciente '{id_pac}' está atualmente internado. "
                      "A consulta foi agendada mas verifique se é necessária.")
                break
    except ImportError:
        pass


# ─── LISTAR ───────────────────────────────────

def listar_consultas(filtro_paciente: str = None, filtro_medico: str = None,
                     filtro_status: str = None) -> tuple:
    resultado = dict(_consultas)

    if filtro_paciente:
        resultado = {k: v for k, v in resultado.items()
                     if v["paciente_id"] == filtro_paciente}
    if filtro_medico:
        resultado = {k: v for k, v in resultado.items()
                     if v["medico_id"] == filtro_medico}
    if filtro_status:
        status_norm = filtro_status.strip().title()
        resultado = {k: v for k, v in resultado.items()
                     if v["status"] == status_norm}

    if not resultado:
        log_servidor(404, "Nenhuma consulta encontrada com os filtros indicados.")
        return 404, "Nenhuma consulta encontrada."

    log_servidor(200, f"{len(resultado)} consulta(s) recuperada(s).")
    return 200, resultado


# ─── CONSULTAR ────────────────────────────────

def consultar_consulta(id_con: str) -> tuple:
    if id_con not in _consultas:
        msg = f"Consulta '{id_con}' não encontrada."
        log_servidor(404, msg)
        return 404, msg
    log_servidor(200, f"Consulta '{id_con}' consultada.")
    return 200, dict(_consultas[id_con])


# ─── ATUALIZAR STATUS ─────────────────────────

def atualizar_status_consulta(id_con: str, novo_status: str,
                               notas_clinicas: str = None) -> tuple:
    """
    Transições de status permitidas:
      Agendada  → Concluida | Cancelada
      Concluida → (imutável)
      Cancelada → (imutável)
    """
    if id_con not in _consultas:
        msg = f"Consulta '{id_con}' não encontrada."
        log_servidor(404, msg)
        return 404, msg

    con = _consultas[id_con]
    status_norm = novo_status.strip().title() if novo_status else ""

    if status_norm not in STATUS_CONSULTA:
        msg = f"Status inválido. Valores permitidos: {', '.join(STATUS_CONSULTA)}."
        log_servidor(400, msg)
        return 400, msg

    status_atual = con["status"]
    if status_atual in ("Concluida", "Cancelada"):
        msg = f"A consulta já está '{status_atual}' e não pode ser alterada."
        log_servidor(409, msg)
        return 409, msg

    if status_norm == "Agendada":
        msg = "Não é possível reverter o status para 'Agendada'."
        log_servidor(400, msg)
        return 400, msg

    con["status"] = status_norm
    if notas_clinicas is not None:
        con["notas_clinicas"] = notas_clinicas.strip()
    con["atualizado_em"] = _agora()

    log_servidor(200, f"Consulta '{id_con}' marcada como '{status_norm}'.")
    return 200, dict(con)


# ─── REMOVER ──────────────────────────────────

def cancelar_consulta(id_con: str, motivo_cancelamento: str = "") -> tuple:
    """Cancela uma consulta agendada (não apaga — altera status)."""
    if id_con not in _consultas:
        msg = f"Consulta '{id_con}' não encontrada."
        log_servidor(404, msg)
        return 404, msg

    con = _consultas[id_con]
    if con["status"] != "Agendada":
        msg = f"Só é possível cancelar consultas 'Agendadas'. Status atual: '{con['status']}'."
        log_servidor(409, msg)
        return 409, msg

    con["status"] = "Cancelada"
    if motivo_cancelamento:
        con["notas_clinicas"] = f"[Cancelada] {motivo_cancelamento.strip()}"
    con["atualizado_em"] = _agora()

    log_servidor(200, f"Consulta '{id_con}' cancelada.")
    return 200, dict(con)


# ─── UTILITÁRIO PRIVADO ───────────────────────

def _agora() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
