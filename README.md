🏥 Sistema de Gestão Hospitalar (Python)

Este é um sistema de linha de comando (CLI) desenvolvido em Python para a gestão de registros de Médicos e Pacientes. O projeto simula o comportamento de um servidor real, utilizando mensagens de log baseadas em Status Codes HTTP.
🚀 Funcionalidades
👨‍⚕️ Gestão de Médicos

    Cadastro: Geração automática de ID e validação de dados (Nome, Especialidade, Data).

    Consulta: Busca detalhada por ID.

    Listagem: Visualização rápida de todos os médicos registrados.

    Atualização: Edição dinâmica de qualquer campo do registro.

    Remoção: Exclusão segura de registros do sistema.

👤 Gestão de Pacientes

    Cadastro: Geração automática de NIF válido (algoritmo oficial) e vínculo com ID médico.

    Consulta: Busca detalhada por NIF.

    Histórico: Registro de alergias, doenças crônicas e cirurgias.

    Atualização e Remoção: Gestão completa dos dados do paciente.

🛠️ Tecnologias Utilizadas

    Python 3.x

    Módulos Nativos: random, datetime

    Simulação de API: Sistema de logs com status 200, 201, 400 e 404.

📁 Estrutura do Projeto
Plaintext

├── main.py          # Ponto de entrada do programa (Menus)
├── medico.py        # Lógica e dicionários de médicos
├── paciente.py      # Lógica e dicionários de pacientes
└── ultils.py        # Funções utilitárias (Geradores de ID/NIF e Logs)


💻 Exemplos de Logs (Simulação HTTP)

O sistema comunica-se com o utilizador através de respostas padronizadas:

    [HTTP 201] : Criado com sucesso - Quando um novo registro é salvo.

    [HTTP 200] : OK - Quando uma consulta ou atualização é bem-sucedida.

    [HTTP 404] : Not Found - Quando um ID ou NIF não existe na base de dados.

    [HTTP 400] : Bad Request - Quando há erro de digitação ou dados inválidos.

📝 Notas de Implementação

    Validação de Dados: O sistema utiliza loops de repetição para garantir que campos críticos (como datas e números) sejam preenchidos corretamente sem interromper o programa.

    Persistência: Os dados são armazenados em dicionários em memória durante a execução da sessão.
