# 🏥 Sistema de Gestão Hospitalar (HMS)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)
![Status](https://img.shields.io/badge/status-fase%200%20(CRUD)-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Este é um sistema de linha de comando (CLI) robusto desenvolvido em Python para a gestão centralizada de **Médicos** e **Pacientes**. O projeto diferencia-se por simular o comportamento de uma **API Backend real**, utilizando um sistema de logs baseado em *Status Codes HTTP* para validar operações.

---

## 🚀 Funcionalidades Core

### 👨‍⚕️ Módulo de Gestão Médica
* **Cadastro Inteligente:** Geração automática de ID único (ex: `M001`) e validação rigorosa de datas.
* **Perfil 360º:** Registo de especialidades, competências linguísticas, pontos fortes/fracos e alocação de turnos.
* **Operações CRUD:** Listagem completa, consulta individualizada por ID, atualização dinâmica de campos e remoção lógica.

### 👤 Módulo de Gestão de Pacientes
* **Segurança de Identidade:** Geração de **NIF (Número de Identificação Fiscal)** validado por algoritmo oficial de dígito de controlo.
* **Integridade Referencial:** Vínculo obrigatório entre o paciente e um médico responsável existente no sistema.
* **Prontuário Clínico:** Gestão de alergias, histórico de doenças crónicas e intervenções cirúrgicas anteriores.

---

## 🛠️ Arquitetura e Tecnologias

O software foi construído seguindo princípios de **Modularidade** para facilitar a manutenção e escalabilidade:

| Ficheiro | Responsabilidade |
| :--- | :--- |
| `main.py` | Interface do Utilizador (CLI) e Orquestração de Menus. |
| `medico.py` | Lógica de negócio e Persistência em Memória para Médicos. |
| `paciente.py` | Lógica de negócio e Persistência em Memória para Pacientes. |
| `ultils.py` | *Helpers*: Geradores de ID/NIF, Validadores de Data e Logs de Sistema. |

---

## 📡 Protocolo de Comunicação (Simulação HTTP)

Para garantir uma experiência próxima de sistemas reais, o software comunica o sucesso ou erro das operações através de códigos de estado:

* 🟢 **`[HTTP 201]` - Created:** Novo registo inserido com sucesso.
* 🔵 **`[HTTP 200]` - OK:** Consulta, atualização ou remoção processada sem erros.
* 🟡 **`[HTTP 400]` - Bad Request:** Falha de validação (ex: formato de data inválido ou campos vazios).
* 🔴 **`[HTTP 404]` - Not Found:** Identificador (ID ou NIF) inexistente na base de dados.

---

## ⚙️ Instalação e Execução

1. Clone este repositório:
   ```bash
   git clone [https://github.com/teu-utilizador/hospital-management-system.git](https://github.com/teu-utilizador/hospital-management-system.git)


📁 Estrutura do Projeto
Plaintext

├── main.py          # Ponto de entrada do programa (Menus)
├── medico.py        # Lógica e dicionários de médicos
├── paciente.py      # Lógica e dicionários de pacientes
└── ultils.py        # Funções utilitárias (Geradores de ID/NIF e Logs)


