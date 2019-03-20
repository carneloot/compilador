from reconhecedor.automato import Automato

if __name__ == '__main__':

    automato = Automato.fromFile('./automato.aut')

    automato.enableLogging()

    print(automato.test('3.141592653589'))
