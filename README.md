# GestorHospitalar
GestorHospitalar.Beta
📊 Sistema de Gestão Hospitalar - Fase 0

Este projeto consiste em um sistema de gerenciamento hospitalar desenvolvido em Python, focado na estruturação de dados e relações entre Médicos e Pacientes. O sistema utiliza estruturas de dados dinâmicas para simular um ambiente de persistência em memória.
🏗️ Estrutura Hierárquica do Sistema

O sistema foi desenhado seguindo uma hierarquia clara de entidades:

    Nível de Dados (Dicionários):

        medicos: Armazena objetos médicos usando ID_MEDICO como chave primária.

        paciente: Armazena registros de pacientes utilizando o NIF como identificador único.

    Nível de Lógica (CRUD): Funções independentes para cada operação (Criar, Ler, Atualizar, Deletar).

    Nível de Relacionamento: Vinculação de pacientes a médicos através de IDs referenciados.

🛠️ Funcionalidades Implementadas
👨‍⚕️ Gestão de Médicos

    Adição com Validação: O sistema impede a duplicação de IDs e o uso do ID 0.

    Perfil Detalhado: Registro de dados básicos, formação, perfil profissional (idiomas, pontos fortes/fracos) e logística (turno/cargo).

    Consulta Dinâmica: Interface que itera sobre as chaves do dicionário para exibir informações formatadas.

🤒 Gestão de Pacientes

    Histórico Médico: Registro de alergias, doenças crônicas e cirurgias anteriores.

    Vínculo Direto: Campo para associar o paciente ao ID de um médico atual.

⚙️ Diferenciais Técnicos

    Tratamento de Erros: Uso de blocos try-except (ValueError) para garantir que entradas de texto não quebrem o sistema em campos numéricos.

    Interface Amigável: Uso do método .title() para nomes e .replace("_", " ").capitalize() para exibir campos de forma legível ao usuário.

💻 Exemplo de Estrutura de Dados (JSON-like)
Python

{
    "ID_MEDICO": {
        "nome": "Dr. Silva",
        "especialidade": "Cardiologia",
        "vinculo": "Unidade 101"
    }
}

🚀 Próximos Passos (Fase 1)

    [ ] Implementar a entidade Consulta para formalizar a relação N:N.

    [ ] Substituir o armazenamento em memória por um banco de dados SQLite.

    [ ] Adicionar interface gráfica ou Web (Flask/FastAPI).

📝 Notas de Versão

    Nota: Atualmente, o sistema utiliza dicionários globais para simular a base de dados. A unicidade é garantida pela verificação manual de chaves antes da inserção.

Dica Profissional: Notei um pequeno erro no seu código na função adicionar_paciente: você usou paciente[paciente] = {...}. O correto seria usar o identificador, como paciente[nif] = {...}.
