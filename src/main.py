from medico import (
    criar_medico, listar_medicos, consultar_medico,
    atualizar_medico, remover_medico, medico_existe
)
from paciente import (
    criar_paciente, listar_pacientes, consultar_paciente,
    atualizar_paciente, remover_paciente
)
from unidade import (
    criar_unidade, listar_unidades, consultar_unidade,
    atualizar_unidade, remover_unidade, unidade_existe
)
from consulta import (
    criar_consulta, listar_consultas, consultar_consulta,
    atualizar_consulta, cancelar_consulta, remover_consulta
)

# ─────────────────────────────────────────────
#  MENUS (cabeçalhos)
# ─────────────────────────────────────────────

def menu_principal():
    print("\n╔══════════════════════════════════════╗")
    print("║   SISTEMA DE GESTÃO HOSPITALAR       ║")
    print("╠══════════════════════════════════════╣")
    print("║  1 - Menu Unidade de Saúde           ║")
    print("║  2 - Menu Médico                     ║")
    print("║  3 - Menu Paciente                   ║")
    print("║  4 - Menu Consulta                   ║")
    print("║  0 - Sair                            ║")
    print("╚══════════════════════════════════════╝")

def menu_unidade():
    print("\n===== MENU UNIDADE DE SAÚDE =====")
    print("1 - Criar unidade")
    print("2 - Listar unidades")
    print("3 - Consultar unidade")
    print("4 - Atualizar unidade")
    print("5 - Remover unidade")
    print("0 - Voltar")

def menu_medico():
    print("\n===== MENU MÉDICO =====")
    print("1 - Criar médico")
    print("2 - Listar médicos")
    print("3 - Consultar médico")
    print("4 - Atualizar médico")
    print("5 - Remover médico")
    print("0 - Voltar")

def menu_paciente():
    print("\n===== MENU PACIENTE =====")
    print("1 - Criar paciente")
    print("2 - Listar pacientes")
    print("3 - Consultar paciente")
    print("4 - Atualizar paciente")
    print("5 - Remover paciente")
    print("0 - Voltar")

def menu_consulta():
    print("\n===== MENU CONSULTA =====")
    print("1 - Criar consulta")
    print("2 - Listar consultas")
    print("3 - Consultar consulta")
    print("4 - Atualizar consulta")
    print("5 - Cancelar consulta")
    print("6 - Remover consulta")
    print("0 - Voltar")

# ─────────────────────────────────────────────
#  SUBMENU UNIDADE
# ─────────────────────────────────────────────

