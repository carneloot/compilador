from .estado import Estado
from .transicao import Transicao
import re


class Automato:

    def __init__(self):
        self._states = {}
        self._final_states = {}
        self._transitions = []
        self._start_state = None
        self._log = False

    def enableLogging(self):
        self._log = True

    def disableLogging(self):
        self._log = False

    def log(self, text: str):
        if self._log:
            print('LOG:', text)

    def setState(self, id: int, label: str = None):
        self._states[id] = Estado(id, f'estado{id}', label)
        self.log(f'Adicionando o estado{id} no automato.')

    def setFinalState(self, id: int):
        if self._states[id] is None:
            raise Exception('Adicione o estado antes de setar como final')

        self._final_states[id] = self._states[id]

        self.log(f'Estado{id} agora é final')

    def setStartState(self, id: int):
        if self._states[id] is None:
            raise Exception('Adicione o estado antes de setar como inicial')

        self._start_state = self._states[id]

        self.log(f'Estado{id} agora é inicial')

    def setTransition(self, origem: int, destino: int, simbolo: str):
        estado_origem = self._states[origem]
        estado_destino = self._states[destino]

        self._transitions.append(
            Transicao(estado_origem, estado_destino, simbolo))

        self.log((
            f'Transição do estado {origem} para {destino} '
            f'com simbolo "{simbolo}" criada'))

    def getTransition(self, origem: int, simbolo: str) -> Transicao:
        for transition in self._transitions:
            if transition.getOrigem().getId() == origem and \
               self.checkSymbol(transition.getSimbolo(), simbolo):
                return transition

        return None

    @staticmethod
    def checkSymbol(regex, symbol):
        return re.compile(regex).match(symbol) is not None

    def getStartState(self) -> Estado:
        return self._start_state

    def getState(self, id: int) -> Estado:
        return self._states[id]

    def getFinalState(self, id: int) -> bool:
        return self._final_states[id]

    def isStartState(self, id: int) -> bool:
        return self._states[id] == self._start_state

    def isFinalState(self, id: int) -> bool:
        return self._final_states.get(id) is not None

    def getFinalStateSize(self):
        return len(self._final_states)

    def test(self, entrada: str) -> (bool, str):

        self.log('Iniciando teste')

        if entrada == '':
            return (self._start_state in self._final_states,
                    self.getStartState().getLabel())

        origem = self.getStartState()

        for posicao, letra in enumerate(entrada):
            transicao = self.getTransition(origem.getId(), letra)

            # Nao encontrou a transicao
            if transicao is None:
                self.log((
                    f'Nao foi possivel encontrar uma transicao '
                    f'para a letra \'{letra}\' na posicao \'{posicao}\'. '
                    f'Estado atual: {origem.getNome()}.'))
                return (False, 'Erro')

            destino = transicao.getDestino()

            self.log((
                f'{origem.getNome()} leu "{letra}" '
                f'foi para {destino.getNome()}'))

            origem = destino

        return (self.isFinalState(origem.getId()), origem.getLabel())
