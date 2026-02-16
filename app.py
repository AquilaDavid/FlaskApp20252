from flask import Flask, request, jsonify
from marshmallow import ValidationError
from psycopg2 import Error

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
    try:
        esquema = PaginationSchema()
        parametros = esquema.load(request.args)

        pagina = parametros["page"]
        limite = parametros["limit"]

        if pagina <= 0 or limite <= 0:
            return jsonify({"mensagem": "page e limit devem ser maiores que zero"}), 400

        deslocamento = (pagina - 1) * limite

        logger.info(f"Listando usuários | page={pagina}, limit={limite}")

        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id, nome, cpf, nascimento
            FROM usuarios
            LIMIT %s OFFSET %s
        """, (limite, deslocamento))

        usuarios = [
            {
                "id": linha[0],
                "nome": linha[1],
                "cpf": linha[2],
                "nascimento": linha[3]
            }
            for linha in cursor.fetchall()
        ]

        conexao.close()

        return jsonify({
            "page": pagina,
            "limit": limite,
            "total": total,
            "data": usuarios
        }), 200

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except Error as e:
        logger.error(f"Erro SQL: {e}")
        return jsonify({"mensagem": "Erro ao buscar usuários"}), 500


@app.get("/instituicoesensino")
def get_instituicoes():
    try:
        esquema = PaginationSchema()
        parametros = esquema.load(request.args)

        pagina = parametros["page"]
        limite = parametros["limit"]

        if pagina <= 0 or limite <= 0:
            return jsonify({"mensagem": "page e limit devem ser maiores que zero"}), 400

        deslocamento = (pagina - 1) * limite

        logger.info(f"Listando instituições | page={pagina}, limit={limite}")

        conexao = get_connection()
        cursor = conexao.cursor()

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
        """, (limite, deslocamento))

        instituicoes = [
            {
                "co_entidade": linha[0],
                "no_entidade": linha[1],
                "sg_uf": linha[2],
                "no_municipio": linha[3],
                "nu_ano_censo": linha[4],
                "qt_mat_total": linha[5]
            }
            for linha in cursor.fetchall()
        ]

        conexao.close()

        return jsonify({
            "page": pagina,
            "limit": limite,
            "total": total,
            "data": instituicoes
        }), 200

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except Error as e:
        logger.error(f"Erro SQL: {e}")
        return jsonify({"mensagem": "Erro ao buscar instituições"}), 500


@app.get("/instituicoesensino/ranking/<int:ano>")
def ranking_instituicoes(ano):
    try:
        if ano <= 0:
            return jsonify({"mensagem": "Ano inválido"}), 400

        esquema = RankingSchema()
        esquema.load({"ano": ano})

        logger.info(f"Gerando ranking | ano={ano}")

        conexao = get_connection()
        cursor = conexao.cursor()

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

        registros = cursor.fetchall()
        conexao.close()

        ranking = []
        for indice, linha in enumerate(registros, start=1):
            ranking.append({
                "no_entidade": linha[0],
                "co_entidade": linha[1],
                "sg_uf": linha[2],
                "co_uf": linha[3],
                "no_municipio": linha[4],
                "co_municipio": linha[5],
                "nu_ano_censo": linha[6],
                "qt_mat_bas": linha[7],
                "qt_mat_prof": linha[8],
                "qt_mat_eja": linha[9],
                "qt_mat_esp": linha[10],
                "qt_mat_fund": linha[11],
                "qt_mat_inf": linha[12],
                "qt_mat_med": linha[13],
                "qt_mat_zr_na": linha[14],
                "qt_mat_zr_rur": linha[15],
                "qt_mat_zr_urb": linha[16],
                "qt_mat_total": linha[17],
                "nu_ranking": indice
            })

        logger.info(f"Ranking gerado com {len(ranking)} instituições")

        return jsonify(ranking), 200

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except Error as e:
        logger.error(f"Erro SQL: {e}")
        return jsonify({"mensagem": "Erro ao gerar ranking"}), 500


if __name__ == "__main__":
    logger.info("Aplicação Flask iniciada")
    app.run(debug=True)