def submenu_unidade():
    TIPOS = ["Hospital Regional", "Centro de Saude", "Clinica"]

    while True:
        menu_unidade()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome da unidade: ")
            localizacao = input("Localização (distrito): ")
            print(f"Tipos disponíveis: {', '.join(TIPOS)}")
            tipo = input("Tipo: ")
            cap_str = input("Capacidade máxima de médicos: ")
            try:
                capacidade = int(cap_str)
            except ValueError:
                print("\n❌ Erro: Capacidade deve ser um número inteiro.")
                continue

            code, obj = criar_unidade(nome, localizacao, tipo, capacidade)
            if code == 201:
                print("\n✅ Unidade criada:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "2":
            code, obj = listar_unidades()
            if code == 200:
                print("\nLista de Unidades de Saúde:")
                for uid, dados in obj.items():
                    print(f"  {uid} | {dados['nome']} | {dados['tipo']} | "
                          f"{dados['localizacao']} | "
                          f"Médicos: {dados['medicos_vinculados']}/{dados['capacidade_maxima']}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "3":
            uid = input("ID da unidade (ex: U001): ").strip().upper()
            code, obj = consultar_unidade(uid)
            if code == 200:
                print(f"\nFicha da Unidade {uid}:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "4":
            uid = input("ID da unidade: ").strip().upper()
            nome = input("Novo nome (enter para manter): ")
            localizacao = input("Nova localização (enter para manter): ")
            print(f"Tipos disponíveis: {', '.join(TIPOS)}")
            tipo = input("Novo tipo (enter para manter): ")
            cap_str = input("Nova capacidade máxima (enter para manter): ")

            capacidade = None
            if cap_str.strip():
                try:
                    capacidade = int(cap_str)
                except ValueError:
                    print("\n❌ Erro: Capacidade deve ser um número inteiro.")
                    continue

            code, obj = atualizar_unidade(
                uid,
                nome        if nome.strip() else None,
                localizacao if localizacao.strip() else None,
                tipo        if tipo.strip() else None,
                capacidade,
            )
            if code == 200:
                print("\n✅ Unidade atualizada:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "5":
            uid = input("ID da unidade: ").strip().upper()
            code, obj = remover_unidade(uid)
            if code == 200:
                print(f"\n✅ Unidade '{obj}' removida.")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")

# ─────────────────────────────────────────────
#  SUBMENU MÉDICO
# ─────────────────────────────────────────────

def submenu_medico():
    while True:
        menu_medico()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome       = input("Nome: ")
            dt_nasc    = input("Data de nascimento (YYYY-MM-DD): ")
            nacional   = input("Nacionalidade: ")
            especial   = input("Especialidade: ")
            dt_registo = input("Data de registo (YYYY-MM-DD): ")
            idiomas    = input("Idiomas: ")
            p_forte    = input("Ponto forte: ")
            p_fraco    = input("Ponto fraco: ")
            id_unidade = input("ID da unidade de saúde (ex: U001): ")
            horario    = input("Horário do turno: ")
            cargo      = input("Cargo: ")

            code, obj = criar_medico(nome, dt_nasc, nacional, especial,
                                     dt_registo, idiomas, p_forte, p_fraco,
                                     id_unidade, horario, cargo)
            if code == 201:
                print("\n✅ Médico criado: " + str(obj))
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "2":
            code, obj = listar_medicos()
            if code == 200:
                print("\nLista de Médicos:")
                for id_med, dados in obj.items():
                    print(f"  {id_med} | {dados['nome']} | "
                          f"{dados['especialidade']} | {dados['cargo']} | "
                          f"Unidade: {dados['id_unidade']}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "3":
            id_medico = input("ID do médico (ex: M001): ").strip().upper()
            code, obj = consultar_medico(id_medico)
            if code == 200:
                print(f"\nFicha do Médico {id_medico}:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "4":
            id_medico  = input("ID do médico: ").strip().upper()
            nome       = input("Novo nome (enter para manter): ")
            dt_nasc    = input("Nova data nascimento YYYY-MM-DD (enter para manter): ")
            nacional   = input("Nova nacionalidade (enter para manter): ")
            especial   = input("Nova especialidade (enter para manter): ")
            dt_registo = input("Nova data de registo YYYY-MM-DD (enter para manter): ")
            idiomas    = input("Novos idiomas (enter para manter): ")
            p_forte    = input("Novo ponto forte (enter para manter): ")
            p_fraco    = input("Novo ponto fraco (enter para manter): ")
            id_unidade = input("Novo ID da unidade (enter para manter): ")
            horario    = input("Novo horário do turno (enter para manter): ")
            cargo      = input("Novo cargo (enter para manter): ")

            code, obj = atualizar_medico(
                id_medico,
                nome       if nome.strip() else None,
                dt_nasc    if dt_nasc.strip() else None,
                nacional   if nacional.strip() else None,
                especial   if especial.strip() else None,
                dt_registo if dt_registo.strip() else None,
                idiomas    if idiomas.strip() else None,
                p_forte    if p_forte.strip() else None,
                p_fraco    if p_fraco.strip() else None,
                id_unidade if id_unidade.strip() else None,
                horario    if horario.strip() else None,
                cargo      if cargo.strip() else None,
            )
            if code == 200:
                print("\n✅ Médico atualizado:\n" + str(obj))
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "5":
            id_medico = input("ID do médico: ").strip().upper()
            code, obj = remover_medico(id_medico)
            if code == 200:
                print(f"\n✅ Médico '{obj}' removido.")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")

# ─────────────────────────────────────────────
#  SUBMENU PACIENTE
# ─────────────────────────────────────────────

def submenu_paciente():
    while True:
        menu_paciente()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome      = input("Nome: ")
            dt_nasc   = input("Data de nascimento (YYYY-MM-DD): ")
            nacional  = input("Nacionalidade: ")
            tipo_sang = input("Tipo sanguíneo: ")
            alergias  = input("Alergias: ")
            doencas   = input("Doenças crónicas: ")
            cirurgias = input("Cirurgias anteriores: ")

            id_medico_str = input("ID do médico responsável (ex: M001): ").strip().upper()
            if not medico_existe(id_medico_str):
                print(f"\n❌ Erro 404: Médico '{id_medico_str}' não encontrado. Registe o médico primeiro.")
                continue

            code, obj = criar_paciente(nome, dt_nasc, nacional, tipo_sang,
                                       alergias, doencas, cirurgias, id_medico_str)
            if code == 201:
                print("\n✅ Paciente criado: " + str(obj))
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "2":
            code, obj = listar_pacientes()
            if code == 200:
                print("\nLista de Pacientes:")
                for nif, dados in obj.items():
                    print(f"  NIF: {nif} | {dados['nome']} | "
                          f"{dados['tipo_sanguineo']} | Médico: {dados['id_medico']}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "3":
            try:
                nif = int(input("NIF do paciente: "))
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue
            code, obj = consultar_paciente(nif)
            if code == 200:
                print(f"\nFicha do Paciente (NIF: {nif}):")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "4":
            try:
                nif = int(input("NIF do paciente: "))
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue

            nome      = input("Novo nome (enter para manter): ")
            dt_nasc   = input("Nova data nascimento YYYY-MM-DD (enter para manter): ")
            nacional  = input("Nova nacionalidade (enter para manter): ")
            tipo_sang = input("Novo tipo sanguíneo (enter para manter): ")
            alergias  = input("Novas alergias (enter para manter): ")
            doencas   = input("Novas doenças crónicas (enter para manter): ")
            cirurgias = input("Novas cirurgias anteriores (enter para manter): ")
            id_medico = input("Novo ID do médico (enter para manter): ")

            if id_medico.strip() and not medico_existe(id_medico.strip().upper()):
                print(f"\n❌ Erro: Médico '{id_medico.strip()}' não encontrado.")
                continue

         
            code, obj = atualizar_paciente(
                nif,
                nome      if nome.strip() else None,
                dt_nasc   if dt_nasc.strip() else None,
                nacional  if nacional.strip() else None,
                tipo_sang if tipo_sang.strip() else None,
                alergias  if alergias.strip() else None,
                doencas   if doencas.strip() else None,
                cirurgias if cirurgias.strip() else None,
                id_medico if id_medico.strip() else None,
            )
            if code == 200:
                print("\n✅ Paciente atualizado:\n" + str(obj))
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "5":
            try:
                nif = int(input("NIF do paciente: "))
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue
            code, obj = remover_paciente(nif)
            if code == 200:
                print(f"\n✅ Paciente '{obj}' removido.")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")

# ─────────────────────────────────────────────
#  SUBMENU CONSULTA
# ─────────────────────────────────────────────

def submenu_consulta():
    ESTADOS = ["Agendada", "Realizada", "Cancelada"]

    while True:
        menu_consulta()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            id_medico = input("ID do médico (ex: M001): ").strip().upper()
            if not medico_existe(id_medico):
                print(f"\n❌ Erro 404: Médico '{id_medico}' não encontrado.")
                continue

            nif_str = input("NIF do paciente: ").strip()
            try:
                nif = int(nif_str)
            except ValueError:
                print("\n❌ Erro: NIF deve ser numérico.")
                continue

            data_hora = input("Data e hora (YYYY-MM-DD HH:MM): ")
            sintomas  = input("Sintomas: ")
            observ    = input("Observações clínicas (opcional): ")

            code, obj = criar_consulta(id_medico, nif, data_hora, sintomas, observ)
            if code == 201:
                print("\n✅ Consulta criada:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "2":
            print("\nFiltros (deixe em branco para listar todas):")
            f_medico  = input("  Filtrar por ID médico: ").strip().upper() or None
            f_pac_str = input("  Filtrar por NIF paciente: ").strip()
            f_estado  = input(f"  Filtrar por estado {ESTADOS} (enter para todos): ").strip() or None

            f_paciente = None
            if f_pac_str:
                try:
                    f_paciente = int(f_pac_str)
                except ValueError:
                    print("\n❌ NIF inválido, filtro de paciente ignorado.")

            code, obj = listar_consultas(f_medico, f_paciente, f_estado)
            if code == 200:
                print(f"\n{len(obj)} consulta(s) encontrada(s):")
                for cid, dados in obj.items():
                    print(f"  {cid} | {dados['data_hora']} | "
                          f"Médico: {dados['id_medico']} | NIF: {dados['id_paciente']} | "
                          f"Estado: {dados['estado']}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "3":
            cid = input("ID da consulta (ex: C001): ").strip().upper()
            code, obj = consultar_consulta(cid)
            if code == 200:
                print(f"\nFicha da Consulta {cid}:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ {obj}")

        elif opcao == "4":
            cid       = input("ID da consulta: ").strip().upper()
            data_hora = input("Nova data/hora YYYY-MM-DD HH:MM (enter para manter): ")
            sintomas  = input("Novos sintomas (enter para manter): ")
            observ    = input("Novas observações (enter para manter): ")
            print(f"Estados válidos: {', '.join(ESTADOS)}")
            estado    = input("Novo estado (enter para manter): ")

            code, obj = atualizar_consulta(
                cid,
                data_hora if data_hora.strip() else None,
                sintomas  if sintomas.strip() else None,
                observ    if observ.strip() else None,
                estado    if estado.strip() else None,
            )
            if code == 200:
                print("\n✅ Consulta atualizada:")
                for k, v in obj.items():
                    print(f"  {k.replace('_', ' ').capitalize()}: {v}")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "5":
            cid = input("ID da consulta a cancelar: ").strip().upper()
            code, obj = cancelar_consulta(cid)
            if code == 200:
                print(f"\n✅ Consulta '{cid}' cancelada.")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "6":
            cid = input("ID da consulta a remover: ").strip().upper()
            code, obj = remover_consulta(cid)
            if code == 200:
                print(f"\n✅ {obj}")
            else:
                print(f"\n❌ Falha ({code}): {obj}")

        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            submenu_unidade()
        elif opcao == "2":
            submenu_medico()
        elif opcao == "3":
            submenu_paciente()
        elif opcao == "4":
            submenu_consulta()
        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!\n")
            break
        else:
            print("\n❌ Opção inválida.")

if __name__ == "__main__":
    main()
