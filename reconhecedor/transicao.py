from estado import Estado


class Transicao:

    def __init__(self, origem: Estado, destino: Estado, simbolo: str):
        self._origem = origem
        self._destino = destino
        self._simbolo = simbolo

    def getOrigem(self) -> Estado:
        return self._origem

    def setOrigem(self, origem: Estado):
        self._origem = origem

    def getDestino(self) -> Estado:
        return self._destino

    def setDestino(self, destino: Estado):
        self._destino = destino

    def getSimbolo(self) -> str:
        return self._simbolo

    def setSimbolo(self, simbolo: str):
        self._simbolo = simbolo

    def __eq__(self, other):
        if self.getOrigem() != other.getOrigem():
            return False
        if self.getDestino() != other.getDestino():
            return False
        if self.getSimbolo() != other.getSimbolo():
            return False
