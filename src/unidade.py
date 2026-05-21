from ultils import log_servidor
import json
import os
import logging

logger = logging.getLogger('gestor')

_unidades = {}
_contador_unidades = 1
unidade_ficheiro = "unidade_ficheiro.json"

def guardar_unidade1():
    logger.debug("A guardar unidades no ficheiro '%s'.", unidade_ficheiro)
    with open(unidade_ficheiro,"w", encoding="utf-8") as unidade:
        json.dump(_unidades, unidade, indent=4, ensure_ascii=False)
    logger.debug("Unidades guardadas com sucesso.")

def carregar_unidade():
    global _unidades
    if os.path.exists(unidade_ficheiro):
        logger.debug("A carregar unidades do ficheiro '%s'.", unidade_ficheiro)
        with open(unidade_ficheiro, "r", encoding="utf-8") as unidade:
            _unidades = json.load(unidade)
        logger.debug("Unidades carregadas: %d registo(s).", len(_unidades))
    else:
        logger.debug("Ficheiro '%s' nao encontrado. A iniciar dicionario vazio.", unidade_ficheiro)
        _unidades = {}

def _gerar_id_unidade():
    global _contador_unidades
    novo_id = f"U{_contador_unidades:03d}"
    _contador_unidades += 1
    logger.debug("ID de unidade gerado: %s", novo_id)
    return novo_id


def criar_unidade(nome, localizacao, tipo, capacidade_maxima):
    """
    Cria uma nova unidade de saúde.
    tipo: 'Hospital Regional' | 'Centro de Saúde' | 'Clínica'
    capacidade_maxima: número máximo de médicos vinculados
    """
    logger.info("Tentativa de criacao de unidade: nome='%s', tipo='%s', localizacao='%s'.",
                nome, tipo, localizacao)
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
    logger.info("Unidade criada com sucesso: ID=%s, nome='%s', tipo='%s', capacidade=%d.",
                id_unidade, nome, tipo, capacidade_maxima)
    guardar_unidade1()
    return 201, dict(_unidades[id_unidade]) | {"id_unidade": id_unidade}

def listar_unidades():
    logger.info("Pedido de listagem de unidades.")
    carregar_unidade()
    if not _unidades:
        log_servidor(404, "Nenhuma unidade registada.")
        return 404, "Nenhuma unidade registada."

    log_servidor(200, "Lista de unidades recuperada.")
    logger.info("Listagem de unidades concluida: %d unidade(s) retornada(s).", len(_unidades))
    return 200, {uid: dict(dados) for uid, dados in _unidades.items()}

def consultar_unidade(id_unidade):
    logger.info("Pedido de consulta da unidade ID='%s'.", id_unidade)
    carregar_unidade()
    if id_unidade not in _unidades:
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        logger.warning("Unidade ID='%s' nao encontrada.", id_unidade)
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    log_servidor(200, f"Unidade '{id_unidade}' encontrada.")
    logger.info("Unidade ID='%s' encontrada e retornada.", id_unidade)
    return 200, dict(_unidades[id_unidade]) | {"id_unidade": id_unidade}


def atualizar_unidade(id_unidade, nome=None, localizacao=None, tipo=None, capacidade_maxima=None):
    logger.info("Pedido de atualizacao da unidade ID='%s'.", id_unidade)
    carregar_unidade()
    if id_unidade not in _unidades:
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        logger.warning("Atualizacao falhada: unidade ID='%s' nao encontrada.", id_unidade)
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    unidade = _unidades[id_unidade]

    if nome is not None and nome.strip():
        logger.debug("Unidade ID='%s': nome alterado de '%s' para '%s'.",
                     id_unidade, unidade["nome"], nome.strip().title())
        unidade["nome"] = nome.strip().title()

    if localizacao is not None and localizacao.strip():
        logger.debug("Unidade ID='%s': localizacao alterada para '%s'.",
                     id_unidade, localizacao.strip().title())
        unidade["localizacao"] = localizacao.strip().title()

    if tipo is not None:
        tipos_validos = ["Hospital Regional", "Centro de Saude", "Clinica"]
        if tipo not in tipos_validos:
            log_servidor(400, f"Tipo invalido: {tipo}")
            logger.warning("Tipo invalido fornecido na atualizacao da unidade ID='%s': '%s'.",
                           id_unidade, tipo)
            return 400, f"Tipo invalido. Use: {', '.join(tipos_validos)}"
        logger.debug("Unidade ID='%s': tipo alterado para '%s'.", id_unidade, tipo)
        unidade["tipo"] = tipo

    if capacidade_maxima is not None:
        try:
            nova_cap = int(capacidade_maxima)
            if nova_cap < unidade["medicos_vinculados"]:
                log_servidor(400, "Nova capacidade inferior ao numero de medicos ja vinculados.")
                logger.warning("Atualizacao rejeitada: nova capacidade (%d) < medicos vinculados (%d) "
                               "na unidade ID='%s'.", nova_cap, unidade["medicos_vinculados"], id_unidade)
                return 400, (
                    f"Capacidade invalida: a unidade ja tem {unidade['medicos_vinculados']} "
                    f"medicos vinculados."
                )
            logger.debug("Unidade ID='%s': capacidade alterada de %d para %d.",
                         id_unidade, unidade["capacidade_maxima"], nova_cap)
            unidade["capacidade_maxima"] = nova_cap
        except (ValueError, TypeError):
            log_servidor(400, "Capacidade invalida.")
            logger.warning("Valor de capacidade invalido fornecido para unidade ID='%s'.", id_unidade)
            return 400, "Capacidade maxima invalida."

    log_servidor(200, f"Unidade '{id_unidade}' atualizada.")
    logger.info("Unidade ID='%s' atualizada com sucesso.", id_unidade)
    guardar_unidade1()
    return 200, dict(unidade) | {"id_unidade": id_unidade}

