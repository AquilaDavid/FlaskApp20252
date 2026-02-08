import pandas as pd
from helpers.logger import logger


def ler_csv_nordeste_json(caminho_csv: str, ano: int):
    logger.info(f"Lendo CSV: {caminho_csv}")

    colunas = {
        "CO_ENTIDADE": "co_entidade",
        "NO_ENTIDADE": "no_entidade",
        "SG_UF": "sg_uf",
        "NO_MUNICIPIO": "no_municipio",
        "CO_MUNICIPIO": "co_municipio",
        "QT_MAT_BAS": "qt_mat_bas",
        "QT_MAT_PROF": "qt_mat_prof",
        "QT_MAT_EJA": "qt_mat_eja",
        "QT_MAT_ESP": "qt_mat_esp",
        "QT_MAT_FUND": "qt_mat_fund",
        "QT_MAT_INF": "qt_mat_inf",
        "QT_MAT_MED": "qt_mat_med",
        "QT_MAT_ZR_NA": "qt_mat_zr_na",
        "QT_MAT_ZR_RUR": "qt_mat_zr_rur",
        "QT_MAT_ZR_URB": "qt_mat_zr_urb",
        "QT_MAT_TOTAL": "qt_mat_total",
    }

    # 🔹 lê somente o cabeçalho
    colunas_csv = pd.read_csv(
        caminho_csv,
        sep=";",
        encoding="latin1",
        nrows=0
    ).columns

    # 🔹 mantém apenas colunas que realmente existem
    colunas_validas = {
        k: v for k, v in colunas.items() if k in colunas_csv
    }

    logger.info(f"Colunas válidas usadas: {list(colunas_validas.keys())}")

    dados_processados = []

    for chunk in pd.read_csv(
        caminho_csv,
        sep=";",
        encoding="latin1",
        usecols=colunas_validas.keys(),
        low_memory=False,
        chunksize=50000
    ):
        chunk = chunk.rename(columns=colunas_validas)
        chunk["nu_ano_censo"] = ano

        colunas_numericas = [
            c for c in chunk.columns
            if c.startswith("qt_") or c in ["co_entidade", "co_municipio"]
        ]

        chunk[colunas_numericas] = chunk[colunas_numericas].fillna(0)
        chunk = chunk[chunk["sg_uf"].notna()]

        dados_processados.extend(chunk.to_dict(orient="records"))

    logger.info(f"Total de registros lidos ({ano}): {len(dados_processados)}")
    return dados_processados

