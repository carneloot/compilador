import argparse
from modules.automato import Automato
from modules.lexico import analiseLexica
from modules.sintatico import AnalisadorDescendente
from modules.tabelahash import TabelaHash
import sys
import json

def getArguments():
    parser = argparse.ArgumentParser(description='Compilador de PASCAL da disciplina de compiladores.')
    parser.add_argument('--automato', '-a', action='store',
                        default='automato.aut', required=False,
                        help='Arquivo para pegar o automato. Padrão: automato.aut')

    parser.add_argument('--reservadas', '-r', action='store',
                        default='reservadas.txt', required=False,
                        help='Arquivo para pegar as palavras reservadas. Padrão: reservadas.txt')

    parser.add_argument('--saida', '-s', action='store', dest='saida',
                        default='saida', required=False,
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
    tokensEspaco, identificacores = analiseLexica(automato, arq_codigo, arq_palavras_reservadas)

    if tokensEspaco is None:
        exit(1)

    # Filtra os espaços do vetor
    tokens = []
    for item in tokensEspaco:
        if item.tipo != 'Espaco':
            item.token = item.token.lower()
            tokens.append(item)

    # Coloca os identificadores numa tabela hash
    # for identificador in identificacores:
    #     tabela_ids[identificador] = identificador


    # Printa os tokens
    with open(f'{argumentos.saida}_tokens.txt', 'w') as arquivo:
        for tokenInfo in tokens:
            print(f'Token: \'{tokenInfo.token}\' Classificação: {tokenInfo.tipo}', file=arquivo)

    # Analise sintatica
    descendente = AnalisadorDescendente(tokens, arq_codigo, tabela_ids)

    ast = descendente.run()

    json.dump(ast, sys.stdout, default=lambda x: x.__dict__, indent=4, sort_keys=True)

    # Printa a tabela hash no arquivo
    with open(f'{argumentos.saida}_tabela.txt', 'w') as arquivo:
        tabela_ids.print(arquivo, print_none=not argumentos.skip_empty)
