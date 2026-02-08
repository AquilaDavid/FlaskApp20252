import os
from helpers.database.postgres_helper import (
    criar_tabela,              # 🔧 ajuste aqui
    inserir_instituicoes_lote
)
from helpers.database.csv_reader import ler_csv_nordeste_json
from helpers.logger import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILES = {
    2022: os.path.join(BASE_DIR, "microdados_ed_basica_2022.csv"),
    2023: os.path.join(BASE_DIR, "microdados_ed_basica_2023.csv"),
    2024: os.path.join(BASE_DIR, "microdados_ed_basica_2024.csv"),
}


def carregar_dados():
    logger.info("==== INICIANDO CARGA DO CENSO ESCOLAR ====")

    # 🔧 agora cria uf + instituicoes_ensino
    criar_tabela()

    for ano, csv_path in CSV_FILES.items():

        if not os.path.exists(csv_path):
            logger.warning(
                f"Arquivo CSV não encontrado para o ano {ano}: {csv_path}"
            )
            continue

        logger.info(f"Iniciando carga do ano {ano}")

        # leitura do CSV (já filtrado e pronto para insert)
        dados = ler_csv_nordeste_json(
            caminho_csv=csv_path,
            ano=ano
        )

        inserir_instituicoes_lote(dados)

        logger.info(
            f"Carga do ano {ano} finalizada. "
            f"Total de registros inseridos: {len(dados)}"
        )

    logger.info("==== CARGA DO CENSO ESCOLAR FINALIZADA ====")


if __name__ == "__main__":
    carregar_dados()
