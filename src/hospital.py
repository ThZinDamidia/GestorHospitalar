# ==============================
# departamento.py
# CRUD de Departamentos Hospitalares
# ==============================

from utils import gerar_id_departamento, validar_nome, normalizar_nome, log_servidor

_departamentos: dict = {}


# ─── HELPERS INTERNOS ────────────────────────

def _dep_existe(id_dep: str) -> bool:
    return id_dep in _departamentos


def departamento_existe(id_dep: str) -> bool:
    """Utilitário público para outros módulos."""
    return _dep_existe(id_dep)


def obter_especialidades_departamento(id_dep: str) -> list[str]:
    """Retorna lista de especialidades de um departamento (ou lista vazia)."""
    if not _dep_existe(id_dep):
        return []
    return list(_departamentos[id_dep]["especialidades"])


# ─── CRIAR ────────────────────────────────────

def criar_departamento(nome: str, especialidades: list[str], descricao: str = "") -> tuple:
    """
    Cria um departamento hospitalar.

    Parâmetros:
        nome          – Nome do departamento (obrigatório, único)
        especialidades– Lista de especialidades médicas cobertas (mínimo 1)
        descricao     – Descrição opcional
    """
    # Validação do nome
    ok, erro = validar_nome(nome)
    if not ok:
        log_servidor(400, erro)
        return 400, erro

    # Especialidades não podem estar vazias
    if not especialidades or not isinstance(especialidades, list):
        msg = "É necessário fornecer pelo menos uma especialidade."
        log_servidor(400, msg)
        return 400, msg

    especialidades_norm = [e.strip().title() for e in especialidades if e.strip()]
    if not especialidades_norm:
        msg = "Especialidades não podem ser strings vazias."
        log_servidor(400, msg)
        return 400, msg

    # Nome único
    nome_norm = normalizar_nome(nome)
    for dep in _departamentos.values():
        if dep["nome"] == nome_norm:
            msg = f"Já existe um departamento com o nome '{nome_norm}'."
            log_servidor(409, msg)
            return 409, msg

    id_dep = gerar_id_departamento()
    _departamentos[id_dep] = {
        "id": id_dep,
        "nome": nome_norm,
        "especialidades": especialidades_norm,
        "descricao": descricao.strip(),
        "medicos": [],       # IDs dos médicos alocados
        "criado_em": _agora(),
    }

    log_servidor(201, f"Departamento '{nome_norm}' criado. ID: {id_dep}")
    return 201, dict(_departamentos[id_dep])


# ─── LISTAR ───────────────────────────────────

def listar_departamentos() -> tuple:
    if not _departamentos:
        log_servidor(404, "Nenhum departamento registado.")
        return 404, "Nenhum departamento registado."
    log_servidor(200, "Lista de departamentos recuperada.")
    return 200, {k: dict(v) for k, v in _departamentos.items()}


# ─── CONSULTAR ────────────────────────────────

def consultar_departamento(id_dep: str) -> tuple:
    if not _dep_existe(id_dep):
        msg = f"Departamento '{id_dep}' não encontrado."
        log_servidor(404, msg)
        return 404, msg
    log_servidor(200, f"Departamento '{id_dep}' consultado.")
    return 200, dict(_departamentos[id_dep])


# ─── ATUALIZAR ────────────────────────────────

def atualizar_departamento(id_dep: str, nome: str = None,
                            especialidades: list = None,
                            descricao: str = None) -> tuple:
    if not _dep_existe(id_dep):
        msg = f"Departamento '{id_dep}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    dep = _departamentos[id_dep]

    if nome is not None:
        ok, erro = validar_nome(nome)
        if not ok:
            log_servidor(400, erro)
            return 400, erro
        nome_norm = normalizar_nome(nome)
        for k, d in _departamentos.items():
            if k != id_dep and d["nome"] == nome_norm:
                msg = f"Já existe um departamento com o nome '{nome_norm}'."
                log_servidor(409, msg)
                return 409, msg
        dep["nome"] = nome_norm

    if especialidades is not None:
        esp_norm = [e.strip().title() for e in especialidades if e.strip()]
        if not esp_norm:
            msg = "Especialidades não podem ficar vazias."
            log_servidor(400, msg)
            return 400, msg
        dep["especialidades"] = esp_norm

    if descricao is not None:
        dep["descricao"] = descricao.strip()

    log_servidor(200, f"Departamento '{id_dep}' atualizado.")
    return 200, dict(dep)


# ─── REMOVER ──────────────────────────────────

def remover_departamento(id_dep: str) -> tuple:
    if not _dep_existe(id_dep):
        msg = f"Departamento '{id_dep}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    dep = _departamentos[id_dep]
    if dep["medicos"]:
        msg = (f"Não é possível remover o departamento '{dep['nome']}': "
               f"tem {len(dep['medicos'])} médico(s) alocado(s). "
               f"Realoque os médicos primeiro.")
        log_servidor(409, msg)
        return 409, msg

    nome = dep["nome"]
    del _departamentos[id_dep]
    log_servidor(200, f"Departamento '{nome}' (ID: {id_dep}) removido.")
    return 200, f"Departamento '{nome}' removido com sucesso."


# ─── OPERAÇÕES INTERNAS ───────────────────────

def _alocar_medico(id_dep: str, id_med: str) -> None:
    """Chamado por medico.py ao criar/transferir um médico."""
    if _dep_existe(id_dep) and id_med not in _departamentos[id_dep]["medicos"]:
        _departamentos[id_dep]["medicos"].append(id_med)


def _desalocar_medico(id_dep: str, id_med: str) -> None:
    """Chamado por medico.py ao remover/transferir um médico."""
    if _dep_existe(id_dep):
        _departamentos[id_dep]["medicos"] = [
            m for m in _departamentos[id_dep]["medicos"] if m != id_med
        ]


# ─── UTILITÁRIO PRIVADO ───────────────────────

def _agora() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
