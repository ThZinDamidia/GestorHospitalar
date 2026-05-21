import json
import os
import logging

logger = logging.getLogger('gestor')

_unidades = {}
_contador_unidades = 1
unidade_ficheiro = "unidade_ficheiro.json"

def guardar_unidade1():
    logger.debug("A guardar ficheiro de unidades.")
    with open(unidade_ficheiro, "w", encoding="utf-8") as unidade:
        json.dump(_unidades, unidade, indent=4, ensure_ascii=False)
    logger.debug("Ficheiro de unidades guardado.")

def carregar_unidade():
    global _unidades
    if os.path.exists(unidade_ficheiro):
        logger.debug("A carregar ficheiro de unidades.")
        with open(unidade_ficheiro, "r", encoding="utf-8") as unidade:
            _unidades = json.load(unidade)
        logger.debug("Ficheiro de unidades carregado: %d registo(s).", len(_unidades))
    else:
        logger.debug("Ficheiro de unidades inexistente. A iniciar vazio.")
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
    logger.info("Tentativa de criacao de unidade.")
    carregar_unidade()
    if not nome or not nome.strip():
        logger.error("Nome da unidade nao pode estar vazio.")
        return 400, "Nome da unidade nao pode estar vazio."

    if not localizacao or not localizacao.strip():
        logger.error("Localizacao nao pode estar vazia.")
        return 400, "Localizacao nao pode estar vazia."

    tipos_validos = ["Hospital Regional", "Centro de Saude", "Clinica"]
    if tipo not in tipos_validos:
        logger.error("Tipo invalido: %s.", tipo)
        return 400, f"Tipo invalido. Use: {', '.join(tipos_validos)}"

    try:
        capacidade_maxima = int(capacidade_maxima)
        if capacidade_maxima <= 0:
            raise ValueError
    except (ValueError, TypeError):
        logger.error("Capacidade maxima deve ser um inteiro positivo.")
        return 400, "Capacidade maxima invalida."

    id_unidade = _gerar_id_unidade()

    _unidades[id_unidade] = {
        "nome": nome.strip().title(),
        "localizacao": localizacao.strip().title(),
        "tipo": tipo,
        "capacidade_maxima": capacidade_maxima,
        "medicos_vinculados": 0,
    }

    logger.info("Unidade criada com sucesso: ID='%s'.", id_unidade)
    guardar_unidade1()
    return 201, dict(_unidades[id_unidade]) | {"id_unidade": id_unidade}

def listar_unidades():
    logger.info("Pedido de listagem de unidades.")
    carregar_unidade()
    if not _unidades:
        logger.error("Nenhuma unidade registada.")
        return 404, "Nenhuma unidade registada."

    logger.info("Listagem concluida: %d unidade(s).", len(_unidades))
    return 200, {uid: dict(dados) for uid, dados in _unidades.items()}

def consultar_unidade(id_unidade):
    logger.info("Pedido de consulta da unidade ID='%s'.", id_unidade)
    carregar_unidade()
    if id_unidade not in _unidades:
        logger.error("Unidade ID='%s' nao encontrada.", id_unidade)
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    logger.info("Unidade ID='%s' retornada.", id_unidade)
    return 200, dict(_unidades[id_unidade]) | {"id_unidade": id_unidade}


def atualizar_unidade(id_unidade, nome=None, localizacao=None, tipo=None, capacidade_maxima=None):
    logger.info("Pedido de atualizacao da unidade ID='%s'.", id_unidade)
    carregar_unidade()
    if id_unidade not in _unidades:
        logger.error("Atualizacao falhada: unidade ID='%s' nao encontrada.", id_unidade)
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    unidade = _unidades[id_unidade]

    if nome is not None and nome.strip():
        unidade["nome"] = nome.strip().title()

    if localizacao is not None and localizacao.strip():
        unidade["localizacao"] = localizacao.strip().title()

    if tipo is not None:
        tipos_validos = ["Hospital Regional", "Centro de Saude", "Clinica"]
        if tipo not in tipos_validos:
            logger.error("Tipo invalido na atualizacao da unidade ID='%s'.", id_unidade)
            return 400, f"Tipo invalido. Use: {', '.join(tipos_validos)}"
        unidade["tipo"] = tipo

    if capacidade_maxima is not None:
        try:
            nova_cap = int(capacidade_maxima)
            if nova_cap < unidade["medicos_vinculados"]:
                logger.error("Atualizacao rejeitada: nova capacidade abaixo dos medicos vinculados "
                              "na unidade ID='%s'.", id_unidade)
                return 400, (
                    f"Capacidade invalida: a unidade ja tem {unidade['medicos_vinculados']} "
                    f"medicos vinculados."
                )
            unidade["capacidade_maxima"] = nova_cap
        except (ValueError, TypeError):
            logger.error("Valor de capacidade invalido na unidade ID='%s'.", id_unidade)
            return 400, "Capacidade maxima invalida."

    logger.info("Unidade ID='%s' atualizada com sucesso.", id_unidade)
    guardar_unidade1()
    return 200, dict(unidade) | {"id_unidade": id_unidade}

def remover_unidade(id_unidade):
    logger.info("Pedido de remocao da unidade ID='%s'.", id_unidade)
    carregar_unidade()
    if id_unidade not in _unidades:
        logger.error("Remocao falhada: unidade ID='%s' nao encontrada.", id_unidade)
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    if _unidades[id_unidade]["medicos_vinculados"] > 0:
        logger.error("Remocao bloqueada: unidade ID='%s' ainda tem medicos vinculados.", id_unidade)
        return 409, (
            f"Nao e possivel remover: a unidade ainda tem "
            f"{_unidades[id_unidade]['medicos_vinculados']} medico(s) vinculado(s)."
        )

    nome = _unidades.pop(id_unidade)["nome"]
    logger.info("Unidade ID='%s' removida com sucesso.", id_unidade)
    guardar_unidade1()
    return 200, nome

def unidade_existe(id_unidade):
    carregar_unidade()
    logger.debug("Verificacao de existencia: unidade ID='%s'.", id_unidade)
    return id_unidade in _unidades

def verificar_capacidade(id_unidade):
    """
    Verifica se a unidade pode receber mais um médico.
    Retorna True se houver vaga, False se estiver lotada.
    """
    carregar_unidade()
    if id_unidade not in _unidades:
        logger.error("Verificacao de capacidade: unidade ID='%s' nao encontrada.", id_unidade)
        return False
    u = _unidades[id_unidade]
    tem_vaga = u["medicos_vinculados"] < u["capacidade_maxima"]
    logger.debug("Verificacao de capacidade da unidade ID='%s': tem_vaga=%s.", id_unidade, tem_vaga)
    return tem_vaga


def incrementar_medicos(id_unidade):
    carregar_unidade()
    """Chamado pelo módulo médico ao criar um médico vinculado a esta unidade."""
    if id_unidade in _unidades:
        _unidades[id_unidade]["medicos_vinculados"] += 1
        logger.debug("Unidade ID='%s': contador de medicos incrementado.", id_unidade)
    guardar_unidade1()


def decrementar_medicos(id_unidade):
    """Chamado pelo módulo médico ao remover um médico desta unidade."""
    carregar_unidade()
    if id_unidade in _unidades:
        _unidades[id_unidade]["medicos_vinculados"] = max(
            0, _unidades[id_unidade]["medicos_vinculados"] - 1
        )
        logger.debug("Unidade ID='%s': contador de medicos decrementado.", id_unidade)
    guardar_unidade1()
