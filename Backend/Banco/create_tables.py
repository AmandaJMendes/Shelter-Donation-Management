import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Definir o diretório base como a pasta "Backend/Banco"
base_dir = os.path.abspath(os.path.join(os.getcwd(), "Backend", "Banco"))

# Diretório para a pasta `instance` dentro de "Backend/Banco"
instance_dir = os.path.join(base_dir, "instance")

# Garantir que o diretório instance exista
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# Criar a aplicação Flask
app = Flask(
    __name__,
    instance_path=instance_dir,  # Caminho absoluto para a pasta instance
    instance_relative_config=True,
)

# Configuração da pasta flask_session dentro de "Backend/Banco"
session_dir = os.path.join(base_dir, "custom_sessions")
if not os.path.exists(session_dir):
    os.makedirs(session_dir)

app.config["SESSION_FILE_DIR"] = session_dir
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SECRET_KEY"] = "sua_chave_secreta"

# Configuração do banco de dados SQLite na pasta instance dentro de "Backend/Banco"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(instance_dir, 'shelter.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Carregar configurações adicionais da pasta instance (opcional)
app.config.from_pyfile("config.py", silent=True)

# Inicializar Flask-Session
Session(app)

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definição das tabelas


class Shelter(db.Model):
    __tablename__ = "shelter"
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    address_street = db.Column(db.String(100), nullable=False)
    address_neighborhood = db.Column(db.String(100), nullable=False)
    address_city = db.Column(db.String(50), nullable=False)
    address_state = db.Column(db.String(2), nullable=False)
    shelter_name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    accepts_pets = db.Column(db.Boolean, nullable=False)
    women_and_children_only = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    perishable = db.Column(db.Boolean, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shelter_id = db.Column(db.Integer, db.ForeignKey("shelter.id"), nullable=False)


class Transaction(db.Model):
    __tablename__ = "transacoes"  # Certifique-se de que o nome da tabela está correto
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(
        db.Integer, db.ForeignKey("item.id"), nullable=False
    )  # id_item mapeado corretamente
    quantity = db.Column(db.Integer, nullable=False)
    origin_shelter_id = db.Column(
        db.Integer, db.ForeignKey("shelter.id"), nullable=False
    )
    destination_shelter_id = db.Column(
        db.Integer, db.ForeignKey("shelter.id"), nullable=False
    )
    status = db.Column(db.String(20), nullable=False)


# Inicializar e criar o banco de dados
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso.")
