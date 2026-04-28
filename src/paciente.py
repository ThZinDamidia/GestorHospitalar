# ==============================
# medico.py
# CRUD de Médicos com integridade referencial
# ==============================

from utils import (
    gerar_id_medico,
    validar_nome, validar_data, validar_data_passada,
    normalizar_nome, log_servidor,
)
from departamento import (
    departamento_existe,
    obter_especialidades_departamento,
    _alocar_medico,
    _desalocar_medico,
)

_medicos: dict = {}

CARGOS_VALIDOS = {
    "Médico Residente", "Médico Especialista", "Médico Chefe",
    "Diretor de Departamento", "Médico Consultor",
}


# ─── HELPERS PÚBLICOS ────────────────────────

def medico_existe(id_med: str) -> bool:
    return id_med in _medicos


def obter_especialidade_medico(id_med: str) -> str | None:
    if id_med not in _medicos:
        return None
    return _medicos[id_med]["especialidade"]


def obter_departamento_medico(id_med: str) -> str | None:
    if id_med not in _medicos:
        return None
    return _medicos[id_med]["id_departamento"]


def medico_tem_consultas_ativas(id_med: str) -> bool:
    """Verificado por consulta.py para integridade referencial."""
    from consulta import _consultas
    return any(
        c["medico_id"] == id_med and c["status"] == "Agendada"
        for c in _consultas.values()
    )


def medico_tem_internamentos_ativos(id_med: str) -> bool:
    """Verificado por internamento.py para integridade referencial."""
    from internamento import _internamentos
    return any(
        i["medico_id"] == id_med and i["status"] == "Ativo"
        for i in _internamentos.values()
    )


# ─── CRIAR ────────────────────────────────────

def criar_medico(nome: str, data_nascimento: str, nacionalidade: str,
                 especialidade: str, data_registo: str, idiomas: str,
                 ponto_forte: str, ponto_fraco: str,
                 id_departamento: str, horario_turno: str, cargo: str) -> tuple:
    """
    Cria um médico e aloca-o ao departamento indicado.

    Regras de negócio:
      - O departamento deve existir.
      - A especialidade do médico deve constar nas especialidades do departamento.
      - O cargo deve ser um dos valores permitidos.
    """
    # — Validações básicas —
    ok, erro = validar_nome(nome)
    if not ok:
        log_servidor(400, erro)
        return 400, erro

    if not validar_data_passada(data_nascimento):
        msg = "Data de nascimento inválida ou no futuro. Use YYYY-MM-DD."
        log_servidor(400, msg)
        return 400, msg

    if not validar_data_passada(data_registo):
        msg = "Data de registo inválida ou no futuro. Use YYYY-MM-DD."
        log_servidor(400, msg)
        return 400, msg

    if not nacionalidade or not nacionalidade.strip():
        msg = "Nacionalidade é obrigatória."
        log_servidor(400, msg)
        return 400, msg

    if not especialidade or not especialidade.strip():
        msg = "Especialidade é obrigatória."
        log_servidor(400, msg)
        return 400, msg

    if not horario_turno or not horario_turno.strip():
        msg = "Horário do turno é obrigatório."
        log_servidor(400, msg)
        return 400, msg

    cargo_norm = cargo.strip().title() if cargo else ""
    if cargo_norm not in CARGOS_VALIDOS:
        msg = f"Cargo inválido. Valores permitidos: {', '.join(sorted(CARGOS_VALIDOS))}."
        log_servidor(400, msg)
        return 400, msg

    # — Validações relacionais —
    if not departamento_existe(id_departamento):
        msg = f"Departamento '{id_departamento}' não encontrado. Crie o departamento primeiro."
        log_servidor(404, msg)
        return 404, msg

    especialidade_norm = especialidade.strip().title()
    especialidades_dep = obter_especialidades_departamento(id_departamento)
    if especialidade_norm not in especialidades_dep:
        msg = (f"A especialidade '{especialidade_norm}' não pertence ao departamento "
               f"'{id_departamento}' (especialidades: {', '.join(especialidades_dep)}).")
        log_servidor(400, msg)
        return 400, msg

    # — Criação —
    id_med = gerar_id_medico()
    _medicos[id_med] = {
        "id": id_med,
        "nome": normalizar_nome(nome),
        "data_nascimento": data_nascimento,
        "nacionalidade": nacionalidade.strip().title(),
        "especialidade": especialidade_norm,
        "data_registo": data_registo,
        "idiomas": idiomas.strip() if idiomas else "",
        "ponto_forte": ponto_forte.strip() if ponto_forte else "",
        "ponto_fraco": ponto_fraco.strip() if ponto_fraco else "",
        "id_departamento": id_departamento,
        "horario_turno": horario_turno.strip(),
        "cargo": cargo_norm,
        "ativo": True,
        "criado_em": _agora(),
        "atualizado_em": _agora(),
    }

    _alocar_medico(id_departamento, id_med)
    log_servidor(201, f"Médico '{normalizar_nome(nome)}' criado. ID: {id_med}")
    return 201, dict(_medicos[id_med])


