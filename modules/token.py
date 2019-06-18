import json

class Token:
    def __init__(self, token, tipo, linha, coluna):
        self.token = token
        self.tipo = tipo
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        return json.dumps(self.__dict__)
