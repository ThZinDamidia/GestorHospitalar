from ultils import log_servidor
import json
import os


_unidades = {}
_contador_unidades = 1
unidade_ficheiro = "unidade_ficheiro.json"
def guardar_unidade1():
    with open(unidade_ficheiro,"w", encoding="utf-8") as unidade:
        json.dump(_unidades, unidade, indent=4, ensure_ascii=False)
def carregar_unidade():
    global _unidades
    if os.path.exists(unidade_ficheiro):
         with open(unidade_ficheiro, "r", encoding="utf-8") as unidade:
            _unidades = json.load(unidade)
    else:
        _unidades = {}
def _gerar_id_unidade():
    global _contador_unidades
    novo_id = f"U{_contador_unidades:03d}"
    _contador_unidades += 1
    return novo_id


def criar_unidade(nome, localizacao, tipo, capacidade_maxima):
    """
    Cria uma nova unidade de saúde.
    tipo: 'Hospital Regional' | 'Centro de Saúde' | 'Clínica'
    capacidade_maxima: número máximo de médicos vinculados
    """
    carregar_unidade()
    if not nome or not nome.strip():
        log_servidor(400, "Nome da unidade nao pode estar vazio.")
        return 400, "Nome da unidade nao pode estar vazio."

    if not localizacao or not localizacao.strip():
        log_servidor(400, "Localizacao nao pode estar vazia.")
        return 400, "Localizacao nao pode estar vazia."

    tipos_validos = ["Hospital Regional", "Centro de Saude", "Clinica"]
    if tipo not in tipos_validos:
        log_servidor(400, f"Tipo invalido. Opcoes: {tipos_validos}")
        return 400, f"Tipo invalido. Use: {', '.join(tipos_validos)}"

    try:
        capacidade_maxima = int(capacidade_maxima)
        if capacidade_maxima <= 0:
            raise ValueError
    except (ValueError, TypeError):
        log_servidor(400, "Capacidade maxima deve ser um inteiro positivo.")
        return 400, "Capacidade maxima invalida."

    id_unidade = _gerar_id_unidade()

    _unidades[id_unidade] = {
        "nome": nome.strip().title(),
        "localizacao": localizacao.strip().title(),
        "tipo": tipo,
        "capacidade_maxima": capacidade_maxima,
        "medicos_vinculados": 0,
    }

    log_servidor(201, f"Unidade '{nome}' criada com ID: {id_unidade}")
    guardar_unidade1()
    return 201, dict(_unidades[id_unidade]) | {"id_unidade": id_unidade}
   


def listar_unidades():
    carregar_unidade()
    if not _unidades:
        log_servidor(404, "Nenhuma unidade registada.")
        return 404, "Nenhuma unidade registada."

    log_servidor(200, "Lista de unidades recuperada.")
    return 200, {uid: dict(dados) for uid, dados in _unidades.items()}



def consultar_unidade(id_unidade):
    carregar_unidade()
    if id_unidade not in _unidades:
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    log_servidor(200, f"Unidade '{id_unidade}' encontrada.")
    carregar_unidade()
    return 200, dict(_unidades[id_unidade]) | {"id_unidade": id_unidade}
 


def atualizar_unidade(id_unidade, nome=None, localizacao=None, tipo=None, capacidade_maxima=None):
    carregar_unidade()
    if id_unidade not in _unidades:
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    unidade = _unidades[id_unidade]

    if nome is not None and nome.strip():
        unidade["nome"] = nome.strip().title()

    if localizacao is not None and localizacao.strip():
        unidade["localizacao"] = localizacao.strip().title()

    if tipo is not None:
        tipos_validos = ["Hospital Regional", "Centro de Saude", "Clinica"]
        if tipo not in tipos_validos:
            log_servidor(400, f"Tipo invalido: {tipo}")
            return 400, f"Tipo invalido. Use: {', '.join(tipos_validos)}"
        unidade["tipo"] = tipo

    if capacidade_maxima is not None:
        try:
            nova_cap = int(capacidade_maxima)
            if nova_cap < unidade["medicos_vinculados"]:
                log_servidor(400, "Nova capacidade inferior ao numero de medicos ja vinculados.")
                return 400, (
                    f"Capacidade invalida: a unidade ja tem {unidade['medicos_vinculados']} "
                    f"medicos vinculados."
                )
            unidade["capacidade_maxima"] = nova_cap
        except (ValueError, TypeError):
            log_servidor(400, "Capacidade invalida.")
            return 400, "Capacidade maxima invalida."

    log_servidor(200, f"Unidade '{id_unidade}' atualizada.")
    guardar_unidade1()
    return 200, dict(unidade) | {"id_unidade": id_unidade}



def remover_unidade(id_unidade):
    carregar_unidade()
    if id_unidade not in _unidades:
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    if _unidades[id_unidade]["medicos_vinculados"] > 0:
        log_servidor(409, f"Unidade '{id_unidade}' tem medicos vinculados.")
        return 409, (
            f"Nao e possivel remover: a unidade ainda tem "
            f"{_unidades[id_unidade]['medicos_vinculados']} medico(s) vinculado(s)."
        )

    nome = _unidades.pop(id_unidade)["nome"]
    log_servidor(200, f"Unidade '{nome}' removida.")
    guardar_unidade1()
    return 200, nome
 


def unidade_existe(id_unidade):
    carregar_unidade()
    return id_unidade in _unidades
  


def verificar_capacidade(id_unidade):
    """
    Verifica se a unidade pode receber mais um médico.
    Retorna True se houver vaga, False se estiver lotada.
    """
    carregar_unidade()
    if id_unidade not in _unidades:
        return False
    u = _unidades[id_unidade]
    return u["medicos_vinculados"] < u["capacidade_maxima"]


def incrementar_medicos(id_unidade):
    carregar_unidade()
    """Chamado pelo módulo médico ao criar um médico vinculado a esta unidade."""
    if id_unidade in _unidades:
        _unidades[id_unidade]["medicos_vinculados"] += 1
    guardar_unidade1()


def decrementar_medicos(id_unidade):
    """Chamado pelo módulo médico ao remover um médico desta unidade."""
    carregar_unidade()
    if id_unidade in _unidades:
        _unidades[id_unidade]["medicos_vinculados"] = max(
            0, _unidades[id_unidade]["medicos_vinculados"] - 1
        )
    guardar_unidade1()
