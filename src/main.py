# ==============================
# main.py
# Interface principal do Sistema de Gestão Hospitalar
# ==============================

import sys
import traceback
from typing import Callable, Any

# ─── IMPORTAÇÕES COM TRATAMENTO DE ERRO ──────

def _importar_modulos():
    """Importa todos os módulos e retorna erros se houver."""
    erros = []
    modulos = {}

    for nome in ["departamento", "medico", "paciente", "consulta"]:
        try:
            modulos[nome] = __import__(nome)
        except ImportError as e:
            erros.append(f"  ✗ Módulo '{nome}' não encontrado: {e}")
        except Exception as e:
            erros.append(f"  ✗ Erro ao importar '{nome}': {e}")

    return modulos, erros


# ─── UTILITÁRIOS DE INTERFACE ─────────────────

LINHA = "─" * 55
LINHA_DUPLA = "═" * 55

def limpar():
    """Imprime separador visual."""
    print()

def cabecalho(titulo: str):
    print(f"\n{LINHA_DUPLA}")
    print(f"  {titulo}")
    print(LINHA_DUPLA)

def secao(titulo: str):
    print(f"\n{LINHA}")
    print(f"  {titulo}")
    print(LINHA)

def sucesso(msg: str):
    print(f"\n  ✔  {msg}")

def erro_msg(msg: str):
    print(f"\n  ✗  {msg}")

def aviso(msg: str):
    print(f"\n  ⚠  {msg}")

def mostrar_resultado(codigo: int, dados: Any):
    """Apresenta o resultado de uma operação de forma legível."""
    if codigo in (200, 201):
        sucesso(f"Operação concluída (HTTP {codigo})")
        if isinstance(dados, dict):
            # Dicionário de registos (listagem)
            if dados and isinstance(next(iter(dados.values())), dict):
                for k, v in dados.items():
                    print(f"\n  [{k}]")
                    for campo, valor in v.items():
                        print(f"    {campo:<20}: {valor}")
            else:
                print()
                for campo, valor in dados.items():
                    print(f"    {campo:<20}: {valor}")
        elif isinstance(dados, str):
            print(f"    {dados}")
    else:
        erro_msg(f"Erro HTTP {codigo}: {dados}")


def ler_input(prompt: str, obrigatorio: bool = True, padrao: str = "") -> str:
    """Lê input do utilizador com validação de campo obrigatório."""
    while True:
        try:
            valor = input(f"  {prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Operação cancelada.")
            return padrao

        if obrigatorio and not valor:
            erro_msg("Campo obrigatório. Tente novamente.")
            continue
        return valor if valor else padrao


def ler_lista(prompt: str) -> list[str]:
    """Lê uma lista separada por vírgulas."""
    valor = ler_input(prompt)
    return [v.strip() for v in valor.split(",") if v.strip()]


