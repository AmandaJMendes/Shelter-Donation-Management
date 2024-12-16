import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from sqlalchemy import MetaData, create_engine, insert, update, delete, select
from sqlalchemy import text


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://192.168.0.215:5000"])
app.secret_key = os.getenv("CHAVE") or "bad-secret-key"

# Configuração do banco de dados
DATABASE_URI = "sqlite:///Backend/Banco/instance/shelter.db"
engine = create_engine(DATABASE_URI)
metadata = MetaData()

metadata.reflect(bind=engine)
shelter_table = metadata.tables["shelter"]
item_table = metadata.tables["item"]
transaction_table = metadata.tables["transacoes"]


# -- LOGIN E LOGOUT --
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"logado": False, "message": "Campos obrigatórios"}), 400

    try:
        with engine.connect() as connection:
            query = select(shelter_table.c.id).where(
                shelter_table.c.email == email, shelter_table.c.password == password
            )
            result = connection.execute(query).fetchone()

            if result:
                session["user_id"] = result[0]
                return jsonify({"logado": True}), 200
            return jsonify({"logado": False, "message": "Credenciais inválidas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"logado": False}), 200
    

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.json
            query = text("""  
                INSERT INTO shelter (
                    admin_name, admin_cpf, email, phone,
                    address_street, address_neighborhood, address_city, address_state,
                    shelter_name, capacity, accepts_pets, women_and_children_only, password
                ) VALUES (
                    :admin_name, :admin_cpf, :email, :phone,
                    :address_street, :address_neighborhood, :address_city, :address_state,
                    :shelter_name, :capacity, :accepts_pets, :women_and_children_only, :password
                )
            """)
            with engine.connect() as connection:
                connection.execute(query, {
                    "admin_name": data['admin_name'],
                    "admin_cpf": data['admin_cpf'],
                    "email": data['email'],
                    "phone": data['phone'],
                    "address_street": data['address_street'],
                    "address_neighborhood": data['address_neighborhood'],
                    "address_city": data['address_city'],
                    "address_state": data['address_state'],
                    "shelter_name": data['shelter_name'],
                    "capacity": data['capacity'],
                    "accepts_pets": data['accepts_pets'],
                    "women_and_children_only": data['women_and_children_only'],
                    "password": data['password']
                })

            return {"message": "Abrigo registrado com sucesso!"}, 200
        except Exception as e:
            print(e)  
            return {"error": "Erro ao registrar abrigo", "details": str(e)}, 500


@app.route("/sessao", methods=["GET"])
def sessao():
    user_id = session.get("user_id")
    if user_id:
        return jsonify({"logado": True, "user_id": user_id}), 200
    return jsonify({"logado": False}), 200


# -- CRUD ABRIGOS --
@app.route("/abrigos", methods=["POST"])
def create_abrigo():
    data = request.json

    # Verificar se o e-mail já existe no banco de dados
    with engine.connect() as connection:
        query = select(shelter_table.c.id).where(
            shelter_table.c.email == data.get("email")
        )
        result = connection.execute(query).fetchone()
        if result:
            return jsonify({"error": "E-mail já registrado"}), 400

    query = text(
        """
    INSERT INTO shelter (admin_name, admin_cpf, email, password, phone, address_street,
        address_neighborhood, address_city, address_state, shelter_name, capacity,
        accepts_pets, women_and_children_only)
    VALUES (:admin_name, :admin_cpf, :email, :password, :phone, :address_street,
        :address_neighborhood, :address_city, :address_state, :shelter_name, :capacity,
        :accepts_pets, :women_and_children_only)
    """
    )

    try:
        with engine.connect() as connection:
            connection.execute(
                query,
                {
                    "admin_name": data["admin_name"],
                    "admin_cpf": data["admin_cpf"],
                    "email": data["email"],
                    "password": data["password"],
                    "phone": data["phone"],
                    "address_street": data["address_street"],
                    "address_neighborhood": data["address_neighborhood"],
                    "address_city": data["address_city"],
                    "address_state": data["address_state"],
                    "shelter_name": data["shelter_name"],
                    "capacity": data["capacity"],
                    "accepts_pets": data["accepts_pets"],
                    "women_and_children_only": data["women_and_children_only"],
                },
            )

            # Confirmar a transação para persistir os dados no banco
            connection.commit()

            # Consultar o ID do abrigo recém-criado
            query = text("SELECT last_insert_rowid()")
            result = connection.execute(query).fetchone()
            shelter_id = result[0]  # O ID gerado

        return jsonify({"message": "Abrigo criado com sucesso", "id": shelter_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/abrigos/<int:id>", methods=["GET"])
def read_abrigo(id):
    try:
        with engine.connect() as connection:
            query = select(shelter_table).where(shelter_table.c.id == id)
            result = connection.execute(query).fetchone()

            if result:
                abrigo = {
                    column: value
                    for column, value in zip(shelter_table.columns.keys(), result)
                }
                return jsonify(abrigo), 200
            else:
                return jsonify({"error": "Abrigo não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/abrigos/<int:id>", methods=["PUT"])
def update_abrigo(id):
    data = request.json

    if not data.get("admin_name") or not data.get("admin_cpf"):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    try:
        with engine.connect() as connection:
            with connection.begin():
                query = text(
                    """
                    UPDATE shelter
                    SET admin_name=:admin_name, admin_cpf=:admin_cpf,
                        email=:email, phone=:phone, address_street=:address_street,
                        address_neighborhood=:address_neighborhood, address_city=:address_city,
                        address_state=:address_state, shelter_name=:shelter_name,
                        capacity=:capacity, accepts_pets=:accepts_pets,
                        women_and_children_only=:women_and_children_only
                    WHERE id=:id
                """
                )

                connection.execute(
                    query,
                    {
                        "admin_name": data["admin_name"],
                        "admin_cpf": data["admin_cpf"],
                        "email": data["email"],
                        "phone": data["phone"],
                        "address_street": data["address_street"],
                        "address_neighborhood": data["address_neighborhood"],
                        "address_city": data["address_city"],
                        "address_state": data["address_state"],
                        "shelter_name": data["shelter_name"],
                        "capacity": data["capacity"],
                        "accepts_pets": data["accepts_pets"],
                        "women_and_children_only": data["women_and_children_only"],
                        "id": id,
                    },
                )

            return jsonify({"message": "Abrigo atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/abrigos/<int:id>", methods=["DELETE"])
def delete_abrigo(id):
    try:
        query = text("DELETE FROM shelter WHERE id = :id")

        with engine.connect() as connection:
            connection.execute(query, {"id": id})
            connection.commit()

        return jsonify({"message": "Abrigo deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -- CRUD ITENS --
@app.route("/itens", methods=["POST"])
def create_item():
    data = request.json

    try:
        # Usando SQLAlchemy para garantir que os dados sejam inseridos corretamente
        query = insert(item_table).values(
            name=data["name"],
            category=data["category"],
            perishable=data["perishable"],
            quantity=data["quantity"],
            shelter_id=data["shelter_id"],
        )

        # Conectar e executar a query
        with engine.connect() as connection:
            connection.execute(query)
            connection.commit()  # Confirma a transação para garantir que os dados sejam salvos

        return jsonify({"message": "Item criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/itens/<int:id>", methods=["GET"])
def read_item(id):
    try:
        with engine.connect() as connection:
            query = select(item_table).where(item_table.c.id == id)
            result = connection.execute(query).fetchone()

            if result:
                item = {
                    column: value
                    for column, value in zip(item_table.columns.keys(), result)
                }
                return jsonify(item), 200
            else:
                return jsonify({"error": "Item não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/itens/<int:id>", methods=["PUT"])
def update_item(id):
    data = request.json
    try:
        with engine.connect() as connection:
            # Verifica se o item com o ID existe
            query_check = select(item_table).where(item_table.c.id == id)
            result = connection.execute(query_check).fetchone()

            if result is None:
                return jsonify({"error": "Item não encontrado"}), 404

            # Atualiza os dados do item com base no ID
            stmt = update(item_table).where(item_table.c.id == id).values(**data)
            connection.execute(stmt)
            connection.commit()  # Confirma a transação

            # Retorna uma mensagem de sucesso
            return jsonify({"message": "Item atualizado com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/itens/<int:id>", methods=["DELETE"])
def delete_item(id):
    try:
        with engine.connect() as connection:
            stmt = delete(item_table).where(item_table.c.id == id)
            connection.execute(stmt)
            connection.commit()
        return jsonify({"message": "Item deletado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -- CRUD TRANSACOES --
@app.route("/transacoes", methods=["POST"])
def create_transacao():
    data = request.json
    try:
        query = """
        INSERT INTO transacoes (id_item, quantidade, id_abrigo_origem, id_abrigo_destino, status_transacao)
        VALUES (:id_item, :quantidade, :id_abrigo_origem, :id_abrigo_destino, :status_transacao)
        """    # noqa: E501

        # Conectando ao banco e executando a query de inserção
        with engine.connect() as connection:
            connection.execute(
                text(query),
                {
                    "id_item": data["id_item"],
                    "quantidade": data["quantidade"],
                    "id_abrigo_origem": data["id_abrigo_origem"],
                    "id_abrigo_destino": data["id_abrigo_destino"],
                    "status_transacao": data["status_transacao"],
                },
            )

        return jsonify({"message": "Transação criada com sucesso"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transacoes", methods=["GET"])
def read_transacoes():
    query = "SELECT * FROM Transacoes"
    return jsonify({"query": query})


@app.route("/transacoes/<int:id>", methods=["PUT"])
def update_transacao(id):
    data = request.json
    query = f"UPDATE Transacoes SET id_item={data['id_item']}, quantidade={data['quantidade']}, id_abrigo_origem={data['id_abrigo_origem']}, id_abrigo_destino={data['id_abrigo_destino']}, status_transacao='{data['status_transacao']}' WHERE id={id}"  # noqa: E501
    return jsonify({"query": query})


@app.route("/transacoes/<int:id>", methods=["DELETE"])
def delete_transacao(id):
    query = f"DELETE FROM Transacoes WHERE id={id}"
    return jsonify({"query": query})


if __name__ == "__main__":
    app.run(debug=True)
