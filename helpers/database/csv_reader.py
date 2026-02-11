import pandas as pd
from helpers.logger import logger


def ler_csv_nordeste_json(caminho_csv: str, ano: int):
    logger.info(f"Lendo CSV: {caminho_csv}")

    colunas = {
        "CO_ENTIDADE": "co_entidade",
        "NO_ENTIDADE": "no_entidade",
        "SG_UF": "sg_uf",
        "CO_UF": "co_uf",
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
    }

    colunas_csv = pd.read_csv(
        caminho_csv,
        sep=";",
        encoding="latin1",
        nrows=0
    ).columns

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
            if c.startswith("qt_") or c in ["co_entidade", "co_municipio", "co_uf"]
        ]

        chunk[colunas_numericas] = chunk[colunas_numericas].fillna(0)
        chunk = chunk[chunk["sg_uf"].notna()]

        # 🔧 GARANTE TODAS AS COLUNAS qt_*
        colunas_qt = [
            "qt_mat_bas", "qt_mat_prof", "qt_mat_eja", "qt_mat_esp",
            "qt_mat_fund", "qt_mat_inf", "qt_mat_med",
            "qt_mat_zr_na", "qt_mat_zr_rur", "qt_mat_zr_urb"
        ]

        for col in colunas_qt:
            if col not in chunk.columns:
                chunk[col] = 0

        # 🔥 total correto
        chunk["qt_mat_total"] = (
            chunk["qt_mat_bas"]
            + chunk["qt_mat_prof"]
            + chunk["qt_mat_eja"]
            + chunk["qt_mat_esp"]
            + chunk["qt_mat_fund"]
            + chunk["qt_mat_inf"]
            + chunk["qt_mat_med"]
        )

        dados_processados.extend(chunk.to_dict(orient="records"))

    logger.info(f"Total de registros lidos ({ano}): {len(dados_processados)}")
    return dados_processados
