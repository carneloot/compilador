from reconhecedor.automato import Automato

if __name__ == '__main__':

    automata = Automato()

    # Setando os estados

    automata.setState(1)
    automata.setState(2,  'ID/Reservada')
    automata.setState(3,  'Espaço')
    automata.setState(4,  'Inteiro')
    automata.setState(5,  'Real')
    automata.setState(6,  'Símbolo especial')
    automata.setState(7,  'Símbolo especial')
    automata.setState(8,  'Símbolo composto')
    automata.setState(9,  'Símbolo especial')
    automata.setState(10, 'Símbolo especial')
    automata.setState(11, 'Símbolo especial')
    automata.setState(12, 'Símbolo especial')
    automata.setState(13, 'Símbolo especial')
    automata.setState(14, 'Símbolo especial')

    # Estados finais e inicial
    automata.setStartState(1)

    automata.setFinalState(2)
    automata.setFinalState(3)
    automata.setFinalState(4)
    automata.setFinalState(5)
    automata.setFinalState(6)
    automata.setFinalState(7)
    automata.setFinalState(8)
    automata.setFinalState(9)
    automata.setFinalState(10)
    automata.setFinalState(11)
    automata.setFinalState(12)
    automata.setFinalState(13)
    automata.setFinalState(14)

    # Transicoes
    automata.setTransition(1, 2, '[a-z]')
    automata.setTransition(2, 2, '[a-z0-9]')

    automata.setTransition(1, 3, '[ \\n]')
    automata.setTransition(3, 3, '[ \\n]')

    automata.setTransition(1, 4, '[0-9]')
    automata.setTransition(4, 4, '[0-9]')
    automata.setTransition(4, 5, '\.')
    automata.setTransition(5, 5, '[0-9]')

    automata.setTransition(1, 6, '[\',;\)=/\[\]\{\}_]')

    automata.setTransition(1, 7, ':')
    automata.setTransition(7, 8, '=')

    automata.setTransition(1, 9, '\.')
    automata.setTransition(9, 8, '\.')

    automata.setTransition(1, 10, '<')
    automata.setTransition(10, 8, '[=>]')

    automata.setTransition(1, 11, '>')
    automata.setTransition(11, 8, '=')

    automata.setTransition(1, 12, '\(')
    automata.setTransition(12, 8, '\*')

    automata.setTransition(1, 13, '\*')
    automata.setTransition(13, 8, '\)')

    automata.setTransition(1, 14, '[+-]')
    automata.setTransition(14, 4, '[0-9]')

    entrada = ''

    print(automata.test(entrada))
