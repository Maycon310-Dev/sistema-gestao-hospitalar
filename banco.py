import sqlite3

NOME_BANCO = 'hospital.db'

def conectar():

    conn = sqlite3.connect(NOME_BANCO, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():

    try:
        with conectar() as conn:
            cursor = conn.cursor()

            # 1. ESPECIALIDADES (4 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS especialidades (
                    id_especialidade INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(100) NOT NULL UNIQUE,
                    descricao TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. MÉDICOS (12 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medicos (
                    id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_especialidade INT NOT NULL,
                    nome VARCHAR(150) NOT NULL,
                    crm VARCHAR(20) UNIQUE NOT NULL,
                    crm_uf VARCHAR(2) NOT NULL,
                    telefone VARCHAR(20) NOT NULL,
                    email VARCHAR(100),
                    salario FLOAT NOT NULL CHECK(salario >= 0),
                    data_admissao DATE NOT NULL,
                    turno VARCHAR(20) CHECK(turno IN ('MATUTINO', 'VESPERTINO', 'NOTURNO', 'INTEGRAL')) NOT NULL,
                    ativo INT DEFAULT 1 CHECK(ativo IN (0, 1)),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_especialidade) REFERENCES especialidades(id_especialidade) ON DELETE RESTRICT
                )
            """)

            # 3. PACIENTES (14 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(150) NOT NULL,
                    cpf VARCHAR(14) UNIQUE NOT NULL,
                    rg VARCHAR(20),
                    data_nascimento DATE NOT NULL,
                    sexo VARCHAR(1) CHECK(sexo IN ('M', 'F', 'O')) NOT NULL,
                    telefone VARCHAR(20) NOT NULL,
                    email VARCHAR(100),
                    endereco VARCHAR(255),
                    cidade VARCHAR(100),
                    estado VARCHAR(2),
                    cep VARCHAR(9),
                    tipo_sanguineo VARCHAR(3) CHECK(tipo_sanguineo IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 4. CONVÊNIOS (6 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS convenios (
                    id_convenio INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(100) NOT NULL UNIQUE,
                    telefone VARCHAR(20),
                    percentual_desconto FLOAT DEFAULT 0 CHECK(percentual_desconto >= 0 AND percentual_desconto <= 100),
                    validade_contrato DATE,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 5. PACIENTE_CONVÊNIO - Tabela Associativa N:M (6 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paciente_convenio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_paciente INT NOT NULL,
                    id_convenio INT NOT NULL,
                    numero_carteirinha VARCHAR(50) UNIQUE NOT NULL,
                    validade DATE NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_paciente) REFERENCES pacientes(id_paciente) ON DELETE CASCADE,
                    FOREIGN KEY(id_convenio) REFERENCES convenios(id_convenio) ON DELETE RESTRICT
                )
            """)

            # 6. CONSULTAS (11 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consultas (
                    id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_paciente INT NOT NULL,
                    id_medico INT NOT NULL,
                    data_consulta DATE NOT NULL,
                    horario TIME NOT NULL,
                    motivo TEXT,
                    diagnostico TEXT,
                    observacoes TEXT,
                    status VARCHAR(20) DEFAULT 'AGENDADA' CHECK(status IN ('AGENDADA', 'CONFIRMADA', 'CONCLUIDA', 'CANCELADA', 'FALTOU')),
                    valor FLOAT NOT NULL CHECK(valor >= 0),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
                    FOREIGN KEY(id_medico) REFERENCES medicos(id_medico) ON DELETE RESTRICT
                )
            """)

            # 7. EXAMES (7 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS exames (
                    id_exame INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(150) NOT NULL UNIQUE,
                    descricao TEXT,
                    valor FLOAT NOT NULL CHECK(valor >= 0),
                    preparo TEXT,
                    tempo_resultado VARCHAR(50),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 8. SOLICITAÇÃO DE EXAMES (8 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS solicitacao_exames (
                    id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_consulta INT NOT NULL,
                    id_exame INT NOT NULL,
                    data_solicitacao DATE DEFAULT CURRENT_DATE,
                    resultado TEXT,
                    data_resultado DATE,
                    status VARCHAR(20) DEFAULT 'PENDENTE' CHECK(status IN ('PENDENTE', 'COLETADO', 'CONCLUIDO', 'CANCELADO')),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
                    FOREIGN KEY(id_exame) REFERENCES exames(id_exame) ON DELETE RESTRICT
                )
            """)

            # 9. MEDICAMENTOS (9 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medicamentos (
                    id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(150) NOT NULL,
                    fabricante VARCHAR(100),
                    lote VARCHAR(50),
                    validade DATE,
                    quantidade_estoque INT DEFAULT 0 CHECK(quantidade_estoque >= 0),
                    valor_unitario FLOAT NOT NULL CHECK(valor_unitario >= 0),
                    categoria VARCHAR(50),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 10. PRESCRIÇÕES (8 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prescricoes (
                    id_prescricao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_consulta INT NOT NULL,
                    id_medicamento INT NOT NULL,
                    dosagem VARCHAR(100) NOT NULL,
                    frequencia VARCHAR(100) NOT NULL,
                    dias_tratamento INT NOT NULL CHECK(dias_tratamento > 0),
                    observacoes TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
                    FOREIGN KEY(id_medicamento) REFERENCES medicamentos(id_medicamento) ON DELETE RESTRICT
                )
            """)

            # 11. QUARTOS (7 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quartos (
                    id_quarto INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero VARCHAR(10) UNIQUE NOT NULL,
                    andar INT NOT NULL,
                    tipo VARCHAR(30) CHECK(tipo IN ('ENFERMARIA', 'APARTAMENTO', 'UTI', 'ISOLAMENTO')) NOT NULL,
                    quantidade_leitos INT NOT NULL CHECK(quantidade_leitos >= 1),
                    status VARCHAR(20) DEFAULT 'DISPONIVEL' CHECK(status IN ('DISPONIVEL', 'OCUPADO', 'MANUTENCAO', 'HIGIENIZACAO')),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 12. INTERNAÇÕES (10 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS internacoes (
                    id_internacao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_paciente INT NOT NULL,
                    id_quarto INT NOT NULL,
                    id_medico_responsavel INT NOT NULL,
                    data_entrada DATETIME NOT NULL,
                    data_saida DATETIME,
                    motivo TEXT NOT NULL,
                    observacoes TEXT,
                    status VARCHAR(20) DEFAULT 'ATIVA' CHECK(status IN ('ATIVA', 'ALTA', 'TRANSFERIDO', 'OBITO')),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_paciente) REFERENCES pacientes(id_paciente) ON DELETE RESTRICT,
                    FOREIGN KEY(id_quarto) REFERENCES quartos(id_quarto) ON DELETE RESTRICT,
                    FOREIGN KEY(id_medico_responsavel) REFERENCES medicos(id_medico) ON DELETE RESTRICT
                )
            """)

            # 13. FUNCIONÁRIOS (11 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(150) NOT NULL,
                    cpf VARCHAR(14) UNIQUE NOT NULL,
                    cargo VARCHAR(100) NOT NULL,
                    salario FLOAT NOT NULL CHECK(salario >= 0),
                    telefone VARCHAR(20),
                    email VARCHAR(100),
                    data_admissao DATE NOT NULL,
                    setor VARCHAR(100),
                    ativo INT DEFAULT 1 CHECK(ativo IN (0, 1)),
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 14. PAGAMENTOS (9 colunas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagamentos (
                    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_consulta INT,
                    forma_pagamento VARCHAR(30) CHECK(forma_pagamento IN ('DINHEIRO', 'CREDITO', 'DEBITO', 'PIX', 'CONVENIO')) NOT NULL,
                    valor FLOAT NOT NULL CHECK(valor >= 0),
                    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'PAGO' CHECK(status IN ('PENDENTE', 'PAGO', 'ESTORNADO')),
                    numero_recibo VARCHAR(50) UNIQUE NOT NULL,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(id_consulta) REFERENCES consultas(id_consulta) ON DELETE SET NULL
                )
            """)

            # --- ÍNDICES DE PERFORMANCE ---
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_paciente_cpf ON pacientes(cpf)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_medico_crm ON medicos(crm)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_consulta_data ON consultas(data_consulta)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_internacao_status ON internacoes(status)")

            print("Banco de dados Hospitalar construído com sucesso!")

    except sqlite3.Error as erro:
        print(f"Erro crítico ao criar o banco de dados hospitalar: {erro}")

if __name__ == "__main__":
    criar_tabelas()

