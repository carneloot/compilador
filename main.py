import argparse
from reconhecedor.automato import Automato
from reconhecedor.lexico import analiseLexica
from hash.tabelahash import TabelaHash

def getArguments():
    parser = argparse.ArgumentParser(description='Compilador de PASCAL da disciplina de compiladores.')
    parser.add_argument('--automato', '-a', action='store',
                        default='automato.aut', required=False,
                        help='Arquivo para pegar o automato. Padrão: automato.aut')

    parser.add_argument('--reservadas', '-r', action='store',
                        default='reservadas.txt', required=False,
                        help='Arquivo para pegar as palavras reservadas. Padrão: reservadas.txt')
    
    parser.add_argument('--saida', '-s', action='store', dest='saida',
                        required=True,
                        help='Nome base para os arquivos de saida.')

    parser.add_argument('--pular-vazios', action='store_true', dest='skip_empty',
                        required=False,
                        help='Não escreve no arquivo da tabela hash os espaços vazios.')
    
    parser.add_argument('entrada', action='store', help='Arquivo de entrada')

    return parser.parse_args()
    
if __name__ == '__main__':

    argumentos = getArguments()

    automato = Automato.fromFile(argumentos.automato)
    tabela_ids = TabelaHash()

    arq_codigo = argumentos.entrada
    arq_palavras_reservadas = argumentos.reservadas

    # Faz a analise
    tokens, identificacores = analiseLexica(automato, arq_codigo, arq_palavras_reservadas)

    if tokens is not None:

        # Coloca os identificadores numa tabela hash
        for identificador in identificacores:
            tabela_ids[identificador] = identificador

        # Printa a tabela hash no arquivo
        with open(f'{argumentos.saida}_tabela.txt', 'w') as arquivo:
            tabela_ids.print(arquivo, print_none=not argumentos.skip_empty)

        # Printa os tokens
        with open(f'{argumentos.saida}_tokens.txt', 'w') as arquivo:
            for token, classificacao in tokens:
                print(f'Token: \'{token}\' Classificação: {classificacao}', file=arquivo)

