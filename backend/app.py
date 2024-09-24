from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import sqlite3
import time
from flasgger import Swagger

# region Constantes
UPLOAD_FOLDER = './uploads' # Configuração da pasta para uploads (caso precise para imagens no futuro)
FRONTEND_FOLDER = '../frontend'
DB_FILE = './db.sqlite'
# endregion

# Inicializa o app Flask
app = Flask(__name__, static_folder=FRONTEND_FOLDER+'static')
app.config['SWAGGER'] = {
    'swagger_ui': True,
    'uiversion': 3,
    'specs_route': '/swagger'  # Configuração para a rota /swagger
}
swagger = Swagger(app)  # Inicialização do Swagger

# region Funções auxiliares

# Função para conectar ao banco de dados SQLite
# Retorna a conexão ou None em caso de erro
def connect_db():
    try:
        conn = sqlite3.connect(DB_FILE)  # Conecta ao banco SQLite
        return conn
    except sqlite3.Error as e:
        return None
    
# Criar a tabela 'clientes' no banco de dados
def setup_db():
    conn = connect_db()  # Conecta ao banco de dados
    if conn is None:
        with app.app_context():
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor = conn.cursor()
        # Cria a tabela 'clientes' se ela ainda não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo_projeto TEXT,
                urgencia TEXT,
                email TEXT NOT NULL,
                descricao TEXT NOT NULL,
                referencia TEXT
            )
        ''')
        conn.commit()  # Confirma a criação da tabela

        # Retorna uma mensagem de sucesso
        with app.app_context():
            return jsonify({'message': 'Tabela de clientes criada com sucesso!'})
        
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
        with app.app_context():
            return jsonify({'error': 'Erro ao criar tabela'}), 500
    finally:
        conn.close()  # Fecha a conexão com o banco de dados

# endregion
        
# region Rotas
        
# Rota principal para servir o arquivo index.html (página inicial)
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

# Rota para servir arquivos estáticos (CSS, JS, imagens)
@app.route('/static/<path:path>')
def serve_static(path):
    print('serve static called')
    # Serve arquivos estáticos da pasta 'frontend/static'
    return send_from_directory(FRONTEND_FOLDER + '/static', path)

# Rota para servir arquivos da subpasta "uploads"
@app.route('/uploads/<path:filename>')
def show_upload(filename):
    files_directory = os.path.join(app.root_path, 'uploads')
    return send_from_directory(files_directory, filename)

# Rota para cadastrar um novo cliente no banco de dados
@app.route('/cadastrar_cliente', methods=['POST'])
def add_customer():
    """
    Cadastra um novo cliente.

    ---
    tags:
      - Clientes
    consumes:
      - multipart/form-data
    parameters:
      - name: nome
        in: formData
        type: string
        required: true
      - name: tipo_projeto
        in: formData
        type: string
        required: true
      - name: urgencia
        in: formData
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: true
      - name: descricao
        in: formData
        type: string
        required: true
      - name: referencia
        in: formData
        type: file
        required: false
    responses:
      201:
        description: Cliente cadastrado com sucesso!
      500:
        description: Erro ao cadastrar o cliente
    """
    conn = connect_db()  # Conecta ao banco de dados
    if conn is None:
        with app.app_context():
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        # Coleta os dados enviados pelo formulário do frontend
        nome = request.form['nome']
        tipo_projeto = request.form['tipo_projeto']
        urgencia = request.form['urgencia']
        email = request.form['email']
        descricao = request.form['descricao']
        referencia = None

        # Salvar o arquivo (se existir) na pasta uploads
        if 'referencia' in request.files:
            file = request.files['referencia']
            referencia = secure_filename(str(int(time.time())) + file.filename) # Sanitizar o nome do arquivo
            file.save(os.path.join(UPLOAD_FOLDER, referencia))
            

        # Insere os dados no banco de dados
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (
                    nome,
                    tipo_projeto,
                    urgencia,
                    email,
                    descricao,
                    referencia
                )
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, tipo_projeto, urgencia, email, descricao, referencia))
        conn.commit()  # Confirma a inserção no banco de dados

        # Retorna uma mensagem de sucesso em JSON
        return jsonify({'message': 'Cliente cadastrado com sucesso!'}), 201
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar cliente: {e}")
        with app.app_context():
            return jsonify({'error': 'Erro ao cadastrar o cliente'}), 500
    finally:
        conn.close()  # Fecha a conexão com o banco de dados

# Rota para listar clientes
@app.route('/clientes', methods=['GET'])
def list_customers():
    """
    Lista todos os clientes cadastrados.

    ---
    tags:
      - Clientes
    responses:
      200:
        description: Lista de clientes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              tipo_projeto:
                type: string
              urgencia:
                type: string
              email:
                type: string
              descricao:
                type: string
              referencia:
                type: string
      500:
        description: Erro ao listar os clientes
    """
    conn = connect_db()  # Conecta ao banco de dados
    conn.row_factory = sqlite3.Row  # Define row_factory para retornar linhas como dicionários
    if conn is None:
        with app.app_context():
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500
    
    try:
        # Executar a query para obter todos os clientes
        clientes = conn.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
        # Transformar os resultados em uma lista de dicionários
        clientes_list = []
        for cliente in clientes:
            clientes_list.append({
                'id': cliente['id'],
                'nome': cliente['nome'],
                'tipo_projeto': cliente['tipo_projeto'],
                'urgencia': cliente['urgencia'],
                'email': cliente['email'],
                'descricao': cliente['descricao'],
                'referencia': cliente['referencia']
            })
        with app.app_context():
            return jsonify(clientes_list)
        
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        with app.app_context():
            return jsonify({'error': 'Erro ao listar os clientes'}), 500
    finally:
        conn.close()

# endregion

if __name__ == '__main__':
    # Verifica se a pasta de uploads existe, cria se não existir
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Verifica se as tabelas do banco de dados existem, cria se não existirem
    setup_db()
    
    # Inicia o servidor Flask
    app.run(debug=True)
