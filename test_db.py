from flask import Flask
from helpers.database.postgres_helper import get_connection

app = Flask(__name__)

with app.app_context():
    try:
        conn = get_connection()
        print("✅ Conectou no PostgreSQL com sucesso!")
        conn.close()
    except Exception as e:
        print("❌ Erro ao conectar no banco:")
        print(e)
