# 🏥 Sistema de Gestão Hospitalar

Sistema de gestão hospitalar desenvolvido em Python, com arquitetura modular orientada a entidades. Permite gerir Unidades de Saúde, Médicos, Pacientes e Consultas através de menus interativos em linha de comandos.

---

## 📁 Estrutura do Projeto

```
GestorHospitalar/
└── src/
    ├── main.py        # Ponto de entrada — menus e navegação
    ├── unidade.py     # Entidade: Unidade de Saúde
    ├── medico.py      # Entidade: Médico
    ├── paciente.py    # Entidade: Paciente
    ├── consulta.py    # Entidade: Consulta
    └── ultils.py      # Funções utilitárias partilhadas
```

---

## ▶️ Como Executar

```bash
cd src
PYTHONPATH=. python main.py
```

> **Nota:** O `PYTHONPATH=.` é necessário para que o Python encontre os módulos locais corretamente no GitHub Codespaces.

---

## ⚙️ Funcionalidades

### 🏢 Unidade de Saúde
- Criar, listar, consultar, atualizar e remover unidades
- Tipos: `Hospital Regional`, `Centro de Saude`, `Clinica`
- Controlo de capacidade máxima de médicos por unidade
- Impede remoção de unidade com médicos vinculados

### 👨‍⚕️ Médico
- CRUD completo com validação de datas
- Vinculação obrigatória a uma Unidade de Saúde existente
- Bloqueio automático se a unidade atingiu a capacidade máxima (HTTP 403)
- Contador de médicos na unidade atualizado automaticamente

### 🧑‍🤝‍🧑 Paciente
- CRUD completo com geração automática de NIF válido (algoritmo oficial português)
- Registo de alergias, doenças crónicas e cirurgias anteriores
- Vinculação obrigatória a um Médico registado

### 📋 Consulta
- Criação com data/hora, sintomas e observações clínicas
- Estados: `Agendada` → `Realizada` / `Cancelada`
- Listagem com filtros por médico, paciente (NIF) ou estado
- Impede edição de consultas canceladas

---

## 🔐 Validações e Regras de Negócio

| Regra | Comportamento |
|---|---|
| Unidade sem vagas | HTTP 403 — médico não é criado |
| Médico não existe | HTTP 404 — paciente/consulta não é criado |
| NIF inválido | Gerado automaticamente com dígito de controlo |
| Data inválida | HTTP 400 — operação rejeitada |
| Unidade com médicos | HTTP 409 — não pode ser removida |
| Consulta cancelada | HTTP 409 — não pode ser editada |

---

## 🧩 Arquitetura

O sistema segue uma arquitetura em camadas simples:

```
main.py  (Interface / Menus)
    │
    ├── unidade.py   ←── ultils.py
    ├── medico.py    ←── ultils.py + unidade.py
    ├── paciente.py  ←── ultils.py
    └── consulta.py  ←── ultils.py
```

Cada módulo é independente e expõe uma API clara com códigos HTTP (`200`, `201`, `400`, `403`, `404`, `409`) para comunicar o resultado de cada operação.

---

## 🛠️ Tecnologias

- **Python 3** — sem dependências externas
- **Armazenamento em memória** — dicionários Python (`_medicos`, `_pacientes`, etc.)
