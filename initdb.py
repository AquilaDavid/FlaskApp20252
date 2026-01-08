from helpers.database.sqlite_helper import criar_tabela, carregar_json

if __name__ == "__main__":
    criar_tabela()
    carregar_json()
    print("✅ Banco SQLite criado e populado com sucesso")
