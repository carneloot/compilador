import sys


class TabelaHash:

    def __init__(self, tamanho: int = 211, alpha: int = 10):
        self._alpha = alpha
        self._tamanho = tamanho
        self._tabela = [None for i in range(tamanho)]

    def __setitem__(self, key, value):
        return self.addItem(key, value)

    def __getitem__(self, key):
        return self.getItem(key)

    def __hash(self, chave: str):
        h = 0

        for i, letra in enumerate(chave):
            h = self._alpha * h + ord(letra)

        return h % self._tamanho

    def getPos(self, chave: str):
        return self.__hash(chave)

    def print(self, filesrc=sys.stdout, print_none=True):
        for i, valor in enumerate(self._tabela):
            if print_none or valor is not None:
                print(f'{str(i).zfill(3)}: {valor}', file=filesrc)

    def addItem(self, key, value):
        if type(key) != str:
            raise TypeError('Tipo da chave utilizada deve ser uma string.')

        posicao = self.__hash(key)
        self._tabela[posicao] = value

    def getItem(self, key):
        if type(key) != str:
            raise TypeError('Tipo da chave utilizada deve ser uma string.')

        posicao = self.__hash(key)
        return self._tabela[posicao]


if __name__ == '__main__':
    tabela = TabelaHash()

    tabela['teste'] = 'teste'

    with open('arquivo.txt', 'w') as arquivo:
        tabela.print(arquivo)
