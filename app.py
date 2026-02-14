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

    logger.info(f"Listando usuários | page={page}, limit={limit}")

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


# =========================
# INSTITUIÇÕES
# =========================
@app.get("/instituicoesensino")
def get_instituicoes():
    schema = PaginationSchema()
    params = schema.load(request.args)

    page = params["page"]
    limit = params["limit"]
    offset = (page - 1) * limit

    logger.info(f"Listando instituições | page={page}, limit={limit}")

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


# =========================
# RANKING
# =========================
@app.get("/instituicoesensino/ranking/<int:ano>")
def ranking_instituicoes(ano):
    schema = RankingSchema()
    schema.load({"ano": ano})

    logger.info(f"Gerando ranking | ano={ano}")

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

    logger.info(f"Ranking gerado com {len(ranking)} instituições")

    return jsonify(ranking), 200


if __name__ == "__main__":
    logger.info("Aplicação Flask iniciada")
    app.run(debug=True)
