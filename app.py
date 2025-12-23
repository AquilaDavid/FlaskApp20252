from flask import Flask, request, jsonify
from helpers.database.sqlite_helper import get_connection

app = Flask(__name__)


@app.get("/")
def index():
    return {"versao": "2.0.0", "banco": "SQLite"}, 200



# USUÁRIOS 

@app.get("/usuarios")
def get_usuarios():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id, nome, cpf, nascimento
        FROM usuarios
        LIMIT ? OFFSET ?
    """, (limit, offset))

    usuarios = [
        {
            "id": row[0],
            "nome": row[1],
            "cpf": row[2],
            "nascimento": row[3]
        }
        for row in cursor.fetchall()
    ]

    conn.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": usuarios
    }), 200


@app.get("/usuarios/<int:id>")
def get_usuario_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, nascimento
        FROM usuarios
        WHERE id = ?
    """, (id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"erro": "Usuário não encontrado"}, 404

    return {
        "id": row[0],
        "nome": row[1],
        "cpf": row[2],
        "nascimento": row[3]
    }, 200


@app.post("/usuarios")
def create_usuario():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, cpf, nascimento)
        VALUES (?, ?, ?)
    """, (data["nome"], data["cpf"], data["nascimento"]))

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return {"id": novo_id, **data}, 201


@app.put("/usuarios/<int:id>")
def update_usuario(id):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, cpf = ?, nascimento = ?
        WHERE id = ?
    """, (
        data.get("nome"),
        data.get("cpf"),
        data.get("nascimento"),
        id
    ))

    conn.commit()
    rows = cursor.rowcount
    conn.close()

    if rows == 0:
        return {"erro": "Usuário não encontrado"}, 404

    return {"mensagem": "Usuário atualizado com sucesso"}, 200


@app.delete("/usuarios/<int:id>")
def delete_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()

    rows = cursor.rowcount
    conn.close()

    if rows == 0:
        return {"erro": "Usuário não encontrado"}, 404

    return {"mensagem": "Usuário removido com sucesso"}, 200



# INSTITUIÇÕES DE ENSINO 

@app.get("/instituicoesensino")
def get_instituicoes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM instituicoes_ensino")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT codigo, nome, co_uf, co_municipio,
               qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp
        FROM instituicoes_ensino
        LIMIT ? OFFSET ?
    """, (limit, offset))

    instituicoes = [
        {
            "codigo": row[0],
            "nome": row[1],
            "co_uf": row[2],
            "co_municipio": row[3],
            "qt_mat_bas": row[4],
            "qt_mat_prof": row[5],
            "qt_mat_eja": row[6],
            "qt_mat_esp": row[7]
        }
        for row in cursor.fetchall()
    ]

    conn.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": instituicoes
    }), 200


@app.get("/instituicoesensino/<int:codigo>")
def get_instituicao_by_codigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT codigo, nome, co_uf, co_municipio,
               qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp
        FROM instituicoes_ensino
        WHERE codigo = ?
    """, (codigo,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"erro": "Instituição não encontrada"}, 404

    return {
        "codigo": row[0],
        "nome": row[1],
        "co_uf": row[2],
        "co_municipio": row[3],
        "qt_mat_bas": row[4],
        "qt_mat_prof": row[5],
        "qt_mat_eja": row[6],
        "qt_mat_esp": row[7]
    }, 200




if __name__ == "__main__":
    app.run(debug=True)
