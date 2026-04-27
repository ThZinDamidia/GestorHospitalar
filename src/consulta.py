from utils import log_servidor, validar_data
from medico import consultar_medico, medico_existe
from paciente import consultar_paciente

_consultas = {}
_proximo_id_consulta = 1

def agendar_consulta(nif_paciente, id_medico, id_hospital, data_consulta, hora_consulta, motivo):
    global _proximo_id_consulta
    
    # 1. Validação de Existência (Erro Lógico Comum: agendar para quem não existe)
    if not medico_existe(id_medico):
        return 404, "Medico nao encontrado."
    
    # Aqui assumimos uma função de verificação no paciente
    from paciente import _pacientes
    if nif_paciente not in _pacientes:
        return 404, "Paciente nao encontrado."

    # 2. Validação de Data
    if not validar_data(data_consulta):
        return 400, "Data invalida. Use YYYY-MM-DD."

    # 3. Regra de Negócio: Verificar se o médico atende a especialidade do hospital
    # (Adicionando complexidade cruzada)
    code_med, med = consultar_medico(id_medico)
    from hospital import _hospitais
    if id_hospital in _hospitais:
        hosp = _hospitais[id_hospital]
        if med["especialidade"] not in hosp["especialidades"]:
            return 400, f"O medico e de {med['especialidade']}, mas o hospital so atende {hosp['especialidades']}."

    id_c = f"C{_proximo_id_consulta:04d}"
    
    _consultas[id_c] = {
        "id_consulta": id_c,
        "paciente_nif": nif_paciente,
        "medico_id": id_medico,
        "hospital_id": id_hospital,
        "data_hora": f"{data_consulta} {hora_consulta}",
        "motivo": motivo,
        "status": "Agendada" # Status: Agendada, Concluida, Cancelada
    }
    
    _proximo_id_consulta += 1
    log_servidor(201, f"Consulta {id_c} agendada.")
    return 201, _consultas[id_c]

def atualizar_status_consulta(id_consulta, novo_status):
    status_permitidos = ["Agendada", "Concluida", "Cancelada"]
    if id_consulta not in _consultas:
        return 404, "Consulta nao encontrada."
    
    if novo_status.title() not in status_permitidos:
        return 400, "Status invalido."

    _consultas[id_consulta]["status"] = novo_status.title()
    return 200, _consultas[id_consulta]
  
