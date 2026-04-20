from datetime import datetime
import random

_contador_ids = 1


def gerar_id_medico():
    global _contador_ids
    novo_id = f"M{_contador_ids:03d}"
    _contador_ids += 1
    return novo_id


def gerar_nif_valido():
    while True:
        nif_lista = [random.choice([1, 2])] + [random.randint(0, 9) for _ in range(7)]
        soma = sum(nif_lista[i] * (9 - i) for i in range(8))
        resto = soma % 11
        digito_controlo = 0 if resto in (0, 1) else 11 - resto
        if digito_controlo < 10:
            nif_lista.append(digito_controlo)
            return int("".join(map(str, nif_lista)))


def validar_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def log_servidor(status, mensagem):
    print(f"\n[HTTP {status}] : {mensagem}")
