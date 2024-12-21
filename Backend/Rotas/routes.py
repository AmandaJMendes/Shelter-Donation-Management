import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from sqlalchemy import MetaData, create_engine, insert, update, delete, select
from sqlalchemy import text


app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000", "http://127.0.0.1:3000"],
)
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
            query = select(shelter_table.c.id, shelter_table.c.shelter_name).where(
                shelter_table.c.email == email, shelter_table.c.password == password
            )
            result = connection.execute(query).fetchone()

            if result:
                session["user_id"] = result[0]
                return (
                    jsonify(
                        {
                            "logado": True,
                            "user_id": result[0],
                            "shelter_name": result[1],
                        }
                    ),
                    200,
                )
            return jsonify({"logado": False, "message": "Credenciais inválidas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"logado": False}), 200


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


@app.route("/abrigos", methods=["GET"])
def read_abrigos():
    try:
        with engine.connect() as connection:
            query = select(shelter_table)
            results = connection.execute(query).fetchall()

            if len(results):
                abrigos = [
                    {
                        column: value
                        for column, value in zip(shelter_table.columns.keys(), result)
                    }
                    for result in results
                ]
                return jsonify(abrigos), 200
            else:
                return jsonify({"error": "Abrigos não encontrados"}), 404
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


@app.route("/itens/shelter/<int:id>", methods=["GET"])
def read_item_by_shelter(id):
    try:
        with engine.connect() as connection:
            query = select(item_table).where(item_table.c.shelter_id == id)
            results = connection.execute(query).fetchall()

            if len(results):
                items = [
                    {
                        column: value
                        for column, value in zip(item_table.columns.keys(), result)
                    }
                    for result in results
                ]
                return jsonify(items), 200
            else:
                return jsonify({"error": "Items não encontrados"}), 404
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
        INSERT INTO transacoes (item_id, quantity, origin_shelter_id, destination_shelter_id, status)
        VALUES (:item_id, :quantity, :origin_shelter_id, :destination_shelter_id, :status)
        """  # noqa: E501

        # Conectando ao banco e executando a query de inserção
        with engine.connect() as connection:
            connection.execute(
                text(query),
                {
                    "item_id": data["item_id"],
                    "quantity": data["quantity"],
                    "origin_shelter_id": data["origin_shelter_id"],
                    "destination_shelter_id": data["destination_shelter_id"],
                    "status": "Pendente",
                },
            )
            connection.commit()

        return jsonify({"message": "Transação criada com sucesso"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transacoes/<int:id>", methods=["GET"])
def read_transacoes(id):
    try:
        query = """
        SELECT * FROM transacoes WHERE origin_shelter_id = :id OR destination_shelter_id = :id
        """
        with engine.connect() as connection:
            results = connection.execute(text(query), {"id": id}).fetchall()

        if len(results):
            items = [
                {
                    column: value
                    for column, value in zip(transaction_table.columns.keys(), result)
                }
                for result in results
            ]
            return jsonify(items), 200
        else:
            return jsonify({"error": "Transações não encontradas"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transacoes/<int:id>", methods=["PUT"])
def update_transacao(id):
    try:
        # Step 1: Fetch the item_id, quantity, and destination_shelter_id from the transaction
        fetch_transaction_query = """
        SELECT item_id, quantity, destination_shelter_id, status
        FROM transacoes
        WHERE id = :id
        """

        with engine.connect() as connection:
            transaction_result = connection.execute(
                text(fetch_transaction_query), {"id": id}
            ).fetchone()
            if not transaction_result:
                return jsonify({"error": "Transação não encontrada"}), 404

            if transaction_result[3] == "Realizada":
                return jsonify({"error": "Transação já foi confirmada!"}), 401

            item_id = transaction_result[0]
            transaction_quantity = transaction_result[1]
            destination_shelter_id = transaction_result[2]

            # Step 2: Fetch the item from the itens table
            fetch_item_query = """
            SELECT id, name, category, perishable, quantity
            FROM item
            WHERE id = :item_id
            """
            item_result = connection.execute(
                text(fetch_item_query), {"item_id": item_id}
            ).fetchone()
            if not item_result:
                return jsonify({"error": "Item não encontrado"}), 404

            current_quantity = item_result[4]

            # Step 3: Decrease the item's quantity
            if current_quantity < transaction_quantity:
                return jsonify({"error": "quantity insuficiente no estoque"}), 400

            updated_quantity = current_quantity - transaction_quantity
            update_item_query = """
            UPDATE item
            SET quantity = :updated_quantity
            WHERE id = :item_id
            """
            connection.execute(
                text(update_item_query),
                {"updated_quantity": updated_quantity, "item_id": item_id},
            )

            # Step 4: Create a new item in the destination shelter
            create_item_query = """
            INSERT INTO item (name, category, perishable, quantity, shelter_id)
            VALUES (:name, :category, :perishable, :quantity, :shelter_id)
            """
            connection.execute(
                text(create_item_query),
                {
                    "name": item_result[1],
                    "category": item_result[2],
                    "perishable": item_result[3],
                    "quantity": transaction_quantity,
                    "shelter_id": destination_shelter_id,
                },
            )

            # Step 5: Update the transaction status
            update_transaction_query = """
            UPDATE transacoes
            SET status = 'Realizada'
            WHERE id = :id
            """
            update_result = connection.execute(
                text(update_transaction_query), {"id": id}
            )
            connection.commit()

        if update_result.rowcount > 0:
            return jsonify({"message": "Transação realizada com sucesso"}), 200
        else:
            return jsonify({"error": "Falha ao atualizar a transação"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transacoes/<int:id>", methods=["DELETE"])
def delete_transacao(id):
    try:
        query = """
        DELETE FROM transacoes WHERE id = :id
        """
        with engine.connect() as connection:
            result = connection.execute(text(query), {"id": id})
            connection.commit()

        if result.rowcount > 0:  # Check if the deletion affected any rows
            return jsonify({"message": "Transação deletada com sucesso"}), 200
        else:
            return jsonify({"error": "Transação não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
