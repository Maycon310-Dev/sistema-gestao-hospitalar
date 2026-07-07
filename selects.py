import sqlite3

NOME_BANCO = 'hospital.db'

def conectar():
    conn = sqlite3.connect(NOME_BANCO)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# 1. QUANTOS PACIENTES ESTÃO INTERNADOS ATUALMENTE POR TIPO DE QUARTO
def select_1():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.tipo, COUNT(i.id_internacao) 
        FROM internacoes i
        INNER JOIN quartos q ON i.id_quarto = q.id_quarto
        WHERE i.status = 'ATIVA'
        GROUP BY q.tipo
    """)
    resultados = cursor.fetchall()

    print("\n=== PACIENTES INTERNADOS POR TIPO DE QUARTO ===")
    print("-" * 60)
    print(f"{'TIPO DE QUARTO':<30}{'TOTAL'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<30}{linha[1]}")
    conn.close()

# 2. TOTAL DE CONSULTAS REALIZADAS POR CADA MÉDICO
def select_2():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nome, COUNT(c.id_consulta) 
        FROM consultas c
        INNER JOIN medicos m ON c.id_medico = m.id_medico
        GROUP BY m.id_medico
    """)
    resultados = cursor.fetchall()

    print("\n=== TOTAL DE CONSULTAS POR MÉDICO ===")
    print("-" * 60)
    print(f"{'MÉDICO':<30}{'CONSULTAS'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<30}{linha[1]}")
    conn.close()

# 3. FATURAMENTO TOTAL DO HOSPITAL POR FORMA DE PAGAMENTO
def select_3():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT forma_pagamento, SUM(valor) 
        FROM pagamentos
        WHERE status = 'PAGO'
        GROUP BY forma_pagamento
    """)
    resultados = cursor.fetchall()

    print("\n=== FATURAMENTO POR FORMA DE PAGAMENTO ===")
    print("-" * 60)
    print(f"{'FORMA PAGAMENTO':<30}{'TOTAL FATURADO (R$)'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<30}{linha[1]:.2f}")
    conn.close()

# 4. MEDICAMENTOS COM ESTOQUE CRÍTICO (ABAIXO DE 500 UNIDADES)
def select_4():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, quantidade_estoque 
        FROM medicamentos
        WHERE quantidade_estoque < 500
    """)
    resultados = cursor.fetchall()

    print("\n=== ALERTA: ESTOQUE CRÍTICO DE MEDICAMENTOS ===")
    print("-" * 60)
    print(f"{'MEDICAMENTO':<35}{'QTD ESTOQUE'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<35}{linha[1]}")
    conn.close()

# 5. OS 5 EXAMES MAIS SOLICITADOS PELOS MÉDICOS
def select_5():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.nome, COUNT(s.id_solicitacao) 
        FROM solicitacao_exames s
        INNER JOIN exames e ON s.id_exame = e.id_exame
        GROUP BY e.id_exame
        ORDER BY COUNT(s.id_solicitacao) DESC
        LIMIT 5
    """)
    resultados = cursor.fetchall()

    print("\n=== TOP 5 EXAMES MAIS SOLICITADOS ===")
    print("-" * 60)
    print(f"{'NOME DO EXAME':<35}{'TOTAL SOLICITAÇÕES'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<35}{linha[1]}")
    conn.close()

# 6. PACIENTES QUE SÃO DOADORES UNIVERSAIS (O+ OU O-)
def select_6():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, cpf, tipo_sanguineo 
        FROM pacientes
        WHERE tipo_sanguineo IN ('O+', 'O-')
    """)
    resultados = cursor.fetchall()

    print("\n=== PACIENTES DOADORES UNIVERSAIS ===")
    print("-" * 60)
    print(f"{'NOME':<25}{'CPF':<20}{'TIPO SANGUÍNEO'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<25}{linha[1]:<20}{linha[2]}")
    conn.close()

# 7. MÉDIA SALARIAL DOS FUNCIONÁRIOS POR CARGO
def select_7():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cargo, AVG(salario) 
        FROM funcionarios
        GROUP BY cargo
    """)
    resultados = cursor.fetchall()

    print("\n=== MÉDIA SALARIAL POR CARGO ===")
    print("-" * 60)
    print(f"{'CARGO':<30}{'MÉDIA SALARIAL (R$)'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<30}{linha[1]:.2f}")
    conn.close()

# 8. MAPEAMENTO GERAL DE CONSULTAS (PACIENTE E MÉDICO)
def select_8():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_consulta, p.nome, m.nome, c.data_consulta
        FROM consultas c
        INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
        INNER JOIN medicos m ON c.id_medico = m.id_medico
        LIMIT 5
    """)
    resultados = cursor.fetchall()

    print("\n=== LISTA DE CONSULTAS (PACIENTE E MÉDICO) ===")
    print("-" * 75)
    print(f"{'ID':<5}{'PACIENTE':<25}{'MÉDICO':<25}{'DATA'}")
    print("-" * 75)

    for linha in resultados:
        print(f"{linha[0]:<5}{linha[1]:<25}{linha[2]:<25}{linha[3]}")
    conn.close()

