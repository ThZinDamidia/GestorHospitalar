# ==============================
# paciente.py
# CRUD de Pacientes com integridade referencial
# ==============================

from utils import (
    gerar_id_paciente, gerar_nif_valido,
    validar_nome, validar_data, validar_tipo_sanguineo,
    normalizar_nome, log_servidor,
)
from medico import medico_existe

_pacientes: dict = {}

# Conjunto de NIFs já usados (para garantir unicidade entre sessões)
_nifs_usados: set = set()


# ─── HELPERS PÚBLICOS ────────────────────────

def paciente_existe(id_pac: str) -> bool:
    return id_pac in _pacientes


def obter_medico_paciente(id_pac: str) -> str | None:
    if id_pac not in _pacientes:
        return None
    return _pacientes[id_pac]["id_medico"]


def paciente_tem_internamento_ativo(id_pac: str) -> bool:
    """Verificado por internamento.py para conflitos de agendamento."""
    from internamento import _internamentos
    return any(
        i["paciente_id"] == id_pac and i["status"] == "Ativo"
        for i in _internamentos.values()
    )


# ─── GERAR NIF ÚNICO ─────────────────────────

def _gerar_nif_unico() -> int:
    tentativas = 0
    while tentativas < 1000:
        nif = gerar_nif_valido()
        if nif not in _nifs_usados:
            _nifs_usados.add(nif)
            return nif
        tentativas += 1
    raise RuntimeError("Não foi possível gerar um NIF único após 1000 tentativas.")


# ─── CRIAR ────────────────────────────────────

def criar_paciente(nome: str, data_nascimento: str, nacionalidade: str,
                   tipo_sanguineo: str, alergias: str, doencas_cronicas: str,
                   cirurgias_anteriores: str, id_medico: str) -> tuple:
    """
    Cria um paciente e associa-o a um médico responsável.

    Regras de negócio:
      - O médico responsável deve existir.
      - O tipo sanguíneo deve ser um valor reconhecido.
      - NIF gerado automaticamente e único.
    """
    ok, erro = validar_nome(nome)
    if not ok:
        log_servidor(400, erro)
        return 400, erro

    if not validar_data(data_nascimento):
        msg = "Data de nascimento inválida. Use YYYY-MM-DD."
        log_servidor(400, msg)
        return 400, msg

    if not nacionalidade or not nacionalidade.strip():
        msg = "Nacionalidade é obrigatória."
        log_servidor(400, msg)
        return 400, msg

    if not tipo_sanguineo or not validar_tipo_sanguineo(tipo_sanguineo):
        msg = "Tipo sanguíneo inválido. Valores aceites: A+, A-, B+, B-, AB+, AB-, O+, O-."
        log_servidor(400, msg)
        return 400, msg

    if not id_medico or not id_medico.strip():
        msg = "ID do médico responsável é obrigatório."
        log_servidor(400, msg)
        return 400, msg

    if not medico_existe(id_medico.strip()):
        msg = f"Médico '{id_medico}' não encontrado. Registe o médico primeiro."
        log_servidor(404, msg)
        return 404, msg

    id_pac = gerar_id_paciente()
    nif = _gerar_nif_unico()

    _pacientes[id_pac] = {
        "id": id_pac,
        "nif": nif,
        "nome": normalizar_nome(nome),
        "data_nascimento": data_nascimento,
        "nacionalidade": nacionalidade.strip().title(),
        "tipo_sanguineo": tipo_sanguineo.strip().upper(),
        "alergias": alergias.strip() if alergias else "Nenhuma",
        "doencas_cronicas": doencas_cronicas.strip() if doencas_cronicas else "Nenhuma",
        "cirurgias_anteriores": cirurgias_anteriores.strip() if cirurgias_anteriores else "Nenhuma",
        "id_medico": id_medico.strip(),
        "criado_em": _agora(),
        "atualizado_em": _agora(),
    }

    log_servidor(201, f"Paciente '{normalizar_nome(nome)}' criado. ID: {id_pac} | NIF: {nif}")
    return 201, dict(_pacientes[id_pac])


# ─── LISTAR ───────────────────────────────────

def listar_pacientes() -> tuple:
    if not _pacientes:
        log_servidor(404, "Nenhum paciente registado.")
        return 404, "Nenhum paciente registado."
    log_servidor(200, "Lista de pacientes recuperada.")
    return 200, {k: dict(v) for k, v in _pacientes.items()}


# ─── CONSULTAR ────────────────────────────────

def consultar_paciente(id_pac: str) -> tuple:
    if id_pac not in _pacientes:
        msg = f"Paciente '{id_pac}' não encontrado."
        log_servidor(404, msg)
        return 404, msg
    log_servidor(200, f"Paciente '{id_pac}' consultado.")
    return 200, dict(_pacientes[id_pac])


# ─── ATUALIZAR ────────────────────────────────

def atualizar_paciente(id_pac: str, nome: str = None, data_nascimento: str = None,
                       nacionalidade: str = None, tipo_sanguineo: str = None,
                       alergias: str = None, doencas_cronicas: str = None,
                       cirurgias_anteriores: str = None, id_medico: str = None) -> tuple:
    if id_pac not in _pacientes:
        msg = f"Paciente '{id_pac}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    pac = _pacientes[id_pac]

    if nome is not None:
        ok, erro = validar_nome(nome)
        if not ok:
            log_servidor(400, erro)
            return 400, erro
        pac["nome"] = normalizar_nome(nome)

    if data_nascimento is not None:
        if not validar_data(data_nascimento):
            msg = "Data de nascimento inválida. Use YYYY-MM-DD."
            log_servidor(400, msg)
            return 400, msg
        pac["data_nascimento"] = data_nascimento

    if nacionalidade is not None:
        pac["nacionalidade"] = nacionalidade.strip().title()

    if tipo_sanguineo is not None:
        if not validar_tipo_sanguineo(tipo_sanguineo):
            msg = "Tipo sanguíneo inválido."
            log_servidor(400, msg)
            return 400, msg
        pac["tipo_sanguineo"] = tipo_sanguineo.strip().upper()

    if alergias is not None:
        pac["alergias"] = alergias.strip()
    if doencas_cronicas is not None:
        pac["doencas_cronicas"] = doencas_cronicas.strip()
    if cirurgias_anteriores is not None:
        pac["cirurgias_anteriores"] = cirurgias_anteriores.strip()

    if id_medico is not None:
        if not medico_existe(id_medico.strip()):
            msg = f"Médico '{id_medico}' não encontrado."
            log_servidor(404, msg)
            return 404, msg
        pac["id_medico"] = id_medico.strip()

    pac["atualizado_em"] = _agora()
    log_servidor(200, f"Paciente '{id_pac}' atualizado.")
    return 200, dict(pac)


# ─── REMOVER ──────────────────────────────────

def remover_paciente(id_pac: str) -> tuple:
    if id_pac not in _pacientes:
        msg = f"Paciente '{id_pac}' não encontrado."
        log_servidor(404, msg)
        return 404, msg

    # Integridade referencial — não pode ter internamento ativo
    if paciente_tem_internamento_ativo(id_pac):
        msg = (f"Não é possível remover o paciente '{id_pac}': "
               "tem um internamento ativo. Dê alta primeiro.")
        log_servidor(409, msg)
        return 409, msg

    pac = _pacientes.pop(id_pac)
    log_servidor(200, f"Paciente '{pac['nome']}' (ID: {id_pac}) removido.")
    return 200, f"Paciente '{pac['nome']}' removido com sucesso."


# ─── UTILITÁRIO PRIVADO ───────────────────────

def _agora() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
