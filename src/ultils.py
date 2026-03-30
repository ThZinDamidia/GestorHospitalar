from datetime import datetime
import random

contador_ids = 1

def gerar_id_medico():
    global contador_ids
    novo_id = f"U{contador_ids:03d}"
    contador_ids += 1
    return novo_id


def validar_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def gerar_nif_valido():
    while True:
        # 1. Gera os primeiros 8 dígitos (começando por 1 ou 2 para pessoas singulares)
        nif_lista = [random.choice([1, 2])] + [random.randint(0, 9) for _ in range(7)]

        # 2. Calcula o dígito de controlo (Algoritmo oficial do NIF em Portugal)
        soma = 0
        for i in range(8):
            soma += nif_lista[i] * (9 - i)

        resto = soma % 11

        if resto == 0 or resto == 1:
            digito_controlo = 0
        else:
            digito_controlo = 11 - resto

        # Se o dígito for 10, o NIF é inválido pelas regras.
        # O loop 'while' garante que tentamos de novo até dar um dígito de 0 a 9.
        if digito_controlo < 10:
            nif_lista.append(digito_controlo)

            # Junta a lista de números numa única string e converte para inteiro
            nif_final = int("".join(map(str, nif_lista)))
            return nif_final

def log_servidor(status, mensagem):
    # Formata uma linha única: [STATUS] Mensagem
    print(f"\n[HTTP {status}] : {mensagem}")
