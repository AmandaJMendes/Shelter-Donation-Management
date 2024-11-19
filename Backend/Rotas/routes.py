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



if __name__ == '__main__':
    app.run(debug=True)