import os

from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = os.getenv('CHAVE')

#    |-LOGIN-|
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('password')

    if not email or not senha:
        return jsonify({"logado": False, "message": "Campos de Email e senha são obrigatórios"}), 400
    
    user_id = bussca_userid_no_banco(email, senha)
    if user_id:
        session['user_id'] = user_id
        return jsonify({'logado': True})
    else:
        return jsonify({'logado': False, "message": "Usuário ou senha inválidos"}), 401
    
#    |-LOGOUT-|
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({"logado": False})



#    |-Verificando user da sessão atual-|
@app.route('/sessao', methods=['GET'])
def sessao():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({"logado": True, "user_id": user_id})
    else:
        return jsonify({"logado": False})


#    |-TODO: Alterar quando tivermos o banco-|
def bussca_userid_no_banco(email, senha):
    exemplo_usuarios = {
        "usuario1@pds2.com": {"id": 1, "password": "senha123"},
        "usuario2@pds2.com": {"id": 2, "password": "senha456"},
    }
    usuario = exemplo_usuarios.get(email)
    if usuario and usuario["password"] == senha:
        return usuario["id"]
    return None

#   |-CRUD-|

# CRUD for Abrigos
@app.route('/abrigos', methods=['POST'])
def create_abrigo():
    data = request.json
    query = f"INSERT INTO Abrigos (nome_completo_administrador, cpf_administrador, email, telefone, endereco, nome_abrigo, capacidade, recebe_pets, so_mulheres_criancas, senha) VALUES ('{data['nome_completo_administrador']}', '{data['cpf_administrador']}', '{data['email']}', '{data['telefone']}', '{data['endereco']}', '{data['nome_abrigo']}', {data['capacidade']}, {data['recebe_pets']}, {data['so_mulheres_criancas']}, '{data['senha']}')"
    return jsonify({"query": query})

@app.route('/abrigos', methods=['GET'])
def read_abrigos():
    query = "SELECT * FROM Abrigos"
    return jsonify({"query": query})

@app.route('/abrigos/<int:id>', methods=['PUT'])
def update_abrigo(id):
    data = request.json
    query = f"UPDATE Abrigos SET nome_completo_administrador='{data['nome_completo_administrador']}', cpf_administrador='{data['cpf_administrador']}', email='{data['email']}', telefone='{data['telefone']}', endereco='{data['endereco']}', nome_abrigo='{data['nome_abrigo']}', capacidade={data['capacidade']}, recebe_pets={data['recebe_pets']}, so_mulheres_criancas={data['so_mulheres_criancas']}, senha='{data['senha']}' WHERE id={id}"
    return jsonify({"query": query})

@app.route('/abrigos/<int:id>', methods=['DELETE'])
def delete_abrigo(id):
    query = f"DELETE FROM Abrigos WHERE id={id}"
    return jsonify({"query": query})

# CRUD for Itens
@app.route('/itens', methods=['POST'])
def create_item():
    data = request.json
    query = f"INSERT INTO Itens (nome_item, categoria, perecivel, quantidade, id_abrigo) VALUES ('{data['nome_item']}', '{data['categoria']}', {data['perecivel']}, {data['quantidade']}, {data['id_abrigo']})"
    return jsonify({"query": query})

@app.route('/itens', methods=['GET'])
def read_itens():
    query = "SELECT * FROM Itens"
    return jsonify({"query": query})

@app.route('/itens/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    query = f"UPDATE Itens SET nome_item='{data['nome_item']}', categoria='{data['categoria']}', perecivel={data['perecivel']}, quantidade={data['quantidade']}, id_abrigo={data['id_abrigo']} WHERE id={id}"
    return jsonify({"query": query})

@app.route('/itens/<int:id>', methods=['DELETE'])
def delete_item(id):
    query = f"DELETE FROM Itens WHERE id={id}"
    return jsonify({"query": query})

# CRUD for Transacoes
@app.route('/transacoes', methods=['POST'])
def create_transacao():
    data = request.json
    query = f"INSERT INTO Transacoes (id_item, quantidade, id_abrigo_origem, id_abrigo_destino, status_transacao) VALUES ({data['id_item']}, {data['quantidade']}, {data['id_abrigo_origem']}, {data['id_abrigo_destino']}, '{data['status_transacao']}')"
    return jsonify({"query": query})

@app.route('/transacoes', methods=['GET'])
def read_transacoes():
    query = "SELECT * FROM Transacoes"
    return jsonify({"query": query})

@app.route('/transacoes/<int:id>', methods=['PUT'])
def update_transacao(id):
    data = request.json
    query = f"UPDATE Transacoes SET id_item={data['id_item']}, quantidade={data['quantidade']}, id_abrigo_origem={data['id_abrigo_origem']}, id_abrigo_destino={data['id_abrigo_destino']}, status_transacao='{data['status_transacao']}' WHERE id={id}"
    return jsonify({"query": query})

@app.route('/transacoes/<int:id>', methods=['DELETE'])
def delete_transacao(id):
    query = f"DELETE FROM Transacoes WHERE id={id}"
    return jsonify({"query": query})

if __name__ == '__main__':
    app.run(debug=True)