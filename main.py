from reconhecedor.automato import Automato
from reconhecedor.lexico import analiseLexica

if __name__ == '__main__':

    automato = Automato.fromFile('./automato.aut')
    arq_codigo = './codigo.txt'
    arq_palavras_reservadas = './palavras_reservadas.txt'

    print(analiseLexica(automato, arq_codigo, arq_palavras_reservadas))
