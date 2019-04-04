from reconhecedor.automato import Automato
from reconhecedor.lexico import *

if __name__ == '__main__':

    automato = Automato.fromFile('./automato.aut')

    automato.enableLogging()
    boolr, m = analiseLexica(automato, '11.11 123.a 123 nome')
    print(m)
    input()

