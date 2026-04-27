from utils import log_servidor

_hospitais = {}

def criar_hospital(id_hospital, nome, cnpj, endereco, especialidades_disponiveis):
    """
    especialidades_disponiveis: deve ser uma lista (ex: ['Cardiologia', 'Pediatria'])
    """
    if not id_hospital or not nome or not cnpj:
        log_servidor(400, "ID, Nome e CNPJ sao obrigatorios.")
        return 400, "Dados obrigatorios ausentes."

    if id_hospital in _hospitais:
        log_servidor(400, f"Hospital ID {id_hospital} ja existe.")
        return 400, "ID de hospital ja cadastrado."

    # Validação simples de CNPJ (apenas tamanho para este exemplo)
    if len(str(cnpj)) != 14:
        log_servidor(400, "CNPJ invalido. Deve conter 14 digitos.")
        return 400, "CNPJ deve ter 14 numeros."

    _hospitais[id_hospital] = {
        "nome": nome.strip().title(),
        "cnpj": cnpj,
        "endereco": endereco,
        "especialidades": [e.strip().title() for e in especialidades_disponiveis],
        "ativo": True
    }
    
    log_servidor(201, f"Hospital '{nome}' cadastrado com sucesso.")
    return 201, _hospitais[id_hospital]

def hospital_existe(id_hospital):
    return id_hospital in _hospitais and _hospitais[id_hospital]["ativo"]

def listar_hospitais():
    return 200, _hospitais if _hospitais else (404, "Nenhum hospital cadastrado.")
