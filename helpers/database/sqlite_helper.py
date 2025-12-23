import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "censo_escolar.db")
JSON_PATH = os.path.join(BASE_DIR, "data", "instituicoesensino.json")


def get_connection():
    return sqlite3.connect(DB_PATH)


def criar_tabela():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_connection()
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
    conn = get_connection()
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
            ie.get("qt_mat_bas", 0),
            ie.get("qt_mat_prof", 0),
            ie.get("qt_mat_eja", 0),
            ie.get("qt_mat_esp", 0)
        ))

    conn.commit()
    conn.close()


def listar_instituicoes(limit=100, offset=0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM instituicoes_ensino
        LIMIT ? OFFSET ?
    """, (limit, offset))

    colunas = [desc[0] for desc in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]

    conn.close()
    return dados


def buscar_por_codigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM instituicoes_ensino WHERE codigo = ?
    """, (codigo,))

    row = cursor.fetchone()
    if not row:
        return None

    colunas = [desc[0] for desc in cursor.description]
    conn.close()

    return dict(zip(colunas, row))


def inserir_instituicao(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO instituicoes_ensino VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["codigo"],
        data["nome"],
        data["co_uf"],
        data["co_municipio"],
        data.get("qt_mat_bas", 0),
        data.get("qt_mat_prof", 0),
        data.get("qt_mat_eja", 0),
        data.get("qt_mat_esp", 0)
    ))

    conn.commit()
    conn.close()


def atualizar_instituicao(codigo, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE instituicoes_ensino
        SET nome = ?, co_uf = ?, co_municipio = ?,
            qt_mat_bas = ?, qt_mat_prof = ?, qt_mat_eja = ?, qt_mat_esp = ?
        WHERE codigo = ?
    """, (
        data["nome"],
        data["co_uf"],
        data["co_municipio"],
        data.get("qt_mat_bas", 0),
        data.get("qt_mat_prof", 0),
        data.get("qt_mat_eja", 0),
        data.get("qt_mat_esp", 0),
        codigo
    ))

    conn.commit()
    conn.close()


def deletar_instituicao(codigo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM instituicoes_ensino WHERE codigo = ?
    """, (codigo,))

    conn.commit()
    conn.close()
