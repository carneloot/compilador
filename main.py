from reconhecedor.automato import Automato
from reconhecedor.lexico import *

if __name__ == '__main__':

    automato = Automato.fromFile('./automato.aut')

    automato.enableLogging()
    boolr, m = analiseLexica(automato, 'nome 2 3.a 123415')
    print(m)