def remover_unidade(id_unidade):
    logger.info("Pedido de remocao da unidade ID='%s'.", id_unidade)
    carregar_unidade()
    if id_unidade not in _unidades:
        log_servidor(404, f"Unidade '{id_unidade}' nao encontrada.")
        logger.warning("Remocao falhada: unidade ID='%s' nao encontrada.", id_unidade)
        return 404, f"Unidade '{id_unidade}' nao encontrada."

    if _unidades[id_unidade]["medicos_vinculados"] > 0:
        log_servidor(409, f"Unidade '{id_unidade}' tem medicos vinculados.")
        logger.warning("Remocao bloqueada: unidade ID='%s' tem %d medico(s) vinculado(s).",
                       id_unidade, _unidades[id_unidade]["medicos_vinculados"])
        return 409, (
            f"Nao e possivel remover: a unidade ainda tem "
            f"{_unidades[id_unidade]['medicos_vinculados']} medico(s) vinculado(s)."
        )

    nome = _unidades.pop(id_unidade)["nome"]
    log_servidor(200, f"Unidade '{nome}' removida.")
    logger.info("Unidade ID='%s' (nome='%s') removida com sucesso.", id_unidade, nome)
    guardar_unidade1()
    return 200, nome

def unidade_existe(id_unidade):
    carregar_unidade()
    existe = id_unidade in _unidades
    logger.debug("Verificacao de existencia da unidade ID='%s': %s.", id_unidade, existe)
    return existe

def verificar_capacidade(id_unidade):
    """
    Verifica se a unidade pode receber mais um médico.
    Retorna True se houver vaga, False se estiver lotada.
    """
    carregar_unidade()
    if id_unidade not in _unidades:
        logger.warning("Verificacao de capacidade: unidade ID='%s' nao encontrada.", id_unidade)
        return False
    u = _unidades[id_unidade]
    tem_vaga = u["medicos_vinculados"] < u["capacidade_maxima"]
    logger.debug("Unidade ID='%s': %d/%d medicos. Tem vaga: %s.",
                 id_unidade, u["medicos_vinculados"], u["capacidade_maxima"], tem_vaga)
    return tem_vaga


def incrementar_medicos(id_unidade):
    carregar_unidade()
    """Chamado pelo módulo médico ao criar um médico vinculado a esta unidade."""
    if id_unidade in _unidades:
        _unidades[id_unidade]["medicos_vinculados"] += 1
        logger.debug("Unidade ID='%s': medicos_vinculados incrementado para %d.",
                     id_unidade, _unidades[id_unidade]["medicos_vinculados"])
    guardar_unidade1()


def decrementar_medicos(id_unidade):
    """Chamado pelo módulo médico ao remover um médico desta unidade."""
    carregar_unidade()
    if id_unidade in _unidades:
        _unidades[id_unidade]["medicos_vinculados"] = max(
            0, _unidades[id_unidade]["medicos_vinculados"] - 1
        )
        logger.debug("Unidade ID='%s': medicos_vinculados decrementado para %d.",
                     id_unidade, _unidades[id_unidade]["medicos_vinculados"])
    guardar_unidade1()
