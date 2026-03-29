import json
from models.InstituicaoEnsino import InstituicaoEnsino


def getInstituicoesEnsino():

    instituicoesEnsino = []

    # IE no formato JSON lido do arquivo.
    with open('data/instituicoesensino.json', 'r', encoding='utf-8') as f:
        instituicoesEnsinoJson = json.load(f)

    # Conversão para o objeto de InstituicaoEnsino.
    for instituicaoEnsinoJson in instituicoesEnsinoJson:
        ie = InstituicaoEnsino(
            instituicaoEnsinoJson["id"],
            instituicaoEnsinoJson["nome_instituicao"],
            instituicaoEnsinoJson["quantidade_matriculas_basico"],
            instituicaoEnsinoJson["codigo_uf"],
            instituicaoEnsinoJson["nome_uf"],
            instituicaoEnsinoJson["municipio"],
            instituicaoEnsinoJson["mesorregiao"],
            instituicaoEnsinoJson["microrregiao"]
        )
        instituicoesEnsino.append(ie)

    return instituicoesEnsino
 