# ─── LISTAR ───────────────────────────────────

def listar_medicos() -> tuple:
    if not _medicos:
        log_servidor(404, "Nenhum médico registado.")
        return 404, "Nenhum médico registado."
    log_servidor(200, "Lista de médicos recuperada.")
    return 200, {k: dict(v) for k, v in _medicos.items()}


# ─── CONSULTAR ────────────────────────────────

def consultar_medico(id_med: str) -> tuple:
    if id_med not in _medicos:
        msg = f"Médico '{id_med}' não encontrado."
        log_servidor(404, msg)
        return 404, msg
    log_servidor(200, f"Médico '{id_med}' consultado.")
    return 200, dict(_medicos[id_med])


# ─── ATUALIZAR ────────────────────────────────

def atualizar_medico(id_med: str, nome: str = None, data_nascimento: str = None,
                     nacionalidade: str = None, especialidade: str = None,
                     data_registo: str = None, idiomas: str = None,
                     ponto_forte: str = None, ponto_fraco: str = None,
                     id_departamento: str = None, horario_turno: str = None,
                     cargo: str = None) -> tuple:
    if id_med not in _medicos:
        msg = f"Médico '{id_med}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    med = _medicos[id_med]

    if nome is not None:
        ok, erro = validar_nome(nome)
        if not ok:
            log_servidor(400, erro)
            return 400, erro
        med["nome"] = normalizar_nome(nome)

    if data_nascimento is not None:
        if not validar_data_passada(data_nascimento):
            msg = "Data de nascimento inválida ou no futuro."
            log_servidor(400, msg)
            return 400, msg
        med["data_nascimento"] = data_nascimento

    if data_registo is not None:
        if not validar_data_passada(data_registo):
            msg = "Data de registo inválida ou no futuro."
            log_servidor(400, msg)
            return 400, msg
        med["data_registo"] = data_registo

    if nacionalidade is not None:
        med["nacionalidade"] = nacionalidade.strip().title()

    # Mudança de especialidade/departamento — validação cruzada
    novo_dep = id_departamento if id_departamento is not None else med["id_departamento"]
    nova_esp = especialidade.strip().title() if especialidade is not None else med["especialidade"]

    if id_departamento is not None or especialidade is not None:
        if not departamento_existe(novo_dep):
            msg = f"Departamento '{novo_dep}' não encontrado."
            log_servidor(404, msg)
            return 404, msg
        especialidades_dep = obter_especialidades_departamento(novo_dep)
        if nova_esp not in especialidades_dep:
            msg = (f"A especialidade '{nova_esp}' não pertence ao departamento "
                   f"'{novo_dep}' (especialidades: {', '.join(especialidades_dep)}).")
            log_servidor(400, msg)
            return 400, msg
        # Realocação
        if id_departamento is not None and id_departamento != med["id_departamento"]:
            _desalocar_medico(med["id_departamento"], id_med)
            _alocar_medico(novo_dep, id_med)
            med["id_departamento"] = novo_dep
        med["especialidade"] = nova_esp

    if idiomas is not None:
        med["idiomas"] = idiomas.strip()
    if ponto_forte is not None:
        med["ponto_forte"] = ponto_forte.strip()
    if ponto_fraco is not None:
        med["ponto_fraco"] = ponto_fraco.strip()
    if horario_turno is not None:
        med["horario_turno"] = horario_turno.strip()

    if cargo is not None:
        cargo_norm = cargo.strip().title()
        if cargo_norm not in CARGOS_VALIDOS:
            msg = f"Cargo inválido. Valores permitidos: {', '.join(sorted(CARGOS_VALIDOS))}."
            log_servidor(400, msg)
            return 400, msg
        med["cargo"] = cargo_norm

    med["atualizado_em"] = _agora()
    log_servidor(200, f"Médico '{id_med}' atualizado.")
    return 200, dict(med)


# ─── REMOVER ──────────────────────────────────

def remover_medico(id_med: str) -> tuple:
    if id_med not in _medicos:
        msg = f"Médico '{id_med}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    # Integridade referencial
    if medico_tem_consultas_ativas(id_med):
        msg = (f"Não é possível remover o médico '{id_med}': "
               "tem consultas com status 'Agendada'. Cancele-as primeiro.")
        log_servidor(409, msg)
        return 409, msg

    if medico_tem_internamentos_ativos(id_med):
        msg = (f"Não é possível remover o médico '{id_med}': "
               "tem internamentos ativos. Transfira os doentes primeiro.")
        log_servidor(409, msg)
        return 409, msg

    med = _medicos.pop(id_med)
    _desalocar_medico(med["id_departamento"], id_med)
    log_servidor(200, f"Médico '{med['nome']}' (ID: {id_med}) removido.")
    return 200, f"Médico '{med['nome']}' removido com sucesso."


# ─── UTILITÁRIO PRIVADO ───────────────────────

def _agora() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
