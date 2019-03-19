from reconhecedor.automato import Automato

if __name__ == '__main__':

    automata = Automato()

    # Setando os estados
    for i in range(8):
        automata.setState(i)

    # Estados finais e inicial
    automata.setStartState(0)

    automata.setFinalState(2)
    automata.setFinalState(4)
    automata.setFinalState(6)
    automata.setFinalState(7)

    # Transicoes
    automata.setTransition(0, 0, '0')
    automata.setTransition(1, 3, '0')
    automata.setTransition(2, 0, '0')
    automata.setTransition(3, 2, '0')
    automata.setTransition(4, 3, '0')
    automata.setTransition(5, 6, '0')
    automata.setTransition(6, 2, '0')
    automata.setTransition(7, 6, '0')

    automata.setTransition(0, 1, '1')
    automata.setTransition(1, 5, '1')
    automata.setTransition(2, 1, '1')
    automata.setTransition(3, 4, '1')
    automata.setTransition(4, 5, '1')
    automata.setTransition(5, 7, '1')
    automata.setTransition(6, 4, '1')
    automata.setTransition(7, 7, '1')

    entrada = '11101100100'

    print(automata.test(entrada))
