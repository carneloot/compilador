from reconhecedor.automato import Automato
from reconhecedor.lexico import *

if __name__ == '__main__':

    automato = Automato.fromFile('./automato.aut')
    arq_codigo = './codigo.txt'
    arq_palavras_reservadas = './palavras_reservadas.txt'

    # automato.enableLogging()

    analiseLexica(automato, arq_codigo, arq_palavras_reservadas)

    #boolr, m = analiseLexica(automato, '11.11 123.a 123 nome')
    #print(m)
    input()

