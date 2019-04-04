from reconhecedor.automato import Automato
from palavras_reservadas import *

if __name__ == '__main__':

    automato = Automato.fromFile('./automato.aut')

    automato.enableLogging()

    palavras_reservadas = criar_palavras_reservadas("palavras_reservadas.txt")

    print(automato.test('3.141592653589'))
