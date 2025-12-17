class InstituicaoEnsino():

    def __init__(self, codigo, nome, co_uf, co_municipio,
                 qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp):
        self.codigo = codigo
        self.nome = nome
        self.co_uf = co_uf
        self.co_municipio = co_municipio
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp

    def __repr__(self):
        return f'<InstituicaoEnsino {self.codigo} - {self.nome}>'

    
    def to_json(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "co_uf": self.co_uf,
            "co_municipio": self.co_municipio,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_prof": self.qt_mat_prof,
            "qt_mat_eja": self.qt_mat_eja,
            "qt_mat_esp": self.qt_mat_esp
        }

    
    @staticmethod
    def from_json(data: dict):
        return InstituicaoEnsino(
            data["codigo"],
            data["nome"],
            data["co_uf"],
            data["co_municipio"],
            data["qt_mat_bas"],
            data["qt_mat_prof"],
            data.get("qt_mat_eja", 0),  
            data["qt_mat_esp"]
        )