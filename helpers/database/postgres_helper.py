import psycopg2
import os
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

load_dotenv()

UF_MAP = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29,
    "CE": 23, "DF": 53, "ES": 32, "GO": 52, "MA": 21,
    "MT": 51, "MS": 50, "MG": 31, "PA": 15, "PB": 25,
    "PR": 41, "PE": 26, "PI": 22, "RJ": 33, "RN": 24,
    "RS": 43, "RO": 11, "RR": 14, "SC": 42, "SP": 35,
    "SE": 28, "TO": 17
}

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()

    with open("helpers/database/schema.sql", "r", encoding="utf-8") as f:
        cursor.execute(f.read())

    conn.commit()
    cursor.close()
    conn.close()

def inserir_instituicoes_lote(dados):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO instituicoes_ensino (
            co_entidade, no_entidade, sg_uf, co_uf,
            no_municipio, co_municipio, nu_ano_censo,
            qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp,
            qt_mat_fund, qt_mat_inf, qt_mat_med
        )
        VALUES (
            %(co_entidade)s, %(no_entidade)s, %(sg_uf)s, %(co_uf)s,
            %(no_municipio)s, %(co_municipio)s, %(nu_ano_censo)s,
            %(qt_mat_bas)s, %(qt_mat_prof)s, %(qt_mat_eja)s, %(qt_mat_esp)s,
            %(qt_mat_fund)s, %(qt_mat_inf)s, %(qt_mat_med)s
        )
        ON CONFLICT (co_entidade, nu_ano_censo)
        DO UPDATE SET qt_mat_total = EXCLUDED.qt_mat_total;
    """

    dados_ajustados = []

    for d in dados:
        sg_uf = d.get("sg_uf")

        # ignora registro inválido
        if not sg_uf:
            continue

        d["co_uf"] = UF_MAP.get(sg_uf)

        # segurança extra
        if not d["co_uf"]:
            continue

        dados_ajustados.append(d)

    execute_batch(cursor, sql, dados_ajustados, page_size=1000)
    conn.commit()
    cursor.close()
    conn.close()
