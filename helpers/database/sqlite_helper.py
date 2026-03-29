import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, "database", "censo_escolar.db")
JSON_PATH = os.path.join(BASE_DIR, "data", "instituicoesensino.json")


def criar_tabela():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes_ensino (
            codigo INTEGER PRIMARY KEY,
            nome TEXT,
            co_uf TEXT,
            co_municipio INTEGER,
            qt_mat_bas INTEGER,
            qt_mat_prof INTEGER,
            qt_mat_eja INTEGER,
            qt_mat_esp INTEGER
        );
    """)

    conn.commit()
    conn.close()


def carregar_json():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for ie in dados:
        cursor.execute("""
            INSERT OR REPLACE INTO instituicoes_ensino (
                codigo, nome, co_uf, co_municipio,
                qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ie["codigo"],
            ie["nome"],
            ie["co_uf"],
            ie["co_municipio"],
            ie["qt_mat_bas"] or 0,
            ie["qt_mat_prof"] or 0,
            ie["qt_mat_eja"] or 0,
            ie["qt_mat_esp"] or 0
        ))

    conn.commit()
    conn.close()
