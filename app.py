from flask import Flask, request, jsonify

from models.Usuario import Usuario
from models.InstituicaoEnsino import InstituicaoEnsino
from helpers.json_helper import read_json, write_json

app = Flask(__name__)

USUARIOS_FILE = "data/usuarios.json"
INSTITUICOES_FILE = "data/instituicoesensino.json"


@app.get("/")
def index():
    return {"versao": "2.0.0"}, 200



# USUÁRIOS

@app.get("/usuarios")
def getUsuarios():
    usuarios_json = read_json(USUARIOS_FILE)
    return jsonify(usuarios_json), 200


@app.get("/usuarios/<int:id>")
def getUsuarioById(id):
    usuarios = read_json(USUARIOS_FILE)

    for usuario in usuarios:
        if usuario["id"] == id:
            return jsonify(usuario), 200

    return {"erro": "Usuário não encontrado"}, 404


@app.post("/usuarios")
def createUsuario():
    data = request.get_json()
    usuarios = read_json(USUARIOS_FILE)

    novo_id = max(u["id"] for u in usuarios) + 1 if usuarios else 1

    novo_usuario = Usuario(
        novo_id,
        data["nome"],
        data["cpf"],
        data["nascimento"]
    )

    usuarios.append(novo_usuario.to_json())
    write_json(USUARIOS_FILE, usuarios)

    return novo_usuario.to_json(), 201


@app.put("/usuarios/<int:id>")
def updateUsuario(id):
    data = request.get_json()
    usuarios = read_json(USUARIOS_FILE)

    for usuario in usuarios:
        if usuario["id"] == id:
            usuario["nome"] = data.get("nome", usuario["nome"])
            usuario["cpf"] = data.get("cpf", usuario["cpf"])
            usuario["nascimento"] = data.get("nascimento", usuario["nascimento"])

            write_json(USUARIOS_FILE, usuarios)
            return usuario, 200

    return {"erro": "Usuário não encontrado"}, 404


@app.delete("/usuarios/<int:id>")
def deleteUsuario(id):
    usuarios = read_json(USUARIOS_FILE)

    usuarios_filtrados = [u for u in usuarios if u["id"] != id]

    if len(usuarios_filtrados) == len(usuarios):
        return {"erro": "Usuário não encontrado"}, 404

    write_json(USUARIOS_FILE, usuarios_filtrados)
    return {"mensagem": "Usuário removido com sucesso"}, 200



# INSTITUIÇÕES DE ENSINO


@app.get("/instituicoesensino")
def getInstituicoes():
    instituicoes = read_json(INSTITUICOES_FILE)
    return jsonify(instituicoes), 200


@app.get("/instituicoesensino/<int:codigo>")
def getInstituicaoByCodigo(codigo):
    instituicoes = read_json(INSTITUICOES_FILE)

    for ie in instituicoes:
        if ie["codigo"] == codigo:
            return jsonify(ie), 200

    return {"erro": "Instituição não encontrada"}, 404


@app.post("/instituicoesensino")
def createInstituicao():
    data = request.get_json()
    instituicoes = read_json(INSTITUICOES_FILE)

    nova_ie = data
    instituicoes.append(nova_ie)

    write_json(INSTITUICOES_FILE, instituicoes)
    return nova_ie, 201


@app.put("/instituicoesensino/<int:codigo>")
def updateInstituicao(codigo):
    data = request.get_json()
    instituicoes = read_json(INSTITUICOES_FILE)

    for ie in instituicoes:
        if ie["codigo"] == codigo:
            ie.update(data)
            write_json(INSTITUICOES_FILE, instituicoes)
            return ie, 200

    return {"erro": "Instituição não encontrada"}, 404


@app.delete("/instituicoesensino/int:codigo>")
def deleteInstituicao(codigo):
    instituicoes = read_json(INSTITUICOES_FILE)

    novas_ie = [ie for ie in instituicoes if ie["codigo"] != codigo]

    if len(novas_ie) == len(instituicoes):
        return {"erro": "Instituição não encontrada"}, 404

    write_json(INSTITUICOES_FILE, novas_ie)
    return {"mensagem": "Instituição removida com sucesso"}, 200


if __name__ == "__main__":
    app.run(debug=True)
