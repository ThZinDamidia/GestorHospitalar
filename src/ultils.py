# ==============================
# utils.py
# Utilitários partilhados — validações, IDs, logging
# ==============================

import re
import random
from datetime import datetime, date

# ─── CONTADORES DE IDs ────────────────────────

_counters = {
    "MED": 0,
    "PAC": 0,
    "CON": 0,
    "HOS": 0,
}

def _next_id(prefix: str) -> str:
    _counters[prefix] += 1
    return f"{prefix}-{_counters[prefix]:04d}"

def gerar_id_medico() -> str:
    return _next_id("MED")

def gerar_id_paciente() -> str:
    return _next_id("PAC")

def gerar_id_consulta() -> str:
    return _next_id("CON")

def gerar_id_hospital() -> str:
    return _next_id("HOS")

# ─── NIF PORTUGUÊS ────────────────────────────

def gerar_nif_valido() -> int:
    while True:
        digitos = [random.choice([1, 2])] + [random.randint(0, 9) for _ in range(7)]
        soma = sum(digitos[i] * (9 - i) for i in range(8))
        resto = soma % 11
        controlo = 0 if resto in (0, 1) else 11 - resto
        if controlo < 10:
            digitos.append(controlo)
            return int("".join(map(str, digitos)))

# ─── CONSTANTES ───────────────────────────────

_DATA_FMT = "%Y-%m-%d"
_HORA_FMT = "%H:%M"

TIPOS_SANGUINEOS = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
STATUS_CONSULTA   = {"Agendada", "Concluida", "Cancelada"}

# ─── VALIDAÇÕES ───────────────────────────────

def validar_data(texto: str) -> bool:
    try:
        datetime.strptime(texto, _DATA_FMT)
        return True
    except (ValueError, TypeError):
        return False

def validar_hora(texto: str) -> bool:
    try:
        datetime.strptime(texto, _HORA_FMT)
        return True
    except (ValueError, TypeError):
        return False

def validar_data_futura(texto: str) -> bool:
    if not validar_data(texto):
        return False
    return datetime.strptime(texto, _DATA_FMT).date() >= date.today()

def validar_data_passada(texto: str) -> bool:
    if not validar_data(texto):
        return False
    return datetime.strptime(texto, _DATA_FMT).date() <= date.today()

def validar_nome(nome: str) -> tuple:
    if not nome or not nome.strip():
        return False, "Nome não pode estar vazio."
    if len(nome.strip()) < 2:
        return False, "Nome demasiado curto (mínimo 2 caracteres)."
    if len(nome.strip()) > 120:
        return False, "Nome demasiado longo (máximo 120 caracteres)."
    if not re.match(r"^[A-Za-zÀ-ÿ\s\-]+$", nome.strip()):
        return False, "Nome contém caracteres inválidos."
    return True, ""

def validar_tipo_sanguineo(tipo: str) -> bool:
    return tipo.strip().upper() in TIPOS_SANGUINEOS

def normalizar_nome(nome: str) -> str:
    return nome.strip().title()

def combinar_data_hora(data: str, hora: str) -> str:
    return f"{data} {hora}"

def parsear_data_hora(texto: str) -> datetime:
    return datetime.strptime(texto, f"{_DATA_FMT} {_HORA_FMT}")

# ─── LOGGING ──────────────────────────────────

def log_servidor(status: int, mensagem: str) -> None:
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{agora}] [HTTP {status}] {mensagem}")
