# ==============================
# hospital.py
# CRUD de Hospitais (serviços/alas hospitalares)
# ==============================

from utils import gerar_id_hospital, validar_nome, normalizar_nome, log_servidor
from datetime import datetime

_hospitais: dict = {}


# ─── HELPERS INTERNOS ────────────────────────

def _hos_existe(id_hos: str) -> bool:
    return id_hos in _hospitais

def hospital_existe(id_hos: str) -> bool:
    return _hos_existe(id_hos)

def obter_especialidades_hospital(id_hos: str) -> list:
    if not _hos_existe(id_hos):
        return []
    return list(_hospitais[id_hos]["especialidades"])

def _alocar_medico(id_hos: str, id_med: str) -> None:
    if _hos_existe(id_hos) and id_med not in _hospitais[id_hos]["medicos"]:
        _hospitais[id_hos]["medicos"].append(id_med)

def _desalocar_medico(id_hos: str, id_med: str) -> None:
    if _hos_existe(id_hos):
        _hospitais[id_hos]["medicos"] = [
            m for m in _hospitais[id_hos]["medicos"] if m != id_med
        ]

def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ─── CRIAR ────────────────────────────────────

def criar_hospital(nome: str, especialidades: list, descricao: str = "") -> tuple:
    ok, erro = validar_nome(nome)
    if not ok:
        log_servidor(400, erro)
        return 400, erro

    if not especialidades or not isinstance(especialidades, list):
        msg = "É necessário fornecer pelo menos uma especialidade."
        log_servidor(400, msg)
        return 400, msg

    especialidades_norm = [e.strip().title() for e in especialidades if e.strip()]
    if not especialidades_norm:
        msg = "Especialidades não podem ser strings vazias."
        log_servidor(400, msg)
        return 400, msg

    nome_norm = normalizar_nome(nome)
    for hos in _hospitais.values():
        if hos["nome"] == nome_norm:
            msg = f"Já existe um hospital/serviço com o nome '{nome_norm}'."
            log_servidor(409, msg)
            return 409, msg

    id_hos = gerar_id_hospital()
    _hospitais[id_hos] = {
        "id": id_hos,
        "nome": nome_norm,
        "especialidades": especialidades_norm,
        "descricao": descricao.strip(),
        "medicos": [],
        "criado_em": _agora(),
    }

    log_servidor(201, f"Hospital/Serviço '{nome_norm}' criado. ID: {id_hos}")
    return 201, dict(_hospitais[id_hos])


# ─── LISTAR ───────────────────────────────────

def listar_hospitais() -> tuple:
    if not _hospitais:
        log_servidor(404, "Nenhum hospital/serviço registado.")
        return 404, "Nenhum hospital/serviço registado."
    log_servidor(200, "Lista de hospitais recuperada.")
    return 200, {k: dict(v) for k, v in _hospitais.items()}


# ─── CONSULTAR ────────────────────────────────

def consultar_hospital(id_hos: str) -> tuple:
    if not _hos_existe(id_hos):
        msg = f"Hospital/Serviço '{id_hos}' não encontrado."
        log_servidor(404, msg)
        return 404, msg
    log_servidor(200, f"Hospital/Serviço '{id_hos}' consultado.")
    return 200, dict(_hospitais[id_hos])


# ─── ATUALIZAR ────────────────────────────────

def atualizar_hospital(id_hos: str, nome: str = None,
                       especialidades: list = None,
                       descricao: str = None) -> tuple:
    if not _hos_existe(id_hos):
        msg = f"Hospital/Serviço '{id_hos}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    hos = _hospitais[id_hos]

    if nome is not None:
        ok, erro = validar_nome(nome)
        if not ok:
            log_servidor(400, erro)
            return 400, erro
        nome_norm = normalizar_nome(nome)
        for k, h in _hospitais.items():
            if k != id_hos and h["nome"] == nome_norm:
                msg = f"Já existe um hospital/serviço com o nome '{nome_norm}'."
                log_servidor(409, msg)
                return 409, msg
        hos["nome"] = nome_norm

    if especialidades is not None:
        esp_norm = [e.strip().title() for e in especialidades if e.strip()]
        if not esp_norm:
            msg = "Especialidades não podem ficar vazias."
            log_servidor(400, msg)
            return 400, msg
        hos["especialidades"] = esp_norm

    if descricao is not None:
        hos["descricao"] = descricao.strip()

    log_servidor(200, f"Hospital/Serviço '{id_hos}' atualizado.")
    return 200, dict(hos)


# ─── REMOVER ──────────────────────────────────

def remover_hospital(id_hos: str) -> tuple:
    if not _hos_existe(id_hos):
        msg = f"Hospital/Serviço '{id_hos}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    hos = _hospitais[id_hos]
    if hos["medicos"]:
        msg = (f"Não é possível remover '{hos['nome']}': "
               f"tem {len(hos['medicos'])} médico(s) alocado(s). "
               f"Realoque os médicos primeiro.")
        log_servidor(409, msg)
        return 409, msg

    nome = hos["nome"]
    del _hospitais[id_hos]
    log_servidor(200, f"Hospital/Serviço '{nome}' (ID: {id_hos}) removido.")
    return 200, f"Hospital/Serviço '{nome}' removido com sucesso."