# 9. QUANTIDADE DE PACIENTES POR CONVÊNIO
def select_9():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT conv.nome, COUNT(pc.id_paciente) 
        FROM paciente_convenio pc
        INNER JOIN convenios conv ON pc.id_convenio = conv.id_convenio
        GROUP BY conv.id_convenio
    """)
    resultados = cursor.fetchall()

    print("\n=== TOTAL DE PACIENTES POR CONVÊNIO ===")
    print("-" * 60)
    print(f"{'CONVÊNIO':<30}{'TOTAL PACIENTES'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<30}{linha[1]}")
    conn.close()

# 10. LISTA DE QUARTOS QUE ESTÃO TOTALMENTE DISPONÍVEIS
def select_10():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT numero, andar, tipo 
        FROM quartos
        WHERE status = 'DISPONIVEL'
    """)
    resultados = cursor.fetchall()

    print("\n=== QUARTOS DISPONÍVEIS ===")
    print("-" * 60)
    print(f"{'NÚMERO':<15}{'ANDAR':<15}{'TIPO'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<15}{linha[1]:<15}{linha[2]}")
    conn.close()

# 11. VALOR TOTAL DE DESCONTOS CONCEDIDOS POR CONVÊNIO
def select_11():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT conv.nome, SUM(c.valor * (conv.percentual_desconto / 100)) 
        FROM consultas c
        INNER JOIN paciente_convenio pc ON c.id_paciente = pc.id_paciente
        INNER JOIN convenios conv ON pc.id_convenio = conv.id_convenio
        GROUP BY conv.nome
    """)
    resultados = cursor.fetchall()

    print("\n=== TOTAL DE DESCONTOS POR CONVÊNIO ===")
    print("-" * 60)
    print(f"{'CONVÊNIO':<30}{'TOTAL ECONOMIZADO (R$)'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<30}{linha[1]:.2f}")
    conn.close()

# 12. PRONTUÁRIO DE PRESCRIÇÕES (PACIENTE E MEDICAMENTO)
def select_12():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nome, m.nome, pr.dosagem 
        FROM prescricoes pr
        INNER JOIN consultas c ON pr.id_consulta = c.id_consulta
        INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
        INNER JOIN medicamentos m ON pr.id_medicamento = m.id_medicamento
        LIMIT 5
    """)
    resultados = cursor.fetchall()

    print("\n=== HISTÓRICO DE PRESCRIÇÕES MÉDICAS ===")
    print("-" * 70)
    print(f"{'PACIENTE':<25}{'MEDICAMENTO':<30}{'DOSAGEM'}")
    print("-" * 70)

    for linha in resultados:
        print(f"{linha[0]:<25}{linha[1]:<30}{linha[2]}")
    conn.close()

# 13. MÉDICOS ATIVOS TRABALHANDO NO PLANTÃO DA NOITE OU INTEGRAL
def select_13():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, crm, turno 
        FROM medicos
        WHERE ativo = 1 AND turno IN ('INTEGRAL', 'NOTURNO')
    """)
    resultados = cursor.fetchall()

    print("\n=== MÉDICOS DE PLANTÃO (INTEGRAL / NOTURNO) ===")
    print("-" * 60)
    print(f"{'MÉDICO':<25}{'CRM':<15}{'TURNO'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<25}{linha[1]:<15}{linha[2]}")
    conn.close()

# 14. EXAMES CUJO LAUDO JÁ FOI CONCLUÍDO
def select_14():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_consulta, status, data_solicitacao 
        FROM solicitacao_exames
        WHERE status = 'CONCLUIDO'
        LIMIT 5
    """)
    resultados = cursor.fetchall()

    print("\n=== EXAMES COM LAUDO CONCLUÍDO ===")
    print("-" * 60)
    print(f"{'ID CONSULTA':<15}{'STATUS':<20}{'DATA SOLICITAÇÃO'}")
    print("-" * 60)

    for linha in resultados:
        print(f"{linha[0]:<15}{linha[1]:<20}{linha[2]}")
    conn.close()

# 15. CUSTO TOTAL DA FOLHA DE PAGAMENTO DOS MÉDICOS
def select_15():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(salario) 
        FROM medicos
    """)
    resultado = cursor.fetchone()

    print("\n=== CUSTO TOTAL DA FOLHA DOS MÉDICOS ===")
    print("-" * 60)
    print(f"Custo mensal total com salários médicos: R$ {resultado[0]:.2f}")
    print("-" * 60)
    conn.close()

# EXECUÇÃO SEQUENCIAL DE TODOS OS SELECTS
if __name__ == "__main__":
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()
    select_11()
    select_12()
    select_13()
    select_14()
    select_15()