def menu(opcoes: list[tuple[str, str]]) -> str:
    """Exibe menu numerado e retorna a opção escolhida."""
    print()
    for i, (chave, descricao) in enumerate(opcoes, 1):
        print(f"  {i}. {descricao}")
    print("  0. Voltar / Sair")
    print()

    while True:
        try:
            escolha = input("  Opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            return "0"

        if escolha == "0":
            return "0"
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(opcoes):
                return opcoes[idx][0]
        except ValueError:
            pass
        erro_msg("Opção inválida. Tente novamente.")


def executar_operacao(func: Callable, *args, **kwargs) -> tuple | None:
    """Executa uma função CRUD com tratamento de exceções."""
    try:
        resultado = func(*args, **kwargs)
        return resultado
    except TypeError as e:
        erro_msg(f"Argumentos inválidos: {e}")
    except Exception as e:
        erro_msg(f"Erro inesperado: {e}")
        if "--debug" in sys.argv:
            traceback.print_exc()
    return None


# ─── MÓDULO: DEPARTAMENTOS ────────────────────

def menu_departamentos(dep):
    while True:
        cabecalho("DEPARTAMENTOS")
        opcao = menu([
            ("criar", "Criar departamento"),
            ("listar", "Listar departamentos"),
            ("consultar", "Consultar departamento"),
            ("atualizar", "Atualizar departamento"),
            ("remover", "Remover departamento"),
        ])

        if opcao == "0":
            break

        elif opcao == "criar":
            secao("Criar Departamento")
            nome = ler_input("Nome do departamento")
            especialidades = ler_lista("Especialidades (separadas por vírgula)")
            descricao = ler_input("Descrição (opcional)", obrigatorio=False)
            resultado = executar_operacao(dep.criar_departamento, nome, especialidades, descricao)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "listar":
            secao("Listar Departamentos")
            resultado = executar_operacao(dep.listar_departamentos)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "consultar":
            secao("Consultar Departamento")
            id_dep = ler_input("ID do departamento (ex: DEP-0001)")
            resultado = executar_operacao(dep.consultar_departamento, id_dep)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "atualizar":
            secao("Atualizar Departamento")
            id_dep = ler_input("ID do departamento")
            print("  (Deixe em branco os campos que não quer alterar)")
            nome = ler_input("Novo nome", obrigatorio=False) or None
            esp_raw = ler_input("Novas especialidades (vírgula)", obrigatorio=False)
            especialidades = [e.strip() for e in esp_raw.split(",") if e.strip()] if esp_raw else None
            descricao = ler_input("Nova descrição", obrigatorio=False) or None
            resultado = executar_operacao(dep.atualizar_departamento, id_dep, nome, especialidades, descricao)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "remover":
            secao("Remover Departamento")
            id_dep = ler_input("ID do departamento")
            confirmar = ler_input(f"Confirmar remoção de '{id_dep}'? (s/N)", obrigatorio=False).lower()
            if confirmar == "s":
                resultado = executar_operacao(dep.remover_departamento, id_dep)
                if resultado:
                    mostrar_resultado(*resultado)
            else:
                aviso("Operação cancelada.")

        input("\n  Prima ENTER para continuar...")


# ─── MÓDULO: MÉDICOS ──────────────────────────

def menu_medicos(med):
    CARGOS = ["Médico Residente", "Médico Especialista", "Médico Chefe",
              "Diretor De Departamento", "Médico Consultor"]

    while True:
        cabecalho("MÉDICOS")
        opcao = menu([
            ("criar", "Criar médico"),
            ("listar", "Listar médicos"),
            ("consultar", "Consultar médico"),
            ("atualizar", "Atualizar médico"),
            ("remover", "Remover médico"),
        ])

        if opcao == "0":
            break

        elif opcao == "criar":
            secao("Criar Médico")
            nome = ler_input("Nome completo")
            data_nasc = ler_input("Data de nascimento (YYYY-MM-DD)")
            nacionalidade = ler_input("Nacionalidade")
            especialidade = ler_input("Especialidade")
            data_reg = ler_input("Data de registo (YYYY-MM-DD)")
            idiomas = ler_input("Idiomas (opcional)", obrigatorio=False)
            ponto_forte = ler_input("Ponto forte (opcional)", obrigatorio=False)
            ponto_fraco = ler_input("Ponto fraco (opcional)", obrigatorio=False)
            id_dep = ler_input("ID do departamento (ex: DEP-0001)")
            horario = ler_input("Horário do turno (ex: 08:00-16:00)")
            print("\n  Cargos disponíveis:")
            for i, c in enumerate(CARGOS, 1):
                print(f"    {i}. {c}")
            cargo_idx = ler_input("Número do cargo")
            try:
                cargo = CARGOS[int(cargo_idx) - 1]
            except (ValueError, IndexError):
                erro_msg("Cargo inválido.")
                input("\n  Prima ENTER para continuar...")
                continue

            resultado = executar_operacao(
                med.criar_medico, nome, data_nasc, nacionalidade, especialidade,
                data_reg, idiomas, ponto_forte, ponto_fraco, id_dep, horario, cargo
            )
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "listar":
            secao("Listar Médicos")
            resultado = executar_operacao(med.listar_medicos)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "consultar":
            secao("Consultar Médico")
            id_med = ler_input("ID do médico (ex: MED-0001)")
            resultado = executar_operacao(med.consultar_medico, id_med)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "atualizar":
            secao("Atualizar Médico")
            id_med = ler_input("ID do médico")
            print("  (Deixe em branco os campos que não quer alterar)")
            nome = ler_input("Novo nome", obrigatorio=False) or None
            data_nasc = ler_input("Nova data nascimento (YYYY-MM-DD)", obrigatorio=False) or None
            nacionalidade = ler_input("Nova nacionalidade", obrigatorio=False) or None
            especialidade = ler_input("Nova especialidade", obrigatorio=False) or None
            id_dep = ler_input("Novo ID departamento", obrigatorio=False) or None
            horario = ler_input("Novo horário turno", obrigatorio=False) or None
            cargo = ler_input("Novo cargo", obrigatorio=False) or None
            resultado = executar_operacao(
                med.atualizar_medico, id_med, nome, data_nasc, nacionalidade,
                especialidade, None, None, None, None, id_dep, horario, cargo
            )
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "remover":
            secao("Remover Médico")
            id_med = ler_input("ID do médico")
            confirmar = ler_input(f"Confirmar remoção de '{id_med}'? (s/N)", obrigatorio=False).lower()
            if confirmar == "s":
                resultado = executar_operacao(med.remover_medico, id_med)
                if resultado:
                    mostrar_resultado(*resultado)
            else:
                aviso("Operação cancelada.")

        input("\n  Prima ENTER para continuar...")


# ─── MÓDULO: PACIENTES ────────────────────────

def menu_pacientes(pac):
    while True:
        cabecalho("PACIENTES")
        opcao = menu([
            ("criar", "Registar paciente"),
            ("listar", "Listar pacientes"),
            ("consultar", "Consultar paciente"),
            ("atualizar", "Atualizar paciente"),
            ("remover", "Remover paciente"),
        ])

        if opcao == "0":
            break

        elif opcao == "criar":
            secao("Registar Paciente")
            nome = ler_input("Nome completo")
            data_nasc = ler_input("Data de nascimento (YYYY-MM-DD)")
            nacionalidade = ler_input("Nacionalidade")
            tipo_sangue = ler_input("Tipo sanguíneo (ex: A+, O-, AB+)")
            morada = ler_input("Morada")
            contacto = ler_input("Contacto (telefone)")
            email = ler_input("Email (opcional)", obrigatorio=False)
            resultado = executar_operacao(
                pac.criar_paciente, nome, data_nasc, nacionalidade,
                tipo_sangue, morada, contacto, email
            )
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "listar":
            secao("Listar Pacientes")
            resultado = executar_operacao(pac.listar_pacientes)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "consultar":
            secao("Consultar Paciente")
            id_pac = ler_input("ID do paciente (ex: PAC-0001)")
            resultado = executar_operacao(pac.consultar_paciente, id_pac)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "atualizar":
            secao("Atualizar Paciente")
            id_pac = ler_input("ID do paciente")
            print("  (Deixe em branco os campos que não quer alterar)")
            nome = ler_input("Novo nome", obrigatorio=False) or None
            morada = ler_input("Nova morada", obrigatorio=False) or None
            contacto = ler_input("Novo contacto", obrigatorio=False) or None
            email = ler_input("Novo email", obrigatorio=False) or None
            resultado = executar_operacao(
                pac.atualizar_paciente, id_pac, nome, None, None, None, morada, contacto, email
            )
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "remover":
            secao("Remover Paciente")
            id_pac = ler_input("ID do paciente")
            confirmar = ler_input(f"Confirmar remoção de '{id_pac}'? (s/N)", obrigatorio=False).lower()
            if confirmar == "s":
                resultado = executar_operacao(pac.remover_paciente, id_pac)
                if resultado:
                    mostrar_resultado(*resultado)
            else:
                aviso("Operação cancelada.")

        input("\n  Prima ENTER para continuar...")


# ─── MÓDULO: CONSULTAS ────────────────────────

def menu_consultas(con):
    while True:
        cabecalho("CONSULTAS")
        opcao = menu([
            ("agendar", "Agendar consulta"),
            ("listar", "Listar consultas"),
            ("consultar", "Consultar detalhes"),
            ("status", "Atualizar status"),
            ("cancelar", "Cancelar consulta"),
        ])

        if opcao == "0":
            break

        elif opcao == "agendar":
            secao("Agendar Consulta")
            id_pac = ler_input("ID do paciente (ex: PAC-0001)")
            id_med = ler_input("ID do médico (ex: MED-0001)")
            id_dep = ler_input("ID do departamento (ex: DEP-0001)")
            data = ler_input("Data (YYYY-MM-DD)")
            hora = ler_input("Hora (HH:MM)")
            motivo = ler_input("Motivo da consulta")
            resultado = executar_operacao(
                con.agendar_consulta, id_pac, id_med, id_dep, data, hora, motivo
            )
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "listar":
            secao("Listar Consultas")
            print("  (Filtros opcionais — deixe em branco para ver todas)")
            filtro_pac = ler_input("Filtrar por ID paciente", obrigatorio=False) or None
            filtro_med = ler_input("Filtrar por ID médico", obrigatorio=False) or None
            filtro_status = ler_input("Filtrar por status (Agendada/Concluida/Cancelada)", obrigatorio=False) or None
            resultado = executar_operacao(con.listar_consultas, filtro_pac, filtro_med, filtro_status)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "consultar":
            secao("Consultar Detalhes da Consulta")
            id_con = ler_input("ID da consulta (ex: CON-0001)")
            resultado = executar_operacao(con.consultar_consulta, id_con)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "status":
            secao("Atualizar Status da Consulta")
            id_con = ler_input("ID da consulta")
            print("\n  Status disponíveis: Concluida | Cancelada")
            novo_status = ler_input("Novo status")
            notas = ler_input("Notas clínicas (opcional)", obrigatorio=False) or None
            resultado = executar_operacao(con.atualizar_status_consulta, id_con, novo_status, notas)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "cancelar":
            secao("Cancelar Consulta")
            id_con = ler_input("ID da consulta")
            motivo = ler_input("Motivo do cancelamento (opcional)", obrigatorio=False)
            confirmar = ler_input(f"Confirmar cancelamento de '{id_con}'? (s/N)", obrigatorio=False).lower()
            if confirmar == "s":
                resultado = executar_operacao(con.cancelar_consulta, id_con, motivo)
                if resultado:
                    mostrar_resultado(*resultado)
            else:
                aviso("Operação cancelada.")

        input("\n  Prima ENTER para continuar...")


# ─── MÓDULO: INTERNAMENTOS ────────────────────

def menu_internamentos(inter):
    while True:
        cabecalho("INTERNAMENTOS")
        opcao = menu([
            ("criar", "Criar internamento"),
            ("listar", "Listar internamentos"),
            ("consultar", "Consultar internamento"),
            ("atualizar", "Atualizar internamento"),
            ("alta", "Dar alta / Transferir"),
        ])

        if opcao == "0":
            break

        elif opcao == "criar":
            secao("Criar Internamento")
            id_pac = ler_input("ID do paciente (ex: PAC-0001)")
            id_med = ler_input("ID do médico responsável (ex: MED-0001)")
            id_dep = ler_input("ID do departamento (ex: DEP-0001)")
            data_entrada = ler_input("Data de entrada (YYYY-MM-DD)")
            quarto = ler_input("Número do quarto")
            motivo = ler_input("Motivo do internamento")
            resultado = executar_operacao(
                inter.criar_internamento, id_pac, id_med, id_dep, data_entrada, quarto, motivo
            )
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "listar":
            secao("Listar Internamentos")
            print("  (Filtros opcionais)")
            filtro_pac = ler_input("Filtrar por ID paciente", obrigatorio=False) or None
            filtro_status = ler_input("Filtrar por status (Ativo/Alta/Transferido)", obrigatorio=False) or None
            resultado = executar_operacao(inter.listar_internamentos, filtro_pac, filtro_status)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "consultar":
            secao("Consultar Internamento")
            id_int = ler_input("ID do internamento (ex: INT-0001)")
            resultado = executar_operacao(inter.consultar_internamento, id_int)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "atualizar":
            secao("Atualizar Internamento")
            id_int = ler_input("ID do internamento")
            print("  (Deixe em branco os campos que não quer alterar)")
            quarto = ler_input("Novo quarto", obrigatorio=False) or None
            notas = ler_input("Notas clínicas", obrigatorio=False) or None
            resultado = executar_operacao(inter.atualizar_internamento, id_int, quarto, notas)
            if resultado:
                mostrar_resultado(*resultado)

        elif opcao == "alta":
            secao("Alta / Transferência")
            id_int = ler_input("ID do internamento")
            print("\n  Status disponíveis: Alta | Transferido")
            novo_status = ler_input("Novo status")
            data_saida = ler_input("Data de saída (YYYY-MM-DD)")
            notas = ler_input("Notas finais (opcional)", obrigatorio=False) or None
            confirmar = ler_input("Confirmar operação? (s/N)", obrigatorio=False).lower()
            if confirmar == "s":
                resultado = executar_operacao(
                    inter.atualizar_status_internamento, id_int, novo_status, data_saida, notas
                )
                if resultado:
                    mostrar_resultado(*resultado)
            else:
                aviso("Operação cancelada.")

        input("\n  Prima ENTER para continuar...")


# ─── MENU PRINCIPAL ───────────────────────────

def menu_principal(modulos: dict):
    dep = modulos.get("departamento")
    med = modulos.get("medico")
    pac = modulos.get("paciente")
    con = modulos.get("consulta")
    inter = modulos.get("internamento")

    opcoes_base = []
    if dep:
        opcoes_base.append(("dep", "Departamentos"))
    if med:
        opcoes_base.append(("med", "Médicos"))
    if pac:
        opcoes_base.append(("pac", "Pacientes"))
    if con:
        opcoes_base.append(("con", "Consultas"))
    if inter:
        opcoes_base.append(("int", "Internamentos"))

    while True:
        cabecalho("SISTEMA DE GESTÃO HOSPITALAR")
        print(f"  Módulos carregados: {len(modulos)}/5")
        opcao = menu(opcoes_base)

        if opcao == "0":
            print("\n  A sair... até breve!\n")
            break
        elif opcao == "dep" and dep:
            menu_departamentos(dep)
        elif opcao == "med" and med:
            menu_medicos(med)
        elif opcao == "pac" and pac:
            menu_pacientes(pac)
        elif opcao == "con" and con:
            menu_consultas(con)
        elif opcao == "int" and inter:
            menu_internamentos(inter)


# ─── ENTRADA PRINCIPAL ────────────────────────

def main():
    print(f"\n{LINHA_DUPLA}")
    print("  A iniciar Sistema de Gestão Hospitalar...")
    print(LINHA_DUPLA)

    modulos, erros = _importar_modulos()

    if erros:
        print("\n  ⚠  Alguns módulos não foram carregados:")
        for e in erros:
            print(e)
        if not modulos:
            print("\n  ✗ Nenhum módulo disponível. Verifique os ficheiros do projeto.")
            sys.exit(1)
        print(f"\n  Continuando com {len(modulos)} módulo(s) disponível(is)...")
        input("  Prima ENTER para continuar...")
    else:
        print(f"\n  ✔  Todos os módulos carregados com sucesso ({len(modulos)}/5)")

    try:
        menu_principal(modulos)
    except KeyboardInterrupt:
        print("\n\n  Interrompido pelo utilizador. A sair...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ✗ Erro crítico inesperado: {e}")
        if "--debug" in sys.argv:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
