from helpers.database.csv_reader import ler_csv_nordeste_json
from helpers.json_helper import write_json

CSV_PATH = 'microdados_ed_basica_2024.csv'
JSON_SAIDA = 'data/instituicoesensino.json'

dados_json = ler_csv_nordeste_json(CSV_PATH, limite=1000)

write_json(JSON_SAIDA, dados_json)

print("CSV do Nordeste convertido para JSON com sucesso.")
