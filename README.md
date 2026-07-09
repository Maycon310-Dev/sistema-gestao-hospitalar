```
Sistema de Gestão Hospitalar
```


**Descrição**
Sistema web desenvolvido em Python para gerenciamento hospitalar, permitindo o cadastro, consulta, edição e gerenciamento de pacientes de forma simples e intuitiva.
*Funcionalidades*
- Cadastro de pacientes
- Listagem de pacientes
- Edição de informações
- Exclusão de registros
- Interface Web
- Banco de dados SQLite
- Templates HTML
*Tecnologias*
- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2
*Estrutura do Projeto*

Sistema de Gestão Hospitalar/
    ├── app.py
    ├── banco.py
    ├── hospital.db
    ├── popula_hospital.py
    ├── selects.py
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── pacientes.html
    │   └── editar_paciente.html
    └── README.md

    Como executar
1. Clone o repositório.
2. Instale as dependências com 'pip install flask'.
3. Execute 'python app.py'.
4. Acesse http://127.0.0.1:5000.

***Banco de Dados***
O sistema utiliza SQLite. Caso necessário, execute 'python popula_hospital.py' para popular o banco.

*Telas*
- Página Inicial
- Cadastro de Pacientes
- Listagem de Pacientes
- Edição de Pacientes
**Autor**
*Maycon Vinicios*

Projeto desenvolvido para fins de estudo e aprendizado em desenvolvimento web utilizando Python e Flask.
