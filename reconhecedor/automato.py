class Reconhecedor:

    def __init__(self, states:dict, startState:Estado, finalStates:dict, transitions:dict):
        self._states: dict = states
        self._finalStates: dict = finalStates
        self._startState: Estado = startState

        pass
    

    def automata():
        pass
    
    def setState(id:int):
        pass

    def setFinalState(id:int):
        pass

    def setTransition(origin:int, destiny:int, symbol:str):
        pass
    
    def getTransition(origin:int, symbol:str) -> Transicao:
        pass
    
    def getStartState() -> Estado:
        pass

    def getFinalState(id:int) -> bool:
        pass
    
    def getState(id:int) -> bool:
        pass
    
    def isStartState(id:int) -> bool:
        pass

    def isFinalState(id:int) -> bool:
        pass
    
    def getFinalStateSize():
        pass
    
    def message():
        pass
