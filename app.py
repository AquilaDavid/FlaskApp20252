from flask import Flask, request, jsonify
from marshmallow import ValidationError
from helpers.database.postgres_helper import get_connection
from helpers.logger import logger
from helpers.database.pagination_schema import PaginationSchema
from helpers.database.ranking_schema import RankingSchema

app = Flask(__name__)

@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"errors": err.messages}), 400

@app.get("/")
def index():
    logger.info("Endpoint raiz acessado")
    return {"versao": "2.0.0", "banco": "PostgreSQL"}, 200

@app.get("/usuarios")
def get_usuarios():
    schema = PaginationSchema()
    params = schema.load(request.args)

    page = params["page"]
    limit = params["limit"]
    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id, nome, cpf, nascimento
        FROM usuarios
        LIMIT %s OFFSET %s
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

@app.post("/usuarios")
def create_usuario():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, cpf, nascimento)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (data["nome"], data["cpf"], data["nascimento"]))

    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"message": "Usuário criado", "id": new_id}), 201

@app.get("/usuarios/<int:id>")
def get_usuario_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, nascimento
        FROM usuarios
        WHERE id = %s
    """, (id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "Usuário não encontrado"}), 404

    return jsonify({
        "id": row[0],
        "nome": row[1],
        "cpf": row[2],
        "nascimento": row[3]
    }), 200

@app.put("/usuarios/<int:id>")
def update_usuario(id):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nome = %s,
            cpf = %s,
            nascimento = %s
        WHERE id = %s
    """, (data["nome"], data["cpf"], data["nascimento"], id))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Usuário não encontrado"}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": "Usuário atualizado"}), 200

@app.delete("/usuarios/<int:id>")
def delete_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Usuário não encontrado"}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": "Usuário removido"}), 200

@app.get("/instituicoesensino")
def get_instituicoes():
    schema = PaginationSchema()
    params = schema.load(request.args)

    page = params["page"]
    limit = params["limit"]
    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM instituicoes_ensino")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            co_entidade,
            no_entidade,
            sg_uf,
            no_municipio,
            nu_ano_censo,
            qt_mat_total
        FROM instituicoes_ensino
        LIMIT %s OFFSET %s
    """, (limit, offset))

    instituicoes = [
        {
            "co_entidade": row[0],
            "no_entidade": row[1],
            "sg_uf": row[2],
            "no_municipio": row[3],
            "nu_ano_censo": row[4],
            "qt_mat_total": row[5]
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

@app.post("/instituicoesensino")
def create_instituicao():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO instituicoes_ensino (
            co_entidade,
            no_entidade,
            sg_uf,
            no_municipio,
            nu_ano_censo,
            qt_mat_total
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["co_entidade"],
        data["no_entidade"],
        data["sg_uf"],
        data["no_municipio"],
        data["nu_ano_censo"],
        data["qt_mat_total"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Instituição criada"}), 201

@app.get("/instituicoesensino/<int:co_entidade>")
def get_instituicao_by_id(co_entidade):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT co_entidade, no_entidade, sg_uf,
               no_municipio, nu_ano_censo, qt_mat_total
        FROM instituicoes_ensino
        WHERE co_entidade = %s
    """, (co_entidade,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"message": "Instituição não encontrada"}), 404

    return jsonify({
        "co_entidade": row[0],
        "no_entidade": row[1],
        "sg_uf": row[2],
        "no_municipio": row[3],
        "nu_ano_censo": row[4],
        "qt_mat_total": row[5]
    }), 200

@app.put("/instituicoesensino/<int:co_entidade>")
def update_instituicao(co_entidade):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE instituicoes_ensino
        SET no_entidade = %s,
            sg_uf = %s,
            no_municipio = %s,
            nu_ano_censo = %s,
            qt_mat_total = %s
        WHERE co_entidade = %s
    """, (
        data["no_entidade"],
        data["sg_uf"],
        data["no_municipio"],
        data["nu_ano_censo"],
        data["qt_mat_total"],
        co_entidade
    ))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Instituição não encontrada"}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": "Instituição atualizada"}), 200

@app.delete("/instituicoesensino/<int:co_entidade>")
def delete_instituicao(co_entidade):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM instituicoes_ensino WHERE co_entidade = %s",
        (co_entidade,)
    )

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Instituição não encontrada"}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": "Instituição removida"}), 200

@app.get("/instituicoesensino/ranking/<int:ano>")
def ranking_instituicoes(ano):
    schema = RankingSchema()
    schema.load({"ano": ano})

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            no_entidade,
            co_entidade,
            sg_uf,
            co_uf,
            no_municipio,
            co_municipio,
            nu_ano_censo,
            qt_mat_bas,
            qt_mat_prof,
            qt_mat_eja,
            qt_mat_esp,
            qt_mat_fund,
            qt_mat_inf,
            qt_mat_med,
            qt_mat_zr_na,
            qt_mat_zr_rur,
            qt_mat_zr_urb,
            qt_mat_total
        FROM instituicoes_ensino
        WHERE nu_ano_censo = %s
        ORDER BY qt_mat_total DESC
        LIMIT 10
    """, (ano,))

    rows = cursor.fetchall()
    conn.close()

    ranking = []
    for idx, row in enumerate(rows, start=1):
        ranking.append({
            "no_entidade": row[0],
            "co_entidade": row[1],
            "sg_uf": row[2],
            "co_uf": row[3],
            "no_municipio": row[4],
            "co_municipio": row[5],
            "nu_ano_censo": row[6],
            "qt_mat_bas": row[7],
            "qt_mat_prof": row[8],
            "qt_mat_eja": row[9],
            "qt_mat_esp": row[10],
            "qt_mat_fund": row[11],
            "qt_mat_inf": row[12],
            "qt_mat_med": row[13],
            "qt_mat_zr_na": row[14],
            "qt_mat_zr_rur": row[15],
            "qt_mat_zr_urb": row[16],
            "qt_mat_total": row[17],
            "nu_ranking": idx
        })

    return jsonify(ranking), 200

if __name__ == "__main__":
    app.run(debug=True)
