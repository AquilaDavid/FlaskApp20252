import pandas as pd

ESTADOS_NORDESTE = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']

def ler_csv_nordeste_json(caminho_csv, limite=None):
    """
    Lê o CSV do Censo Escolar de forma paginada,
    filtra apenas a Região Nordeste
    e retorna os dados em formato JSON (list[dict]).
    """

    resultado = []
    chunksize = 50000

    for chunk in pd.read_csv(
        caminho_csv,
        sep=';',
        encoding='latin1',
        chunksize=chunksize
    ):
        
        nordeste = chunk[chunk['SG_UF'].isin(ESTADOS_NORDESTE)]
        
        dados = nordeste[[
            'CO_ENTIDADE',
            'NO_ENTIDADE',
            'SG_UF',
            'CO_MUNICIPIO',
            'QT_MAT_BAS',
            'QT_MAT_PROF',
            'QT_MAT_EJA',
            'QT_MAT_ESP'
        ]]

        # AJUSTE IMPORTANTE: tratar NaN
        dados = dados.fillna(0)

        
        json_chunk = dados.rename(columns={
            'CO_ENTIDADE': 'codigo',
            'NO_ENTIDADE': 'nome',
            'SG_UF': 'co_uf',
            'CO_MUNICIPIO': 'co_municipio',
            'QT_MAT_BAS': 'qt_mat_bas',
            'QT_MAT_PROF': 'qt_mat_prof',
            'QT_MAT_EJA': 'qt_mat_eja',
            'QT_MAT_ESP': 'qt_mat_esp'
        }).to_dict(orient='records')

        resultado.extend(json_chunk)

       
        if limite and len(resultado) >= limite:
            return resultado[:limite]

    return resultado


if __name__ == "__main__":
    caminho_csv = "microdados_ed_basica_2024.csv"

    dados = ler_csv_nordeste_json(caminho_csv, limite=5)

    print(dados)
