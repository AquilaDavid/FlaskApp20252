from flask import Flask, request, jsonify
from helpers.database.sqlite_helper import get_connection
from helpers.logger import logger

app = Flask(__name__)


@app.get("/")
def index():
    logger.info("Endpoint raiz acessado")
    return {"versao": "2.0.0", "banco": "SQLite"}, 200



# USUÁRIOS


@app.get("/usuarios")
def get_usuarios():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    logger.info(f"Listando usuários | page={page}, limit={limit}")

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



# INSTITUIÇÕES DE ENSINO


@app.get("/instituicoesensino")
def get_instituicoes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
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
        LIMIT ? OFFSET ?
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



# RANKING DE MATRÍCULAS


@app.get("/instituicoesensino/ranking/<int:ano>")
def ranking_instituicoes(ano):
    if ano not in (2022, 2023, 2024):
        logger.warning(f"Ano inválido informado: {ano}")
        return {"erro": "Ano inválido. Utilize 2022, 2023 ou 2024."}, 400

    logger.info(f"Gerando ranking de instituições | ano={ano}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            no_entidade,
            co_entidade,
            no_uf,
            sg_uf,
            co_uf,
            no_municipio,
            co_municipio,
            no_mesorregiao,
            co_mesorregiao,
            no_microrregiao,
            co_microrregiao,
            nu_ano_censo,
            no_regiao,
            co_regiao,
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
        WHERE nu_ano_censo = ?
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
            "no_uf": row[2],
            "sg_uf": row[3],
            "co_uf": row[4],
            "no_municipio": row[5],
            "co_municipio": row[6],
            "no_mesorregiao": row[7],
            "co_mesorregiao": row[8],
            "no_microrregiao": row[9],
            "co_microrregiao": row[10],
            "nu_ano_censo": row[11],
            "no_regiao": row[12],
            "co_regiao": row[13],
            "qt_mat_bas": row[14],
            "qt_mat_prof": row[15],
            "qt_mat_eja": row[16],
            "qt_mat_esp": row[17],
            "qt_mat_fund": row[18],
            "qt_mat_inf": row[19],
            "qt_mat_med": row[20],
            "qt_mat_zr_na": row[21],
            "qt_mat_zr_rur": row[22],
            "qt_mat_zr_urb": row[23],
            "qt_mat_total": row[24],
            "nu_ranking": idx
        })

    logger.info(f"Ranking gerado com {len(ranking)} instituições | ano={ano}")

    return jsonify(ranking), 200


if __name__ == "__main__":
    logger.info("Aplicação Flask iniciada")
    app.run(debug=True)
