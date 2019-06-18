from typing import List

from .automato import Automato
from .palavras_reservadas import criar_palavras_reservadas
from .token import Token


def analiseLexica(automato: Automato, nome_arq_codigo: str, nome_arq_palavras_reservadas: str):
    qtd_linhas = 0
    vetor_de_token_info = []

    palavras_reservadas = criar_palavras_reservadas(nome_arq_palavras_reservadas)

    em_comentario = False

    with open(nome_arq_codigo, 'r') as arq:
        conteudo_arq = arq.read()
        conteudo_arq = conteudo_arq.split('\n')

        while(qtd_linhas < len(conteudo_arq)):
            linha = conteudo_arq[qtd_linhas]

            linha_correta, tokens_info = classificaTokens(automato, linha, qtd_linhas + 1, em_comentario)

            if linha_correta is True:
                tokens_info.pop(0)
                for token_info in tokens_info:

                    if token_info.tipo == 'Entrada Comentario':
                        em_comentario = True

                    if not em_comentario:
                        vetor_de_token_info.append(token_info)

                    if token_info.tipo == 'Saida Comentario':
                        if not em_comentario:
                            vetor_de_token_info.append(token_info)

                        em_comentario = False

            else:
                erro_resultado = tokens_info
                print(f'./{nome_arq_codigo}:{qtd_linhas+1}:{erro_resultado[0]}: {erro_resultado[2]}. Depois do token "{erro_resultado[1]}"')
                return None, None

            qtd_linhas += 1
    # vetor_de_token_info.pop()

    vetor_identificadores = []

    contador = 0
    while contador < len(vetor_de_token_info):
        token_info = vetor_de_token_info[contador]

        # AQUI LIDAREMOS COM A CLASSIFICAÇÃO DOS TOKENS ENTRE IDENTIFICADORES E PALAVRAS RESERVADAS
        if(token_info.tipo == 'ID/Reservada'):
            token_maiusculo = token_info.token.upper()

            if (token_maiusculo in palavras_reservadas):
                token_info.tipo = 'Reservada'

            else:
                token_info.tipo = 'ID'

                vetor_identificadores.append(token_info)

        contador += 1

    return (vetor_de_token_info, vetor_identificadores)

def classificaTokens(automato: Automato, entrada: str, linha: int, ehComentario: bool):
    entrada += ' '
    coluna_atual = 0

    vetor_de_token_info: List[Token] = []
    vetor_de_token_info.append(Token('inicio', 'inicio', -1, -1))

    retorno = None

    tamanho_entrada = len(entrada)
    label_anterior = 'inicio'
    while len(entrada) > 1:
        saida, label, posicao = automato.test(entrada)

        token = entrada[:posicao]
        entrada = entrada[posicao:]

        if label == 'Entrada Comentario':
            ehComentario = True
            vetor_de_token_info.append(Token(token, label, linha, coluna_atual + posicao))

        if label == 'Saida Comentario':
            ehComentario = False

        if not saida:
            entrada = entrada[1:]

        if ehComentario:
            continue

        # Se o automato retornar falso, um erro foi encontrado:
        #   Parar a análise e avisar o problema
        if saida is False:
                return (False, (coluna_atual + posicao, vetor_de_token_info[-1].token, label))
        else:
            # Ainda pode existir um erro:
            if (label_anterior == 'Inteiro') or (label_anterior == 'Real'):
                if (label != 'Espaco' and label != 'Simbolo especial' and label != 'Simbolo Composto'):
                    vetor_de_token_info.pop()
                    return (False, (coluna_atual + posicao, vetor_de_token_info[-1].token, 'Erro Léxico'))

            # print(f'Label "{label}"')
            # print(f'Token "{token}" entrada "{entrada}"')
            # print(f'Token "{token}"')
            if(label == 'Real') and (entrada[0] == ' '):  # CHECA SE HÁ UM ESPAÇO APÓS UM REAL OU SEJA, "3.3" OU "3."
                if entrada != ' ':  # CHECA SE NÃO É O FINAL DA STRING
                    if token[-1] == '.':  # CHECA SE ESTA NO FORMATO "2."
                        return (False, (coluna_atual + posicao, vetor_de_token_info[-1].token, 'Erro Léxico'))
            if (label == 'Real') and ((ord(entrada[0]) >= 65 and ord(entrada[0]) <= 90) or (ord(entrada[0]) >= 97 and ord(entrada[0]) <= 122)):
                # CHECA SE É "3.3A" OU "3.A"
                if token[-1] != '.':  # ERRO SE FOR "3.3A"
                    return (False, (coluna_atual + posicao, vetor_de_token_info[-1].token, 'Erro Léxico'))
                token = token.split('.', 1)
                token = token[0]
                label = 'Inteiro'
                vetor_de_token_info.append(Token(token, label, linha, coluna_atual + posicao))
                token = '.'
                label = 'Simbolo especial'

            vetor_de_token_info.append(Token(token, label, linha, coluna_atual + posicao))
            # fim do token
        label_anterior = label
        coluna_atual += posicao

    return(True, vetor_de_token_info)
