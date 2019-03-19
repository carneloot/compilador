class Estado:

    def __init__(self, id: int, nome: str, label: str = 'Erro'):
        self._id = id
        self._nome = nome
        if label is None:
            self._label = 'Erro'

        else:
            self._label = label

    def getId(self) -> int:
        return self._id

    def setId(self, id: int):
        self._id = id

    def getNome(self) -> str:
        return self._nome

    def setNome(self, nome: str):
        self._nome = nome

    def getLabel(self) -> str:
        return self._label

    def setLabel(self, label: str):
        self._label = label

    def __str__(self):
        return f'{self._id}({self._nome})'
