from flask import Flask, render_template, request, redirect, url_for
import sqlite3
NOME_BANCO = 'hospital.db'

def conectar():
    conn = sqlite3.connect(NOME_BANCO, timeout=20)
    conn.execute("PRAGMA foreign_kerys = ON")
    return conn

app = Flask (__name__)

@app.route('/')
def index():
    return render_template ('index.html')

app.route('/pacientes')
# (O seu código anterior continua igual aqui em cima...)

@app.route('/pacientes')
def listar_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_paciente, nome, cpf, telefone, tipo_sanguineo " \
    "FROM pacientes " \
    "ORDER BY id_paciente DESC")
    
    pacientes_banco = cursor.fetchall()
    
    conn.close()
  
    return render_template('pacientes.html', lista=pacientes_banco)

@app.route('/pacientes/cadastrar', methods=['POST'])
def cadastrar_pacientes():
    nome_paciente = request.form['nome']
    cpf_paciente = request.form['cpf']
    telefone_paciente = request.form['telefone']
    sangue_paciente = request.form['tipo_sanguineo']
    
    data_nasci = request.form['data_nascimento']
    sexo_paciente = request.form['sexo']

    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO pacientes (nome, cpf, telefone, tipo_sanguineo, data_nascimento, sexo) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome_paciente, cpf_paciente, telefone_paciente, sangue_paciente, data_nasci, sexo_paciente))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('listar_pacientes'))

@app.route('/pacientes/editar/<int:id_paciente>', methods=['GET'])
def editar_paciente(id_paciente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute ("""SELECT id_paciente, nome, telefone, tipo_sanguineo"
    "FROM pacientes"
    "WHERE id_paciente = ? """,
    (id_paciente,))

    paciente_encontrado = cursor.fetchone()
    conn.close

    return render_template('editar_paciente.html', p = paciente_encontrado)

@app.route('/pacientes/salvar', methods=['POST'])
def salvar_ed_paciente():
    id_paciente = request.form['id_paciente']
    nome_novo = request.form['nome']
    telefone_novo = request.form['telefone']
    sangue_novo = request.form['tipo_sanguineo']

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pacientes
        SET nome = ?, telefone = ?, tipo_sanguineo = ?
        WHERE id_paciente = ?
""", (nome_novo, telefone_novo, sangue_novo, id_paciente))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_pacientes'))
    


if __name__ == '__main__':
    app.run(debug= True)
    # Liga o servidor no modo Debug. Se você mudar o código e salvar, o site reinicia sozinho.