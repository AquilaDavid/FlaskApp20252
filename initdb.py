import os
from helpers.database.sqlite_helper import (
    criar_tabela,
    inserir_instituicoes_lote
)
from helpers.database.csv_reader import read_censo_csv_paginated
from helpers.logger import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILES = {
    2022: os.path.join(BASE_DIR, "microdados_ed_basica_2022.csv"),
    2023: os.path.join(BASE_DIR, "microdados_ed_basica_2023.csv"),
    2024: os.path.join(BASE_DIR, "microdados_ed_basica_2024.csv"),

}


def carregar_dados():
    logger.info("==== INICIANDO CARGA DO CENSO ESCOLAR ====")

   
    criar_tabela()

    
    for ano, csv_path in CSV_FILES.items():

        if not os.path.exists(csv_path):
            logger.warning(
                f"Arquivo CSV não encontrado para o ano {ano}: {csv_path}"
            )
            continue

        logger.info(f"Iniciando carga do ano {ano}")

        
        total_registros = 0

        for page in read_censo_csv_paginated(
            csv_path=csv_path,
            ano=ano,
            page_size=10000
        ):
            inserir_instituicoes_lote(page)
            total_registros += len(page)

        logger.info(
            f"Carga do ano {ano} finalizada. "
            f"Total de registros inseridos: {total_registros}"
        )

    logger.info("==== CARGA DO CENSO ESCOLAR FINALIZADA ====")


if __name__ == "__main__":
    carregar_dados()
