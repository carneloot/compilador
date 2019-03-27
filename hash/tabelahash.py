class TabelaHash:
    ALPHA = 10

    def __init__(self, tamanho: int = 211):
        self._tamanho = tamanho
        self._tabela = [None for i in range(tamanho)]

    def __hash(self, chave: str):
        h = 0

        for i, letra in enumerate(chave):
            h = TabelaHash.ALPHA * h + ord(letra)

        return h % self._tamanho

    def __setitem__(self, key, value):
        if type(key) != str:
            return None

        posicao = self.__hash(key)
        self._tabela[posicao] = value

    def __getitem__(self, key):
        if type(key) != str:
            return None

        posicao = self.__hash(key)
        return self._tabela[posicao]


if __name__ == '__main__':
    tabela = TabelaHash()

    tabela['teste'] = 10

    print(tabela['teste'])
