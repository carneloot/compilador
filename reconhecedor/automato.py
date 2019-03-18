from estado import Estado
from transicao import Transicao


class Automato:

    def __init__(self):
        self._states = {}
        self._final_states = {}
        self._transitions = {}
        self._start_state = None

    def setState(self, id: int):
        self._states[id] = Estado(id, str(id), str(id))

    def setFinalState(self, id: int):
        if self._states[id] is None:
            raise Error('Adicione o estado antes de setar como final')

        self._final_states[id] = self._states[id]

    def setStartState(self, id: int):
        if self._states[id] is None:
            raise Error('Adicione o estado antes de setar como inicial')

        self._start_state = self._states[id]

    def setTransition(self, origem: int, destino: int, simbolo: str):
        estado_origem = self._states[origem]
        estado_destino = self._states[destino]

        self._transitions.add(
            Transicao(estado_origem, estado_destino, simbolo))

    def getTransition(self, origem: int, simbolo: str) -> Transicao:
        for transition in self._transitions:
            if transition.getOrigem() == origem and transition.getSimbolo() == simbolo:
                return transition

        return None

    def getStartState(self) -> Estado:
        return self._start_state

    def getState(self, id: int) -> Estado:
        return self._states[id]

    def getFinalState(self, id: int) -> bool:
        return self._final_states[id]

    def isStartState(self, id: int) -> bool:
        return self._states[id] == self._start_state

    def isFinalState(self, id: int) -> bool:
        return self._final_states[id] is not None

    def getFinalStateSize(self):
        return len(self._final_states)
